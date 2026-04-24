import logging
import httpx
from search_engine import get_live_snippets, extract_useful_info

# We'll use this to keep track of any network or parsing hiccups
logger = logging.getLogger(__name__)

async def get_fmcsa_data(company_name):
    """
    This function digs into the web to find trucking-related data.
    It's truly autonomous—it searches, extracts in-memory, and moves on.
    """
    
    # First, let's see what the web has to say about this company's fleet
    query = f"{company_name} waste hauler USDOT number fleet size"
    raw_snippets = await get_live_snippets(query)
    
    # Dig for the DOT and fleet count in the raw search text
    info = extract_useful_info(raw_snippets)
    dot = info.get("dot")
    
    # If we managed to snag a DOT number, let's verify it with a real API
    # This turns our 'guess' into verified data.
    if dot:
        url = f"https://saferwebapi.com/v2/usdot/{dot}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    return {
                        "dot_number": dot,
                        "fleet_size": data.get("power_units"),
                        "operating_status": data.get("operating_status"),
                        "address": data.get("physical_address"),
                        "status": "success"
                    }
        except Exception as e:
            logger.debug(f"Couldn't reach the SAFER API for {dot}, falling back to search data.")

    # If the API was a bust, we return the best guess from our web search
    return {
        "dot_number": dot,
        "fleet_size": info.get("fleet"),
        "operating_status": "Inferred (Live)" if dot else "Not Found",
        "status": "live_extracted" if dot else "not_found"
    }
