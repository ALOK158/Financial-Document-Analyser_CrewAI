# agents.py (top section)

import os
from dotenv import load_dotenv
load_dotenv()
from crewai import LLM

from langchain_groq import ChatGroq  
from crewai import Agent

# ✅ Import the lowercase variable name
from tools import search_tool, financial_document_tool, investment_analysis_tool, risk_assessment_tool
# Setting up Groq LLM
# ✅ NEW: Use the string format. CrewAI will automatically use the GROQ_API_KEY from your .env
# Now this will work:
# Use this smaller, faster model to avoid rate limits
llm = "groq/llama-3.1-8b-instant"


# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst",
    goal="Analyze the financial document in relation to the user's query: {query}. "
    "Provide insightful summaries including profitability, liquidity, "
    "growth metrics, and potential market opportunities based on the data.",
    verbose=True,
    memory=False,
    backstory=(
       "You are an experienced financial analyst with over a decade "
        "of experience in interpreting corporate financial statements, "
        "market trends, and balance sheet metrics. Your analysis is "
        "precise, data-driven, and avoids speculation."
    ),
    # ✅ Pass the instantiated variable directly
    tools=[financial_document_tool],
    llm=llm,
    allow_delegation=True  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Validate whether the uploaded document is a financial report "
        "relevant to the user's query: {query}. Check for the presence "
        "of balance sheets, income statements, or structured numeric data "
        "to confirm its authenticity and suitability for further analysis.",
    verbose=True,
    memory=False,
    backstory=(
        "You are a compliance specialist responsible for ensuring that "
        "uploaded documents are authentic financial records. You pay close "
        "attention to identifying structured financial content such as tables, "
        "figures, and key performance indicators before allowing further processing."
    ),
    llm=llm,
    allow_delegation=False
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal=(
        "Based on the financial insights derived from the document and the user's query: {query}, "
        "provide responsible and diversified investment recommendations. "
        "Ensure each recommendation is backed by data and aligns with general financial prudence."
    ),
    backstory=(
        "You are a seasoned financial advisor with expertise in equity markets, mutual funds, and "
        "long-term wealth management. You prioritize ethical investment strategies, "
        "transparency, and client-specific portfolio planning."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False
)



risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal=(
        "Analyze the financial document and assess potential risks "
        "associated with the user's query: {query}. "
        "Identify key risk areas including liquidity, credit exposure, "
        "operational vulnerabilities, and market volatility. "
        "Provide actionable recommendations for mitigating those risks."
    ),
    backstory=(
        "You are an experienced quantitative risk analyst with expertise in "
        "enterprise risk management, compliance, and financial modeling. "
        "Your insights help organizations anticipate and mitigate threats "
        "to capital and market stability. You communicate risk clearly and responsibly."
    ),
    tools=[risk_assessment_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False
)

