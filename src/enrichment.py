import logging

logger = logging.getLogger(__name__)

def generate_signal_score(company_data):
    """
    This is our logic engine to decide if a company is an 'Acquisition Target'.
    We look at fleet size, ownership structure, and location.
    """
    name = company_data.get("company_name", "Unknown")
    state = company_data.get("state", "Unknown")
    fmcsa = company_data.get("fmcsa_data", {})
    sos = company_data.get("sos_data", {})
    
    fleet_size = fmcsa.get("fleet_size")
    status = sos.get("entity_status")
    
    # Starting score
    score = 1
    rationale_parts = []
    
    # If we couldn't find anything, we don't guess—we flag it for manual review.
    if fleet_size is None and status == "Not Found":
        return 1, "Automated search was inconclusive. Needs a human to double-check the filings."

    # Now let's apply our M&A logic
    score = 3
    if fleet_size:
        if fleet_size > 100:
            score = 4
            rationale_parts.append(f"Strong presence with {fleet_size} trucks.")
        elif 10 < fleet_size <= 100:
            # The 'Sweet Spot' for many acquisitions
            score = 5
            rationale_parts.append(f"Ideal acquisition size with {fleet_size} units.")

    # Looking for family-owned markers (e.g., 'Smith & Sons')
    if any(word in name.lower() for word in ["family", "sons", "bros", "&"]):
        score = min(score + 1, 5)
        rationale_parts.append("Likely a family-owned operation.")

    rationale_parts.append(f"Active market participant in {state}.")
    
    return score, " ".join(rationale_parts)

def estimate_revenue(fleet_size):
    """
    Very rough napkin-math for revenue estimation based on typical industry benchmarks:
    ~$250k - $350k annual revenue per truck.
    """
    if fleet_size is None:
        return "Unknown"
    
    rev_min = fleet_size * 220000
    rev_max = fleet_size * 380000
    return f"${rev_min/1e6:.1f}M - ${rev_max/1e6:.1f}M"

def enrich_with_llm(company_data):
    """
    Simulates what an LLM would do: analyzing multiple data points to 
    provide qualitative insights (Score & Revenue).
    """
    fmcsa = company_data.get("fmcsa_data", {})
    fleet_size = fmcsa.get("fleet_size")
    
    revenue_range = estimate_revenue(fleet_size)
    score, rationale = generate_signal_score(company_data)
    
    return {
        "estimated_annual_revenue": revenue_range,
        "signal_score": score,
        "signal_rationale": rationale
    }
