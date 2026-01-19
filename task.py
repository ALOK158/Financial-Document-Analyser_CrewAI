## Importing libraries and files


from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import FinancialDocumentTool, InvestmentTool, RiskTool,search_tool
from crewai import Task

## Creating a task to help solve user's query
analyze_financial_document_task = Task(
    description=(
        "Analyze the uploaded financial document in context of the user's query: {query}. "
        "Extract key insights such as revenue trends, profit margins, debt ratios, "
        "and liquidity indicators. Identify any anomalies or notable financial movements."
    ),
    expected_output=(
        "A concise 3–4 paragraph summary detailing financial performance, "
        "highlighting profitability, liquidity, and growth metrics, backed by extracted data."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    agent=financial_analyst
)


## Creating an investment analysis task
investment_analysis_task = Task(
    description=(
        "Using the findings from the financial analysis and the user's query: {query}, "
        "generate responsible investment recommendations. Consider profitability, growth potential, "
        "debt management, and market conditions. Use the InvestmentTool to support your insights."
    ),
    expected_output=(
        "A structured investment report with 3–5 recommendations, "
        "each justified by financial reasoning or evidence from the document."
    ),
    tools=[InvestmentTool.analyze_investment_tool],
    agent=investment_advisor
)


risk_assessment_task = Task(
    description=(
        "Perform a detailed risk evaluation based on the document data and user's query: {query}. "
        "Identify potential threats such as market volatility, credit exposure, or liquidity shortages. "
        "Use the RiskTool to extract indicators and provide mitigation suggestions."
    ),
    expected_output=(
        "A structured 2–3 paragraph risk report highlighting major financial risks "
        "and offering at least two actionable mitigation recommendations."
    ),
    tools=[RiskTool.create_risk_assessment_tool],
    agent=risk_assessor
)


    
verify_document_task = Task(
    description=(
        "Verify whether the uploaded document contains legitimate financial content "
        "that is relevant to the user's query: {query}. "
        "Use the FinancialDocumentTool to inspect structure, figures, and tables "
        "to confirm authenticity."
    ),
    expected_output=(
        "A short validation report confirming whether the document is a financial report. "
        "If invalid, provide a one-line explanation why."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    agent=verifier
)
