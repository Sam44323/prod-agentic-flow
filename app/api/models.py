from typing import Optional

from pydantic import BaseModel, Field


# request for the interaction of the api
class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Message to send to the model from the user",
    )

    thread_id: Optional[str] = Field(
        min_length=1,
        max_length=100,
        description="Thread ID for resuming the flow",
    )


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
