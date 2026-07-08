import sqlite3
import json

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
)


class SQLiteMemory:
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                messages TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

