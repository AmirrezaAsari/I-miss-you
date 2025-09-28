import json

# ---- CONFIG ----
INPUT_FILE = r"input_file"
OUTPUT_FILE = r"output_file"
TARGET_NAME = "name of your target"

# ---- LOAD DATA ----
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---- FIND THE CHAT ----
sara_chat = None
for chat in data.get("chats", {}).get("list", []):
    if chat.get("name") == TARGET_NAME:
        sara_chat = chat
        break

if not sara_chat:
    print(f"No chat found with name '{TARGET_NAME}'")
    exit(1)

# ---- EXTRACT MESSAGES ----
messages = []
for msg in sara_chat.get("messages", []):
    # Determine text content
    text_content = ""
    if "text" in msg:
        if isinstance(msg["text"], list):
            for part in msg["text"]:
                if isinstance(part, str):
                    text_content += part
                elif isinstance(part, dict) and "text" in part:
                    text_content += part["text"]
        else:
            text_content = msg["text"]
        text_content = text_content.strip()

    # Prepare media metadata if exists
    media_info = None
    if "media_type" in msg:
        media_info = {
            "type": msg.get("media_type"),
            "file_name": msg.get("file", ""),
        }
        # Add duration if audio/video
        if "duration_seconds" in msg:
            media_info["duration_seconds"] = msg["duration_seconds"]
        # Add mime type if exists
        if "mime_type" in msg:
            media_info["mime_type"] = msg["mime_type"]

    # Skip messages with neither text nor media
    if not text_content and not media_info:
        continue

    messages.append({
        "sender": msg.get("from"),
        "timestamp": msg.get("date"),
        "message": text_content,
        "media": media_info
    })

# ---- SAVE TO NEW JSON FILE ----
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(messages, f, ensure_ascii=False, indent=2)

print(f"Done! Extracted {len(messages)} messages from '{TARGET_NAME}' to {OUTPUT_FILE}")