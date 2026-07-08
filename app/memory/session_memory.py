# session-memory is a memory that stores the conversation history for a session

from app.memory.sqlite_memory import SQLiteMemory

memory = SQLiteMemory()


def get_messages(session_id):
    return memory.get_messages(session_id)


def save_messages(session_id, messages):
    memory.save_messages(session_id, messages)


def clear_messages(session_id):
    memory.clear_messages(session_id)
