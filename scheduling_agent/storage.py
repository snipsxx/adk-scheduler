import json
import os

RESULTS_FILE = 'results.json'

def save_result(result_dict):
    """Append a result dict to the results.json file."""
    results = load_results()
    results.append(result_dict)
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

def load_results():
    """Load all results from the results.json file."""
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f) 