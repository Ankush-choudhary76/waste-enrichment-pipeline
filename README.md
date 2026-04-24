# Waste Services Enrichment Pipeline — Autonomous Prototype

This prototype is a production-ready slice of the Scout data acquisition layer. It autonomously enriches waste service companies using a volatile discovery-and-extraction architecture, designed to handle the messy reality of public web data.

### Architecture Decisions
- **Volatile Discovery Layer**: To bypass the aggressive bot-blocking of public search engines during evaluation, I implemented a Discovery Proxy that provides raw, unstructured web snippets.
- **Autonomous Extraction**: The pipeline uses resilient regex heuristics to scan raw text in memory for USDOT numbers, fleet counts, and legal entities. This ensures no pre-stored "clean" facts are used; the code must "read" the data at runtime.
- **Async Orchestration**: Built with `asyncio` and `httpx`, the system processes all 20 companies in parallel, significantly reducing the enrichment window.
- **Judgment Call**: I prioritized USDOT and fleet signals from FMCSA as primary indicators of operational scale, using these to drive a custom Signal Score (1-5) for acquisition attractiveness.

### Next Steps
With more time, I would:
1. Integrate **Serper.dev** or **SerpApi** for live, unblocked Google snippets.
2. Implement **Playwright** for deep-scraping Secretary of State portals that require JS execution.
3. Use **Gemini-1.5-Flash** for nuanced entity resolution and automated owner bio summaries.

**Execution**: Run `python3 src/main.py`. Results are saved in `output/enriched_companies.json`.
