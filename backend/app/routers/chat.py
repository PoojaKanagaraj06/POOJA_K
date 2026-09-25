from fastapi import APIRouter, HTTPException

from app.database import documents_collection
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import generate_answer
from app.services.retrieval_service import retrieve_relevant_documents

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse, summary="Ask a question about uploaded documents")
async def ask_question(payload: ChatRequest):
    question = (payload.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    documents = list(documents_collection.find({}))
    relevant_docs = retrieve_relevant_documents(question, documents, top_k=3)

    if not relevant_docs:
        return {"answer": "I could not find relevant information in the uploaded documents.", "sources": []}

    context_parts = []
    sources = []
    for doc in relevant_docs:
        context_parts.append(doc.get("extractedText", ""))
        sources.append({
            "id": str(doc["_id"]),
            "originalName": doc["originalName"],
        })

    context = "\n\n---\n\n".join(context_parts)
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": sources,
    }
