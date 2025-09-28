# I Miss You – Chat Agent Project

## Overview
This project is an experimental AI agent that can chat in the style of a person using historical conversation data.  
The dataset is based on **Telegram exports** (screenshots and text), which are preprocessed into a structured format before being fed into models for training or retrieval.  

The long-term goal of this project is to create a chatbot that mimics conversational patterns, style, and personality extracted from past chats.

---
## Purpose & Flow

1. **Collect Data**  
   Export from Telegram (`.json` or text), or extract from screenshots if needed.  

2. **Prepare Data**  
   Run `data.py` → outputs normalized dataset in `data/processed/`.  

3. **Embed Data**  
   Store message embeddings in a **vector database** (e.g., FAISS, Chroma, or Pinecone).  

4. **Chat Agent**  
   - User sends a message.  
   - System retrieves similar past messages (context) via vector search.  
   - Agent replies in the style/personality of the past chat partner.  

5. **Future Additions**  
   - More metadata (voice, gifs, music).  
   - Personality profiling.  
   - Telegram-style UI for interaction.  
   - Fine-tuning or RAG pipelines for stronger contextual accuracy.
     
---

## Data Preparation (`data.py`)

The `data.py` script handles cleaning and structuring raw Telegram data.

### Responsibilities:
- **Parsing raw chat exports**: JSON/text exports from Telegram (and later, screenshots converted to text).  
- **Normalizing fields**: user, message, timestamp, type (text, sticker, gif, voice, etc.).  
- **Metadata extraction**:  
  - Timestamps (where available)  
  - Media type (gif, music, sticker, image)  
  - Optional metadata (titles, captions, file names)  
- **Output format**: JSON/CSV ready for downstream tasks.

### Example output (simplified):
```json
{
  "id": "msg_123",
  "sender": "You",
  "text": "Hey, how are you?",
  "timestamp": "2023-05-12 14:35:00",
  "type": "text"
}
```
Media messages include metadata:
```json
{
  "id": "msg_124",
  "sender": "Her",
  "type": "music",
  "title": "Song Name",
  "file": "track123.mp3",
  "timestamp": "2023-05-12 14:37:00"
}
```
####Notes
Some chat messages (like from screenshots) may lack timestamps.
These can still be used for personality/style learning, but are less useful for time-based context.
Data will grow as more exports are added. Just rerun data.py to regenerate.


##Agent

(Future: Describe how the chat agent will work — retrieval, style mimic, response generation.)

##APP

(Future: details about the app that will get messages from user to llm.)

##UI

(Future: Add details about the planned Telegram-style interface.)

#License

Personal/research project – not intended for production use.
