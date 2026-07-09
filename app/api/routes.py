from fastapi import APIRouter
import uuid

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from app.api.models import ChatRequest, ChatResponse, ApprovalRequest
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

    # if there's a node/edge in the graph that requires an interruption, we'll return the interruption-info
    if "__interrupt__" in result:
        interrupt = result["__interrupt__"][0]

        return ChatResponse(
            approval_required=True,
            thread_id=thread_id,
            approval_message=interrupt.value["message"],
            approval_reason=interrupt.value["reason"],
        )

    return ChatResponse(answer=result["final_answer"])


# route for the approval and resuming the graph
@router.post("/approve", response_model=ChatResponse)
def approve(request: ApprovalRequest):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }

    result = graph.invoke(
        Command(resume=request.approved),
        config=config,
    )

    return ChatResponse(
        answer=result["final_answer"],
    )
