import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import LOAD_ENV, MONGO_URI
from app.routers.chat import router as chat_router
from app.routers.documents import router as documents_router

load_dotenv()

app = FastAPI(
    title="Document Management & AI Assistant",
    description="Upload documents, retrieve relevant content, and ask questions using a simple AI assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"], summary="Health check")
async def health_check():
    return {"message": "Document AI Backend is running"}


app.include_router(documents_router)
app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
