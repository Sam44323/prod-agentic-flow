from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.graph.nodes import llm_node, calculator_node
from app.graph.router import router

# This is telling lang-graph that every node in the flow would be using the AgentState
graph = StateGraph(AgentState)

graph.add_node("llm", llm_node)
graph.add_node("calculator", calculator_node)

# defining the flow
# Flow diagram:
#   START ──→ router ──┬──→ llm ──→ END
#                      │
#                      └──→ calculator ──→ END
#
# Router: "+" in input → calculator, else → llm

# conditional-edges: route from START, using router() to decide,
# mapping its return value ("llm"/"calculator") to actual node names
graph.add_conditional_edges(
    START,
    router,
    {"calculator": "calculator", "llm": "llm"},
)

graph.add_edge("llm", END)
graph.add_edge("calculator", END)


# compiling the graph
app = graph.compile()

