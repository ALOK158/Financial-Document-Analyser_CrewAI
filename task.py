## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import financial_document_tool, investment_analysis_tool, risk_assessment_tool, search_tool

## 1. ANALYSIS TASK
analyze_financial_document_task = Task(
    description=(
        "Analyze the financial document located at '{file_path}' in context of the user's query: {query}. "
        "Use the FinancialDocumentTool to read the file at that path. "
        "Extract key insights such as revenue trends, profit margins, debt ratios, "
        "and liquidity indicators."
    ),
    expected_output=(
        "A concise 3–4 paragraph summary detailing financial performance, "
        "highlighting profitability, liquidity, and growth metrics, backed by extracted data."
    ),
    tools=[financial_document_tool],
    agent=financial_analyst
)

## 2. INVESTMENT TASK
investment_analysis_task = Task(
    description=(
        "Using the findings from the financial analysis of '{file_path}' and the user's query: {query}, "
        "generate responsible investment recommendations. Consider profitability, growth potential, "
        "debt management, and market conditions."
    ),
    expected_output=(
        "A structured investment report with 3–5 recommendations, "
        "each justified by financial reasoning or evidence from the document."
    ),
    tools=[investment_analysis_tool],
    agent=investment_advisor
)

## 3. RISK TASK
risk_assessment_task = Task(
    description=(
        "Perform a detailed risk evaluation based on the data in '{file_path}' and user's query: {query}. "
        "Identify potential threats such as market volatility, credit exposure, or liquidity shortages. "
        "Use the RiskTool to extract indicators and provide mitigation suggestions."
    ),
    expected_output=(
        "A structured 2–3 paragraph risk report highlighting major financial risks "
        "and offering at least two actionable mitigation recommendations."
    ),
    tools=[risk_assessment_tool],
    agent=risk_assessor
)

## 4. VERIFICATION TASK
verify_document_task = Task(
    description=(
        "Verify whether the document at '{file_path}' contains legitimate financial content "
        "relevant to the user's query: {query}. "
        "Use the FinancialDocumentTool to inspect structure, figures, and tables "
        "to confirm authenticity."
    ),
    expected_output=(
        "A short validation report confirming whether the document is a financial report. "
        "If invalid, provide a one-line explanation why."
    ),
    tools=[financial_document_tool],
    agent=verifier
)

__all__ = [
    "verify_document_task",
    "analyze_financial_document_task",
    "investment_analysis_task",
    "risk_assessment_task"
]