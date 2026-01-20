from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid
import shutil

# Import our new DB and Worker modules
from database import engine, Base, get_db
from models import AnalysisResult
from celery_worker import run_crew_task

# Create DB tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Analyzer (Async)")

@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document"),
    db: Session = Depends(get_db)
):
    """
    Submit a document for asynchronous analysis.
    Returns a Task ID to check status later.
    """
    try:
        # 1. Save file uniquely
        file_id = str(uuid.uuid4())
        # Ensure absolute path for the worker
        upload_dir = os.path.abspath("data")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"financial_document_{file_id}.pdf")
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # 2. Create Database Record (Status: PENDING)
        db_record = AnalysisResult(
            task_id=file_id, # Using file_id as task_id for simplicity
            query=query,
            status="PENDING"
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        # 3. Dispatch to Celery Worker
        # This returns immediately, not blocking the server
        run_crew_task.delay(query=query, file_path=file_path, db_id=db_record.id)

        return {
            "status": "submitted",
            "task_id": file_id,
            "message": "Analysis started in background. Check status at /status/{task_id}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}")
async def get_analysis_status(task_id: str, db: Session = Depends(get_db)):
    """
    Check the status of a submitted analysis task.
    """
    record = db.query(AnalysisResult).filter(AnalysisResult.task_id == task_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    response = {
        "task_id": task_id,
        "status": record.status,
        "submitted_at": record.created_at
    }

    if record.status == "SUCCESS":
        response["analysis"] = record.result_text
    elif record.status == "FAILED":
        response["error"] = record.result_text

    return response