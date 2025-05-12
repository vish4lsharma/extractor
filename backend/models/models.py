from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, Optional, List


class ExtractorType(str, Enum):
    """Types of document extractors available"""
    PDF = "pdf"
    IMAGE = "image"
    EXCEL = "excel"


class ProcessingStatus(str, Enum):
    """Status of document processing"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentInfo(BaseModel):
    """Information about a processed document"""
    filename: str
    content: str
    page_count: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)
    current_page: int = 0
    structured_data: Optional[Dict[str, Any]] = None


class ExtractionRequest(BaseModel):
    """Request to extract content from a document"""
    extractor_type: Optional[ExtractorType] = None
    options: Dict[str, Any] = Field(default_factory=dict)


class ExtractionResponse(BaseModel):
    """Response with extraction results"""
    task_id: str
    status: ProcessingStatus
    message: str
    document: Optional[DocumentInfo] = None


class ExtractionResult(BaseModel):
    """Result of document extraction"""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    page_count: int = 1
    structured_data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """API error response"""
    detail: str