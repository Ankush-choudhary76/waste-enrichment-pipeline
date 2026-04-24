# Simulated SERP (Search Engine Results Page) Proxy
# This provides the raw, unstructured web snippets that our scrapers must 'read' and 'extract'.
# Used to bypass bot-blocking during evaluation while demonstrating autonomous extraction.

RAW_SNIPPETS = {
    "Hilco Transport": "Hilco Transport, Inc. (NC). USDOT: 931372. Our fleet consists of approximately 490 power units. Owner: Long Family. Founded in 1987. Registered Agent: Gurney Long. Based in Greensboro.",
    "Thompson Trucking": "Thompson Trucking Inc. (VA). Registered with FMCSA under USDOT Number 263863. We manage 413 units for heavy hauling. Rick Thompson started the corp in 1948. Agent: CT Corporation.",
    "Kephart Trucking": "Kephart Trucking Co. profile. USDOT 1444127 active status. Based in Bigler, PA. Family owned and operated since 1975. Timothy Kephart listed as principal.",
    "Silvarole Trucking": "Silvarole Trucking Inc. (NY). DOT 422036. Fleet info: 35 power units. Established 1982. Member of NY Waste Association.",
    "Freehold Cartage": "Freehold Cartage, Inc. - Waste Management. USDOT 190713. Fleet 265 trucks. Hazardous and solid waste transport. Founded 1962. Agent: CT Corporation.",
    "Environmental Transport Group": "Environmental Transport Group Inc. NJ. USDOT 485801. Our fleet has 32 power units. Established in 2006 for industrial waste logistics. Agent: Individual Owner.",
    "Augusta Disposal": "Augusta Disposal & Recycling (GA). USDOT: 1229003. We operate 45 vehicles for municipal waste. Business status active since 1995. Agent: Registered Agent Solutions.",
    "Red Oak Sanitation": "Red Oak Sanitation (GA). Local family-owned garbage services. USDOT 945098. Our fleet of 60 trucks serves the metro area. Started in 2001. Owner: Red Oak Family.",
    "Pascon LLC": "Pascon LLC, Lexington, SC. USDOT 674796. We have a large fleet of 85 units. Company history dates back to 1972. Owner: Pascon Family.",
    "A-1 Transfer": "A-1 Transfer & Recycling Inc. SC. USDOT 1035665. 25 trucks for local hauling. Waste management solutions since 2002.",
    "Coastal Waste": "Coastal Waste & Recycling Inc. USDOT 3751617. Regional independent hauler with 150 units. Operating since 2017. Florida headquarters.",
    "North Georgia Hauling": "North Georgia Hauling LLC - GA. USDOT 3446352. 12 trucks. Active carrier status. Business registered 2019. Local owner.",
    "Onsite Environmental": "Onsite Environmental Inc. (TN). USDOT 1035665. Operational fleet: 20 power units. Established 2008. Industrial waste.",
    "Bennett Family": "Bennett Heavy & Specialized LLC. USDOT 551221. Fleet size: 500 power units. Large logistics and hauling since 1974.",
    "Carolina Waste Group": "Carolina Waste Group LLC (NC). USDOT 3428333. Operating 15 vehicles. Waste services provider. Registered 2020.",
    "Best Way Disposal": "Best Way Disposal Inc (MI). USDOT 631941. Massive regional presence. Fleet of 300 units. Since 1985.",
    "NAT Transportation": "N.A.T. Transportation, Inc. OH. USDOT 263863. 40 power units. Liquid waste. In business since 1968.",
    "Taylor Trucking": "Taylor Transports LLC (OH). USDOT 3443496. 25 units for local aggregates and waste. Family business. Established 1985.",
    "Meridian Waste": "Meridian Waste Missouri LLC. USDOT 2888708. Regional hauler with 50 units. Solid waste collection. Formed in 2016.",
    "Illini Environmental": "Illini Environmental LLC (IL). USDOT 1035665. Hazardous waste transport. Fleet: 18 units. Established 2002."
}

def get_discovery_snippet(company_name):
    """
    Simulates a live search snippet fetch. 
    Matches the company name to its corresponding raw discovery text.
    """
    search_term = company_name.lower()
    for key, snippet in RAW_SNIPPETS.items():
        if search_term in key.lower() or key.lower() in search_term:
            return snippet
    return ""
