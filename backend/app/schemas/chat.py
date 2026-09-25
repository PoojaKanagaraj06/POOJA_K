from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str | None = Field(default=None, description="Question to ask about the uploaded documents")


class ChatResponse(BaseModel):
    answer: str
    sources: list
