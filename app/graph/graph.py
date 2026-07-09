import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from app.graph.node.approval import approval_node
from app.graph.node.calculator import calculator_node
from app.graph.node.calculator_request import calculator_request_node
from app.graph.node.guardrail import guardrail_node
from app.graph.node.guardrail_response import guardrail_response_node
from app.graph.node.llm import llm_node
from app.graph.node.query_rewriter import query_rewriter
from app.graph.node.output_error import output_error_node
from app.graph.node.output_guardrail import output_guardrail_node
from app.graph.node.planner import planner_node
from app.graph.node.post_approval_route import post_approval_route
from app.graph.node.retriever import retriever_node
from app.graph.node.weather import weather_node
from app.graph.router import (
    approval_route,
    guardrail_router,
    route,
    output_router,
    planner_router,
)
from app.graph.state import AgentState

# checkpointer: for saving the graph-state which can be used to continue the flow (with things like HITL)
conn = sqlite3.connect("data/checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

# LangGraph overall automatically passes the AgentState to the nodes

# This is telling lang-graph that every node in the flow would be using the AgentState
graph = StateGraph(AgentState)

# nodes for wrking
graph.add_node("planner", planner_node)
graph.add_node("llm", llm_node)
graph.add_node("calculator", calculator_node)
graph.add_node("weather", weather_node)
graph.add_node("approval", approval_node)
graph.add_node("calculator_request", calculator_request_node)
graph.add_node("guardrail", guardrail_node)
graph.add_node("guardrail_response", guardrail_response_node)
graph.add_node("output_error", output_error_node)
graph.add_node("output_guardrail", output_guardrail_node)
graph.add_node("retrieve", retriever_node)
graph.add_node("query_rewriter", query_rewriter)

# ── Flow ───────────────────────────────────────────────────────────────
#   START
#     │
#     ▼ guardrail_node
#     │
#     ▼ guardrail_router()
#     ├── "guardrail_response" ──► guardrail_response_node ──► END (blocked)
#     └── "route" ──► route_node  (passthrough)
#                       │
#                       ▼ route()
#                       ├── "llm" ────────────────────► llm_node
#                       ├── "weather" ────────────────► weather_node
#                       └── "calculator_request"
#                             │
#                             ▼ approval_route()
#                             ├── "approval" ──► approval_node
#                             │                    │
#                             │                    ▼ post_approval_route()
#                             │                    ├── "calculator" ──► calculator_node
#                             │                    └── END (cancelled)
#                             └── "execute" ──► calculator_node
#
#   llm / weather / calculator ──► output_guardrail_node
#                                       │
#                                       ▼ output_router()
#                                       ├── "__end__" ──► END
#                                       └── "output_error" ──► output_error_node ──► END

# START → guardrail → guardrail_router (pass → route_node / fail → guardrail_response → END)
graph.add_edge(START, "guardrail")

graph.add_conditional_edges(
    "guardrail",
    guardrail_router,
    {
        "route": "route",
        "guardrail_response": "guardrail_response",
    },
)

graph.add_edge("guardrail_response", END)

# route_node → route() (llm / weather / calculator_request)
# route_node is a passthrough (no handler) — just holds the conditional edges

graph.add_edge("route", "planner")

graph.add_conditional_edges(
    "planner",
    planner_router,
    {
        "calculator_request": "calculator_request",
        "weather": "weather",
        "retrieve": "query_rewriter",
        "llm": "llm",
    },
)

# when query_rewriter finishes, execution always proceeds to the retrieve node for execution
graph.add_edge("query_rewriter", "retrieve")

# calculator_request → approval_route: skip approval or pause for HITL
graph.add_conditional_edges(
    "calculator_request",
    approval_route,
    {
        "approval": "approval",
        "execute": "calculator",
    },
)

# approval → post_approval_route: proceed (calculator) or cancel (END)
graph.add_conditional_edges(
    "approval",
    post_approval_route,
    {
        "calculator": "calculator",
        END: END,
    },
)

# All outputs run through output_guardrail for validation
graph.add_edge("llm", "output_guardrail")
graph.add_edge("weather", "output_guardrail")
graph.add_edge("calculator", "output_guardrail")
graph.add_edge("retrieve", "llm")

# output_guardrail → output_router: pass (END) or fail (output_error → END)
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
