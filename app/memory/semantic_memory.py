# semantic-memory is a technique where we store information about the messages history based on the core idea instead of verbatim
# we can use this to store the information about the user's intents, goals, and other relevant information
# this can be used to improve the quality of the responses and is diff from conversation type memory


from typing import Optional
import sqlite3


# Example of the schema
# session_id | key                | value
# ---------------------------------------------
# default    | name               | Adam
# default    | favorite_language  | Rust
# default    | occupation         | Blockchain Developer


class SemanticMemory:
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_facts (
                session_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                PRIMARY KEY (session_id, key)
            )
        """)

        conn.commit()
        conn.close()

    def save_fact(
        self,
        session_id: str,
        key: str,
        value: str,
    ) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO user_facts
            (session_id, key, value)
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                key,
                value,
            ),
        )

        conn.commit()
        conn.close()

    def get_fact(
        self,
        session_id: str,
        key: str,
    ) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT value
            FROM user_facts
            WHERE session_id = ? AND key = ?
            """,
            (
                session_id,
                key,
            ),
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return row[0]

    def get_all_facts(
        self,
        session_id: str,
    ) -> dict[str, str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT key, value
            FROM user_facts
            WHERE session_id = ?
            """,
            (session_id,),
        )

        rows = cursor.fetchall()
        conn.close()

        return {key: value for key, value in rows}
