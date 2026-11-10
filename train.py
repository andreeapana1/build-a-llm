"""Train a tiny next-token-prediction model on fineweb_corpus.txt (CPU, ~60 s).

Run:  python train.py            (or: python train.py --seconds 120)

Everything this prints and saves comes from YOUR run. Outputs go to results/:
  training_log.csv     step, loss, elapsed time, tokens/second
  loss_plot.png        loss curve
  samples.txt          generated text before, during and after training
  model.pt             trained model checkpoint (weights + vocabulary)
"""
import argparse
import csv
import math
import os
import re
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tiktoken
import torch

from model import TinyGPT, generate, StreamPrinter, save_checkpoint

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "fineweb_corpus.txt")
TOKENS = os.path.join(HERE, "fineweb_tokens.txt")
OUT = os.path.join(HERE, "results")

PROMPT = "The company is"   # same sentence beginning every time
SEED = 42                   # same random seed every time
SAMPLE_EVERY = 20           # generate a sample every 20 updates
SAMPLE_TOKENS = 30          # length of each sample
CTX = 64                    # how many tokens the model sees at once
BATCH = 16                  # sequences per update
LR = 2e-3


def check_tokens(enc, corpus):
    """Compare the IDs from Tiktokenizer with tiktoken's own encoding."""
    fresh = enc.encode_ordinary(corpus)
    with open(TOKENS, encoding="utf-8") as f:
        from_file = [int(x) for x in re.findall(r"\d+", f.read())]

    print(f"Token IDs in fineweb_tokens.txt : {len(from_file):,}")
    print(f"Token IDs from tiktoken (corpus): {len(fresh):,}")
    if from_file == fresh:
        print("OK: fineweb_tokens.txt matches the corpus exactly.\n")
        return fresh

    first_diff = next((i for i, (a, b) in enumerate(zip(from_file, fresh)) if a != b),
                      min(len(from_file), len(fresh)))
    print(f"MISMATCH: first difference at position {first_diff}. "
          "Using IDs regenerated from the corpus instead.")
    regen = os.path.join(OUT, "fineweb_tokens_regenerated.txt")
    with open(regen, "w", encoding="utf-8") as f:
        f.write(", ".join(map(str, fresh)))
    print(f"Saved regenerated IDs to {regen}\n")
    return fresh


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=60.0,
                        help="training time budget (sampling time not counted)")
    args = parser.parse_args()

    os.makedirs(OUT, exist_ok=True)
    torch.manual_seed(SEED)

    # 1. Tokenize with GPT-4o's tokenizer and validate against your file.
    enc = tiktoken.get_encoding("o200k_base")
    with open(CORPUS, encoding="utf-8") as f:
        corpus = f.read()
    ids = check_tokens(enc, corpus)

    # 2. Compact vocabulary: only the token IDs that occur in the corpus.
    vocab = sorted(set(ids))                      # internal ID -> GPT-4o ID
    stoi = {tok: i for i, tok in enumerate(vocab)}  # GPT-4o ID -> internal ID
    data = torch.tensor([stoi[t] for t in ids], dtype=torch.long)
    print(f"GPT-4o vocabulary size : {enc.n_vocab:,}")
    print(f"Compact vocabulary size: {len(vocab):,} distinct tokens in the corpus")

    # 3. Sentence beginning for samples (must use known tokens).
    prompt_gpt = enc.encode_ordinary(PROMPT)
    if all(t in stoi for t in prompt_gpt):
        prompt_text = PROMPT
    else:
        prompt_gpt = ids[:4]
        prompt_text = enc.decode(prompt_gpt)
        print(f"Note: '{PROMPT}' has unknown tokens; using '{prompt_text}' instead.")
    prompt_ids = [stoi[t] for t in prompt_gpt]

    # 4. Build a randomly initialized model.
    model = TinyGPT(len(vocab), ctx=CTX)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters       : {n_params:,}")
    print(f"Loss of a pure random guess = ln({len(vocab)}) = {math.log(len(vocab)):.2f}\n")
    opt = torch.optim.AdamW(model.parameters(), lr=LR)

    samples = []

    def sample(step, label):
        print(f"\n--- sample ({label}, step {step}) ---")
        print(prompt_text, end="", flush=True)
        printer = StreamPrinter(enc, vocab)
        generate(model, prompt_ids, SAMPLE_TOKENS, SEED, on_token=printer)
        print("\n" + "-" * 40)
        samples.append((step, label, prompt_text + printer.text))

    def get_batch():
        ix = torch.randint(len(data) - CTX - 1, (BATCH,))
        x = torch.stack([data[i:i + CTX] for i in ix])
        y = torch.stack([data[i + 1:i + CTX + 1] for i in ix])  # next tokens
        return x, y

    sample(0, "before training")

    print(f"\nTraining for ~{args.seconds:.0f} s on CPU ...")
    print(" step |   loss  | elapsed | tokens/second")
    log = []
    step, train_time, tokens_seen = 0, 0.0, 0
    model.train()
    while train_time < args.seconds:
        t0 = time.perf_counter()
        x, y = get_batch()
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        train_time += time.perf_counter() - t0   # sampling time is excluded
        step += 1
        tokens_seen += x.numel()
        tps = tokens_seen / train_time
        print(f"{step:5d} | {loss.item():7.4f} | {train_time:6.1f}s | {tps:,.0f}", flush=True)
        log.append((step, loss.item(), train_time, tps))
        if step % SAMPLE_EVERY == 0:
            sample(step, "during training")

    sample(step, "after training")

    # 5. Save everything.
    with open(os.path.join(OUT, "training_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["step", "loss", "elapsed_seconds", "tokens_per_second"])
        w.writerows(log)

    plt.figure(figsize=(8, 4.5))
    plt.plot([r[0] for r in log], [r[1] for r in log], linewidth=1)
    plt.axhline(math.log(len(vocab)), linestyle="--", color="grey",
                label=f"random guess = ln({len(vocab)})")
    plt.xlabel("training step")
    plt.ylabel("loss (cross-entropy)")
    plt.title("Tiny transformer trained on 10 FineWeb documents")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "loss_plot.png"), dpi=150)

    with open(os.path.join(OUT, "samples.txt"), "w", encoding="utf-8") as f:
        f.write(f"Prompt: {prompt_text!r}   seed: {SEED}   tokens per sample: {SAMPLE_TOKENS}\n\n")
        for s, label, text in samples:
            f.write(f"=== step {s} ({label}) ===\n{text}\n\n")

    save_checkpoint(os.path.join(OUT, "model.pt"), model, vocab,
                    extra={"prompt": prompt_text, "seed": SEED, "steps": step})

    print(f"\nDone: {step} steps in {train_time:.1f} s, final loss {log[-1][1]:.4f}")
    print(f"Saved training_log.csv, loss_plot.png, samples.txt and model.pt in {OUT}")


if __name__ == "__main__":
    main()
