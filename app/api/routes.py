from fastapi import APIRouter

from app.api.models import ChatRequest, ChatResponse
from app.graph.graph import app as graph

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = graph.invoke({"user_input": request.message, "final_answer": ""})

    return ChatResponse(answer=result["final_answer"])
