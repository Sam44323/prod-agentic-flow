from typing import Optional, TypedDict, NotRequired
from langchain_core.messages import BaseMessage


# TypedDict is a way to define a dictionary with a specific set of keys and types
class AgentState(TypedDict):
    user_input: str

    # conversation-history for the state
    messages: list[BaseMessage]

    # tool-states
    tool_name: str
    tool_input: str
    tool_output: str
    error: str

    # interruption-state
    approval_required: bool
    approval_granted: Optional[bool]
    approval_reason: str

    # guardrails-state
    guardrail_passed: bool
    guardrail_reason: str

    # validation of output
    output_valid: bool
    output_validation_reason: str

    # authorized-guard
    tooL_authorized: NotRequired[bool]
    tool_authorization_reason: NotRequired[str]
    # running-state for outputs
    final_answer: str

    # retrieval-state
    planner_action: str  # what the planner decided (answer, retrieve, etc.)
    rewritten_query: str  # query post rewriting
    retreived_documents: list[str]  # documents retrieved
    retrieval_attemps: int  # number of attempts
    retrieval_success: bool  # whether the retrieval was successful
