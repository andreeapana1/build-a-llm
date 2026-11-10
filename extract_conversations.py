"""Step 5: pick 3 question/answer pairs from the OpenAssistant (oasst1) sample.

Run:  python extract_conversations.py
Reads oasst_sample.json and writes conversations.json.

Rules:
- a question = a 'prompter' message that starts a conversation (no parent), in English
- its answer  = the 'assistant' reply that volunteers ranked best (rank 0)
- keep the first 3 such pairs, in dataset order
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "oasst_sample.json")
DST = os.path.join(HERE, "conversations.json")
N = 3

with open(SRC, encoding="utf-8") as f:
    rows = [r["row"] for r in json.load(f)["rows"]]

conversations = []
for q in rows:
    if q["role"] != "prompter" or q["parent_id"] is not None or q["lang"] != "en":
        continue
    replies = [r for r in rows if r["parent_id"] == q["message_id"] and r["role"] == "assistant"]
    best = [r for r in replies if r["rank"] == 0]
    if not best:
        continue
    a = best[0]
    conversations.append({
        "messages": [
            {"role": "user", "content": q["text"]},
            {"role": "assistant", "content": a["text"]},
        ],
        "source": {
            "dataset": "OpenAssistant/oasst1",
            "message_tree_id": q["message_tree_id"],
            "question_id": q["message_id"],
            "answer_id": a["message_id"],
            "answer_rank": a["rank"],
            "answers_written_for_this_question": len(replies),
        },
    })
    if len(conversations) == N:
        break

with open(DST, "w", encoding="utf-8") as f:
    json.dump(conversations, f, ensure_ascii=False, indent=2)

for i, c in enumerate(conversations, 1):
    print(f"{i}. Q: {c['messages'][0]['content'][:80]}")
    print(f"   A: {c['messages'][1]['content'][:80]}...")
print(f"\nSaved {len(conversations)} conversations to {DST}")
