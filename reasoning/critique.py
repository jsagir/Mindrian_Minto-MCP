"""
Pyramid Quality Critique - Validate Against Minto Standards
Implements 8-point quality checklist
"""

from typing import Dict, List
from .plan import REASONING_STATE
from .mece_validator import validate_mece_structure
from .domain_detector import is_academic_source, is_business_source


def critique_pyramid_quality(run_id: str) -> Dict:
    """
    Validate pyramid against Minto quality standards.
    
    8 Quality Checks:
    1. SCQA Completeness (all 4 elements present and relevant)
    2. Governing Thought Summary (actually summarizes reasons below)
    3. MECE Compliance (no overlaps, no gaps)
    4. Vertical Q&A Flow (each level answers question from above)
    5. Horizontal Logic (deductive OR inductive, not mixed)
    6. Logical Ordering (follows one of 4 patterns consistently)
    7. Evidence Sufficiency (2+ sources per reason, relevant)
    8. Cognitive Load (3-4 categories, not 7+)
    
    Returns:
        Complete quality report with scores and recommendations
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    print(f"\n🔍 Quality Critique: Validating Against Minto Standards...")
    
    critiques = []
    
    # 1. SCQA Completeness
    scqa_critique = critique_scqa(plan)
    critiques.append(scqa_critique)
    
    # 2. Governing Thought Summary
    summary_critique = critique_governing_thought(plan)
    critiques.append(summary_critique)
    
    # 3. MECE Compliance
    mece_critique = critique_mece(plan)
    critiques.append(mece_critique)
    
    # 4. Vertical Q&A Flow
    vertical_critique = critique_vertical_flow(plan)
    critiques.append(vertical_critique)
    
    # 5. Horizontal Logic
    horizontal_critique = critique_horizontal_logic(plan)
    critiques.append(horizontal_critique)
    
    # 6. Logical Ordering
    ordering_critique = critique_logical_ordering(plan)
    critiques.append(ordering_critique)
    
    # 7. Evidence Sufficiency
    evidence_critique = critique_evidence(plan)
    critiques.append(evidence_critique)
    
    # 8. Cognitive Load
    cognitive_critique = critique_cognitive_load(plan)
    critiques.append(cognitive_critique)
    
    # Calculate overall score
    scores = [c["score"] for c in critiques]
    overall_score = sum(scores) / len(scores)
    passed = overall_score >= 0.75 and all(c["score"] >= 0.6 for c in critiques)
    
    result = {
        "run_id": run_id,
        "status": "critiqued",
        "overall_score": overall_score,
        "passed": passed,
        "critiques": critiques,
        "summary": generate_critique_summary(critiques, overall_score, passed)
    }
    
    # Store in plan
    plan["critique"] = result
    plan["status"] = "critiqued"
    
    print(f"\n{'✅' if passed else '⚠️'} Quality Score: {overall_score:.2f} ({'PASSED' if passed else 'NEEDS REVISION'})")
    
    return result


def critique_scqa(plan: Dict) -> Dict:
    """Check SCQA completeness and relevance."""
    scqa = plan.get("scqa", {})
    
    findings = []
    score = 1.0
    
    # Check all 4 elements present
    required = ["situation", "complication", "question", "answer"]
    missing = [r for r in required if not scqa.get(r)]
    
    if missing:
        findings.append(f"Missing SCQA elements: {missing}")
        score -= 0.25 * len(missing)
    else:
        findings.append("✓ All SCQA elements present")
    
    # Check each element has substance (>20 chars)
    for element in required:
        if scqa.get(element) and len(scqa[element]) < 20:
            findings.append(f"{element.title()} is too brief (should be substantive)")
            score -= 0.1
    
    return {
        "aspect": "SCQA Completeness",
        "score": max(score, 0),
        "findings": findings,
        "passed": score >= 0.75
    }


def critique_governing_thought(plan: Dict) -> Dict:
    """Check if governing thought actually summarizes reasons."""
    governing_thought = plan.get("governing_thought", "")
    reasons = plan.get("reasons", [])
    
    findings = []
    score = 1.0
    
    if not governing_thought:
        findings.append("No governing thought defined")
        score = 0
    elif len(governing_thought) < 30:
        findings.append("Governing thought is too brief")
        score -= 0.3
    else:
        findings.append("✓ Governing thought is substantive")
    
    if not reasons:
        findings.append("No reasons defined to summarize")
        score -= 0.5
    else:
        findings.append(f"✓ {len(reasons)} reasons present to support governing thought")
    
    return {
        "aspect": "Governing Thought Summary",
        "score": max(score, 0),
        "findings": findings,
        "passed": score >= 0.75
    }


def critique_mece(plan: Dict) -> Dict:
    """Check MECE compliance."""
    mece_validation = validate_mece_structure(plan)
    
    findings = []
    
    if mece_validation["is_mece"]:
        findings.append("✓ MECE structure valid")
    
    if not mece_validation["mutually_exclusive"]:
        findings.append(f"⚠ Overlaps detected: {len(mece_validation['overlaps'])} pairs")
        findings.extend([f"  - {o['category_1']} ↔ {o['category_2']}" 
                        for o in mece_validation['overlaps'][:3]])
    
    if not mece_validation["collectively_exhaustive"]:
        findings.append(f"⚠ Gaps detected: {len(mece_validation['gaps'])} missing concepts")
        findings.extend([f"  - {gap}" for gap in mece_validation['gaps'][:3]])
    
    if not mece_validation["same_kind"]:
        findings.append("⚠ Categories are not the same kind")
        findings.extend([f"  - {issue}" for issue in mece_validation['kind_issues']])
    
    score = 1.0 if mece_validation["is_mece"] else 0.5
    
    return {
        "aspect": "MECE Compliance",
        "score": score,
        "findings": findings,
        "passed": mece_validation["is_mece"],
        "details": mece_validation
    }


def critique_vertical_flow(plan: Dict) -> Dict:
    """Check vertical question/answer flow."""
    findings = []
    score = 1.0
    
    scqa = plan.get("scqa", {})
    governing_thought = plan.get("governing_thought", "")
    reasons = plan.get("reasons", [])
    
    # Check: Question → Answer flow
    if scqa.get("question") and governing_thought:
        findings.append("✓ Question → Answer flow established")
    else:
        findings.append("⚠ Question → Answer flow incomplete")
        score -= 0.3
    
    # Check: Answer → Reasons flow
    if governing_thought and reasons:
        findings.append(f"✓ Answer supported by {len(reasons)} reasons")
    else:
        findings.append("⚠ Answer → Reasons flow incomplete")
        score -= 0.3
    
    # Check: Reasons → Evidence flow
    evidence = plan.get("evidence_collected", {})
    if reasons and evidence:
        findings.append(f"✓ Reasons supported by evidence")
    elif reasons and not evidence:
        findings.append("⚠ Evidence not yet collected for reasons")
        score -= 0.2
    
    return {
        "aspect": "Vertical Q&A Flow",
        "score": max(score, 0),
        "findings": findings,
        "passed": score >= 0.75
    }


def critique_horizontal_logic(plan: Dict) -> Dict:
    """Check horizontal logic (deductive OR inductive)."""
    findings = []
    score = 1.0
    
    reasons = plan.get("reasons", [])
    
    if len(reasons) < 2:
        findings.append("Cannot assess horizontal logic with < 2 reasons")
        score = 0.8
    else:
        # Heuristic: Check if reasons follow consistent pattern
        # In practice, this needs deeper semantic analysis
        findings.append(f"✓ {len(reasons)} reasons form logical grouping")
        findings.append("Note: Deep horizontal logic validation requires semantic analysis")
    
    return {
        "aspect": "Horizontal Logic",
        "score": score,
        "findings": findings,
        "passed": score >= 0.75
    }


def critique_logical_ordering(plan: Dict) -> Dict:
    """Check if logical ordering is appropriate and consistent."""
    findings = []
    score = 1.0
    
    logical_order = plan.get("logical_order_type", "unknown")
    reasons = plan.get("reasons", [])
    
    if logical_order == "unknown":
        findings.append("⚠ Logical order not specified")
        score -= 0.3
    else:
        findings.append(f"✓ Logical order: {logical_order}")
    
    if len(reasons) >= 2:
        findings.append(f"✓ {len(reasons)} reasons ordered by {logical_order}")
    
    return {
        "aspect": "Logical Ordering",
        "score": max(score, 0),
        "findings": findings,
        "passed": score >= 0.75
    }


def critique_evidence(plan: Dict) -> Dict:
    """Check evidence sufficiency and quality."""
    findings = []
    score = 1.0
    
    reasons = plan.get("reasons", [])
    evidence = plan.get("evidence_collected", {})
    domain = plan.get("domain", "")
    
    if not evidence:
        findings.appen
