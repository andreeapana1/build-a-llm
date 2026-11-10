"""Load the trained model and complete "The sky is" 100 times.

Run:  python sky_test.py
Saves sky_completions.txt (or, if the model cannot read the prompt, an
explanation of which tokens it has never seen).
"""
import os
import sys

import tiktoken

from model import load_checkpoint, generate, StreamPrinter

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = os.path.join(HERE, "results", "model.pt")
OUTFILE = os.path.join(HERE, "sky_completions.txt")

PROMPT = "The sky is"
N_COMPLETIONS = 100
N_TOKENS = 20


def main():
    enc = tiktoken.get_encoding("o200k_base")
    model, vocab, stoi, _ = load_checkpoint(CHECKPOINT)

    prompt_gpt = enc.encode_ordinary(PROMPT)
    print(f"Prompt: {PROMPT!r}")
    print("GPT-4o tokens:")
    missing = []
    for t in prompt_gpt:
        known = t in stoi
        print(f"  {t:>7}  {enc.decode([t])!r:<10} {'known' if known else 'NOT in the model vocabulary'}")
        if not known:
            missing.append(t)

    if missing:
        words = ", ".join(repr(enc.decode([t])) for t in missing)
        msg = (f"FAILED: the model cannot read {PROMPT!r}.\n"
               f"Token(s) {words} never appeared in fineweb_corpus.txt, so they are not in\n"
               f"the model's {len(vocab):,}-token vocabulary. It has no input slot for them\n"
               "and cannot generate a completion.\n")
        print("\n" + msg)
        with open(OUTFILE, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {PROMPT!r}\nGPT-4o token IDs: {prompt_gpt}\n\n{msg}")
        print(f"Saved this explanation to {OUTFILE}")
        sys.exit(1)

    prompt_ids = [stoi[t] for t in prompt_gpt]
    lines = []
    for i in range(N_COMPLETIONS):
        printer = StreamPrinter(enc, vocab, echo=False)
        # A different seed for each completion so the 100 samples differ.
        generate(model, prompt_ids, N_TOKENS, seed=i, on_token=printer)
        text = PROMPT + printer.text.replace("\n", " ")
        print(f"{i + 1:3d}: {text}")
        lines.append(f"{i + 1:3d}: {text}")

    with open(OUTFILE, "w", encoding="utf-8") as f:
        f.write(f"Prompt: {PROMPT!r}   completions: {N_COMPLETIONS}   tokens each: {N_TOKENS}   "
                "seeds: 0-99\n\n")
        f.write("\n".join(lines) + "\n")
    print(f"\nSaved {N_COMPLETIONS} completions to {OUTFILE}")


if __name__ == "__main__":
    main()
