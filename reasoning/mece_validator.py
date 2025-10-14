"""
MECE Validator - Ensures Mutually Exclusive, Collectively Exhaustive
Implements Barbara Minto's core principle for logical decomposition
"""

from typing import Dict, List, Tuple


def validate_mece_structure(plan: Dict) -> Dict:
    """
    Validate MECE compliance of pyramid structure.
    
    Checks:
    1. Mutually Exclusive: No overlaps between categories
    2. Collectively Exhaustive: No gaps in coverage
    3. Cognitive Load: 3-4 categories (not 7+)
    4. Same Kind: All categories at same logical level
    
    Returns validation report with specific findings.
    """
    reasons = plan.get("reasons", [])
    brief = plan.get("brief", "")
    domain = plan.get("domain", "")
    
    # Check 1: Cognitive Load (3-4 categories)
    category_count = len(reasons)
    cognitive_load_ok = 1 <= category_count <= 4
    
    # Check 2: Mutually Exclusive (no overlaps)
    overlaps = check_mutual_exclusivity(reasons)
    has_overlaps = len(overlaps) > 0
    
    # Check 3: Collectively Exhaustive (no gaps)
    gaps = check_collective_exhaustiveness(reasons, brief, domain)
    has_gaps = len(gaps) > 0
    
    # Check 4: Same Kind
    same_kind, kind_issues = check_same_kind(reasons)
    
    # Overall MECE compliance
    is_mece = (not has_overlaps) and (not has_gaps) and cognitive_load_ok and same_kind
    
    return {
        "is_mece": is_mece,
        "passed": is_mece,
        
        # Mutually Exclusive
        "mutually_exclusive": not has_overlaps,
        "has_overlaps": has_overlaps,
        "overlaps": overlaps,
        
        # Collectively Exhaustive
        "collectively_exhaustive": not has_gaps,
        "has_gaps": has_gaps,
        "gaps": gaps,
        
        # Cognitive Load
        "category_count": category_count,
        "cognitive_load_ok": cognitive_load_ok,
        "cognitive_load_message": get_cognitive_load_message(category_count),
        
        # Same Kind
        "same_kind": same_kind,
        "kind_issues": kind_issues,
        
        # Recommendations
        "recommendations": generate_mece_recommendations(
            has_overlaps, has_gaps, cognitive_load_ok, same_kind,
            overlaps, gaps, category_count, kind_issues
        )
    }


def check_mutual_exclusivity(reasons: List[Dict]) -> List[Dict]:
    """
    Check if categories overlap (violates mutual exclusivity).
    
    Method:
    - Compare category titles and descriptions for semantic overlap
    - Identify shared keywords that suggest overlap
    """
    overlaps = []
    
    for i, reason1 in enumerate(reasons):
        for j, reason2 in enumerate(reasons):
            if i >= j:
                continue
            
            title1 = reason1["title"].lower()
            title2 = reason2["title"].lower()
            
            # Extract key words
            words1 = set(title1.split())
            words2 = set(title2.split())
            
            # Check for significant word overlap
            common_words = words1 & words2
            # Remove common function words
            common_words = common_words - {'and', 'or', 'the', 'a', 'an', 'of', 'for', 'in', 'on', 'with'}
            
            if len(common_words) >= 2:  # Significant overlap
                overlaps.append({
                    "category_1": reason1["title"],
                    "category_2": reason2["title"],
                    "overlap": list(common_words),
                    "severity": "high" if len(common_words) >= 3 else "medium"
                })
    
    return overlaps


def check_collective_exhaustiveness(reasons: List[Dict], brief: str, domain: str) -> List[str]:
    """
    Check if categories cover all aspects (collectively exhaustive).
    
    Method:
    - Extract key concepts from original question
    - Check if all concepts are addressed by at least one category
    """
    gaps = []
    
    # Extract key concepts from brief
    brief_lower = brief.lower()
    key_concepts = extract_key_concepts(brief_lower, domain)
    
    # Check if each concept is covered by at least one reason
    for concept in key_concepts:
        covered = False
        for reason in reasons:
            title_lower = reason["title"].lower()
            if concept in title_lower or any(synonym in title_lower for synonym in get_synonyms(concept)):
                covered = True
                break
        
        if not covered:
            gaps.append(concept)
    
    return gaps


