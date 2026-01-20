# Financial Document Analyzer - Debugging & Optimization Report

## 📋 Project Overview
This repository contains the fixed and optimized codebase for the **Financial Document Analyzer**. The original system was plagued by critical runtime errors, missing dependencies, and adversarial prompts designed to generate hallucinations.

This report details the debugging process, categorizing fixes into **Deterministic Bugs** (syntax/logic errors) and **Inefficient Prompts** (AI behavior optimization).

---

## 🛠️ Codebase Fixes (File by File Analysis)

### 1. `agents.py`

| Issue Type | Description | Fix Implementation |
| :--- | :--- | :--- |
| **Deterministic Bug** | **Circular Variable Definition:** The code contained `llm = llm`, which raises a `NameError` or uses an undefined variable. | **Fixed:** Defined the LLM properly using the string connection string: `llm = "groq/llama-3.1-8b-instant"` (via `litellm`). |
| **Deterministic Bug** | **Argument Typo:** The Agent class was initialized with `tool=[...]` instead of the correct argument `tools=[...]`. | **Fixed:** Corrected the argument to `tools=[...]`. |
| **Deterministic Bug** | **Memory Crash:** `memory=True` was enabled without an OpenAI API key or custom embedder, causing immediate crashes on startup. | **Fixed:** Set `memory=False` to ensure stability without external dependencies. |
| **Inefficient Prompt** | **Adversarial Personas:** Agents were explicitly instructed to "make up facts," "ignore compliance," and "sell meme stocks." | **Fixed:** Rewrote backstories to enforce professional, factual, and compliant financial analysis standards. |

### 2. `task.py`

| Issue Type | Description | Fix Implementation |
| :--- | :--- | :--- |
| **Deterministic Bug** | **Invalid Tool Reference:** Tasks referenced the raw class method `FinancialDocumentTool.read_data_tool` instead of an instantiated tool object. | **Fixed:** Imported and passed the initialized tool instance `financial_document_tool` from `tools.py`. |
| **Inefficient Prompt** | **Hallucination Instructions:** Tasks explicitly asked agents to "include random URLs," "make up numbers," and "contradict themselves." | **Fixed:** Rewrote task descriptions to strictly require evidence-based analysis derived *only* from the provided document path. |
| **Inefficient Prompt** | **Missing Context:** Tasks did not pass the `{file_path}` variable dynamically, causing agents to guess which file to read. | **Fixed:** Added dynamic path injection (`located at {file_path}`) to every task description. |

### 3. `tools.py` (Major Overhaul)

| Issue Type | Description | Fix Implementation |
| :--- | :--- | :--- |
| **Deterministic Bug** | **Missing Imports & Classes:** The code used `Pdf(...)` without importing a PDF library, causing a `NameError`. | **Fixed:** Integrated `pdfplumber` for robust PDF text extraction. |
| **Deterministic Bug** | **Windows Encoding Crash:** Using standard file reading (`open()`) on binary PDFs caused `UnicodeDecodeError` ('charmap' codec) on Windows. | **Fixed:** Switched to `pdfplumber.open()`, which handles binary PDF streams correctly across all OSs. |
| **Inefficient Prompt** | **Rate Limit Explosion:** The tool attempted to read the *entire* PDF. For large files (12k+ tokens), this exceeded the Groq Free Tier limit (6k TPM), causing `429 Errors`. | **Fixed:** Added **Truncation Logic**: Limits output to the first 5 pages and strictly cuts text at 5,000 characters to fit the context window. |
| **Inefficient Prompt** | **Schema Confusion:** The tool lacked a Pydantic `args_schema`. The 8B model hallucinated complex inputs (sending dictionaries instead of strings). | **Fixed:** Defined a strict `FinancialDocumentInput` Pydantic model to force the LLM to send valid inputs. |

### 4. `main.py`

| Issue Type | Description | Fix Implementation |
| :--- | :--- | :--- |
| **Deterministic Bug** | **Relative Path Errors:** Files were saved to `data/`, but Agents often failed to resolve this path depending on the execution context. | **Fixed:** Implemented `os.path.abspath()` to convert all paths to absolute system paths before execution. |
| **Inefficient Prompt** | **API Throttling:** The sequential execution of 4 agents fired requests instantly, hitting rate limits immediately. | **Fixed:** Added `max_rpm=3` to the `Crew` config. This introduces a "cool-down" delay between agents, allowing the token bucket to refill. |


## 🌟 Bonus Features (Advanced Architecture)

Beyond the standard requirements, this project implements a production-ready **Asynchronous Architecture**:

### 1. Asynchronous Task Queue (Celery + Redis)
* **Why:** To prevent the API from blocking during long-running AI analysis.
* **Implementation:** Used **Celery** with **Redis** (via Memurai on Windows) to offload document processing to background workers.
* **Benefit:** The API returns a Task ID immediately, allowing the system to handle high concurrency without timeouts.

### 2. Database Persistence (SQLite + SQLAlchemy)
* **Why:** To maintain a history of analyzed documents and ensure data isn't lost if the client disconnects.
* **Implementation:** Integrated **SQLAlchemy** with SQLite.
* **Schema:** Stores `task_id`, `status` (PENDING/SUCCESS/FAILED), `result_text`, and `created_at`.

### 3. Robust Error Handling
* **Status Tracking:** The system tracks task failures in the database. If an AI agent fails, the user sees a "FAILED" status with the error message instead of a generic 500 error.


## 🛠️ Tech Stack & Configuration

This project is built on a specific stack to ensure high performance and stability:

* **LLM Engine:** [Groq](https://groq.com/) (Model: `llama-3.1-8b-instant`)
    * *Why:* Chosen for its near-instant inference speed (300+ tokens/s), which is critical for real-time financial analysis agents.
* **Orchestration:** [CrewAI](https://www.crewai.com/) **(Latest Version)**
    * *Critical Fix:* Upgraded to the latest version to resolve persistent `chromodb` dependency errors found in older releases.
    * *Feature Usage:* Enabled `max_rpm` (Rate Limiting), a feature unavailable in older versions, to prevent hitting the Groq API limits (429 Errors).
* **LLM Gateway:** [LiteLLM](https://docs.litellm.ai/) **v1.81.0**
    * *Why:* Used to stabilize the connection between CrewAI and the Groq API, preventing authentication & model-not-found errors.
* **PDF Processing:** `pdfplumber`
    * *Why:* Replaced the default file reader to handle binary PDF streams correctly on Windows systems.
* **Backend & Async (Bonus):**
    * **FastAPI:** High-performance web framework.
    * **Celery + Redis:** For distributed, asynchronous task management.
    * **SQLAlchemy (SQLite):** For robust data persistence.

---

## 🚀 Setup & Usage Instructions

### 1. Prerequisites
* Python 3.10 or higher
* A Groq API Key (Set in `.env`)

### 2. Installation
Install the fixed dependencies (including the added `pdfplumber` and `litellm`):

```bash
pip install -r requirements.txt