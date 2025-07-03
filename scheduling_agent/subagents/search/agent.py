"""
Search Agent

This agent is responsible for finding the scorecard URL for cricket matches
based on match type and tournament information.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Helper function to find scorecard URL using the mapping file
def find_scorecard_url(match_info, mapping_path):
    # mapping file: match_type,tournament,url\n...
    mapping = {}
    with open(mapping_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(',')]
            if len(parts) == 3:
                key = (parts[0].lower(), parts[1].lower())
                mapping[key] = parts[2]
    key = (match_info['match_type'].lower(), match_info['tournament'].lower())
    url = mapping.get(key, 'https://dummy-scorecard-url.com')
    return {
        'url': url,
        'match_name': f"{match_info['teams']} - {match_info['tournament']}",
        'match_type': match_info['match_type']
    }

# Function to process all matches
def process_matches(state):
    matches = state.get('matches', [])
    mapping_path = state.get('mapping_path', '')
    results = []
    
    for match in matches:
        result = find_scorecard_url(match, mapping_path)
        results.append(result)
    
    return {**state, 'results': results}

# Create the search agent
search_agent = LlmAgent(
    name="SearchAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Cricket Scorecard Search AI.
    
    Your task is to find scorecard URLs for cricket matches based on:
    - Match Type (ODI, T20, Test, etc.)
    - Tournament name
    
    Use the mapping file to determine which website to visit for each match type and tournament.
    The mapping file path is provided in the state as 'mapping_path'.
    The matches to search for are provided in the state as 'matches'.
    
    For each match, return:
    - URL of the scorecard
    - Match name (formatted as "Teams - Tournament")
    - Match type
    
    Format the output as a JSON array of result objects.
    """,
    description="Finds scorecard URLs for cricket matches.",
    output_key="results",
    # This function will be called before the LLM to process the matches
    before_agent_callback=process_matches
)
