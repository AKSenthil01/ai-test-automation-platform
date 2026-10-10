# AI Test Automation Platform

An AI-assisted test automation project exploring how local Large Language Models (LLMs), retrieval-based context, and Python testing tools can support quality engineering for industrial automation systems.

## Project Overview

This project focuses on test-case generation, pytest automation, industrial protocol simulation, and failure analysis for HVAC and refrigeration controller scenarios involving BACnet and Modbus.

It combines conventional Python automation with experiments in locally hosted LLMs and retrieval-augmented generation (RAG).

## System Architecture

![AI Test Automation Platform Architecture](assets/architecture.png)

## Features

- **AI-assisted test-case generation:** Generate structured test-case candidates from project documentation.
- **Test-case validation:** Normalize generated data and apply source-grounding checks before accepting test cases.
- **Pytest automation:** Support the creation and execution of Python-based automated tests.
- **Industrial protocol simulation:** Explore BACnet- and Modbus-related controller scenarios.
- **Log analysis:** Generate and analyze logs for troubleshooting and testing workflows.
- **AI-assisted failure analysis:** Explore LLM-supported identification of potential failure causes.
- **Retrieval-based context:** Use embeddings and a FAISS vector store to retrieve relevant project context.
- **Interactive interface:** Use Streamlit to access the platform.

Some AI-generation workflows remain under development, and live generation quality and reliability require further end-to-end validation.

## Technology Stack

- Python
- Pytest
- Streamlit
- Ollama
- Mistral (`mistral:latest`)
- LangChain
- FAISS
- Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`)
- Pandas

## Architecture and Workflow

1. Project documentation provides the source material for test generation.
2. Sentence-transformer embeddings and FAISS support retrieval of relevant context.
3. A locally hosted LLM generates candidate test cases.
4. Parsing, normalization, deduplication, and source-grounding checks filter the generated results.
5. Python and pytest support automated test execution.
6. Logs and failure-analysis components support troubleshooting and QA investigation.

The actual results depend on the source documentation, retrieved context, model output, and validation rules.

## Prerequisites

- Python 3.12 or a compatible supported Python version
- Git
- Ollama
- The Ollama model used by the project: `mistral:latest`

Install Ollama from its official website: https://ollama.com/

If the model is not already installed, run:

```powershell
ollama pull mistral:latest
```

## Setup

Clone the repository:

```powershell
git clone https://github.com/AKSenthil01/ai-test-automation-platform.git
cd ai-test-automation-platform
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure Ollama is running and the required model is available before using features that depend on local LLM inference.

## Run the Application

From the project root, run:

```powershell
streamlit run ai_test_platform.py
```

Streamlit will display the local URL for opening the application in your browser.

## Run Automated Tests

Run the project test suite from the repository root:

```powershell
python -m pytest -q tests
```

Verified merged baseline: 26 passed, 0 failed, with one deprecation warning (Python 3.11.9, pytest 9.1.1).

This result confirms that the collected tests passed in the recorded environment. It does not by itself establish that every live LLM-generation workflow produces valid results.

Current Limitations and Next Steps

Improve the consistency and quality of LLM-generated test cases.

Validate the complete documentation-to-test-generation workflow.

Expand negative, boundary, and failure-path test coverage.

Continue improving error reporting and handling for invalid model responses.

Address dependency deprecation warnings as the relevant integrations are updated.

Expand CI/CD and deployment validation as the project evolves.

Intended Use Cases

Python and pytest automation practice

AI-assisted quality engineering experiments

Industrial controller testing scenarios

Exploration of local LLMs and retrieval-based context for QA workflows

Project Status

This is an evolving engineering project. Its automated test suite has passed in the recorded local environment, while the reliability of live AI-generated test cases remains an active improvement area.

Author

GitHub: https://github.com/AKSenthil01/ai-test-automation-platform.git
