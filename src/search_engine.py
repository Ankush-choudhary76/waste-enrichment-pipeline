import logging
import asyncio
from googlesearch import search
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

import os

async def get_live_snippets(query):
    """
    Fetches real search results using SerpAPI (Google Search Engine).
    Requires SERPAPI_API_KEY environment variable.
    """
    logger.info(f"Searching SerpAPI for: {query}")
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        logger.error("SERPAPI_API_KEY not found in environment variables!")
        return "ERROR: Missing API Key"

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5
    }
    
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                results = resp.json()
                
                # Combine organic results into a single text block for extraction
                snippets = []
                for result in results.get("organic_results", []):
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    snippets.append(f"{title}: {snippet}")
                
                return "\n".join(snippets)
            else:
                logger.warning(f"SerpAPI returned status {resp.status_code}: {resp.text}")
                return ""
    except Exception as e:
        logger.error(f"SerpAPI call failed: {e}")
        return ""



def extract_useful_info(raw_text):
    """
    Heuristic-based extraction logic. 
    Scans the raw discovery text for USDOT and Fleet markers.
    """
    import re
    # More aggressive regex for DOT - looking for any 5-8 digit number near "DOT"
    dot = re.search(r"(?:USDOT|DOT)\s*(?:Number|#)?[:\s]*(\d{5,8})", raw_text, re.IGNORECASE)
    
    # If not found, try just looking for a standalone 6-7 digit number which is often the DOT
    if not dot:
        dot = re.search(r"\b(\d{6,7})\b", raw_text)

    # Regex for Fleet
    fleet = re.search(r"(\d+)\s*(?:power units|trucks|tractors|units|vehicles)", raw_text, re.IGNORECASE)
    
    return {
        "dot": dot.group(1) if dot else None,
        "fleet": int(fleet.group(1)) if fleet else None
    }


