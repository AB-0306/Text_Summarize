from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Configuration Models (for creating graphs) ---

class NodeConfig(BaseModel):
    id: str
    function_name: str  # Must match a registered tool/function

class EdgeConfig(BaseModel):
    source: str
    target: str

class ConditionalEdgeConfig(BaseModel):
    source: str
    condition_function: str # Name of a registered conditional function
    mapping: Dict[str, str] # Maps condition output to target node IDs

class GraphDefinition(BaseModel):
    nodes: List[NodeConfig]
    edges: List[EdgeConfig]
    conditional_edges: Optional[List[ConditionalEdgeConfig]] = []

# --- Runtime Models (for running graphs) ---

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class RunResponse(BaseModel):
    run_id: str
    status: str
    final_state: Optional[Dict[str, Any]] = None
    logs: List[str] = []