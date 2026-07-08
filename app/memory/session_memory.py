from langchain_core.messages import BaseMessage

# session_id -> conversation history
# we'd post this shift this to sqlite or redis
_MEMORY: dict[str, list[BaseMessage]] = {}


def get_messages(session_id: str) -> list[BaseMessage]:
    """Return the conversation history for a session."""
    return _MEMORY.setdefault(session_id, [])


def save_messages(session_id: str, messages: list[BaseMessage]) -> None:
    """Persist the updated conversation history."""
    _MEMORY[session_id] = messages


def clear_messages(session_id: str) -> None:
    """Delete a session's conversation history."""
    _MEMORY.pop(session_id, None)
