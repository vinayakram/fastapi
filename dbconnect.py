from sqlalchemy import create_engine
import os


# Fetch variables
USER = "postgres"
PASSWORD = "Improve123!"
HOST = "db.behkfibwlpbwlwlbwgwo.supabase.co"
PORT = "5432"
DBNAME = "postgres"

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql://postgres:root@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")