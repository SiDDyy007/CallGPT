from utils.openai_utils import transcribe_audio, embed_text, call_gpt
from db.db import search_entries

async def process_query(recording_url, user_id):
    query = await transcribe_audio(recording_url)
    query_embedding = await embed_text(query)

    top_matches = await search_entries(user_id, query_embedding)

    if not top_matches:
        return "I couldn't find any matching entries."

    combined_summaries = "\n".join([f"- {e['summary']}" for e in top_matches])
    answer = call_gpt(f"""User asked: "{query}"\n
    Here are the summaries:\n{combined_summaries}
    Respond with the most relevant answer to the query.""")

    return answer
