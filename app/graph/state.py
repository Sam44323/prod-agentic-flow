from typing import TypedDict


# TypedDict is a way to define a dictionary with a specific set of keys and types
class AgentState(TypedDict):
    user_input: str
    tool_name: str
    tool_input: str
    tool_output: str
    final_answer: str
