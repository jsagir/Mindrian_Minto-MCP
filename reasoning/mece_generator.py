"""
MECE Category Generation with Cognitive Load Optimization
Implements Minto's principle: 3-4 categories ideal, based on domain
"""

from typing import List, Dict, Optional
from .domain_detector import DomainType, AnalysisLens, detect_domain


# Enhanced MECE templates following Minto's cognitive load principle (3-4 categories)
MECE_TEMPLATES = {
    DomainType.TECHNICAL_ENGINEERING: {
        'optimization': [
            "Problem Formulation & Constraints",
            "Solution Methods & Convergence",
            "Implementation & Validation"
        ],
        'photonics': [
            "Device Design & Geometry",
            "Fabrication Constraints & Foundry Rules",
            "Performance Optimization & Validation"
        ],
        'system_design': [
            "System Architecture & Components",
            "Scalability & Performance",
            "Reliability & Operations"
        ],
        'algorithm': [
            "Algorithm Design & Complexity",
            "Implementation Techniques",
            "Performance & Validation"
        ],
        'ai_ml': [
            "Model Architecture & Design",
            "Training & Optimization",
            "Deployment & Performance"
        ],
        'default': [
            "Technical Requirements & Constraints",
            "Solution Approach & Methods",
            "Implementation & Validation"
        ]
    },
    
    DomainType.NATURAL_SCIENCES: {
        'physics': [
            "Theoretical Framework",
            "Experimental Methods",
            "Analysis & Implications"
        ],
        'chemistry': [
            "Chemical Mechanisms",
            "Experimental Design",
            "Results & Applications"
        ],
        'biology': [
            "Biological Systems",
            "Research Methods",
            "Findings & Implications"
        ],
        'default': [
            "Theoretical Foundation",
            "Experimental Approach",
            "Results & Implications"
        ]
    },
    
    DomainType.MEDICAL_HEALTH: {
        'clinical': [
            "Clinical Assessment",
            "Diagnostic & Treatment Options",
            "Outcomes & Prognosis"
        ],
        'pharmaceutical': [
            "Drug Mechanism & Properties",
            "Clinical Efficacy",
            "Safety & Administration"
        ],
        'default': [
            "Clinical Presentation",
            "Treatment Approaches",
            "Expected Outcomes"
        ]
    },
    
    DomainType.BUSINESS_ECONOMICS: {
        'strategy': [
            "Market Position & Competition",
            "Strategic Capabilities",
            "Growth Opportunities"
        ],
        'operations': [
            "Process Efficiency",
            "Resource Optimization",
            "Quality & Performance"
        ],
        'finance': [
            "Revenue Drivers",
            "Cost Structure",
            "Financial Performance"
        ],
        'default': [
            "Market Position",
            "Operational Factors",
            "Financial Implications"
        ]
    },
    
    DomainType.MATHEMATICS: {
        'default': [
            "Mathematical Framework",
            "Theoretical Analysis",
            "Applications & Examples"
        ]
    },
    
    DomainType.SOCIAL_POLICY: {
        'policy': [
            "Policy Context & Stakeholders",
            "Implementation Mechanisms",
            "Impact & Outcomes"
        ],
        'default': [
            "Social Context",
            "Policy Approaches",
            "Expected Impact"
        ]
    },
    
    DomainType.LAW_GOVERNANCE: {
        'default': [
            "Legal Framework",
            "Compliance Requirements",
            "Implications & Risks"
        ]
    },
    
    DomainType.ARTS_HUMANITIES: {
        'default': [
            "Historical Context",
            "Critical Analysis",
            "Cultural Significance"
        ]
    },
    
    DomainType.INTERDISCIPLINARY: {
        'default': [
            "Disciplinary Foundations",
            "Integration & Synergies",
            "Emergent Capabilities"
        ]
    },
    
    DomainType.GENERAL: {
        'default': [
            "Current State & Context",
            "Key Challenges",
            "Potential Solutions"
        ]
    }
}


# Alternative templates based on analysis lenses (when subdomain unclear)
LENS_BASED_TEMPLATES = {
    AnalysisLens.SYSTEM: [
        "System Components",
        "Interactions & Interfaces",
        "Performance & Optimization"
    ],
    AnalysisLens.PROCESS: [
        "Process Steps",
        "Resource Requirements",
        "Quality & Outcomes"
    ],
    AnalysisLens.STAKEHOLDER: [
        "Stakeholder Needs",
        "Impact & Benefits",
        "Implementation Considerations"
    ],
    AnalysisLens.TEMPORAL: [
        "Historical Context",
        "Current State",
        "Future Trajectory"
    ],
    AnalysisLens.SCALE: [
        "Individual Level",
        "System Level",
        "Ecosystem Level"
    ],
    AnalysisLens.CAUSAL: [
        "Root Causes",
        "Contributing Factors",
        "Effects & Outcomes"
    ],
    AnalysisLens.DISCIPLINARY: [
        "Theoretical Foundation",
        "Methodological Approach",
        "Practical Applications"
    ]
}


