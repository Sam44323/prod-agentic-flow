import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    approval_node,
    calculator_node,
    calculator_request_node,
    guardrail_node,
    output_error_node,
    output_guardrail_node,
    guardrail_response_node,
    llm_node,
    post_approval_route,
    weather_node,
)
from app.graph.router import approval_route, guardrail_router, route, output_router
from app.graph.state import AgentState

# checkpointer: for saving the graph-state which can be used to continue the flow (with things like HITL)
conn = sqlite3.connect("data/checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

# LangGraph overall automatically passes the AgentState to the nodes

# This is telling lang-graph that every node in the flow would be using the AgentState
graph = StateGraph(AgentState)

# nodes for wrking
graph.add_node("llm", llm_node)
graph.add_node("calculator", calculator_node)
graph.add_node("weather", weather_node)
graph.add_node("approval", approval_node)
graph.add_node("calculator_request", calculator_request_node)
graph.add_node("guardrail", guardrail_node)
graph.add_node("guardrail_response", guardrail_response_node)
graph.add_node("output_error", output_error_node)
graph.add_node("output_guardrail", output_guardrail_node)

# ── Flow ──────────────────────────────────────────────
#   START
#     │
#     ▼ route()
#     ├── "llm" ────────────────────────────────────► llm_node ──► END
#     ├── "weather" ─────────────────────────────────► weather_node ──► END
#     └── "calculator_request"
#           │
#           ▼ approval_route()
#           ├── "approval" ──► approval_node
#           │                      │
#           │                      ▼ post_approval_route()
#           │                      ├── "calculator" ──► calculator_node ──► END
#           │                      └── END
#           └── "execute" ──► calculator_node ──► END

# START → route() dispatches to llm / weather / calculator_request
graph.add_edge(START, "guardrail")  # or START -> load_memory -> guardrail

graph.add_conditional_edges(
    "guardrail",
    guardrail_router,
    {
        "route": "route",
        "guardrail_response": "guardrail_response",
    },
)

graph.add_edge("guardrail_response", END)


graph.add_conditional_edges(
    "route",
    route,
    {
        "calculator_request": "calculator_request",
        "llm": "llm",
        "weather": "weather",
    },
)
# calculator_request → approval_route(): skip approval or pause for HITL
graph.add_conditional_edges(
    "calculator_request",
    approval_route,
    {
        "approval": "approval",
        "execute": "calculator",
    },
)
# approval → post_approval_route(): proceed or cancel based on user's answer
graph.add_conditional_edges(
    "approval",
    post_approval_route,
    {
        "calculator": "calculator",
        END: END,
    },
)
# terminal edges
graph.add_edge("llm", "output_guardrail")
graph.add_edge("weather", "output_guardrail")
graph.add_edge("calculator", "output_guardrail")

graph.add_conditional_edges(
    "output_guardrail",
    output_router,
    {
        "__end__": END,
        "output_error": "output_error",
    },
)

graph.add_edge("output_error", END)


# compiling the graph
app = graph.compile(checkpointer=checkpointer)
