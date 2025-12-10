# Text_Summarize
Tredence Assignment 

# Minimal Workflow Engine: Recursive Summarizer Agent

This repository contains an iterative text summarization and refinement agent built on a custom graph engine using *FastAPI* and *LangGraph*. The agent utilizes a cyclic workflow to split long texts, generate parallel summaries, merge them, and recursively refine the output until it meets specific length constraints.

## Features

- *Cyclic Execution:* Supports workflows with loops based on dynamic runtime conditions.
- *State Persistence:* Maintains context and data integrity across multiple refinement iterations.
- *Structured Output:* Utilizes Pydantic parsers to ensure consistent data formatting from the LLM (Claude 3 Haiku).
- *Rate Limiting:* Includes built-in safeguards to respect API rate limits during batch processing.

## Prerequisites

- Python 3.9 or higher
- An Anthropic API Key

## Installation

1. *Clone the repository* and navigate to the project directory.

2. *Create and activate a virtual environment:*

   Linux/macOS:
   python -m venv venv
   source venv/bin/activate


   Windows:
   python -m venv venv
   .\venv\Scripts\activate


3. *Install the required dependencies:*
bash
   pip install -r requirements.txt


4. *Configure environment variables:*
   
   Create a .env file in the root directory and add your API key:

   ANTHROPIC_API_KEY=sk-ant-api03...


## Usage

### 1. Start the Server

Launch the application server to handle workflow requests.
bash
uvicorn app.main:app --reload


The server will start at http://127.0.0.1:8000.

### 2. Run the Agent

The included client script demonstrates how to build a cyclic graph programmatically and process a long text input.
bash
python test_client.py


The script will output the iteration count and the final refined summary.

## Workflow Logic

1. *Split:* The input text is divided into chunks of 2000 characters.
2. *Summarize:* Each chunk is summarized independently.
3. *Merge:* Chunk summaries are concatenated into a single draft.
4. *Refine:* The draft is processed to reduce length by approximately 30%.
5. *Evaluate:* The engine checks if the summary is under 200 characters. If not, it loops back to the Refine step (up to 3 times).


