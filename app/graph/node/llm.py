from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.graph.dependencies import semantic_memory
from app.graph.state import AgentState
from app.llm.qwen import generate
from app.memory.fact_extractor import extract_facts
from app.tools.executor import execute_tool


def llm_node(state: AgentState) -> AgentState:
    messages = state.get("messages", [])

    messages.append(
        HumanMessage(content=state["user_input"]),
    )

    session_id = "default"

    # Extract and store facts
    facts = extract_facts(state["user_input"])

    for key, value in facts.items():
        semantic_memory.save_fact(
            session_id=session_id,
            key=key,
            value=value,
        )

    # Inject semantic memory
    facts = semantic_memory.get_all_facts(session_id)

    # Injecting the known-facts into the context
    if facts:
        memory_context = "\n".join(f"{key}: {value}" for key, value in facts.items())

        messages.insert(
            0,
            SystemMessage(content=f"Known facts about the user:\n{memory_context}"),
        )

    # Inject the retrieved RAG context
    retrieved_documents = state.get("retrieved_documents", [])

    if retrieved_documents:
        retrieval_context = "\n\n".join(retrieved_documents)

        messages.insert(
            0,
            SystemMessage(
                content=(
                    "Use the following retrieved context when answering the user's question.\n\n"
                    f"{retrieval_context}"
                ),
            ),
        )

    response = execute_tool(generate, messages)

    messages.append(
        AIMessage(content=response),
    )

    state["messages"] = messages
    state["final_answer"] = response

    return state
