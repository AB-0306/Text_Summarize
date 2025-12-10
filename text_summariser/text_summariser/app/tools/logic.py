import time
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from app.registry import registry

load_dotenv()

llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0
)

class ChunkSummary(BaseModel):
    summary: str = Field(description="The summary of the specific text chunk")

class RefinedSummary(BaseModel):
    summary: str = Field(description="The refined, shorter version of the text")

parser_chunk = PydanticOutputParser(pydantic_object=ChunkSummary)
parser_refine = PydanticOutputParser(pydantic_object=RefinedSummary)

def split_text(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 1: Split long text into chunks."""
    text = state.get("text", "")
    chunk_size = 2000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return {**state, "chunks": chunks}

def summarize_chunks(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 2: Summarize each chunk independently."""
    chunks = state.get("chunks", [])
    summaries = []
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize the following text concisely.\n{format_instructions}"),
        ("user", "{chunk}")
    ])
    chain = prompt | llm | parser_chunk

    for chunk in chunks:
        try:
            time.sleep(1)
            result = chain.invoke({
                "chunk": chunk,
                "format_instructions": parser_chunk.get_format_instructions()
            })
            summaries.append(result.summary)
        except Exception as e:
            summaries.append(f"[Error: {str(e)}]")
            
    return {**state, "summaries": summaries}

def merge_summaries(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 3: Combine chunk summaries into one text."""
    summaries = state.get("summaries", [])
    merged_text = "\n\n".join(summaries)
    return {**state, "current_summary": merged_text}

def refine_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 4: Refine and shorten the summary."""
    current_text = state.get("current_summary", "")
    iteration = state.get("iteration", 0) + 1
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Refine this summary. Make it about 30% shorter.\n{format_instructions}"),
        ("user", "{text}")
    ])
    chain = prompt | llm | parser_refine
    
    try:
        time.sleep(1)
        result = chain.invoke({
            "text": current_text,
            "format_instructions": parser_refine.get_format_instructions()
        })
        return {
            **state, 
            "current_summary": result.summary, 
            "iteration": iteration
        }
    except Exception as e:
        return {**state, "error": str(e)}

def check_length(state: Dict[str, Any]) -> str:
    """
    Decides whether to loop back or finish.
    Condition: Stop if length < 200 chars OR iterations > 3
    """
    summary = state.get("current_summary", "")
    iteration = state.get("iteration", 0)

    if len(summary) > 200 and iteration < 3:
        return "continue"
    return "stop"


def register_tools():
    registry.register_tool("split_text", split_text)
    registry.register_tool("summarize_chunks", summarize_chunks)
    registry.register_tool("merge_summaries", merge_summaries)
    registry.register_tool("refine_summary", refine_summary)
    
    registry.register_condition("check_length", check_length)