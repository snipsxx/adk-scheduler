"""
Cricket Match Scorecard Pipeline

This is a sequential agent pipeline that:
1. Extracts cricket match information from an Excel file
2. Finds scorecard URLs for each match based on a mapping file
3. Stores the results in a local JSON file
"""

import sys
import json
from google.adk.agents import SequentialAgent

# Import the subagents
from subagents.excel.agent import excel_extractor_agent
from subagents.search.agent import search_agent
from storage import save_result

# Create the sequential agent
root_agent = SequentialAgent(
    name="CricketScoreCardPipeline",
    sub_agents=[excel_extractor_agent, search_agent],
    description="A pipeline that extracts cricket match info and finds scorecard URLs"
)

def store_results(state):
    """Store the results from the pipeline in a local JSON file."""
    results = state.get('results', [])
    for result in results:
        save_result(result)
        print(f"Stored result: {result}")
    return state

def main():
    """CLI entry point for the pipeline."""
    if len(sys.argv) != 3:
        print("Usage: python -m scheduling_agent.agent <excel_file_path> <mapping_file_path>")
        sys.exit(1)
        
    excel_path = sys.argv[1]
    mapping_path = sys.argv[2]
    
    # Initialize the state with the input file paths
    initial_state = {
        'excel_path': excel_path,
        'mapping_path': mapping_path
    }
    
    # Run the pipeline
    print(f"Starting pipeline with Excel file: {excel_path}")
    final_state = root_agent.run_async(initial_state).result()
    
    # Store the results
    store_results(final_state)
    
    print("Pipeline completed successfully.")
    print(f"Processed {len(final_state.get('results', []))} matches.")

if __name__ == "__main__":
    main()

