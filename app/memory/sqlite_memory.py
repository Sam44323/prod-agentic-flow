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

    def save_messages(
        self,
        session_id: str,
        messages: list[BaseMessage],
    ) -> None:
        serialized = []

        # serializing the messages into proper json type format
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "human"
            elif isinstance(message, AIMessage):
                role = "ai"
            else:
                role = "system"

            serialized.append(
                {
                    "role": role,
                    "content": message.content,
                }
            )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO conversations
            (session_id, messages)
            VALUES (?, ?)
            """,
            (
                session_id,
                json.dumps(serialized),
            ),
        )

        conn.commit()
        conn.close()

    def get_messages(
        self,
        session_id: str,
    ) -> list[BaseMessage]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT messages
            FROM conversations
            WHERE session_id = ?
            """,
            (session_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return []

        # getting the first column of the database which is the messages
        serialized = json.loads(row[0])

        messages: list[BaseMessage] = []

        # converting the json type into the respective langchain message-type
        for message in serialized:
            if message["role"] == "human":
                messages.append(HumanMessage(content=message["content"]))
            elif message["role"] == "ai":
                messages.append(AIMessage(content=message["content"]))

        return messages

    def clear_messages(
        self,
        session_id: str,
    ) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # deleting the conversation from the database
        cursor.execute(
            """
            DELETE FROM conversations
            WHERE session_id = ?
            """,
            (session_id,),
        )

        conn.commit()
        conn.close()
