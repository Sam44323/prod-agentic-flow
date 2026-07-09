from fastapi import APIRouter
import uuid

from langchain_core.runnables import RunnableConfig

from app.api.models import ChatRequest, ChatResponse
from app.graph.graph import app as graph
from app.graph.state import AgentState  # wherever AgentState is defined

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    thread_id = str(uuid.uuid4())

    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    initial_state: AgentState = {
        "user_input": request.message,
        "final_answer": "",
        "messages": [],
        "tool_name": "",
        "tool_input": "",
        "tool_output": "",
        "error": "",
        "approval_required": False,
        "approval_granted": False,
        "approval_reason": "",
    }

    # in this we are thread_id to every execution so that we can use it a reference for resuming
    result = graph.invoke(initial_state, config=config)

    return ChatResponse(answer=result["final_answer"])

