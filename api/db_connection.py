# backend/api/db_connection.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db_handle():
    client = MongoClient(os.getenv("MONGO_URI"))
    db_handle = client[os.getenv("DB_NAME")]
    return db_handle, client

# Global handles to use in your views
db, client = get_db_handle()