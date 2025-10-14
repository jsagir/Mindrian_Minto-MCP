"""MECE category generation with domain-specific templates."""

from typing import List, Dict
from .domain_detector import detect_domain, classify_technical_problem


# Domain-specific MECE templates
MECE_TEMPLATES = {
    "technical": {
        "algorithm": [
            "Problem Formulation & Requirements",
            "Solution Approach & Methods",
            "Implementation Strategy",
            "Validation & Performance Metrics"
        ],
        "optimization": [
            "Objective Functions & Goals",
            "Constraint Handling Mechanisms",
            "Search & Convergence Methods",
            "Solution Quality & Validation"
        ],
        "system_design": [
            "System Architecture & Components",
            "Data Flow & Processing Pipeline",
            "Scalability & Performance",
            "Reliability & Error Handling"
        ],
        "implementation": [
            "Technology Stack Selection",
            "Development Approach & Methodology",
            "Integration & Dependencies",
            "Testing & Deployment Strategy"
        ],
        "architecture": [
            "Structural Components",
            "Interface Definitions",
            "Communication Patterns",
            "Quality Attributes"
        ]
    },
    "business": {
        "growth": [
            "Market Position Analysis",
            "Operational Efficiency",
            "Revenue Model Evolution",
            "Strategic Positioning"
        ],
        "profitability": [
            "Revenue Drivers",
            "Cost Structure",
            "Pricing Strategy",
            "Market Dynamics"
        ],
        "strategy": [
            "Competitive Landscape",
            "Core Capabilities",
            "Growth Opportunities",
            "Risk Mitigation"
        ]
    },
    "medical": {
        "diagnosis": [
            "Clinical Presentation",
            "Diagnostic Workup",
            "Differential Considerations",
            "Treatment Planning"
        ]
    },
    "general": [
        "Current State Analysis",
        "Key Challenges",
        "Potential Solutions",
        "Implementation Considerations"
    ]
}


def generate_mece_reasons(brief: str) -> List[Dict[str, str]]:
    """
    Generate domain-appropriate MECE categories.
    
    Returns list of reason dictionaries with id, title, and claim.
    """
    domain = detect_domain(brief)
    
    if domain == "technical":
        problem_type = classify_technical_problem(brief)
        categories = MECE_TEMPLATES["technical"].get(problem_type, 
                                                     MECE_TEMPLATES["technical"]["algorithm"])
    elif domain == "business":
        # Detect business problem type (growth, profitability, strategy)
        if any(word in brief.lower() for word in ['revenue', 'profit', 'margin']):
            categories = MECE_TEMPLATES["business"]["profitability"]
        elif any(word in brief.lower() for word in ['strategy', 'competitive', 'positioning']):
            categories = MECE_TEMPLATES["business"]["strategy"]
        else:
            categories = MECE_TEMPLATES["business"]["growth"]
    elif domain in MECE_TEMPLATES:
        # Get first template for domain
        templates = MECE_TEMPLATES[domain]
        categories = list(templates.values())[0]
    else:
        categories = MECE_TEMPLATES["general"]
    
    # Convert to reason format
    reasons = []
    for i, category in enumerate(categories):
        reasons.append({
            "id": f"reason_{i+1}",
            "title": category,
            "claim": f"Analysis of {category.lower()} reveals key insights",
            "tasks_count": 2
        })
    
    return reasons


def get_search_strategy(domain: str) -> str:
    """
    Determine search strategy based on domain.
    
    Returns: 'academic', 'business', 'medical', 'general'
    """
    strategy_map = {
        'technical': 'academic',
        'business': 'business',
        'medical': 'medical',
        'legal': 'legal',
        'general': 'general'
    }
    return strategy_map.get(domain, 'general')
