import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def reset_documents():
    try:
        from app.database import documents_collection
        documents_collection.delete_many({})
    except Exception:
        pass


def test_empty_question():
    reset_documents()
    response = client.post("/api/chat", json={"question": ""})
    assert response.status_code == 400


def test_whitespace_question():
    reset_documents()
    response = client.post("/api/chat", json={"question": "   "})
    assert response.status_code == 400


def test_question_with_relevant_document():
    reset_documents()
    client.post(
        "/api/documents/upload",
        files={"file": ("leave-policy.txt", io.BytesIO(b"Employees receive 20 days of annual leave"), "text/plain")},
    )
    response = client.post("/api/chat", json={"question": "How many days of annual leave do employees receive?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["sources"]) >= 1


def test_question_with_no_relevant_document():
    reset_documents()
    client.post(
        "/api/documents/upload",
        files={"file": ("finance.txt", io.BytesIO(b"The office opens at 9am and closes at 5pm"), "text/plain")},
    )
    response = client.post("/api/chat", json={"question": "How many annual leave days are available?"})
    assert response.status_code == 200
    data = response.json()
    assert "I could not find relevant information" in data["answer"]
    assert data["sources"] == []
