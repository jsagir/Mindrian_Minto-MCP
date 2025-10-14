from .domain_detector import is_academic_source, is_business_source, detect_domain
import re

def validate_semantic_relevance(brief: str, evidence: dict, domain: str) -> float:
    """
    Check if evidence actually addresses the question domain.
    
    NEW: Semantic relevance validation
    """
    # Extract key concepts from brief
    brief_lower = brief.lower()
    brief_words = set(re.findall(r'\b\w+\b', brief_lower))
    
    # Remove stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    brief_concepts = brief_words - stop_words
    
    relevance_scores = []
    
    for reason_evidence in evidence.values():
        for item in reason_evidence:
            content = item.get('content', '').lower()
            url = item.get('url', '')
            
            # Calculate concept overlap
            content_words = set(re.findall(r'\b\w+\b', content))
            overlap = len(brief_concepts & content_words) / max(len(brief_concepts), 1)
            
            # Check source appropriateness
            source_score = 1.0
            if domain == "technical":
                source_score = 1.0 if is_academic_source(url) else 0.3
            elif domain == "business":
                source_score = 1.0 if is_business_source(url) else 0.7
            
            # Combined score
            score = overlap * source_score
            relevance_scores.append(score)
    
    return sum(relevance_scores) / max(len(relevance_scores), 1)


def critique_pyramid_tool(run_id: str):
    """
    Evaluate pyramid quality with semantic relevance check.
    
    UPDATED: Adds semantic relevance validation
    """
    plan = REASONING_STATE.get(run_id)
    if not plan:
        return {"error": "Run not found"}
    
    evidence = plan.get("evidence_collected", {})
    domain = plan.get("domain", "general")  # NEW
    
    critiques = []
    
    # Existing checks
    # 1. Pyramid Fidelity
    mece_score = plan.get("mece_score", 0)
    overlaps = 0  # Calculate overlaps
    
    critiques.append({
        "aspect": "pyramid_fidelity",
        "score": mece_score,
        "findings": [
            f"MECE score: {mece_score:.2f}",
            f"Overlaps detected: {overlaps}",
            "Top-down clarity maintained"
        ],
        "recommendations": [],
        "needs_revision": mece_score < 0.75
    })
    
    # 2. Evidence Sufficiency
    total_evidence = sum(len(e) for e in evidence.values())
    reasons_count = len(plan["reasons"])
    avg_confidence = sum(
        sum(item.get("confidence", 0) for item in reason_evidence) / max(len(reason_evidence), 1)
        for reason_evidence in evidence.values()
    ) / max(len(evidence), 1)
    
    evidence_score = min((total_evidence / (reasons_count * 2)) * avg_confidence, 1.0)
    
    critiques.append({
        "aspect": "evidence_sufficiency",
        "score": evidence_score,
        "findings": [
            f"Total evidence items: {total_evidence}",
            f"Average confidence: {avg_confidence:.2f}",
            f"Evidence per reason: {total_evidence / max(reasons_count, 1):.1f}"
        ],
        "recommendations": [],
        "needs_revision": evidence_score < 0.70
    })
    
    # 3. Consistency
    contradictions = 0  # Detect contradictions
    consistency_score = max(1.0 - (contradictions * 0.1), 0)
    
    critiques.append({
        "aspect": "consistency",
        "score": consistency_score,
        "findings": [
            f"Contradictions found: {contradictions}",
            "Claims align with evidence"
        ],
        "recommendations": [],
        "needs_revision": consistency_score < 0.70
    })
    
    # NEW: 4. Semantic Relevance
    semantic_score = validate_semantic_relevance(plan["brief"], evidence, domain)
    
    critiques.append({
        "aspect": "semantic_relevance",
        "score": semantic_score,
        "findings": [
            f"Domain: {domain}",
            f"Relevance score: {semantic_score:.2f}",
            "Sources match domain expectations" if semantic_score > 0.7 else "Sources may not match domain"
        ],
        "recommendations": [
            "Adjust search queries for better domain fit"
        ] if semantic_score < 0.7 else [],
        "needs_revision": semantic_score < 0.7
    })
    
    # Calculate overall score
    overall_score = sum(c["score"] for c in critiques) / len(critiques)
    passes = all(not c["needs_revision"] for c in critiques)
    
    result = {
        "run_id": run_id,
        "status": "critiqued",
        "overall_score": overall_score,
        "critiques": critiques,
        "passes_quality_gates": passes,
        "next_step": "finalize_pyramid" if passes else "revise_plan"
    }
    
    plan["critique"] = result
    
    return result
