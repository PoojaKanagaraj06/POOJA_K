from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    originalName: str
    storedName: str
    filePath: str
    fileType: str
    fileSize: int
    extractedText: str
    uploadedAt: datetime = Field(default_factory=datetime.utcnow)
