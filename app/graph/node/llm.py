from app.graph.state import AgentState
from app.llm.qwen import generate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.memory.fact_extractor import extract_facts
from app.memory.semantic_memory import SemanticMemory
from app.tools.executor import execute_tool

semantic_memory = SemanticMemory()


def llm_node(state: AgentState) -> AgentState:
    print(state)

    messages = state.get("messages", [])

    messages.append(
        HumanMessage(content=state["user_input"]),
    )

    facts = extract_facts(state["user_input"])

    session_id = "default"

    for key, value in facts.items():
        semantic_memory.save_fact(
            session_id=session_id,
            key=key,
            value=value,
        )

    session_id = "default"

    facts = semantic_memory.get_all_facts(session_id)

    if facts:
        memory_context = "\n".join(f"{key}: {value}" for key, value in facts.items())

        messages.insert(
            0,
            SystemMessage(content=f"Known facts about the user:\n{memory_context}"),
        )

    response = execute_tool(generate, messages)

    messages.append(AIMessage(content=response))
    state["messages"] = messages
    state["final_answer"] = response
    print("exiting the llm_node")

    return state
