import json

# === config ===
INPUT_FILE = "./data/sara_chat.json"   # your current message dataset
OUTPUT_FILE = "./data/train.jsonl"    # output for fine-tuning
TARGET_SENDER = "Sara"         # the person whose style you want to model

# === load data ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    messages = json.load(f)

# === sort by timestamp just in case ===
messages.sort(key=lambda x: x["timestamp"])

# === merge consecutive messages from the same sender ===
merged = []
for msg in messages:
    if merged and merged[-1]["sender"] == msg["sender"]:
        merged[-1]["message"] += "\n" + msg["message"]
    else:
        merged.append({
            "sender": msg["sender"],
            "message": msg["message"],
            "timestamp": msg["timestamp"]
        })

# === create training samples ===
samples = []
for i in range(len(merged) - 1):
    curr = merged[i]
    nxt = merged[i + 1]

    # only use turns where the next message is from the target sender (Sara)
    if nxt["sender"] == TARGET_SENDER and curr["sender"] != TARGET_SENDER:
        samples.append({
            "instruction": f"Continue the chat as {TARGET_SENDER} in her usual style.",
            "input": f"{curr['sender']}: {curr['message']}",
            "output": nxt["message"]
        })

# === save to jsonl ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for sample in samples:
        f.write(json.dumps(sample, ensure_ascii=False) + "\n")

print(f"✅ Done! Generated {len(samples)} training samples in {OUTPUT_FILE}")
