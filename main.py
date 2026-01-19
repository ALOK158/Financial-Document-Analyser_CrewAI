from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import (
    verify_document_task,
    analyze_financial_document_task,
    investment_analysis_task,
    risk_assessment_task
)


def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the complete financial document analysis crew sequentially."""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[
            verify_document_task,
            analyze_financial_document_task,
            investment_analysis_task,
            risk_assessment_task
        ],
        process=Process.sequential,
    )

    result = financial_crew.kickoff(inputs={"query": query, "file_path": file_path})
    return result


app = FastAPI(title="Financial Document Analyzer")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "✅ Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze the uploaded financial report comprehensively.")
):
    """Analyze financial document and generate investment, risk, and performance insights."""
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if not query.strip():
            query = "Analyze the uploaded financial report comprehensively."

        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "file_processed": file.filename,
            "crew_summary": str(response)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # ignore cleanup issues


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)