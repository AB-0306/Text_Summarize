from fastapi import FastAPI, HTTPException
from app.models import GraphDefinition, RunRequest, RunResponse
from app.engine import create_graph, run_graph, runs_db
from app.tools.logic import register_tools  # <--- CHANGED IMPORT

app = FastAPI(title="Summarization Agent")

# Register Tools
register_tools()

@app.post("/graph/create")
def api_create_graph(config: GraphDefinition):
    try:
        graph_id = create_graph(config)
        return {"graph_id": graph_id, "message": "Graph created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/graph/run")
def api_run_graph(request: RunRequest):
    try:
        run_id = run_graph(request.graph_id, request.initial_state)
        # In a real app, you might want to return run_id immediately and poll for status.
        # Here we return the final result for simplicity.
        run_data = runs_db[run_id]
        return {
            "run_id": run_id, 
            "status": run_data["status"],
            "final_state": run_data.get("final_state"),
            "logs": run_data.get("logs")
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Graph not found")