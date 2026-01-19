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
    async def analyze_investment_tool(financial_document_data):
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement investment analysis logic here
        return "Investment analysis functionality to be implemented"

## Creating Risk Assessment Tool
class RiskTool:
    async def create_risk_assessment_tool(financial_document_data):        
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"