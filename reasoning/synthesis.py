"""
Pyramid Synthesis - Build Final Deliverable
Implements full Minto structure: SCQA + Answer + Key Line + Evidence
"""

from typing import Dict
from .plan import REASONING_STATE


def synthesize_deliverable(run_id: str, format: str = "markdown") -> Dict:
    """
    Synthesize final Minto Pyramid deliverable.
    
    Structure (Top-Down):
    1. Introduction (SCQA)
       - Situation (context reader knows)
       - Complication (what changed/went wrong)
       - Question (what reader needs answered)
    2. Answer (Governing Thought)
    3. Key Line (3-4 MECE Reasons)
    4. Supporting Evidence (for each reason)
    5. Logical Ordering (based on reasoning type)
    
    Args:
        run_id: The pyramid identifier
        format: "markdown", "json", or "both"
    
    Returns:
        Complete pyramid deliverable with citations
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    print(f"\n📝 Synthesizing Pyramid Deliverable...")
    
    # Get components
    scqa = plan.get("scqa", {})
    governing_thought = plan.get("governing_thought", "")
    reasons = plan.get("reasons", [])
    evidence = plan.get("evidence_collected", {})
    logical_order = plan.get("logical_order_type", "comparative")
    
    # Build deliverable
    if format in ["markdown", "both"]:
        markdown = build_markdown_deliverable(
            scqa, governing_thought, reasons, evidence, logical_order, plan
        )
    else:
        markdown = None
    
    if format in ["json", "both"]:
        json_output = build_json_deliverable(
            scqa, governing_thought, reasons, evidence, logical_order, plan
        )
    else:
        json_output = None
    
    # Update status
    plan["status"] = "synthesized"
    plan["deliverable"] = {
        "markdown": markdown,
        "json": json_output,
        "format": format
    }
    
    print(f"✅ Deliverable Ready")
    
    return {
        "run_id": run_id,
        "status": "synthesized",
        "markdown": markdown,
        "json": json_output,
        "format": format,
        "next_step": "critique_pyramid"
    }


def build_markdown_deliverable(
    scqa: Dict,
    governing_thought: str,
    reasons: List[Dict],
    evidence: Dict,
    logical_order: str,
    plan: Dict
) -> str:
    """
    Build markdown format following Minto structure.
    """
    md = []
    
    # Title
    md.append(f"# Minto Pyramid Analysis\n")
    md.append(f"**Domain:** {plan.get('domain', 'N/A')}\n")
    md.append(f"**Logical Order:** {logical_order.title()}\n")
    md.append(f"**Generated:** {plan.get('created_at', 'N/A')}\n")
    md.append("\n---\n\n")
    
    # SCQA Introduction
    md.append("## Introduction (SCQA)\n\n")
    md.append(f"**Situation:** {scqa.get('situation', 'N/A')}\n\n")
    md.append(f"**Complication:** {scqa.get('complication', 'N/A')}\n\n")
    md.append(f"**Question:** {scqa.get('question', 'N/A')}\n\n")
    
    # Answer (Governing Thought)
    md.append("## Answer (Governing Thought)\n\n")
    md.append(f"**{governing_thought}**\n\n")
    md.append("This is supported by the following key findings:\n\n")
    
    # Key Line (MECE Reasons)
    md.append(f"## Key Line ({len(reasons)} MECE Categories)\n\n")
    
    for i, reason in enumerate(reasons, 1):
        md.append(f"### {i}. {reason['title']}\n\n")
        
        # Evidence for this reason
        reason_evidence = evidence.get(reason['id'], [])
        
        if reason_evidence:
            md.append("**Supporting Evidence:**\n\n")
            for j, evid in enumerate(reason_evidence[:3], 1):  # Top 3 evidence items
                md.append(f"{j}. {evid.get('content', 'N/A')}\n")
                md.append(f"   - *Source:* {evid.get('source', 'N/A')}\n")
                md.append(f"   - *Confidence:* {evid.get('confidence', 0):.2f}\n")
                md.append(f"   - *URL:* [{evid.get('url', 'N/A')}]({evid.get('url', '#')})\n\n")
        else:
            md.append("*Evidence gathering in progress...*\n\n")
    
    # Summary
    md.append("## Summary\n\n")
    md.append(f"This analysis follows the **{logical_order}** ordering pattern, ")
    md.append(f"decomposing the question into **{len(reasons)} MECE categories** ")
    md.append(f"that collectively answer: *{scqa.get('question', 'N/A')}*\n\n")
    
    # MECE Validation
    mece_validation = plan.get("mece_validation", {})
    if mece_validation.get("is_mece"):
        md.append("✅ **MECE Validation:** Passed (no overlaps, no gaps)\n\n")
    else:
        md.append("⚠️ **MECE Validation:** Issues detected - see critique for details\n\n")
    
    return "".join(md)


def build_json_deliverable(
    scqa: Dict,
    governing_thought: str,
    reasons: List[Dict],
    evidence: Dict,
    logical_order: str,
    plan: Dict
) -> Dict:
    """
    Build JSON format with full structure.
    """
    return {
        "meta": {
            "run_id": plan.get("run_id"),
            "domain": plan.get("domain"),
            "subdomain": plan.get("subdomain"),
            "logical_order": logical_order,
            "created_at": plan.get("created_at"),
            "status": plan.get("status")
        },
        "introduction": {
            "scqa": scqa,
            "structure_type": "Situation-Complication-Question-Answer"
        },
        "governing_thought": governing_thought,
        "key_line": {
            "reasons": reasons,
            "count": len(reasons),
            "mece_validated": plan.get("mece_validation", {}).get("is_mece", False)
        },
        "evidence": {
            "by_reason": evidence,
            "total_count": sum(len(e) for e in evidence.values()),
            "summary": plan.get("evidence_summary", [])
        },
        "quality_metrics": {
            "mece_validation": plan.get("mece_validation", {}),
            "critique": plan.get("critique", {})
        }
    }


__all__ = ['synthesize_deliverable']