def check_same_kind(reasons: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Check if all categories are the same kind of idea.
    
    Examples of SAME kind:
    - All reasons (why we should do X)
    - All steps (how to do X)
    - All problems (what's wrong with X)
    - All components (parts of X)
    
    Examples of MIXED kind (BAD):
    - Mix of reasons and steps
    - Mix of problems and solutions
    """
    if len(reasons) <= 1:
        return True, []
    
    issues = []
    
    # Detect category types
    category_types = []
    for reason in reasons:
        title = reason["title"].lower()
        cat_type = detect_category_type(title)
        category_types.append(cat_type)
    
    # Check if all same type
    unique_types = set(category_types)
    
    if len(unique_types) > 1:
        issues.append(f"Mixed category types detected: {unique_types}")
        issues.append("All categories should be the same kind (all reasons, or all steps, or all components)")
        return False, issues
    
    return True, []


def detect_category_type(title: str) -> str:
    """
    Detect what kind of category this is.
    """
    title_lower = title.lower()
    
    # Process-based (steps, phases, stages)
    if any(word in title_lower for word in ['process', 'step', 'phase', 'stage', 'workflow', 'procedure']):
        return "process"
    
    # Component-based (parts, elements, components)
    if any(word in title_lower for word in ['component', 'element', 'part', 'module', 'system', 'architecture']):
        return "component"
    
    # Problem-based (issues, challenges, barriers)
    if any(word in title_lower for word in ['problem', 'issue', 'challenge', 'barrier', 'obstacle', 'constraint']):
        return "problem"
    
    # Solution-based (approaches, methods, strategies)
    if any(word in title_lower for word in ['solution', 'approach', 'method', 'strategy', 'technique', 'mechanism']):
        return "solution"
    
    # Analysis-based (factors, dimensions, aspects)
    if any(word in title_lower for word in ['factor', 'dimension', 'aspect', 'consideration', 'analysis']):
        return "analysis"
    
    return "general"


def extract_key_concepts(text: str, domain: str) -> List[str]:
    """Extract key concepts that should be covered."""
    # Simple heuristic: extract important nouns
    words = text.split()
    
    # Filter to meaningful words (>3 chars, not common words)
    common_words = {'the', 'and', 'for', 'that', 'with', 'from', 'this', 'have', 'what', 'how', 'can', 'will', 'should'}
    
    key_words = [
        word.strip('.,?!') 
        for word in words 
        if len(word) > 3 and word.lower() not in common_words
    ]
    
    # Return unique key concepts (limit to avoid noise)
    return list(set(key_words))[:8]


def get_synonyms(word: str) -> List[str]:
    """Get simple synonyms for concept matching."""
    synonym_map = {
        'optimization': ['optimize', 'optimizing', 'optimal'],
        'design': ['designing', 'designed', 'designer'],
        'constraint': ['constraints', 'limitation', 'restrictions'],
        'performance': ['efficiency', 'effectiveness'],
        'algorithm': ['algorithms', 'algorithmic', 'computational'],
        'method': ['methods', 'methodology', 'approach', 'technique'],
        'problem': ['problems', 'issue', 'challenge'],
        'solution': ['solutions', 'solve', 'solving']
    }
    
    return synonym_map.get(word.lower(), [word])


def get_cognitive_load_message(count: int) -> str:
    """Get message about cognitive load."""
    if count == 1:
        return "Only 1 category - consider if this can be decomposed further"
    elif count <= 4:
        return f"✓ Good: {count} categories (within cognitive limit of 3-4)"
    elif count <= 7:
        return f"⚠ Warning: {count} categories (approaching cognitive limit of 7±2)"
    else:
        return f"✗ Poor: {count} categories (exceeds cognitive limit - should be 3-4)"


def generate_mece_recommendations(
    has_overlaps: bool,
    has_gaps: bool,
    cognitive_load_ok: bool,
    same_kind: bool,
    overlaps: List[Dict],
    gaps: List[str],
    category_count: int,
    kind_issues: List[str]
) -> List[str]:
    """Generate specific recommendations to fix MECE issues."""
    recommendations = []
    
    if has_overlaps:
        recommendations.append("**Overlaps Detected**: Merge or clarify overlapping categories:")
        for overlap in overlaps:
            recommendations.append(f"  - '{overlap['category_1']}' and '{overlap['category_2']}' share: {overlap['overlap']}")
    
    if has_gaps:
        recommendations.append("**Gaps Detected**: Consider adding categories to cover:")
        for gap in gaps[:5]:  # Limit to top 5
            recommendations.append(f"  - {gap}")
    
    if not cognitive_load_ok:
        if category_count > 4:
            recommendations.append(f"**Too Many Categories**: Reduce from {category_count} to 3-4 by grouping related items")
        elif category_count == 0:
            recommendations.append("**No Categories**: Generate 3-4 MECE categories to structure analysis")
    
    if not same_kind:
        recommendations.append("**Mixed Category Types**: Ensure all categories are same kind:")
        recommendations.extend([f"  - {issue}" for issue in kind_issues])
    
    if not recommendations:
        recommendations.append("✓ MECE structure is valid - no issues detected")
    
    return recommendations


__all__ = ['validate_mece_structure']
