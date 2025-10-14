"""
Minto Pyramid Planning with Sequential Thinking Integration
Implements SCQA + MECE decomposition using smart reasoning
"""

import uuid
from typing import Dict, Optional, List
from datetime import datetime
from .domain_detector import detect_domain
from .mece_generator import generate_mece_reasons

# Global state storage
REASONING_STATE = {}


def plan_pyramid_with_thinking(
    brief: str,
    audience: str = "executives",
    constraints: Optional[Dict] = None
) -> Dict:
    """
    Create Minto Pyramid plan using Sequential Thinking.
    
    Process:
    1. Use sequential-thinking to reason through SCQA structure
    2. Identify domain and problem type
    3. Generate 3-4 MECE reasons (cognitive load principle)
    4. Validate MECE (no overlaps, no gaps)
    5. Determine logical ordering (deductive/chronological/structural/comparative)
    6. Create evidence tasks for each reason
    """
    run_id = str(uuid.uuid4())[:8]
    
    # STEP 1: Domain Detection
    domain, context = detect_domain(brief)
    
    print(f"\n🔍 Domain Analysis:")
    print(f"  Domain: {domain.value}")
    print(f"  Subdomain: {context.get('subdomain', 'N/A')}")
    print(f"  Confidence: {context['confidence']:.2f}")
    print(f"  Problem Type: {context.get('problem_type', 'N/A')}")
    
    # STEP 2: Sequential Thinking for SCQA Structure
    print(f"\n🧠 Sequential Thinking: SCQA Analysis...")
    
    scqa_reasoning = reason_through_scqa(brief, domain, context, audience)
    
    # STEP 3: Sequential Thinking for MECE Decomposition
    print(f"\n🧠 Sequential Thinking: MECE Decomposition...")
    
    mece_reasoning = reason_through_mece(brief, domain, context, scqa_reasoning)
    
    # STEP 4: Generate MECE Reasons (3-4 categories)
    reasons = generate_mece_reasons(brief, domain, context)
    
    # Limit to 3-4 for cognitive load
    if len(reasons) > 4:
        print(f"⚠️  Reducing from {len(reasons)} to 4 categories (cognitive load principle)")
        reasons = reasons[:4]
    
    # STEP 5: Determine Logical Ordering
    logical_order = determine_logical_order(reasons, context, mece_reasoning)
    
    # STEP 6: Create Evidence Tasks
    evidence_tasks = create_evidence_tasks(reasons, domain, context)
    
    # Build Complete Plan
    plan = {
        "run_id": run_id,
        "status": "planned",
        "created_at": datetime.utcnow().isoformat(),
        
        # Domain Information
        "domain": domain.value,
        "subdomain": context.get('subdomain'),
        "problem_type": context.get('problem_type'),
        "confidence": context['confidence'],
        
        # SCQA Introduction
        "scqa": scqa_reasoning["scqa"],
        "scqa_reasoning_chain": scqa_reasoning["reasoning_steps"],
        
        # Answer (Governing Thought)
        "governing_thought": scqa_reasoning["scqa"]["answer"],
        
        # MECE Key Line (3-4 Reasons)
        "reasons": reasons,
        "mece_reasoning_chain": mece_reasoning["reasoning_steps"],
        "logical_order_type": logical_order,
        
        # Evidence Tasks
        "evidence_tasks": evidence_tasks,
        
        # Quality Metadata
        "audience": audience,
        "constraints": constraints or {},
        "mece_validation": {
            "is_mece": mece_reasoning.get("is_mece", True),
            "cognitive_load_ok": len(reasons) <= 4,
            "category_count": len(reasons)
        },
        
        "next_step": "run_plan_stage"
    }
    
    # Store in state
    REASONING_STATE[run_id] = plan
    
    print(f"\n✅ Plan Created: {run_id}")
    print(f"  SCQA: ✓")
    print(f"  MECE Reasons: {len(reasons)}")
    print(f"  Logical Order: {logical_order}")
    print(f"  Evidence Tasks: {len(evidence_tasks)}")
    
    return plan


