from datetime import datetime
from pathlib import Path

from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.database import documents_collection
from app.services.file_service import ALLOWED_EXTENSIONS, extract_text_from_file, save_uploaded_file, validate_file

router = APIRouter(prefix="/api/documents", tags=["documents"])


def validate_object_id(document_id: str) -> ObjectId:
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=400, detail="Invalid document ID.")
    return ObjectId(document_id)


@router.post("/upload", summary="Upload a document", description="Upload a .txt, .md, or .json file and store metadata and extracted text.")
async def upload_document(file: UploadFile = File(...)):
    validate_file(file)

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="File is empty.")

    extracted_text = extract_text_from_file(file.filename, file_bytes)
    stored_name, file_path = save_uploaded_file(file.filename, file_bytes)

    document = {
        "originalName": file.filename,
        "storedName": stored_name,
        "filePath": file_path,
        "fileType": Path(file.filename).suffix.lower(),
        "fileSize": len(file_bytes),
        "extractedText": extracted_text,
        "uploadedAt": datetime.utcnow(),
    }
    result = documents_collection.insert_one(document)
    created = documents_collection.find_one({"_id": result.inserted_id})

    return {
        "id": str(created["_id"]),
        "originalName": created["originalName"],
        "fileType": created["fileType"],
        "fileSize": created["fileSize"],
        "uploadedAt": created["uploadedAt"],
    }


@router.get("", summary="List documents", description="Return uploaded documents sorted by newest first.")
async def list_documents():
    documents = list(documents_collection.find({}).sort("uploadedAt", -1))
    return [
        {
            "id": str(doc["_id"]),
            "originalName": doc["originalName"],
            "fileType": doc["fileType"],
            "fileSize": doc["fileSize"],
            "uploadedAt": doc["uploadedAt"],
        }
        for doc in documents
    ]


@router.get("/{document_id}/download", summary="Download a document", description="Download the stored file for a valid document ID.")
async def download_document(document_id: str):
    object_id = validate_object_id(document_id)
    document = documents_collection.find_one({"_id": object_id})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = Path(document["filePath"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Physical file is missing.")

    return FileResponse(path=str(file_path), filename=document["originalName"])


@router.delete("/{document_id}", summary="Delete a document", description="Delete the document metadata and the uploaded physical file.")
async def delete_document(document_id: str):
    object_id = validate_object_id(document_id)
    document = documents_collection.find_one({"_id": object_id})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = Path(document["filePath"])
    if file_path.exists():
        file_path.unlink()

    documents_collection.delete_one({"_id": object_id})
    return {"message": "Document deleted successfully"}
