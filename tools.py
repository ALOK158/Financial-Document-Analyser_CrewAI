import os
from dotenv import load_dotenv

# 1. Import BaseTool from the main crewai package
from crewai.tools import BaseTool 

# 2. Import specific tools from the crewai_tools package
from crewai_tools import FileReadTool, SerperDevTool

load_dotenv()

# ... rest of your code ...

# ----------------------------------------
# 🔍 Search Tool (Pre-made CrewAI Tool)
# ----------------------------------------
search_tool = SerperDevTool()

# ----------------------------------------
# 📄 Financial Document Reader Tool
# ----------------------------------------
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads, cleans, and formats PDF-based financial documents. Takes a file path as input."

    def _run(self, path: str = "data/sample.pdf") -> str:
        try:
            if not os.path.exists(path):
                return f"⚠️ Error: File not found at path '{path}'. Please upload a valid PDF."

            if not path.lower().endswith(".pdf"):
                return f"⚠️ Error: Unsupported file type. Expected a .pdf file, got '{os.path.splitext(path)[1]}' instead."

            # Use CrewAI's FileReadTool internally to read the raw file
            reader = FileReadTool(file_path=path)
            # Note: FileReadTool._run returns the content directly as a string usually, 
            # but if using the class wrapper, we might need to handle it differently.
            # Here we initialize and run it.
            content = reader._run(file_path=path)

            if not content:
                return "⚠️ Error: No readable content found in the uploaded PDF."

            return content.strip()

        except Exception as e:
            return f"❌ An unexpected error occurred while reading the document: {str(e)}"

# Instantiate the tool
financial_document_tool = FinancialDocumentTool()


# ----------------------------------------
# 💹 Investment Analysis Tool
# ----------------------------------------
class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "Analyze the financial document data and summarize investment insights."

    def _run(self, financial_document_data: str) -> str:
        try:
            if not financial_document_data or len(financial_document_data) < 100:
                return "⚠️ Document too short or invalid for meaningful investment analysis."

            key_terms = ["revenue", "profit", "growth", "debt", "cash flow", "operating margin"]
            findings = [term for term in key_terms if term.lower() in financial_document_data.lower()]

            insights = "📊 Investment Analysis Summary:\n"
            if findings:
                insights += f"- Key financial metrics mentioned: {', '.join(findings)}.\n"
            else:
                insights += "- No major financial metrics identified.\n"

            insights += (
                "- Review revenue growth and profit margins.\n"
                "- Evaluate debt ratios and liquidity levels.\n"
                "- Focus on diversification to reduce risk exposure.\n"
                "- Maintain a long-term outlook guided by fundamentals."
            )
            return insights.strip()

        except Exception as e:
            return f"❌ Error during investment analysis: {str(e)}"

# Instantiate the tool
investment_analysis_tool = InvestmentTool()


# ----------------------------------------
# ⚠️ Risk Assessment Tool
# ----------------------------------------
class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Create a structured risk assessment based on financial data."

    def _run(self, financial_document_data: str) -> str:
        try:
            if not financial_document_data or len(financial_document_data) < 50:
                return "⚠️ Insufficient data for risk assessment."

            risk_terms = ["debt", "loss", "liability", "volatility", "inflation", "exposure", "decline"]
            found_terms = [term for term in risk_terms if term.lower() in financial_document_data.lower()]

            report = "⚠️ Risk Assessment Report:\n"
            if found_terms:
                report += f"- Detected potential risk indicators: {', '.join(found_terms)}.\n"
            else:
                report += "- No major risk indicators detected.\n"

            report += (
                "- Review credit exposure and liquidity risks.\n"
                "- Monitor market volatility and inflation trends.\n"
                "- Assess compliance and operational resilience.\n"
                "- Recommend appropriate hedging or diversification strategies."
            )
            return report.strip()

        except Exception as e:
            return f"❌ Error during risk assessment: {str(e)}"

# Instantiate the tool
risk_assessment_tool = RiskTool()