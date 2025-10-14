"""
Evidence Execution with Domain-Aware Search
Each evidence piece must support a specific MECE reason
"""

from typing import Dict, List
import asyncio
from .plan import REASONING_STATE
from .domain_detector import generate_search_queries


async def search_web_evidence_async(query: str, search_type: str, max_results: int = 5) -> List[Dict]:
    """
    Execute web search for evidence.
    
    TODO: Integrate with actual Tavily API
    For now, returns mock evidence structure
    """
    # Mock evidence for demonstration
    return [
        {
            "content": f"Evidence supporting: {query}",
            "url": f"https://example.com/{query.replace(' ', '-')[:50]}",
            "source": "Research Paper" if search_type == "academic" else "Industry Report",
            "confidence": 0.85,
            "relevance": 0.90,
            "recency": "2024-10-01"
        }
        for _ in range(min(max_results, 3))
    ]


def execute_evidence_gathering(run_id: str, stage: str = "all") -> Dict:
    """
    Execute evidence gathering for pyramid analysis.
    
    Each piece of evidence must:
    1. Support a specific MECE reason
    2. Help answer the question that reason raises
    3. Be relevant to the domain
    4. Have credibility and recency
    
    Args:
        run_id: The pyramid identifier
        stage: "all" or specific reason ("reason_1", "reason_2", etc.)
    
    Returns:
        Evidence organized by reason with quality metrics
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    # Get evidence tasks
    if stage == "all":
        tasks = plan["evidence_tasks"]
    else:
        tasks = [t for t in plan["evidence_tasks"] if t["reason_id"] == stage]
    
    print(f"\n🔍 Gathering Evidence:")
    print(f"  Tasks: {len(tasks)}")
    print(f"  Stage: {stage}")
    
    # Execute searches (async)
    evidence_collected = asyncio.run(gather_all_evidence(tasks, plan))
    
    # Calculate metrics
    evidence_summary = []
    total_evidence = 0
    
    for reason in plan["reasons"]:
        reason_id = reason["id"]
        evidence = evidence_collected.get(reason_id, [])
        
        if evidence:
            avg_confidence = sum(e.get("confidence", 0) for e in evidence) / len(evidence)
            avg_relevance = sum(e.get("relevance", 0) for e in evidence) / len(evidence)
        else:
            avg_confidence = 0
            avg_relevance = 0
        
        evidence_summary.append({
            "reason_id": reason_id,
            "reason_title": reason["title"],
            "evidence_count": len(evidence),
            "avg_confidence": avg_confidence,
            "avg_relevance": avg_relevance,
            "sources": [e.get("source") for e in evidence]
        })
        
        total_evidence += len(evidence)
    
    # Store in plan
    plan["evidence_collected"] = evidence_collected
    plan["status"] = "evidence_collected"
    plan["evidence_summary"] = evidence_summary
    
    print(f"\n✅ Evidence Collected:")
    print(f"  Total: {total_evidence} items")
    print(f"  Per Reason: {total_evidence / max(len(plan['reasons']), 1):.1f} avg")
    
    return {
        "run_id": run_id,
        "stage": stage,
        "status": "evidence_collected",
        "evidence_by_reason": evidence_summary,
        "total_evidence": total_evidence,
        "next_step": "synthesize_pyramid"
    }


async def gather_all_evidence(tasks: List[Dict], plan: Dict) -> Dict[str, List[Dict]]:
    """
    Gather evidence for all tasks in parallel.
    """
    domain = plan.get("domain", "general")
    
    # Create async tasks
    async_tasks = []
    for task in tasks:
        query = task["query"]
        search_type = task.get("search_type", "general")
        async_tasks.append(search_web_evidence_async(query, search_type))
    
    # Execute in parallel
    results = await asyncio.gather(*async_tasks)
    
    # Organize by reason
    evidence_by_reason = {}
    for i, task in enumerate(tasks):
        reason_id = task["reason_id"]
        if reason_id not in evidence_by_reason:
            evidence_by_reason[reason_id] = []
        evidence_by_reason[reason_id].extend(results[i])
    
    return evidence_by_reason


__all__ = ['execute_evidence_gathering']
