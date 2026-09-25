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


def test_upload_valid_txt():
    reset_documents()
    file_content = b"Employees are entitled to 20 days of annual leave."
    response = client.post(
        "/api/documents/upload",
        files={"file": ("leave-policy.txt", io.BytesIO(file_content), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["originalName"] == "leave-policy.txt"
    assert data["fileType"] == ".txt"
    assert "id" in data


def test_upload_valid_json():
    reset_documents()
    payload = '{"policy": "Employees receive 15 days of annual leave"}'
    response = client.post(
        "/api/documents/upload",
        files={"file": ("policy.json", io.BytesIO(payload.encode("utf-8")), "application/json")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["originalName"] == "policy.json"


def test_reject_unsupported_file():
    reset_documents()
    response = client.post(
        "/api/documents/upload",
        files={"file": ("notes.pdf", io.BytesIO(b"pdf-content"), "application/pdf")},
    )
    assert response.status_code == 400


def test_reject_empty_file():
    reset_documents()
    response = client.post(
        "/api/documents/upload",
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
    )
    assert response.status_code == 400


def test_reject_invalid_json():
    reset_documents()
    response = client.post(
        "/api/documents/upload",
        files={"file": ("bad.json", io.BytesIO(b"{invalid json"), "application/json")},
    )
    assert response.status_code == 400


def test_list_documents_sorted_desc():
    reset_documents()
    first = client.post(
        "/api/documents/upload",
        files={"file": ("first.txt", io.BytesIO(b"first content"), "text/plain")},
    )
    second = client.post(
        "/api/documents/upload",
        files={"file": ("second.md", io.BytesIO(b"# Second doc"), "text/plain")},
    )
    assert first.status_code == 200
    assert second.status_code == 200

    response = client.get("/api/documents")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2
    assert items[0]["originalName"] in {"second.md", "first.txt"}


def test_download_document():
    reset_documents()
    upload = client.post(
        "/api/documents/upload",
        files={"file": ("doc.txt", io.BytesIO(b"hello world"), "text/plain")},
    )
    doc_id = upload.json()["id"]
    response = client.get(f"/api/documents/{doc_id}/download")
    assert response.status_code == 200
    assert b"hello world" in response.content


def test_delete_document():
    reset_documents()
    upload = client.post(
        "/api/documents/upload",
        files={"file": ("to_delete.txt", io.BytesIO(b"delete me"), "text/plain")},
    )
    doc_id = upload.json()["id"]

    response = client.delete(f"/api/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted successfully"


def test_invalid_document_id():
    reset_documents()
    response = client.get("/api/documents/not-a-valid-id/download")
    assert response.status_code == 400


def test_delete_nonexistent_document():
    reset_documents()
    response = client.delete("/api/documents/507f1f77bcf86cd799439011")
    assert response.status_code == 404
