import logging
import httpx
from bs4 import BeautifulSoup
from search_engine import get_live_snippets, extract_useful_info

# We'll use this to keep track of any network or parsing hiccups
logger = logging.getLogger(__name__)





async def get_fmcsa_data(company_name):
    """
    This function digs into the web to find trucking-related data.
    It fetches live search snippets, extracts a USDOT number, 
    and then scrapes the official SAFER website for verified details.
    """
    
    # Step 1: Search for the USDOT number
    query = f"{company_name} waste hauler USDOT number"
    raw_snippets = await get_live_snippets(query)
    
    # Step 2: Extract the DOT number from search results
    info = extract_useful_info(raw_snippets)
    dot = info.get("dot")
    
    # Step 3: If we have a DOT number, scrape the real SAFER website
    if dot:
        # The official SAFER snapshot URL
        url = f"https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string={dot}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    
                    # Parsing SAFER's old-school table layout
                    power_units = "Unknown"
                    operating_status = "Unknown"
                    address = "Unknown"
                    
                    # Power Units is usually in a cell near "Power Units"
                    pu_label = soup.find(string=lambda t: "Power Units" in t if t else False)
                    if pu_label:
                        pu_cell = pu_label.find_parent('td').find_next_sibling('td')
                        if pu_cell:
                            power_units = pu_cell.get_text(strip=True)
                    
                    # Operating Status
                    status_label = soup.find(string=lambda t: "Operating Status" in t if t else False)
                    if status_label:
                        status_cell = status_label.find_parent('td').find_next_sibling('td')
                        if status_cell:
                            operating_status = status_cell.get_text(strip=True)
                    
                    # Address
                    addr_label = soup.find(string=lambda t: "Physical Address" in t if t else False)
                    if addr_label:
                        addr_cell = addr_label.find_parent('td').find_next_sibling('td')
                        if addr_cell:
                            address = addr_cell.get_text(separator=' ', strip=True)

                    # Try to convert power_units to int
                    try:
                        fleet_size_int = int(power_units.replace(',', ''))
                    except:
                        fleet_size_int = None

                    return {
                        "dot_number": dot,
                        "fleet_size": fleet_size_int,
                        "fleet_size_raw": power_units,
                        "operating_status": operating_status,
                        "address": address,
                        "status": "success"
                    }
        except Exception as e:
            logger.debug(f"Scraping SAFER failed for {dot}: {e}")

    # Fallback to search-extracted data if scraping fails
    return {
        "dot_number": dot,
        "fleet_size": info.get("fleet") or 0,
        "operating_status": "Inferred from Search" if dot else "Not Found",
        "status": "extracted" if dot else "not_found"
    }
