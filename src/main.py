import asyncio
import logging
import csv
from pathlib import Path
from dotenv import load_dotenv







# Load API keys from .env file
load_dotenv()

from fmcsa import get_fmcsa_data
from sos_scraper import get_sos_data, search_owner_info
from enrichment import enrich_with_llm
from utils import save_output

# Setting up basic logging so we can see what's happening in real-time
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def process_company(company_name, state):
    """
    This is the core worker. It takes a company name, hits the web, 
    extracts what it can, and then passes it through our enrichment logic.
    """
    logger.info(f"Checking out: {company_name} ({state})")
    
    try:
        # Step 1: Fire off the web searches for SOS and FMCSA data in parallel
        # We don't want to wait for one to finish before starting the other.
        fmcsa_task = asyncio.create_task(get_fmcsa_data(company_name))
        sos_task = asyncio.create_task(get_sos_data(company_name, state))
        owner_task = asyncio.create_task(search_owner_info(company_name, state))
        
        fmcsa_data, sos_data, owner_info = await asyncio.gather(fmcsa_task, sos_task, owner_task)
        
        # Step 2: Combine everything we found into one big record
        company_data = {
            "company_name": company_name,
            "state": state,
            "fmcsa_data": fmcsa_data,
            "sos_data": sos_data,
            "owner_info": owner_info
        }
        
        # Step 3: Run it through the 'LLM-style' enrichment to score the lead
        enriched_results = enrich_with_llm(company_data)
        
        # Step 4: Flatten the final dictionary so it's easy to read in JSON/CSV
        return {
            "input_name": company_name,
            "input_state": state,
            "legal_entity_name": sos_data.get("legal_entity_name"),
            "formation_date": sos_data.get("formation_date"),
            "entity_status": sos_data.get("entity_status"),
            "registered_agent": sos_data.get("registered_agent"),
            "officers": sos_data.get("officers"),
            "usdot_number": fmcsa_data.get("dot_number"),
            "fleet_size": fmcsa_data.get("fleet_size"),
            "operating_status": fmcsa_data.get("operating_status"),
            "physical_yard_address": fmcsa_data.get("address") or sos_data.get("physical_yard_address"),
            "owner_name": owner_info.get("owner_name"),
            "owner_email": owner_info.get("owner_email"),
            "estimated_annual_revenue": enriched_results.get("estimated_annual_revenue"),
            "signal_score": enriched_results.get("signal_score"),
            "signal_rationale": enriched_results.get("signal_rationale"),
            "enrichment_status": "Complete"
        }
    except Exception as e:
        logger.error(f"Something went wrong with {company_name}: {e}")
        return {"input_name": company_name, "enrichment_status": "Failed"}

async def main():
    # Let's find our input file
    input_file = Path("data/input_small.csv")



    if not input_file.exists():
        logger.error("Wait, I can't find data/input.csv!")
        return

    # Load the companies we need to research
    companies = []
    with open(input_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)

    logger.info(f"Alright, starting the research for {len(companies)} companies...")
    
    # Run all company lookups at the same time to save time
    tasks = [process_company(c['company_name'], c['state']) for c in companies]
    results = await asyncio.gather(*tasks)
    
    # Save the final structured dataset
    output_path = "output/enriched_companies.json"
    save_output(results, output_path)
    logger.info(f"All done! You can find the results in {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
