import asyncpg
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async def save_entry(user_id, text, summary, tags, category, embedding):

    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO journal_entries (user_id, text, summary, tags, category, embedding, created_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """, user_id, text, summary, tags, category, embedding_str, datetime.utcnow())
    await conn.close()


async def search_entries(user_id, query_embedding, limit=5):
    query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT summary, text
        FROM journal_entries
        WHERE user_id = $1
        ORDER BY embedding <#> $2
        LIMIT $3
    """, user_id, query_embedding_str, limit)
    await conn.close()
    return [dict(row) for row in rows]
