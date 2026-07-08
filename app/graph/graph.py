from langgraph.graph import END, START, StateGraph

from app.graph.nodes import calculator_node, llm_node
from app.graph.router import route
from app.graph.state import AgentState

# LangGraph overall automatically passes the AgentState to the nodes

# This is telling lang-graph that every node in the flow would be using the AgentState
graph = StateGraph(AgentState)

# nodes for wrking
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
# mapping its return-value ("llm"/"calculator") to actual node names
graph.add_conditional_edges(
    START,
    route,
    {
        "calculator": "calculator",
        "llm": "llm",
    },  # this is not needed here as return-values are same-name to nodes but just in-case
)

graph.add_edge("llm", END)
graph.add_edge("calculator", END)


# compiling the graph
app = graph.compile()
