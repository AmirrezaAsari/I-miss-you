## convert the chat data to a lm tuning friendly
import json
import random
import json

input_path = "./data/sara_chat.json"     # main chat file
output_path = "tinyllama_chat.jsonl" # final result

system_prompt = "Continue the chat as Sara in her usual style."

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    data = json.load(infile)

    messages = [{"role": "system", "content": system_prompt}]

    for item in data:
        text = item.get("message", "").strip()
        if not text:
            continue  
        role = "assistant" if item.get("sender") == "Sara" else "user"
        messages.append({"role": role, "content": text})

    
    json.dump({"messages": messages}, outfile, ensure_ascii=False)
    outfile.write("\n")

print(f"Conversion done! Output saved to {output_path}")
