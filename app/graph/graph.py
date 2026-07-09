from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from app.graph.nodes import (
    calculator_node,
    llm_node,
    post_approval_route,
    guardrail_node,
    weather_node,
    approval_node,
    calculator_request_node,
)
from app.graph.router import route, approval_route, guardrail_router
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
        "__end__": END,
    },
)


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
graph.add_edge("llm", END)
graph.add_edge("weather", END)
graph.add_edge("calculator", END)


# compiling the graph
app = graph.compile(checkpointer=checkpointer)
