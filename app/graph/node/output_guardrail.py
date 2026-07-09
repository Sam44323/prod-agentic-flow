from app.graph.state import AgentState
from app.graph.dependencies import policy_engine


def output_guardrail_node(state: AgentState) -> AgentState:
    response = state["messages"][-1].content

    valid, reason = policy_engine.validate_output(str(response))

    state["output_valid"] = valid
    state["output_validation_reason"] = reason

    return state
