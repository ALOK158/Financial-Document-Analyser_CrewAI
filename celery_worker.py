import os
from celery import Celery
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document_task 
from database import SessionLocal
from models import AnalysisResult

# Configure Celery to use Redis (or Memurai on Windows)
celery_app = Celery(
    "financial_analyzer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(bind=True)
def run_crew_task(self, query: str, file_path: str, db_id: int):
    """
    Background task to run the CrewAI process.
    """
    try:
        # 1. Initialize the Crew
        financial_crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document_task], 
            process=Process.sequential,
            max_rpm=3 # Keep our safety limit!
        )

        # 2. Run the analysis
        # ✅ FIX: We added 'file_path' to the inputs dictionary below
        result = financial_crew.kickoff(inputs={
            'query': query, 
            'file_path': file_path
        })
        
        result_str = str(result)

        # 3. Update Database with Success
        db = SessionLocal()
        record = db.query(AnalysisResult).filter(AnalysisResult.id == db_id).first()
        if record:
            record.status = "SUCCESS"
            record.result_text = result_str
            db.commit()
        db.close()

        return result_str

    except Exception as e:
        # 4. Handle Failure
        db = SessionLocal()
        record = db.query(AnalysisResult).filter(AnalysisResult.id == db_id).first()
        if record:
            record.status = "FAILED"
            record.result_text = str(e)
            db.commit()
        db.close()
        raise e