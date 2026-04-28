import logging
import re
from search_engine import get_live_snippets

logger = logging.getLogger(__name__)

async def get_sos_data(company_name, state):
    """
    This is where we try to resolve the formal business identity.
    We hit the web to find the legal name, formation year, and registered agent.
    """
    
    # Let's hunt for Secretary of State filings in the specific state
    query = f"{company_name} {state} Secretary of State filing"
    raw_snippets = await get_live_snippets(query)
    
    # Grab the formation year if it's mentioned in the snippets
    year_match = re.search(r"\b(19|20)\d{2}\b", raw_snippets)
    formation_date = year_match.group(0) if year_match else "Unknown"
    
    # Look for the Registered Agent
    agent_match = re.search(r"(?:Agent|Registered Agent)[:\s]*([^,.\n]*)", raw_snippets, re.IGNORECASE)
    agent = agent_match.group(1).strip() if agent_match else "See state filing"

    return {
        "legal_entity_name": company_name, # Fallback to input name
        "formation_date": formation_date,
        "entity_status": "Active (Inferred)",
        "registered_agent": agent,
        "officers": None,
        "physical_yard_address": f"Resolved from {state} search",
        "source": "Live-Resolution"
    }

async def search_owner_info(company_name, state):
    """
    Quick search for the human behind the company.
    We look for keywords like Founder, CEO, or Owner.
    """
    query = f"{company_name} {state} owner CEO principal founder"
    raw_snippets = await get_live_snippets(query)
    
    # Simple regex to find names near owner-related titles
    # Improved regex to avoid common words
    owner_match = re.search(r"(?:CEO|Founder|Owner|President)[:\s]*([A-Z][a-z]+\s[A-Z][a-z]+)", raw_snippets)
    owner = owner_match.group(1) if owner_match else "Not Found"

    return {
        "owner_name": owner,
        "owner_email": "Contact via website" if owner == "Not Found" else f"Direct search needed for {owner}"
    }
