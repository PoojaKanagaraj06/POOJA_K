from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    id: str
    originalName: str
    fileType: str
    fileSize: int
    uploadedAt: datetime


class DocumentListItem(BaseModel):
    id: str
    originalName: str
    fileType: str
    fileSize: int
    uploadedAt: datetime


class DocumentDetail(DocumentListItem):
    extractedText: str
