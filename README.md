# 📊 Financial Document Analyzer
## Debugging, Optimization & Production Hardening Report

---

## 📌 Project Overview

This repository contains the **debugged, optimized, and production-hardened** implementation of the **Financial Document Analyzer**.

The original codebase suffered from:
- Critical runtime failures
- Missing or misconfigured dependencies
- Incorrect tool usage
- Adversarial and hallucination-inducing prompts

This document provides a **systematic breakdown of all fixes**, classified into:

- **Deterministic Bugs** – Syntax, logic, API misuse, or configuration errors  
- **Prompt & Design Inefficiencies** – Issues degrading AI reliability, accuracy, or stability  

The final system is **stable, compliant, and scalable**, suitable for real-world financial document analysis.

---

## 🛠️ Codebase Fixes (File-by-File Analysis)

---

### 1️⃣ `agents.py`

| Category | Issue | Resolution |
|--------|------|------------|
| **Deterministic Bug** | Circular variable definition (`llm = llm`) caused undefined behavior | Properly defined the LLM using LiteLLM routing: `llm = "groq/llama-3.1-8b-instant"` |
| **Deterministic Bug** | Incorrect parameter name (`tool` instead of `tools`) | Corrected to `tools=[...]` as required by the Agent API |
| **Deterministic Bug** | `memory=True` without embedder or OpenAI key caused startup crashes | Disabled memory (`memory=False`) to remove hidden dependencies |
| **Prompt Design Issue** | Adversarial personas encouraged hallucination and non-compliance | Rewrote agent backstories to enforce factual, professional financial analysis |

---

### 2️⃣ `task.py`

| Category | Issue | Resolution |
|--------|------|------------|
| **Deterministic Bug** | Tasks referenced a class method instead of a tool instance | Imported and passed the instantiated `financial_document_tool` |
| **Prompt Design Issue** | Tasks explicitly instructed hallucinations (fake URLs, numbers, contradictions) | Replaced with strict evidence-based instructions |
| **Prompt Design Issue** | Missing dynamic file path context | Injected `{file_path}` explicitly into all task descriptions |

---

### 3️⃣ `tools.py` — Major Refactor

| Category | Issue | Resolution |
|--------|------|------------|
| **Deterministic Bug** | Missing PDF library (`Pdf(...)` undefined) | Integrated `pdfplumber` for robust PDF parsing |
| **Deterministic Bug** | Windows `UnicodeDecodeError` when reading PDFs | Replaced `open()` with `pdfplumber.open()` |
| **Prompt Efficiency Issue** | Entire PDFs loaded causing token overflow and `429` errors | Implemented hard truncation (≤5 pages, ≤5000 characters) |
| **Prompt Reliability Issue** | No `args_schema`, leading to malformed tool calls | Added strict Pydantic schema (`FinancialDocumentInput`) |

---

### 4️⃣ `main.py`

| Category | Issue | Resolution |
|--------|------|------------|
| **Deterministic Bug** | Relative path resolution failures | Converted all paths to absolute paths using `os.path.abspath()` |
| **Prompt Efficiency Issue** | Agents executed too quickly, triggering rate limits | Added `max_rpm=3` to Crew configuration |

---

## 🌟 Bonus Features (Production Architecture)

---

### ⚙️ Asynchronous Task Queue (Celery + Redis)

- Prevents API blocking during long-running document analysis
- Uses Celery workers with Redis (Memurai on Windows)
- API returns a task ID immediately for high concurrency handling

---

### 🗄️ Database Persistence (SQLite + SQLAlchemy)

- Persists task execution history
- Schema includes:
  - `task_id`
  - `status` (PENDING / SUCCESS / FAILED)
  - `result_text`
  - `created_at`

---

### 🛡️ Robust Error Handling

- Failures are recorded at task level
- Users receive meaningful error messages instead of generic 500 responses

---

## 🧰 Tech Stack & Configuration

- **LLM Engine:** Groq (`llama-3.1-8b-instant`)
- **Orchestration:** CrewAI (1.8)
- **LLM Gateway:** LiteLLM v1.81.0
- **PDF Processing:** pdfplumber
- **Backend:** FastAPI
- **Async Processing:** Celery + Redis
- **Persistence:** SQLite with SQLAlchemy ORM

---
## 🚀 Setup & Usage Instructions

### 1. Prerequisites
* **Python 3.10+**
* **Redis Server** (Required for the Task Queue):
    * *Windows:* Install [Memurai Developer Edition](https://www.memurai.com/) (Redis-compatible for Windows) or run Redis via Docker.
    * *Linux/Mac:* Install standard Redis (`sudo apt install redis`).

### 2. Installation
1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  Install the fixed dependencies (including `celery`, `redis`, `pdfplumber`, and `litellm`):
    ```bash
    pip install -r requirements.txt
    ```

3.  Create a `.env` file in the root directory and add your Groq API Key:
    ```env
    GROQ_API_KEY=gsk_your_actual_api_key_here
    ```

### 3. Running the Application
Because this is now an asynchronous microservice, you need **3 separate terminals** running simultaneously:

**Terminal 1: Start Redis/Memurai** (Skip if running as a background service)
```bash
# Verify it is running
memurai-cli ping
# Output should be: "PONG"
```
**Terminal 2: Start the Celery Worker** (The Background AI)
```
Bash

# On Windows, the '--pool=solo' flag is CRITICAL
celery -A celery_worker.celery_app worker --pool=solo --loglevel=info
```
**Terminal 3: Start the FastAPI Server** (The API)
```
Bash

uvicorn main:app --reload
```