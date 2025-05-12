from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
from typing import List, Optional
import uvicorn
from core.data_extraction import DataExtractionApp
from models.models import (
    ExtractionResponse, 
    ExtractionRequest, 
    DocumentInfo, 
    ExtractorType,
    ProcessingStatus
)

app = FastAPI(
    title="Document Extraction API",
    description="API for extracting content from various document types",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory storage for background tasks (replace with database in production)
extraction_tasks = {}

@app.get("/")
def read_root():
    return {"message": "Document Extraction API is running"}

@app.post("/upload", response_model=ExtractionResponse)
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload a document file for extraction"""
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{task_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Determine extractor type based on file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext in ['.pdf']:
        extractor_type = ExtractorType.PDF
    elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
        extractor_type = ExtractorType.IMAGE
    elif file_ext in ['.xlsx', '.xls', '.csv']:
        extractor_type = ExtractorType.EXCEL
    else:
        os.remove(file_path)  # Clean up file
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # Add task to queue
    extraction_tasks[task_id] = {
        "status": ProcessingStatus.PENDING,
        "file_path": file_path,
        "file_name": file.filename,
        "extractor_type": extractor_type,
        "result": None,
        "error": None
    }
    
    # Process in background
    if background_tasks:
        background_tasks.add_task(process_document, task_id)
    else:
        # For sync processing (useful for testing)
        await process_document(task_id)
    
    return ExtractionResponse(
        task_id=task_id,
        status=ProcessingStatus.PENDING,
        message="Document uploaded and queued for processing"
    )

async def process_document(task_id: str):
    """Process document in background"""
    if task_id not in extraction_tasks:
        return
    
    task = extraction_tasks[task_id]
    extraction_app = DataExtractionApp()
    
    try:
        # Update status
        task["status"] = ProcessingStatus.PROCESSING
        extraction_tasks[task_id] = task
        
        # Process document
        result = extraction_app.extract(
            task["file_path"], 
            extractor_type=task["extractor_type"]
        )
        
        # Update task with results
        task["status"] = ProcessingStatus.COMPLETED
        task["result"] = result
        extraction_tasks[task_id] = task
        
    except Exception as e:
        # Update task with error
        task["status"] = ProcessingStatus.FAILED
        task["error"] = str(e)
        extraction_tasks[task_id] = task

@app.get("/status/{task_id}", response_model=ExtractionResponse)
async def get_status(task_id: str):
    """Get status of an extraction task"""
    if task_id not in extraction_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = extraction_tasks[task_id]
    
    response = ExtractionResponse(
        task_id=task_id,
        status=task["status"],
        message=f"Document extraction {task['status'].value}"
    )
    
    if task["status"] == ProcessingStatus.COMPLETED and task["result"]:
        response.document = DocumentInfo(
            filename=task["file_name"],
            content=task["result"]["content"],
            page_count=task["result"].get("page_count", 1),
            metadata=task["result"].get("metadata", {})
        )
    elif task["status"] == ProcessingStatus.FAILED:
        response.message = f"Processing failed: {task['error']}"
    
    return response

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task and its associated files"""
    if task_id not in extraction_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Remove file if it exists
    task = extraction_tasks[task_id]
    if "file_path" in task and os.path.exists(task["file_path"]):
        os.remove(task["file_path"])
    
    # Remove task from memory
    del extraction_tasks[task_id]
    
    return {"message": f"Task {task_id} and associated files deleted"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)