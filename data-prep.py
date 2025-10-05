import json
import random

# === config ===
INPUT_FILE = "./data/sara_chat.json"    # your raw message dataset
OUTPUT_TRAIN = "./train.jsonl"    # output for training
OUTPUT_VALID = "./valid.jsonl"    # output for validation
TARGET_SENDER = "Sara"          # person whose style you want to model
VALID_RATIO = 0.2               # 20% for validation

# === load data ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    messages = json.load(f)

# === sort by time (important if unsorted) ===
messages.sort(key=lambda x: x["timestamp"])

# === merge consecutive messages from same sender ===
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

# === create samples ===
samples = []
for i in range(len(merged) - 1):
    curr = merged[i]
    nxt = merged[i + 1]

    if nxt["sender"] == TARGET_SENDER and curr["sender"] != TARGET_SENDER:
        samples.append({
            "instruction": f"Continue the chat as {TARGET_SENDER} in her usual style.",
            "input": f"{curr['sender']}: {curr['message']}",
            "output": nxt["message"]
        })

# === shuffle and split ===
random.shuffle(samples)
split_idx = int(len(samples) * (1 - VALID_RATIO))
train_samples = samples[:split_idx]
valid_samples = samples[split_idx:]

# === save ===
def save_jsonl(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for s in data:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

save_jsonl(OUTPUT_TRAIN, train_samples)
save_jsonl(OUTPUT_VALID, valid_samples)

print(f"✅ Done! {len(train_samples)} train + {len(valid_samples)} valid samples created.")
