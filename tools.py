import os
from dotenv import load_dotenv
load_dotenv()

# ✅ Correct imports for your environment (CrewAI Tools 1.8.1)
from langchain.tools import tool
from crewai_tools.tools import FileReadTool, SerperDevTool

# ----------------------------------------
# 🔍 Search Tool
# ----------------------------------------
search_tool = SerperDevTool()

# ----------------------------------------
# 📄 Financial Document Reader Tool
# ----------------------------------------
class FinancialDocumentTool:
    """Reads, cleans, and formats PDF-based financial documents."""

    @staticmethod
    @tool("Read and clean data from a financial document PDF file.")
    def read_data_tool(path: str = "data/sample.pdf") -> str:
        """
        Reads, cleans, and formats PDF-based financial documents.
        Handles missing files and unsupported formats safely.
        """
        try:
            if not os.path.exists(path):
                return f"⚠️ Error: File not found at path '{path}'. Please upload a valid PDF."

            if not path.lower().endswith(".pdf"):
                return f"⚠️ Error: Unsupported file type. Expected a .pdf file, got '{os.path.splitext(path)[1]}' instead."

            reader = FileReadTool(file_path=path)
            docs = reader.load()

            if not docs:
                return "⚠️ Error: No readable content found in the uploaded PDF."

            full_report = " ".join(doc.page_content.strip() for doc in docs)
            return full_report.strip()

        except Exception as e:
            return f"❌ An unexpected error occurred while reading the document: {str(e)}"


# ----------------------------------------
# 💹 Investment Analysis Tool
# ----------------------------------------
class InvestmentTool:
    """Performs simplified investment analysis on extracted document data."""

    @staticmethod
    @tool("Analyze the financial document data and summarize investment insights.")
    def analyze_investment_tool(financial_document_data: str) -> str:
        """
        Analyzes financial document text to identify investment-relevant insights
        such as profitability, growth, and cash flow indicators.
        """
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


# ----------------------------------------
# ⚠️ Risk Assessment Tool
# ----------------------------------------
class RiskTool:
    """Assesses risk factors from financial document text."""

    @staticmethod
    @tool("Create a structured risk assessment based on financial data.")
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """
        Evaluates the financial text for risk-related indicators such as
        debt, losses, market volatility, and liquidity exposure.
        """
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
