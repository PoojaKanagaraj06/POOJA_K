from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question to ask about the uploaded documents")


class ChatResponse(BaseModel):
    answer: str
    sources: list
