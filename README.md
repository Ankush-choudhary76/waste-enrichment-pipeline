# Waste Services Enrichment Pipeline — Autonomous Prototype (Final)

This pipeline autonomously enriches waste service companies using real-world data sources. It has been upgraded to replace all simulated components with live discovery and extraction.

### Real Data Architecture
- **Discovery Layer**: Integrated **SerpAPI** (Google Search) for real-time discovery of company profiles, USDOT numbers, and fleet signals.
- **Autonomous Extraction**: Uses heuristic regex patterns to "read" live search snippets and HTML content to identify business metrics at runtime.
- **No Simulation**: All hardcoded discovery proxies and pre-written snippets have been removed.

### What Works
- **USDOT & Fleet Resolution**: Successfully identifies USDOT numbers and fleet counts for major haulers (e.g., Hilco, Silvarole, Best Way) autonomously from the live web.
- **Market Signal Scoring**: Calculates a Signal Score (1-5) based on real fleet sizes and ownership structure.
- **Revenue Estimation**: Generates annual revenue ranges using industry-standard benchmarks applied to real-world fleet data.
- **Entity Resolution**: Infers legal status and formation dates from Secretary of State and business directory snippets.

### What Fails or is Incomplete
- **Direct SAFER Scraping**: The official FMCSA SAFER portal (`safer.fmcsa.dot.gov`) actively blocks automated `httpx` requests with a **403 Forbidden** error. While the code attempts a direct connection, it currently falls back to high-quality search snippets for verification.
- **Direct Contact Info**: Detailed owner emails and phones are rarely public. The pipeline identifies owner names (e.g., *Brendon Pantano*, *Sue Brannan*) but flags contact info for manual research.

### Limitations & Data Gaps
- **Snippet Dependency**: When direct government scraping is blocked, the pipeline relies on search engine snippets. If a company has a very small digital footprint, data may be incomplete.
- **API Key Required**: Requires a `SERPAPI_API_KEY` in the environment or `.env` file to function.
- **Rate Limits**: Subject to the rate limits and activation status of the SerpAPI account.

### Disclosure: Simulation Status
**Zero simulation is used in this version.** 
Every piece of data in the `enriched_companies.json` output was fetched via live API calls or web requests during the run. Fields marked as "Not Found" or "Unknown" represent real gaps in publicly accessible digital data for those specific companies.

### Execution
1. Set your key: `export SERPAPI_API_KEY='your_key'`
2. Run: `python3 src/main.py`
3. Check results: `output/enriched_companies.json`
