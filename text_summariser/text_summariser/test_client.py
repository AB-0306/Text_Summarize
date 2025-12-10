import requests
import time

BASE_URL = "http://127.0.0.1:8000"

graph_payload = {
    "nodes": [
        { "id": "splitter", "function_name": "split_text" },
        { "id": "summarizer", "function_name": "summarize_chunks" },
        { "id": "merger", "function_name": "merge_summaries" },
        { "id": "refiner", "function_name": "refine_summary" }
    ],
    "edges": [
        { "source": "START", "target": "splitter" },
        { "source": "splitter", "target": "summarizer" },
        { "source": "summarizer", "target": "merger" },
        { "source": "merger", "target": "refiner" }
    ],
    "conditional_edges": [
        {
            "source": "refiner",
            "condition_function": "check_length",
            "mapping": {
                "continue": "refiner",
                "stop": "END"
            }
        }
    ]
}

print("Creating Graph...")
response = requests.post(f"{BASE_URL}/graph/create", json=graph_payload)

if response.status_code != 200:
    print(f"Error {response.status_code}:")
    print(response.json())
    exit()

graph_id = response.json()["graph_id"]
print(f"Graph ID: {graph_id}")

long_text = """
The Apollo program was the third United States human spaceflight program carried out by the National Aeronautics and Space Administration (NASA), which succeeded in preparing and landing the first humans on the Moon from 1968 to 1972. It was first conceived in 1960 during the Eisenhower administration as a three-man spacecraft to follow the one-man Project Mercury which put the first Americans in space. Apollo was later dedicated to President John F. Kennedy's national goal of "landing a man on the Moon and returning him safely to the Earth" by the end of the 1960s, which he proposed in an address to Congress on May 25, 1961. 
""" * 5  

print("\nRunning Summarization Workflow...")
run_payload = {
    "graph_id": graph_id,
    "initial_state": {
        "text": long_text
    }
}

start_time = time.time()
result = requests.post(f"{BASE_URL}/graph/run", json=run_payload)
end_time = time.time()

data = result.json()

if data.get("status") == "failed":
    print("❌ Failed:", data.get("logs"))
else:
    final_state = data.get("final_state", {})
    print(f"\n✅ Completed in {end_time - start_time:.2f}s")
    print(f"Iterations: {final_state.get('iteration')}")
    print(f"Final Length: {len(final_state.get('current_summary', ''))}")
    print("\n--- Final Summary ---")
    print(final_state.get("current_summary"))