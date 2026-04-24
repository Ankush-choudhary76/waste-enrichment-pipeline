import re
import logging
import asyncio
from web_discovery import get_discovery_snippet

logger = logging.getLogger(__name__)

async def get_live_snippets(query):
    """
    Simulates fetching search results from the web.
    We hit our Discovery Proxy to get the raw messy snippets.
    This demonstrates the code's ability to extract data from raw text.
    """
    # Small delay to mimic network latency
    await asyncio.sleep(0.1)
    
    # Extract the base company name from the query
    company_name = query.split(" ")[0]
    
    snippet = get_discovery_snippet(company_name)
    return snippet

def extract_useful_info(raw_text):
    """
    Heuristic-based extraction logic. 
    Scans the raw discovery text for USDOT and Fleet markers.
    """
    # Regex for DOT
    dot = re.search(r"USDOT\s*(?:Number)?[:\s]*(\d{5,8})", raw_text, re.IGNORECASE)
    # Regex for Fleet
    fleet = re.search(r"(\d+)\s*(?:power units|trucks|tractors|units)", raw_text, re.IGNORECASE)
    
    return {
        "dot": dot.group(1) if dot else None,
        "fleet": int(fleet.group(1)) if fleet else None
    }
