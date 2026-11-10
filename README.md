# From internet text to an AI assistant

Case assignment for **AI in Accounting and Business** (SDU, MSc, 3rd semester), based on Andrej Karpathy's video *Deep Dive into LLMs like ChatGPT*. The case follows how an LLM is built, from raw web text to a chat assistant, through seven hands-on steps.

**Author:** Andreea Pana

📘 **Start here:** [`exam_notes.md`](exam_notes.md) has my results for every step, what they show, and how they link to business.

## The seven steps

| Step | What I did | Files | Key finding |
|---|---|---|---|
| **1. Training data** | Downloaded 10 FineWeb documents and joined their text into one corpus | `fineweb_sample.json`, `fineweb_corpus.txt` | Web text is messy (login pages, menus), all from May 2013, and nothing is labelled true or false |
| **2. Text representation** | Turned the first sentence into bits and bytes (CyberChef), and the whole corpus into GPT-4o tokens (Tiktokenizer) | `fineweb_bits.txt`, `fineweb_bytes.txt`, `fineweb_tokens.txt` | 22,044 characters → 4,731 tokens (~4.7 characters per token) |
| **3. Train a small model** | Trained a tiny transformer (~1.3M parameters) on my corpus for 60 s on CPU, then tested it | `train.py`, `model.py`, `requirements.txt`, `results/`, `sky_test.py`, `sky_completions.txt`, `corpus_test.py`, `corpus_completions.txt` | Loss fell 7.68 → 0.07: the model **memorized** the corpus and mixed documents into fluent but invented sentences; "The sky is" failed because "sky" was never in the data |
| **4. Base model vs assistant** | Compared SmolLM2-135M (base) with SmolLM2-135M-Instruct; prompted a base model with a chat transcript; tested the knowledge cutoff | `step4_base_vs_assistant.md`, `step4_screenshots/` | The base model gave no answer to "What is 2+2?"; the assistant answered (not always correctly). The 2026 Nobel prize was confidently attributed to the 1999 winner |
| **5. Supervised fine-tuning** | Extracted 3 question/best-answer conversations from the OpenAssistant dataset | `oasst_sample.json`, `extract_conversations.py`, `conversations.json` | Even a top-ranked human answer cited a real but irrelevant paper, which models learn to imitate |
| **6. Hallucinations, thinking and tools** | Tested Claude on an academic article without and with the source, "Who created you?", a profit calculation (thinking vs non-thinking), and tokenization puzzles (without and with code) | `step6_results.md`, `step6_answer_key.py`, `step6_screenshots/` | 3/5 correct without the article → 5/5 with it; a non-thinking model's neat calculation showed a €610 loss instead of a €930 profit |
| **7. Run a model locally** | Ran Llama 3.2 1B Instruct (Q8_0, 1.3 GB) in LM Studio on my Mac | `local_model.png` | A model is just a file of weights; local = private and free, but much weaker |

## Reproducing Step 3

Requires Python 3.10+. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train.py          # trains for ~60 s, writes results/
python sky_test.py       # "The sky is" test → sky_completions.txt
python corpus_test.py    # corpus-sentence test → corpus_completions.txt
```

Results will differ slightly from mine (CPU speed and timing affect the number of training steps).

## How AI was used

The Python scripts were written with the help of Claude (Anthropic). I ran every script, website test and chat myself, and all results in this repository come from my own runs. The correct answers in Step 6 were checked with code (`step6_answer_key.py`) and against the sources.

## Data sources

- [FineWeb](https://huggingface.co/datasets/HuggingFaceFW/fineweb) (Hugging Face), ODC-By 1.0
- [OpenAssistant oasst1](https://huggingface.co/datasets/OpenAssistant/oasst1), Apache 2.0
- Mori, Sassetti, Cavaliere & Bonti (2025), *Personnel Review* 54(3), 854–878 (CC BY 4.0), used as the test article in Step 6 (not included here)
