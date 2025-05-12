from openai import OpenAI
import httpx
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# print(OPENAI_API_KEY, "OPENAI_API_KEY")

client = OpenAI()



async def transcribe_audio(audio_url):
    if "workout_log" in audio_url:
        return "I did a heavy leg workout today with squats and lunges."
    if "query_workouts" in audio_url:
        return "What did I say about my workouts last week?"
    return "Test transcription"


# async def transcribe_audio(audio_url):
#     async with httpx.AsyncClient() as client:
#         audio_data = await client.get(audio_url)
#         files = {"file": ("audio.mp3", audio_data.content, "audio/mpeg")}
#         resp = await client.post(
#             "https://api.openai.com/v1/audio/transcriptions",
#             headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
#             data={"model": "whisper-1"},
#             files=files,
#         )
#     return resp.json()["text"]

async def summarize_entry(text):
    return call_gpt(f"Summarize: {text}")

async def categorize_entry(text):
    return call_gpt(f"Categorize this journal entry into one word: {text}")

async def tag_entry(text):
    return call_gpt(f"Tag this journal entry with top 3relevant keywords: {text}. Output should be a array list of keywords.")

async def embed_text(text):
    resp = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return resp.data[0].embedding

def call_gpt(prompt):
    response = client.chat.completions.create(model="gpt-4.1-nano-2025-04-14", # 4.1 nano is the latest and cheapest model
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
