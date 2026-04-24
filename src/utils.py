import re
import json
from pathlib import Path

def extract_dot_number(text):
    """Finds USDOT numbers using regex."""
    match = re.search(r"USDOT\s*(?:Number)?[:\s]*(\d{5,8})", text, re.IGNORECASE)
    return match.group(1) if match else None

def extract_legal_name(text, company_name):
    """Fuzzy extracts formal legal name from text."""
    pattern = rf"({company_name}[^,.\n]*?(?:Inc|LLC|Corporation|Corp|Ltd)\.?)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else f"{company_name} (Resolved)"

def save_output(data, output_path):
    """Saves data to a JSON file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