def generate_mece_reasons(
    brief: str,
    domain: DomainType = None,
    context: Dict = None
) -> List[Dict[str, any]]:
    """
    Generate 3-4 MECE categories (Minto's cognitive load principle).
    
    Process:
    1. Detect domain if not provided
    2. Select appropriate template based on subdomain or lens
    3. Ensure 3-4 categories (never more than 4)
    4. Format as reason dictionaries
    
    Args:
        brief: The question/problem
        domain: Pre-detected domain (optional)
        context: Domain detection context (optional)
    
    Returns:
        List of 3-4 MECE reason dictionaries
    """
    # Detect domain if not provided
    if domain is None or context is None:
        domain, context = detect_domain(brief)
    
    subdomain = context.get('subdomain')
    lenses = context.get('lenses', [])
    
    # Select appropriate template
    categories = select_mece_template(domain, subdomain, lenses)
    
    # Ensure 3-4 categories (Minto's cognitive load principle)
    if len(categories) > 4:
        categories = categories[:4]
        print(f"⚠️  Reduced to 4 categories (Minto cognitive load principle)")
    elif len(categories) < 3:
        print(f"⚠️  Only {len(categories)} categories - consider expanding to 3-4")
    
    # Convert to reason format
    reasons = []
    for i, category in enumerate(categories):
        reasons.append({
            "id": f"reason_{i+1}",
            "title": category,
            "claim": f"Analysis of {category.lower()} reveals key insights",
            "tasks_count": 2,  # Will create 2 evidence tasks per reason
            "category_type": detect_category_type(category)
        })
    
    return reasons


def select_mece_template(
    domain: DomainType,
    subdomain: Optional[str],
    lenses: List[AnalysisLens]
) -> List[str]:
    """
    Select most appropriate MECE template.
    
    Priority:
    1. Domain + Subdomain specific template
    2. Domain default template
    3. Lens-based template
    4. General fallback
    """
    # Try domain + subdomain
    if domain in MECE_TEMPLATES:
        domain_templates = MECE_TEMPLATES[domain]
        
        # Check for subdomain-specific template
        if isinstance(domain_templates, dict):
            if subdomain and subdomain in domain_templates:
                return domain_templates[subdomain]
            elif 'default' in domain_templates:
                return domain_templates['default']
            else:
                # Return first available template
                return list(domain_templates.values())[0]
        else:
            return domain_templates
    
    # Fallback to lens-based template
    if lenses and lenses[0] in LENS_BASED_TEMPLATES:
        return LENS_BASED_TEMPLATES[lenses[0]]
    
    # Ultimate fallback
    return MECE_TEMPLATES[DomainType.GENERAL]['default']


def detect_category_type(title: str) -> str:
    """
    Detect what kind of category this is (for MECE validation).
    
    Types:
    - component: Parts of a whole
    - process: Steps in sequence
    - factor: Contributing factors
    - dimension: Different aspects
    - stakeholder: Different groups
    """
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['component', 'part', 'element', 'module']):
        return "component"
    elif any(word in title_lower for word in ['step', 'phase', 'stage', 'process']):
        return "process"
    elif any(word in title_lower for word in ['factor', 'driver', 'contributor', 'cause']):
        return "factor"
    elif any(word in title_lower for word in ['dimension', 'aspect', 'perspective', 'view']):
        return "dimension"
    elif any(word in title_lower for word in ['stakeholder', 'actor', 'participant', 'group']):
        return "stakeholder"
    else:
        return "general"


def get_search_strategy(domain: DomainType) -> str:
    """
    Determine search strategy based on domain.
    
    Returns: 'academic', 'business', 'medical', 'legal', or 'general'
    """
    strategy_map = {
        DomainType.TECHNICAL_ENGINEERING: 'academic',
        DomainType.NATURAL_SCIENCES: 'academic',
        DomainType.MEDICAL_HEALTH: 'medical',
        DomainType.BUSINESS_ECONOMICS: 'business',
        DomainType.MATHEMATICS: 'academic',
        DomainType.SOCIAL_POLICY: 'general',
        DomainType.LAW_GOVERNANCE: 'legal',
        DomainType.ARTS_HUMANITIES: 'academic',
        DomainType.INTERDISCIPLINARY: 'academic',
        DomainType.GENERAL: 'general'
    }
    return strategy_map.get(domain, 'general')


def explain_mece_choice(categories: List[str], domain: DomainType, subdomain: Optional[str]) -> Dict:
    """
    Explain why these MECE categories were chosen.
    
    Returns explanation for transparency.
    """
    return {
        "domain": domain.value,
        "subdomain": subdomain or "general",
        "category_count": len(categories),
        "categories": categories,
        "rationale": f"Selected {len(categories)} categories based on {domain.value} domain patterns",
        "cognitive_load": "3-4 categories optimal (Minto principle: mind holds 7±2 items)",
        "mece_properties": {
            "mutually_exclusive": "Each category addresses distinct aspect",
            "collectively_exhaustive": "Together, categories cover full scope"
        }
    }


__all__ = [
    'generate_mece_reasons',
    'get_search_strategy',
    'select_mece_template',
    'explain_mece_choice',
    'MECE_TEMPLATES',
    'LENS_BASED_TEMPLATES'
]
