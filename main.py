from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from crewai import Crew, Process
# Import your agents and tasks
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import (
    verify_document_task,
    analyze_financial_document_task,
    investment_analysis_task,
    risk_assessment_task
)

# Initialize FastAPI
app = FastAPI(title="Financial Document Analyzer")

# main.py

def run_crew(query: str, file_path: str):
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
        
        # ✅ ADD THIS LINE: Limit the crew to 5 requests per minute
        # This forces a delay between agents, giving the API time to reset your token counter.
        max_rpm=5, 
        
        verbose=True
    )

    result = financial_crew.kickoff(inputs={"query": query, "file_path": file_path})
    return result

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
    
    # Generate a unique filename to prevent conflicts
    file_id = str(uuid.uuid4())
    filename = f"financial_document_{file_id}.pdf"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save the file temporarily
    relative_path = os.path.join("data", filename)
    
    # ---------------------------------------------------------
    # 🔑 CRITICAL FIX 1: Convert to Absolute Path
    # Agents work best when given the full system path (C:\Users\...)
    # ---------------------------------------------------------
    absolute_file_path = os.path.abspath(relative_path)

    try:
        # Write the uploaded file to disk
        with open(absolute_file_path, "wb") as f:
            f.write(await file.read())

        if not query.strip():
            query = "Analyze the uploaded financial report comprehensively."

        # ---------------------------------------------------------
        # 🔑 CRITICAL FIX 2: Pass the ABSOLUTE path to the crew
        # ---------------------------------------------------------
        response = run_crew(query=query.strip(), file_path=absolute_file_path)

        return {
            "status": "success",
            "query": query,
            "file_processed": file.filename,
            "crew_summary": str(response)
        }

    except Exception as e:
        # Log the error to console for debugging
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    finally:
        # Cleanup: Remove the file after processing to keep folder clean
        if os.path.exists(absolute_file_path):
            try:
                os.remove(absolute_file_path)
                print(f"🗑️ Cleanup: Removed {filename}")
            except Exception as e:
                print(f"⚠️ Warning: Could not remove temporary file: {e}")

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to make it accessible
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)