"""
Pyramid Planning with Domain-Aware MECE Generation
"""

import uuid
from typing import Dict, Optional
from .domain_detector import detect_domain
from .mece_generator import generate_mece_reasons, get_search_strategy

# Global state storage
REASONING_STATE = {}


def plan_pyramid(brief: str, audience: str = "executives", 
                constraints: Optional[Dict] = None) -> Dict:
    """
    Create reasoning plan with automatic domain detection.
    
    NEW in v3.1: Automatically detects domain and applies appropriate framework.
    """
    run_id = str(uuid.uuid4())[:8]
    
    # DOMAIN DETECTION - NEW!
    domain, context = detect_domain(brief)
    
    print(f"🔍 Detected domain: {domain.value}")
    print(f"📊 Subdomain: {context.get('subdomain', 'N/A')}")
    print(f"🎯 Confidence: {context['confidence']:.2f}")
    
    # Generate governing thoughts
    governing_thoughts = [
        f"Transform {brief[:50]}... into actionable insights",
        f"Identify critical factors in {brief[:50]}...",
        f"Systematic approach to resolve {brief[:50]}..."
    ]
    
    # DOMAIN-AWARE MECE GENERATION - NEW!
    reasons = generate_mece_reasons(brief, domain, context)
    
    # DOMAIN-AWARE SEARCH STRATEGY - NEW!
    search_strategy = get_search_strategy(domain)
    
    # Create evidence tasks
    evidence_tasks = []
    for reason in reasons:
        evidence_tasks.extend([
            {
                "reason_id": reason["id"],
                "query": f"{reason['title']} {brief[:50]}",
                "search_type": search_strategy,
                "acceptance_criteria": f"Relevant to {domain.value}"
            },
            {
                "reason_id": reason["id"],
                "query": f"{reason['title']} recent developments",
                "search_type": search_strategy,
                "acceptance_criteria": "Current data from 2024-2025"
            }
        ])
    
    plan = {
        "run_id": run_id,
        "status": "planned",
        "domain": domain.value,  # NEW
        "subdomain": context.get('subdomain'),  # NEW
        "search_strategy": search_strategy,  # NEW
        "confidence": context['confidence'],  # NEW
        "brief": brief,
        "audience": audience,
        "constraints": constraints or {},
        "governing_thoughts": governing_thoughts,
        "selected_thought": governing_thoughts[0],
        "reasons": reasons,
        "evidence_tasks": evidence_tasks,
        "mece_score": 1.0,
        "mece_valid": True,
        "total_tasks": len(evidence_tasks),
        "risks": [
            f"Domain-specific data availability ({domain.value})",
            "Assumptions about current state",
            "Time constraints"
        ],
        "next_step": "run_plan_stage"
    }
    
    # Store in global state
    REASONING_STATE[run_id] = plan
    
    return plan


def get_plan(run_id: str) -> Optional[Dict]:
    """Retrieve a plan by run_id."""
    return REASONING_STATE.get(run_id)


__all__ = ['plan_pyramid', 'get_plan', 'REASONING_STATE']
