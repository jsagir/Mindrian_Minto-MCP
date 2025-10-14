"""
Minto Pyramid Logic MCP Server v3.1
Implements Barbara Minto's Pyramid Principle with Sequential Thinking
"""

from fastmcp import FastMCP
from typing import Dict, List, Optional
from datetime import datetime

# Import reasoning modules
from reasoning.domain_detector import detect_domain
from reasoning.plan import plan_pyramid_with_thinking, REASONING_STATE
from reasoning.execution import execute_evidence_gathering
from reasoning.synthesis import synthesize_deliverable
from reasoning.critique import critique_pyramid_quality
from reasoning.mece_validator import validate_mece_structure

# Initialize FastMCP server
mcp = FastMCP("Minto Pyramid Logic v3.1")


# ============================================================
# STAGE 1: PLANNING (SCQA + MECE with Sequential Thinking)
# ============================================================

@mcp.tool()
def plan_pyramid(
    brief: str,
    audience: str = "executives",
    constraints: Optional[Dict] = None
) -> Dict:
    """
    Create Minto Pyramid plan using Sequential Thinking.
    
    Implements Barbara Minto's methodology:
    1. SCQA Introduction (Situation-Complication-Question-Answer)
    2. MECE Decomposition (3-4 categories, no overlaps, no gaps)
    3. Vertical Q&A Dialogue (each level answers question above)
    4. Horizontal Logic (deductive OR inductive, never mixed)
    5. Logical Ordering (deductive/chronological/structural/comparative)
    
    Uses sequential-thinking tool to reason through proper structure.
    
    Args:
        brief: The question/problem to analyze
        audience: Target audience (affects SCQA framing)
        constraints: Optional constraints
    
    Returns:
        {
            run_id, 
            scqa: {situation, complication, question, answer},
            mece_reasons: [3-4 categories],
            domain, confidence,
            logical_order_type,
            reasoning_chain: [sequential thinking steps]
        }
    """
    return plan_pyramid_with_thinking(brief, audience, constraints)


# ============================================================
# MECE VALIDATION (Core Minto Principle)
# ============================================================

@mcp.tool()
def validate_mece(run_id: str) -> Dict:
    """
    Validate MECE compliance of pyramid structure.
    
    Checks:
    - Mutually Exclusive: No overlaps between categories
    - Collectively Exhaustive: No gaps, covers everything
    - Cognitive Load: 3-4 categories (not 7+)
    - Same Kind: All categories at same logical level
    
    Returns:
        {
            is_mece: bool,
            has_overlaps: bool,
            overlaps: [list of overlapping pairs],
            has_gaps: bool,
            gaps: [list of missing areas],
            category_count: int,
            cognitive_load_ok: bool,
            same_kind: bool
        }
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    return validate_mece_structure(plan)


# ============================================================
# STAGE 2: EVIDENCE EXECUTION (Domain-Aware)
# ============================================================

@mcp.tool()
def run_plan_stage(
    run_id: str,
    stage: str = "all"
) -> Dict:
    """
    Execute evidence gathering with domain-aware search.
    
    Each piece of evidence must SUPPORT a specific MECE reason
    and help answer the question it raises.
    
    Args:
        run_id: The pyramid run identifier
        stage: Which stage to run ("all", "reason_1", etc.)
    
    Returns:
        {
            run_id, status,
            evidence_by_reason: {reason_id: [evidence]},
            total_evidence, avg_confidence
        }
    """
    return execute_evidence_gathering(run_id, stage)


# ============================================================
# STAGE 3: SYNTHESIS (Build Pyramid Deliverable)
# ============================================================

@mcp.tool()
def synthesize_pyramid(
    run_id: str,
    format: str = "markdown"
) -> Dict:
    """
    Synthesize final Minto Pyramid deliverable.
    
    Structure:
    1. Introduction (SCQA)
       - Situation (context)
       - Complication (what changed)
       - Question (what reader needs to know)
    2. Answer (Governing Thought)
    3. Key Line (3-4 MECE reasons)
    4. Supporting Evidence (for each reason)
    5. Logical Ordering (based on reasoning type)
    
    Args:
        run_id: The pyramid run identifier
        format: "markdown", "json", or "both"
    
    Returns:
        {
            deliverable: {scqa, answer, reasons, evidence},
            format, citations
        }
    """
    return synthesize_deliverable(run_id, format)


# ============================================================
# STAGE 4: CRITIQUE (Quality Validation)
# ============================================================

@mcp.tool()
def critique_pyramid(run_id: str) -> Dict:
    """
    Validate pyramid against Minto quality standards.
    
    Checks:
    1. SCQA completeness and relevance
    2. Governing thought is actual summary of reasons
    3. MECE compliance (no overlaps, no gaps)
    4. Vertical Q&A flow (each level answers question above)
    5. Horizontal logic (deductive OR inductive, consistent)
    6. Logical ordering (follows one of 4 patterns)
    7. Evidence sufficiency and relevance
    8. Cognitive load (3-4 categories max)
    
    Returns:
        {
            overall_score, 
            passed: bool,
            findings: {scqa, mece, vertical, horizontal, ordering, evidence},
            recommendations: [list]
        }
    """
    return critique_pyramid_quality(run_id)


# ============================================================
# HELPER TOOLS
# ============================================================

@mcp.tool()
def get_pyramid_status(run_id: str) -> Dict:
    """
    Get current status and structure of pyramid analysis.
    
    Returns:
        Current pyramid state with SCQA, MECE reasons, evidence counts, quality scores
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    return {
        "run_id": run_id,
        "status": plan.get("status"),
        "domain": plan.get("domain"),
        "scqa": plan.get("scqa"),
        "mece_reasons": [r["title"] for r in plan.get("reasons", [])],
        "mece_valid": plan.get("mece_validation", {}).get("is_mece"),
        "evidence_count": sum(len(e) for e in plan.get("evidence_collected", {}).values()),
        "quality_score": plan.get("critique", {}).get("overall_score")
    }


