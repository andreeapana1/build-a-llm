"""Complete a sentence beginning taken from the training data, 100 times.

Run:  python corpus_test.py
Picks a short sentence that appears exactly in fineweb_corpus.txt (preferring
a common opening such as "The" or "It"), uses its first few words as the
beginning, checks every token is in the model's vocabulary, and saves the
sentence, the beginning and 100 completions to corpus_completions.txt.
"""
import os
import random
import re
from collections import Counter

import tiktoken

from model import load_checkpoint, generate, StreamPrinter

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "fineweb_corpus.txt")
CHECKPOINT = os.path.join(HERE, "results", "model.pt")
OUTFILE = os.path.join(HERE, "corpus_completions.txt")

COMMON_OPENINGS = ["The", "It", "This", "We", "In", "A", "If", "You", "I"]
MIN_WORDS, MAX_WORDS = 5, 15   # "short" sentence
BEGIN_WORDS = 3                # how many words to use as the beginning
N_COMPLETIONS = 100
N_TOKENS = 20
SEED = 42


def candidate_sentences(corpus):
    sentences = re.split(r"(?<=[.!?])\s+", corpus)
    out = []
    for s in sentences:
        s = s.strip()
        words = s.split()
        if MIN_WORDS <= len(words) <= MAX_WORDS and s[0].isupper() and s[-1] in ".!?":
            out.append(s)
    # Shuffle reproducibly, then put sentences with a common opening first.
    random.Random(SEED).shuffle(out)
    out.sort(key=lambda s: s.split()[0] not in COMMON_OPENINGS)
    return out


def main():
    enc = tiktoken.get_encoding("o200k_base")
    model, vocab, stoi, _ = load_checkpoint(CHECKPOINT)
    with open(CORPUS, encoding="utf-8") as f:
        corpus = f.read()

    chosen = None
    for sentence in candidate_sentences(corpus):
        assert sentence in corpus  # appears exactly in the training data
        beginning = " ".join(sentence.split()[:BEGIN_WORDS])
        ids = enc.encode_ordinary(beginning)
        missing = [enc.decode([t]) for t in ids if t not in stoi]
        if missing:
            print(f"Skipped {beginning!r}: tokens not in vocabulary: {missing}")
            continue
        chosen = (sentence, beginning, ids)
        break

    if chosen is None:
        raise SystemExit("No suitable sentence found.")

    sentence, beginning, ids = chosen
    occurrences = corpus.count(beginning)
    print(f"Chosen sentence : {sentence}")
    print(f"Beginning       : {beginning!r}  (appears {occurrences}x in the corpus)")
    print(f"Tokens          : {[enc.decode([t]) for t in ids]} - all in vocabulary\n")

    prompt_ids = [stoi[t] for t in ids]
    completions = []
    for i in range(N_COMPLETIONS):
        printer = StreamPrinter(enc, vocab, echo=False)
        generate(model, prompt_ids, N_TOKENS, seed=i, on_token=printer)
        text = beginning + printer.text
        completions.append(text)
        print(f"{i + 1:3d}: {text}")

    # Simple summary: how often did the model reproduce the original sentence?
    target = sentence[len(beginning):][:40]   # next 40 characters in the real text
    exact = sum(1 for c in completions if c[len(beginning):].startswith(target))
    distinct = len(Counter(completions))
    summary = (f"Completions that continue the original sentence (first 40 chars after the "
               f"beginning): {exact}/{N_COMPLETIONS}\nDistinct completions: {distinct}/{N_COMPLETIONS}")
    print("\n" + summary)

    with open(OUTFILE, "w", encoding="utf-8") as f:
        f.write(f"Chosen sentence: {sentence}\n")
        f.write(f"Beginning: {beginning!r}  (appears {occurrences}x in the corpus)\n")
        f.write(f"Completions: {N_COMPLETIONS}   tokens each: {N_TOKENS}   seeds: 0-{N_COMPLETIONS - 1}\n")
        f.write(summary + "\n\n")
        for i, c in enumerate(completions, 1):
            f.write(f"{i:3d}: {c}\n")
    print(f"\nSaved to {OUTFILE}")


if __name__ == "__main__":
    main()