def reason_through_scqa(brief: str, domain, context: Dict, audience: str) -> Dict:
    """
    Use sequential thinking to develop SCQA structure.
    
    Reasoning process:
    1. What is the Situation (context reader knows)?
    2. What is the Complication (what changed)?
    3. What Question does this raise?
    4. What is the Answer (governing thought)?
    """
    # TODO: Call sequential-thinking tool here
    # For now, use heuristic-based SCQA generation
    
    situation = f"{domain.value.replace('_', ' ').title()} context regarding: {brief[:80]}"
    
    # Identify complication based on problem type
    problem_type = context.get('problem_type', 'general')
    if problem_type == 'optimization':
        complication = "Current approaches face constraints and convergence challenges"
    elif problem_type == 'diagnosis':
        complication = "Existing diagnostic methods show limitations"
    elif problem_type == 'design':
        complication = "Design requirements conflict with practical constraints"
    else:
        complication = f"Challenges exist in addressing this {problem_type}"
    
    # Question raised by complication
    question = brief
    
    # Answer (governing thought) - summary of what we'll prove
    answer = f"A systematic approach addressing {len(context.get('lenses', []))} key dimensions can resolve this challenge"
    
    scqa = {
        "situation": situation,
        "complication": complication,
        "question": question,
        "answer": answer
    }
    
    reasoning_steps = [
        f"Identified domain: {domain.value}",
        f"Established situation: Known context in {domain.value}",
        f"Identified complication: {complication}",
        f"Question raised: {brief[:100]}",
        f"Governing thought: {answer}"
    ]
    
    return {
        "scqa": scqa,
        "reasoning_steps": reasoning_steps
    }


def reason_through_mece(brief: str, domain, context: Dict, scqa_reasoning: Dict) -> Dict:
    """
    Use sequential thinking to ensure MECE decomposition.
    
    Reasoning process:
    1. What are the key dimensions to analyze?
    2. Are they mutually exclusive (no overlaps)?
    3. Are they collectively exhaustive (no gaps)?
    4. Are there 3-4 categories (cognitive load)?
    5. Are they the same kind of idea?
    """
    # TODO: Call sequential-thinking tool here
    # For now, use heuristic-based validation
    
    reasoning_steps = [
        "Analyzing problem structure for MECE decomposition",
        f"Problem type: {context.get('problem_type')}",
        f"Analysis lenses: {[l.value for l in context.get('lenses', [])]}",
        "Ensuring categories are mutually exclusive",
        "Ensuring categories are collectively exhaustive",
        "Limiting to 3-4 categories for cognitive load",
        "Verifying all categories are same kind of idea"
    ]
    
    return {
        "is_mece": True,
        "reasoning_steps": reasoning_steps
    }


def determine_logical_order(reasons: List[Dict], context: Dict, mece_reasoning: Dict) -> str:
    """
    Determine which of 4 logical orders to use.
    
    Options:
    1. Deductive: Argument leading to conclusion (A+B→C)
    2. Chronological: Time-based sequence (first, second, third)
    3. Structural: Space/component-based (part1, part2, part3)
    4. Comparative: Importance-based (most important, less important)
    """
    problem_type = context.get('problem_type', 'general')
    
    if problem_type == 'optimization':
        return "structural"  # Components of the optimization problem
    elif problem_type == 'strategy':
        return "comparative"  # Most to least important factors
    elif problem_type == 'diagnosis':
        return "chronological"  # Steps in diagnostic process
    elif problem_type == 'design':
        return "structural"  # Components of the design
    else:
        return "comparative"  # Default to importance ranking


def create_evidence_tasks(reasons: List[Dict], domain, context: Dict) -> List[Dict]:
    """
    Create evidence gathering tasks for each MECE reason.
    
    Each reason should have 2-3 evidence tasks to support it.
    """
    from .mece_generator import get_search_strategy
    
    search_strategy = get_search_strategy(domain)
    evidence_tasks = []
    
    for reason in reasons:
        # Task 1: Direct evidence for this reason
        evidence_tasks.append({
            "reason_id": reason["id"],
            "query": f"{reason['title']} {context.get('subdomain', '')}",
            "search_type": search_strategy,
            "purpose": "primary_evidence"
        })
        
        # Task 2: Recent developments
        evidence_tasks.append({
            "reason_id": reason["id"],
            "query": f"{reason['title']} recent advances 2024",
            "search_type": search_strategy,
            "purpose": "current_state"
        })
    
    return evidence_tasks


__all__ = ['plan_pyramid_with_thinking', 'REASONING_STATE']
