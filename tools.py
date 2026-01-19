## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tools
from crewai_tools.tools.serper_dev_tool import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool:
    """Reads, cleans, and formats PDF-based financial documents."""

    @staticmethod
    @tool("Read and clean data from a financial document PDF file.")
    def read_data_tool(path: str = "data/sample.pdf") -> str:
        try:
            if not os.path.exists(path):
                return f"⚠️ Error: File not found at path '{path}'. Please upload a valid PDF."

            if not path.lower().endswith(".pdf"):
                return f"⚠️ Error: Unsupported file type. Expected a .pdf file, got '{os.path.splitext(path)[1]}'."

            reader = PDFReadTool(file_path=path)
            docs = reader.load()

            if not docs:
                return "⚠️ Error: No readable content found in the uploaded PDF."

            full_report = ""
            for doc in docs:
                content = " ".join(doc.page_content.strip().split())
                full_report += content + "\n"

            return full_report.strip()

        except Exception as e:
            return f"❌ An unexpected error occurred while reading the document: {str(e)}"


## Creating Investment Analysis Tool
class InvestmentTool:
    """Performs simplified investment analysis on extracted document data."""

    @staticmethod
    @tool("Analyze the financial document data and summarize investment insights.")
    def analyze_investment_tool(financial_document_data: str) -> str:
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


## Creating Risk Assessment Tool
class RiskTool:
    async def create_risk_assessment_tool(financial_document_data):        
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"