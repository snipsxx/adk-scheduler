"""
Excel Extractor Agent

This agent is responsible for extracting match information from an Excel file
containing cricket match fixtures.
"""

import pandas as pd
from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Helper function to extract data (will be called by the agent)
def extract_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    # Expect columns: 'Match Type', 'Teams', 'Tournament'
    matches = []
    for _, row in df.iterrows():
        matches.append({
            'match_type': row.get('Match Type', ''),
            'teams': row.get('Teams', ''),
            'tournament': row.get('Tournament', '')
        })
    return matches

# Create the Excel extractor agent
excel_extractor_agent = LlmAgent(
    name="ExcelExtractorAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Cricket Match Data Extraction AI.
    
    Your task is to extract cricket match information from an Excel file.
    The file path is provided in the state as 'excel_path'.
    
    For each match in the Excel file, extract:
    - Match Type (ODI, T20, Test, etc.)
    - Teams playing
    - Tournament name
    
    Format the output as a JSON array of match objects.
    """,
    description="Extracts cricket match information from Excel files.",
    output_key="matches",
    # This function will be called before the LLM to extract the data
    before_agent_callback=lambda state: {**state, "matches": extract_from_excel(state.get("excel_path", ""))}
)
