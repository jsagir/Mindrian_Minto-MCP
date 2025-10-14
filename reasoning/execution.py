"""
Evidence Execution with Domain-Aware Search Routing
"""

from typing import List, Dict, Optional
import asyncio
from .plan import REASONING_STATE
from .domain_detector import generate_search_queries


async def search_web_evidence(query: str, max_results: int = 5) -> List[Dict]:
    """
    Placeholder for Tavily search integration.
    Replace with actual Tavily API calls.
    """
    # TODO: Integrate with Tavily search
    # For now, return mock results
    return [
        {
            "content": f"Mock evidence for query: {query}",
            "url": f"https://example.com/{query.replace(' ', '-')}",
            "confidence": 0.95
        }
    ]


async def search_evidence_domain_aware(query: str, search_type: str, 
                                      domain: str, max_results: int = 5) -> List[Dict]:
    """
    Route search to appropriate sources based on domain.
    
    NEW: Domain-aware search routing
    """
    # Generate domain-specific queries
    enhanced_queries = []
    
    if search_type == "academic":
        # For technical/scientific questions, prioritize academic sources
        enhanced_queries = [
            f"{query} site:arxiv.org OR site:ieee.org OR site:sciencedirect.com",
            f"{query} research paper",
            f"{query} journal article"
        ]
    
    elif search_type == "business":
        # For business questions, use existing approach
        enhanced_queries = [
            f"{query} market analysis",
            f"{query} industry report",
            query
        ]
    
    elif search_type == "medical":
        # For medical questions, prioritize medical sources
        enhanced_queries = [
            f"{query} site:pubmed.ncbi.nlm.nih.gov OR site:nejm.org",
            f"{query} clinical study",
            query
        ]
    
    else:
        enhanced_queries = [query]
    
    # Execute searches
    all_results = []
    for enhanced_query in enhanced_queries[:2]:  # Use top 2 queries
        results = await search_web_evidence(enhanced_query, max_results=3)
        all_results.extend(results)
        if len(all_results) >= max_results:
            break
    
    return all_results[:max_results]


async def run_plan_stage_async(run_id: str, stage: str = "all") -> Dict:
    """
    Execute evidence gathering with domain-aware routing.
    
    UPDATED: Uses domain-aware search strategy
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    search_strategy = plan.get("search_strategy", "general")
    domain = plan.get("domain", "general")
    
    # Collect evidence for specified stage(s)
    if stage == "all":
        tasks = plan["evidence_tasks"]
    else:
        tasks = [t for t in plan["evidence_tasks"] if t["reason_id"] == stage]
    
    evidence_collected = {}
    
    # Execute searches
    search_tasks = []
    for task in tasks:
        reason_id = task["reason_id"]
        query = task["query"]
        search_type = task.get("search_type", search_strategy)
        
        # Create async search task
        search_tasks.append(
            search_evidence_domain_aware(query, search_type, domain)
        )
    
    # Execute all searches in parallel
    results = await asyncio.gather(*search_tasks)
    
    # Organize by reason
    for i, task in enumerate(tasks):
        reason_id = task["reason_id"]
        if reason_id not in evidence_collected:
            evidence_collected[reason_id] = []
        evidence_collected[reason_id].extend(results[i])
    
    # Calculate metrics
    evidence_summary = []
    for reason in plan["reasons"]:
        reason_id = reason["id"]
        evidence = evidence_collected.get(reason_id, [])
        avg_confidence = sum(e.get("confidence", 0) for e in evidence) / max(len(evidence), 1)
        
        evidence_summary.append({
            "reason_id": reason_id,
            "reason_title": reason["title"],
            "evidence_count": len(evidence),
            "avg_confidence": avg_confidence
        })
    
    # Store evidence in state
    plan["evidence_collected"] = evidence_collected
    plan["status"] = "evidence_collected"
    
    return {
        "run_id": run_id,
        "stage": stage,
        "status": "evidence_collected",
        "evidence_collected": evidence_summary,
        "total_evidence": sum(len(e) for e in evidence_collected.values()),
        "next_step": "synthesize_pyramid"
    }


def run_plan_stage(run_id: str, stage: str = "all") -> Dict:
    """Synchronous wrapper for async execution."""
    return asyncio.run(run_plan_stage_async(run_id, stage))


__all__ = ['run_plan_stage', 'search_evidence_domain_aware']