@mcp.tool()
def list_active_pyramids() -> List[Dict]:
    """
    List all active pyramid analyses in memory.
    
    Returns:
        List of {run_id, brief, domain, status, created_at}
    """
    return [
        {
            "run_id": run_id,
            "brief": plan.get("brief", "")[:100] + "...",
            "domain": plan.get("domain"),
            "status": plan.get("status"),
            "created_at": plan.get("created_at")
        }
        for run_id, plan in REASONING_STATE.items()
    ]


# ============================================================
# SERVER INFO
# ============================================================

@mcp.tool()
def get_minto_principles() -> Dict:
    """
    Return the core Minto Pyramid Principle rules.
    
    Educational tool for understanding the methodology.
    """
    return {
        "three_rules": {
            "rule_1": "Ideas at any level must ALWAYS be summaries of ideas grouped below",
            "rule_2": "Ideas in each grouping must ALWAYS be the SAME KIND of idea",
            "rule_3": "Ideas in each grouping must ALWAYS be LOGICALLY ORDERED (deductive/chronological/structural/comparative)"
        },
        "mece_principle": {
            "mutually_exclusive": "No overlaps between categories (avoid double-counting)",
            "collectively_exhaustive": "No gaps in coverage (avoid missing information)"
        },
        "scqa_structure": {
            "situation": "Establish context the reader knows",
            "complication": "What changed or went wrong",
            "question": "What question does this raise in reader's mind?",
            "answer": "The governing thought (main message)"
        },
        "cognitive_load": "Limit to 3-4 categories (mind holds 7±2 items, 3 is ideal)",
        "vertical_relationship": "Each statement raises a question (Why? How?) answered by level below",
        "horizontal_relationship": "Use deductive OR inductive logic (never mix in same grouping)",
        "logical_orders": ["Deductive (argument)", "Chronological (time)", "Structural (space)", "Comparative (importance)"]
    }


if __name__ == "__main__":
    print("🏛️  Minto Pyramid Logic MCP Server v3.1")
    print("📚 Based on Barbara Minto's Pyramid Principle")
    print("\n✨ Features:")
    print("  ✅ SCQA Introduction (Situation-Complication-Question-Answer)")
    print("  ✅ MECE Decomposition (3-4 categories, validated)")
    print("  ✅ Sequential Thinking Integration (smart reasoning)")
    print("  ✅ Vertical Q&A Dialogue (question/answer flow)")
    print("  ✅ Horizontal Logic (deductive OR inductive)")
    print("  ✅ 4 Logical Orders (deductive/chronological/structural/comparative)")
    print("  ✅ Domain-Aware Evidence Gathering")
    print("  ✅ Quality Validation (8 checkpoints)")
    print("\n🚀 Server running...")
    
    mcp.run()
