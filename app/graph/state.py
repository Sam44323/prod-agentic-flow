from typing import TypedDict


# TypedDict is a way to define a dictionary with a specific set of keys and types
class AgentState(TypedDict):
    user_input: str

    # conversation-history
    messages: list

    # tool-states
    tool_name: str
    tool_input: str
    tool_output: str
    error: str

    # running-state for outputs
    final_answer: str
