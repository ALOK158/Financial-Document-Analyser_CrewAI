import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
import pdfplumber

load_dotenv()


search_tool = SerperDevTool()

# ----------------------------------------
# 📄 Financial Document Reader Tool (Prompt Engineered)
# ----------------------------------------

# 1. Keep the Pydantic model for validation
class FinancialDocumentInput(BaseModel):
    path: str = Field(..., description="The absolute file path to the PDF document.")

class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    # ✅ BETTER PROMPTING: Explicitly tell the model the exact JSON format to use
    description: str = (
        "Reads and extracts text from a financial PDF. "
        "INPUT FORMAT: You must provide a JSON object with a single key 'path'. "
        "Example: {'path': 'C:/data/file.pdf'}. "
        "Do NOT include 'properties', 'type', or schema definitions in your input."
    )
    args_schema: type[BaseModel] = FinancialDocumentInput

    def _run(self, path: str) -> str:
        try:
            # 1. Clean the path string
            clean_path = path.strip('"').strip("'")
            
            # 2. Check existence
            if not os.path.exists(clean_path):
                return f"⚠️ Error: File not found at '{clean_path}'."

            # 3. Read PDF safely using pdfplumber
            text_content = []
            with pdfplumber.open(clean_path) as pdf:
                # Limit to first 5 pages to save tokens
                for i, page in enumerate(pdf.pages):
                    if i >= 5: 
                        break
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            
            full_text = "\n".join(text_content)
            
            # 4. SAFETY CUT: Limit to 1000 characters
            if len(full_text) > 1000:
                full_text = full_text[:1000] + "\n... [TRUNCATED TO PREVENT RATE LIMIT ERROR]"
            
            if not full_text:
                return "⚠️ Error: The PDF appears to be empty."
                
            return full_text.strip()

        except Exception as e:
            return f"❌ Error reading PDF: {str(e)}"

financial_document_tool = FinancialDocumentTool()


# ----------------------------------------
# 💹 Investment Analysis Tool
# ----------------------------------------
class InvestmentInput(BaseModel):
    financial_document_data: str = Field(..., description="The extracted text content.")

class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "Analyze financial text for investment metrics."
    args_schema: type[BaseModel] = InvestmentInput

    def _run(self, financial_document_data: str) -> str:
        try:
            if not financial_document_data or len(financial_document_data) < 50:
                return "⚠️ Data insufficient."
            
            key_terms = ["revenue", "profit", "growth", "debt", "cash", "margin"]
            findings = [t for t in key_terms if t.lower() in financial_document_data.lower()]
            
            return f"📊 Found keywords: {', '.join(findings)}. Analyze these sections."

        except Exception as e:
            return f"❌ Error: {str(e)}"

investment_analysis_tool = InvestmentTool()


# ----------------------------------------
# ⚠️ Risk Assessment Tool
# ----------------------------------------
class RiskInput(BaseModel):
    financial_document_data: str = Field(..., description="The extracted text content.")

class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Scan financial text for risk factors."
    args_schema: type[BaseModel] = RiskInput

    def _run(self, financial_document_data: str) -> str:
        try:
            risk_terms = ["litigation", "risk", "debt", "default", "loss"]
            found_risks = [t for t in risk_terms if t.lower() in financial_document_data.lower()]
            
            if found_risks:
                return f"⚠️ Detected risks: {', '.join(found_risks)}."
            return "✅ No immediate risks found."

        except Exception as e:
            return f"❌ Error: {str(e)}"

risk_assessment_tool = RiskTool()