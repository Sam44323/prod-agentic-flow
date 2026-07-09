from typing import Optional

from pydantic import BaseModel


# request for the interaction of the api
class ChatRequest(BaseModel):
    message: str


# response for the api
class ChatResponse(BaseModel):
    answer: Optional[str] = None

    approval_required: bool = False
    thread_id: Optional[str] = None
    approval_message: Optional[str] = None
    approval_reason: Optional[str] = None


# interrruption-information request
class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool
