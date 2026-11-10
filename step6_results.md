# Step 6: Hallucinations, thinking and tools

Date tested: ____
Screenshots: `step6_screenshots/`

---

## 6.1 Obscure article: without vs with the source

**Article:** Mori, Sassetti, Cavaliere & Bonti, "A systematic literature review on artificial intelligence in recruiting and selection: a matter of ethics"
**Link / source:** Personnel Review, Vol. 54 No. 3 (2025), pp. 854–878, DOI 10.1108/PR-03-2023-0257 (PDF, 25 pages)
**Published:** online July 2024 (ahead of print), issue 2025: niche academic paper
**Setup "without":** new chat, prompt started with "Answer from your own knowledge only. Do not search the web or use any tools." (no search line appeared)
**Assistant used:** ____ (name + model, e.g. "ChatGPT, GPT-x" or "Claude, model y")

| # | Question | Correct answer (from the article) | Answer WITHOUT article | ✅/❌ | Answer WITH article attached | ✅/❌ |
|---|---|---|---|---|---|---|
| 1 | How many articles did Mori et al. (2025) review? | 120 | "51 articles" (said it was not fully confident; told me to check the PRISMA flow diagram) | ❌ | "120" (also: 1,492 after merging and de-duplicating, screened down to 120) | ✅ |
| 2 | Which two databases did they search? | Web of Science and Scopus | "Scopus and Web of Science" ("the standard pair for systematic reviews in management and HRM"; not confirmed) | ✅ (lucky guess from the usual pattern) | "Web of Science (Social Science Citation Index) and Scopus" | ✅ |
| 3 | Which three ethical theories structure their review? | Utilitarian theories, theories of justice, theories of rights | "Utilitarianism, deontology, virtue ethics" ("fairly sure"; admitted it might be "filling in the standard set") | ❌ (1 of 3: utilitarianism right; justice missing; virtue ethics invented) | "Utilitarian theories, theories of justice, theories of rights" (following Cavanagh et al.) | ✅ |
| 4 | SHRM survey (Feb 2022): share of employers using AI/automation for R&S? | 79% (paper: "79% of employers use AI and/or automation for R&S", citing Friedman, 2023) | "79%" (confident about the SHRM figure, less sure it's the paper's number); added that SHRM's 79% applies only to the ~1 in 4 organisations already using AI/automation in HR | ✅ | "79%", cited as Friedman, 2023 | ✅ |
| 5 | Which journal ranking guide did they use? | 2021 Academic Journal Guide of the Chartered Association of Business Schools (CABS 2021), specific management subcategories | "CABS/ABS Academic Journal Guide, probably the 2021 edition" ("best guess", lower confidence, inferred from what is standard; added "typically 2 stars or higher", which is not stated in the paper's method text) | ✅ (guide + edition right; the star threshold is an unverified add-on) | "2021 Academic Journal Guide, Chartered Association of Business Schools (CABS 2021)" | ✅ |

**Score:** without article **3/5** · with article **5/5**

**What I noticed** (did it admit it didn't know, or invent answers? did it quote the article?):
- Q1 without the article: it recalled the **exact title** correctly, so the paper was probably in its training data, but invented the **number** (51 instead of 120). Knowing *that* a paper exists ≠ remembering its details.
- It **hedged** ("I'm not fully confident… check the methods section"), which is better than a flat wrong answer, but still gave a specific false number.
- Its advice "check the **PRISMA** flow diagram" is itself a guess: the paper used the **SPAR-4-SLR** protocol. A plausible default filled in.
- Q2 was **right for the wrong reason**: it said so itself ("the standard pair… this paper follows that pattern"). When the true answer is the most common pattern, prediction looks like knowledge; when it isn't (Q1: 120 articles), the same mechanism gives a wrong answer. You can't tell which case you're in without the source.
- Q3: it gave the **textbook default** (utilitarianism / deontology / virtue ethics) instead of the paper's framework (utilitarian / **justice** / **rights**). It even explained *why* it fit ("fits the paper's subtitle"), a convincing justification for a wrong answer. Its confidence went up ("fairly sure") while it was wrong.
- Q4 was right because the **79% statistic is widely repeated online**: it remembered the popular fact, not this paper (it said so). Facts that appear many times in training data are recalled well (same as my Step 3 model memorizing repeated text).
- Its caveat is a real point: in SHRM's report the 79% refers to the roughly one in four organisations that already use AI/automation in HR, not all employers. The paper's sentence ("79% of employers…") repeats the common simplification. **Even a published source can carry a misquoted number**, and models trained on such text repeat it.
- Q5 was again **right by pattern**: it said it was "inferring it from what is standard in the field". It also added a detail ("2 stars or higher") that the paper's method text doesn't state: a correct core with an invented extra.
- **Overall without the article: 3/5 correct (Q2, Q4, Q5), and none of the three came from remembering this paper.** Correct answers came from *common patterns* or *widely repeated facts*; wrong answers (Q1, Q3) were exactly the paper-specific details. Its hedging was honest, but it still gave specific wrong answers.
- **With the article attached: 5/5**, no hedging, and it added correct details I could verify in the PDF (1,492 articles before screening; the three theories come from Cavanagh et al., 1981). It "ran 2 commands", meaning it used code to read the PDF: a tool putting the source text into the context.
- **Same model, same questions: 3/5 → 5/5.** The only change was the evidence in the context. The weights didn't change (inference, not training).

**Extra observation: with web search ON (by accident)**
Question 1 asked with web search still enabled. The assistant **searched the web on its own** ("Searched the web: Mori Sassetti Cavaliere Bonti 2025 Personnel Review…") and answered **120 articles** ✅, plus correct extra details (Web of Science and Scopus, the three ethical views, the SPAR-4-SLR protocol, published online July 2024, Personnel Review 54, pp. 854–878), each with **links to its sources** (Emerald full text, University of Florence repository, UNIECAMPUS record).
→ Retrieval works like attaching the article: it puts the evidence **in the context**, so the answer is grounded and checkable. That's why this run can't count as "without the article"; the test was repeated with search off.

---

## 6.2 "Who created you?"

| Model asked | Its answer | What the documentation says (link) | Correct? |
|---|---|---|---|
| Claude (claude.ai), new chat | "I was made by Anthropic. I'm Claude, and the model you're talking to right now is Claude Opus 5.5." | Claude models are developed by Anthropic ([Anthropic models overview](https://docs.anthropic.com/en/docs/about-claude/models/overview)); model picker in claude.ai confirmed **Claude Opus 5.5** | ✅ |
| `HuggingFaceTB/SmolLM2-135M-Instruct` (SLM Testing, Chat mode, CPU) (`smollm2_instruct_who_created_you.webp`) | "I'm a descendant of the renowned British artist and writer … known as 'The Great,' who was born in 1846 in … Stoke-on-Trent, England. His name is Gaius Julius Caesar of London. I've spent many years studying his works…" | Built by **Hugging Face** (HuggingFaceTB team) ([model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)) | ❌ |

**What I noticed:**
- **Claude answered correctly and precisely** (company + model version). Big assistants are deliberately taught their identity during post-training, and the app can add it in the system prompt. It isn't self-knowledge; it's trained or provided text.
- **SmolLM2 didn't even understand it is an AI.** It answered "Who created you?" as if it were a *person* writing a memoir, inventing an ancestor ("Gaius Julius Caesar of London", born 1846 in Stoke-on-Trent, a painter and poet). The tiny model wasn't trained on its own identity, so it continued with a likely-sounding personal story.
- **Lesson:** a model's statements about itself are **predicted text like any other**. Check the documentation (model card, provider docs) rather than asking the model.

---

## 6.3 Retailer profit: thinking vs non-thinking

**Correct answer (computed with code, `step6_answer_key.py`): €930.46**

Working: 1,035 sold (83%, rounded down) → 72 returned (7%, rounded down) → 963 kept × €57.112 (€64.90 − 12%) = €54,998.856 · 212 unsold × €21.40 = €4,536.80 · purchase 1,247 × €38.75 = €48,321.25 · shipping 1,247 × €2.85 = €3,553.95 · fixed €6,730 → **€930.456 ≈ €930.46**

| Model (exact name) | Thinking? | Request | Final answer | Correct? | Notes |
|---|---|---|---|---|---|
| Claude **Opus 3** (2024, no thinking mode; Effort option disappears) | Non-thinking | "Give only the final answer" | €930.46 | ✅ | **Ignored the instruction**: wrote out the full calculation anyway. Also **rounded intermediate amounts** (refund €4,112.064 → €4,112.06; revenue €54,998.856 → €54,998.86) although told to round only the final amount; here the rounding happened not to change the result |
| Claude **Opus 3** | Non-thinking | "Show the calculation before answering" | **−€610.34** (a loss) | ❌ | **Logic error, not arithmetic:** computed unsold units as 1,247 − 1,035 − **72** = 140 instead of 212, subtracting the returned units a second time (they came out of the *sold* units, not the unsold stock). That loses 72 × €21.40 = €1,540.80 → €930.46 − €1,540.80 = −€610.34. Every multiplication was correct; one wrong step flipped profit into a loss. Same model as chat 1, different answer |
| Claude **Opus 5.5**, Effort **High** | Thinking | "Give only the final answer" | €930.46 | ✅ | **Followed the instruction**: the visible reply was only "€930.46". The working happened in a hidden thinking phase (status line "Recalculating the discounted price and returns"), so it could compute step by step without showing it |
| Claude **Opus 5.5**, Effort **High** | Thinking | "Show the calculation before answering" | €930.46 | ✅ | Thought first ("Working out the sales and returns figures"), then a clean, structured calculation. **Kept full precision** (€54,998.856, €59,535.656, €930.456) and rounded only at the end. **Explicitly handled both traps**: "Unsold: 1,247 − 1,035 = 212… the 72 returned units can't be resold, so they aren't added here", and "Returns are refunded at the price the customer actually paid". Small slip: it put the final answer at the top although asked to show the calculation *before* answering |

**What I noticed** (where did wrong answers go wrong? rounding, returns resold, refund at the wrong price…):
- **Score: Opus 3 (non-thinking) 1/2 · Opus 5.5 High (thinking) 2/2.**
- **The only wrong answer was a reasoning error, not an arithmetic error:** Opus 3 subtracted the 72 returned units from the unsold stock (140 instead of 212), turning a €930.46 profit into a −€610.34 loss. All its multiplications were right.
- **Same model, different answers:** Opus 3 was right in chat 1 and wrong in chat 2. Outputs are sampled, so one correct run doesn't prove reliability.
- **Instruction-following differed:** Opus 3 ignored "give only the final answer" and reasoned out loud anyway (its only way to "think"); Opus 5.5 did its working in a hidden thinking phase and returned just the number.
- **Precision:** Opus 3 rounded intermediate amounts despite "round only the final amount" (lucky here); Opus 5.5 kept full precision until the end.
- **The thinking model resolved the ambiguity explicitly** (returned units not resold, refund at the paid price), the exact step where Opus 3 went wrong in chat 2.
- **Caveat:** the comparison mixes *thinking vs no thinking* with *model generation* (Opus 3, 2024, vs Opus 5.5, 2026). And with only 2 runs each, the sample is tiny.
- **Business lesson:** a fluent step-by-step calculation can contain one wrong logical step that flips the result. For invoices, budgets and profit, verify with executed code or a spreadsheet (the code answer key gives €930.46).

---

## 6.4 9.11 vs 9.9, strawberry, Ubiquitous

Correct answers (from code): **9.9** is larger · **3** r's in strawberry · every 3rd character of Ubiquitous from the 1st = **"Uqts"**

**Model used:** Claude Opus 5.5 (Effort Medium), new chat for each round

| Task | Answer WITHOUT code | ✅/❌ | Answer WITH executed code | ✅/❌ |
|---|---|---|---|---|
| Which is larger, 9.11 or 9.9? | "9.9 is larger. 9.9 is the same as 9.90, and 9.90 is more than 9.11." | ✅ | 9.9: `max(9.11, 9.9)` → 9.9 | ✅ |
| How many r's in "strawberry"? | "There are 3 r's." | ✅ | 3: `"strawberry".count("r")` → 3 | ✅ |
| Every 3rd character of "Ubiquitous", starting with the first | "Uqts", positions 1 (U), 4 (q), 7 (t), 10 (s) | ✅ | Uqts: `"Ubiquitous"[::3]` → Uqts | ✅ |

**What I noticed:**
- **Without code: 3/3 correct.** These puzzles are famous LLM failures (older models said "9.11 is larger" and "2 r's"), so they are now in training data and were targeted in post-training. The model also wrote out intermediate steps ("9.9 = 9.90"; positions 1, 4, 7, 10), which works around tokenization.
- **With code: 3/3 correct**, and it showed the executed code ("Run Python…"): `max(9.11, 9.9)`, `"strawberry".count("r")`, `"Ubiquitous"[::3]`. These are the same one-liners as my own answer key (`step6_answer_key.py`).
- **The difference is *why* it's right:** without code the model is right because it has learned these cases; with code it's right **by construction**, because the code operates on the actual characters and numbers. The model still sees tokens, not letters, so a less famous variant could still fail without code.
- The with-code reply said "positions 0, 3, 6 and 9" (Python counts from 0); the no-code reply said 1, 4, 7, 10 (counting from 1). Both describe the same letters.
