from .domain_detector import detect_domain
from .mece_generator import generate_mece_reasons, get_search_strategy

def plan_pyramid(brief: str, audience: str = "executives", constraints: dict = None):
    """
    Create reasoning plan with domain-aware MECE decomposition.
    
    NEW: Automatically detects domain and applies appropriate framework.
    """
    import uuid
    
    run_id = str(uuid.uuid4())[:8]
    
    # NEW: Domain detection
    domain = detect_domain(brief)
    
    # Generate governing thoughts (can be domain-specific in future)
    governing_thoughts = [
        f"Transform {brief[:50]}... into competitive advantage",
        f"Identify hidden opportunities in {brief[:50]}...",
        f"Systematic approach to resolve {brief[:50]}..."
    ]
    
    # NEW: Domain-aware MECE generation
    reasons = generate_mece_reasons(brief)
    
    # NEW: Domain-aware search strategy
    search_strategy = get_search_strategy(domain)
    
    # Create evidence tasks
    evidence_tasks = []
    for reason in reasons:
        evidence_tasks.extend([
            {
                "reason_id": reason["id"],
                "query": f"{reason['title']} {brief[:50]}",
                "search_type": search_strategy,  # NEW
                "acceptance_criteria": "High relevance to technical question"
            },
            {
                "reason_id": reason["id"],
                "query": f"{reason['title']} industry trends",
                "search_type": search_strategy,  # NEW
                "acceptance_criteria": "Current data from 2024-2025"
            }
        ])
    
    plan = {
        "run_id": run_id,
        "status": "planned",
        "domain": domain,  # NEW
        "search_strategy": search_strategy,  # NEW
        "brief": brief,
        "audience": audience,
        "constraints": constraints or {},
        "governing_thoughts": governing_thoughts,
        "selected_thought": governing_thoughts[0],
        "reasons": reasons,
        "evidence_tasks": evidence_tasks,
        "mece_score": 1.0,  # Will be validated
        "mece_valid": True,
        "total_tasks": len(evidence_tasks),
        "risks": [
            "Limited data availability",
            "Assumptions about market conditions",
            "Time constraints"
        ],
        "next_step": "run_plan_stage"
    }
    
    # Store plan in state
    REASONING_STATE[run_id] = plan
    
    return plan
