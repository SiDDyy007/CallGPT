from utils.openai_utils import transcribe_audio, categorize_entry, summarize_entry, tag_entry, embed_text
from db.db import save_entry
import json
async def process_voice_entry(recording_url: str, user_id: str):
    transcript = await transcribe_audio(recording_url)
    summary = await summarize_entry(transcript)
    category = await categorize_entry(transcript)
    tags = await tag_entry(transcript)
    embedding = await embed_text(transcript)

    list_of_tags = json.loads(tags)

    print(transcript, "transcript")
    print(summary, "summary")
    print(list_of_tags, "tags")
    print(category, "category")
    # print(embedding, "embedding")
    
    await save_entry(user_id, transcript, summary, list_of_tags, category, embedding)
