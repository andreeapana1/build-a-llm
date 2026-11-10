"""A tiny GPT-style causal transformer, plus helpers shared by the scripts.

The model never sees GPT-4o's full ~200,000-token vocabulary. It only knows
the token IDs that actually occur in fineweb_corpus.txt, renumbered 0..V-1
(the "compact internal vocabulary"). `vocab[i]` maps internal ID i back to
the real GPT-4o token ID so tiktoken can turn it back into text.
"""
import codecs
import sys

import torch
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    """One transformer layer: attention (look at earlier tokens) + MLP (think)."""

    def __init__(self, d_model, n_head, ctx):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_head, batch_first=True)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
        )
        # Causal mask: True = "not allowed to look". Each position may only
        # attend to itself and earlier positions, never to future tokens.
        mask = torch.triu(torch.ones(ctx, ctx, dtype=torch.bool), diagonal=1)
        self.register_buffer("mask", mask, persistent=False)

    def forward(self, x):
        T = x.size(1)
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=self.mask[:T, :T], need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, d_model=128, n_layer=4, n_head=4, ctx=64):
        super().__init__()
        self.ctx = ctx
        self.config = dict(vocab_size=vocab_size, d_model=d_model,
                           n_layer=n_layer, n_head=n_head, ctx=ctx)
        self.tok_emb = nn.Embedding(vocab_size, d_model)   # token ID -> vector
        self.pos_emb = nn.Embedding(ctx, d_model)          # position -> vector
        self.blocks = nn.ModuleList(Block(d_model, n_head, ctx) for _ in range(n_layer))
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)  # vector -> score per token

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        for block in self.blocks:
            x = block(x)
        logits = self.head(self.ln_f(x))
        loss = None
        if targets is not None:
            # Cross-entropy: how surprised the model is by the real next token.
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss


@torch.no_grad()
def generate(model, start_ids, n_new, seed, temperature=1.0, on_token=None):
    """Sample n_new internal token IDs after start_ids.

    A fresh generator seeded with `seed` is used every call, so the random
    draws are identical each time; only the model's weights change the text.
    """
    was_training = model.training
    model.eval()
    g = torch.Generator().manual_seed(seed)
    idx = torch.tensor([start_ids], dtype=torch.long)
    for _ in range(n_new):
        logits, _ = model(idx[:, -model.ctx:])
        probs = F.softmax(logits[0, -1] / temperature, dim=-1)
        nxt = torch.multinomial(probs, 1, generator=g)
        idx = torch.cat([idx, nxt.view(1, 1)], dim=1)
        if on_token is not None:
            on_token(nxt.item())
    if was_training:
        model.train()
    return idx[0].tolist()


class StreamPrinter:
    """Prints tokens as they arrive. Uses byte-level decoding so a character
    split across two tokens (e.g. '€') is printed once it is complete."""

    def __init__(self, enc, vocab, echo=True):
        self.enc = enc
        self.vocab = vocab
        self.echo = echo
        self.decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        self.text = ""

    def __call__(self, internal_id):
        b = self.enc.decode_single_token_bytes(self.vocab[internal_id])
        piece = self.decoder.decode(b)
        self.text += piece
        if self.echo:
            sys.stdout.write(piece)
            sys.stdout.flush()


def save_checkpoint(path, model, vocab, extra=None):
    torch.save({
        "model_state": model.state_dict(),
        "config": model.config,
        "vocab": vocab,          # internal ID -> GPT-4o token ID
        "extra": extra or {},
    }, path)


def load_checkpoint(path):
    ckpt = torch.load(path, map_location="cpu")
    model = TinyGPT(**ckpt["config"])
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    vocab = ckpt["vocab"]
    stoi = {tok: i for i, tok in enumerate(vocab)}
    return model, vocab, stoi, ckpt.get("extra", {})
