from .domain_detector import detect_domain

async def search_evidence_domain_aware(query: str, search_type: str, max_results: int = 5):
    """
    Route search to appropriate sources based on domain.
    
    NEW: Domain-aware search routing
    """
    if search_type == "academic":
        # For technical questions, prioritize academic sources
        # Note: In production, add actual arXiv/Scholar API integration
        results = await search_web_evidence(
            query=f"{query} site:arxiv.org OR site:ieee.org OR site:nature.com OR site:sciencedirect.com",
            max_results=max_results
        )
        
        # If no academic results, fallback to general with academic keywords
        if not results or len(results) < 2:
            results = await search_web_evidence(
                query=f"{query} research paper academic journal",
                max_results=max_results
            )
    
    elif search_type == "business":
        # For business questions, use existing Tavily
        results = await search_web_evidence(query, max_results)
    
    elif search_type == "medical":
        # For medical questions, prioritize medical sources
        results = await search_web_evidence(
            query=f"{query} site:pubmed.ncbi.nlm.nih.gov OR site:nejm.org",
            max_results=max_results
        )
    
    else:
        # General fallback
        results = await search_web_evidence(query, max_results)
    
    return results
