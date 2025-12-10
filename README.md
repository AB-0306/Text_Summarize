# Text_Summarize
Tredence Assignment 

# Minimal Workflow Engine: Recursive Summarizer Agent

This repository implements an iterative text summarization and refinement agent using a custom graph-based workflow engine built with FastAPI and LangGraph. The agent uses a cyclic execution model to split long text inputs, generate parallel summaries, merge them, and recursively refine the result until it satisfies predefined length constraints. Summaries are generated using Anthropic’s Claude 3 Haiku model with structured parsing via Pydantic.

---

## Features

* *Cyclic Execution*
  Supports workflows containing loops that continue until dynamic runtime conditions are met.

* *State Persistence*
  Maintains workflow state across iterations to ensure context integrity and reproducible refinement.

* *Structured LLM Output*
  Uses Pydantic models to validate and enforce consistent structured outputs from Claude.

* *Rate Limiting Controls*
  Includes basic safeguards to prevent API overuse when processing large batches of text.

---

## Prerequisites

* Python 3.9 or higher
* Anthropic API Key

---

## Installation

Clone the repository and enter the project directory:


git clone <repository-url>
cd <project-directory>


### 1. Create and activate a virtual environment

macOS/Linux:


python -m venv venv
source venv/bin/activate


Windows:


python -m venv venv
.\venv\Scripts\activate


### 2. Install required dependencies


pip install -r requirements.txt


### 3. Configure environment variables

Create a .env file in the project root:


ANTHROPIC_API_KEY=sk-ant-api03...


---

## Usage

### 1. Start the Server

Launch the FastAPI application:


uvicorn app.main:app --reload


The server will run at:


http://127.0.0.1:8000


### 2. Run the Agent

Use the included test client to construct a cyclic workflow graph and run a full summarization cycle:


python test_client.py


The script will output the number of refinement iterations performed and the final summarized text.

