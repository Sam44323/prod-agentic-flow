from typing import TypedDict

# TypedDict is a way to define a dictionary with a specific set of keys and types
class AgentState(TypedDict):
    user_input: str
    final_answer: str
