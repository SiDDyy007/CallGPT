import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
import os
import sys

def create_database_schema():
    """Create the PostgreSQL database schema with pgvector extension and journal_entries table."""
    
    # Database connection details (adjust as needed)
    username = os.environ.get("DB_USER", os.getlogin())  # Use system username by default
    database_name = os.environ.get("DB_NAME", "voice_journal")
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    
    # Connect to the default postgres database first to create our database if it doesn't exist
    postgres_engine = create_engine(f"postgresql://{username}@{host}:{port}/postgres")
    
    # Create database if it doesn't exist
    with postgres_engine.connect() as conn:
        # Disconnect other users to allow dropping the database if it exists
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {database_name}"))
        conn.execute(text("COMMIT"))
        conn.execute(text(f"CREATE DATABASE {database_name}"))
        print(f"Created database: {database_name}")
    
    # Connect to our newly created database
    engine = create_engine(f"postgresql://{username}@{host}:{port}/{database_name}")
    
    # Create pgvector extension and table
    with engine.connect() as conn:
        # Create the pgvector extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        print("Created pgvector extension")
        
        # Create the journal_entries table
        conn.execute(text("""
        CREATE TABLE journal_entries (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            text TEXT,
            summary TEXT,
            tags TEXT[],
            category TEXT,
            embedding VECTOR(1536),
            created_at TIMESTAMP
        )
        """))
        print("Created journal_entries table")
        
        # Commit the transaction
        conn.execute(text("COMMIT"))
    
    print("Database setup completed successfully!")
    
    # Return the connection string for future use
    return f"postgresql://{username}@{host}:{port}/{database_name}"

if __name__ == "__main__":
    connection_string = create_database_schema()
    print(f"Connection string: {connection_string}")