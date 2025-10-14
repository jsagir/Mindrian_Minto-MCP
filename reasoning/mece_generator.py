"""
Expert MECE Category Generation
Universal templates for any domain detected
"""

from typing import List, Dict, Optional
from .domain_detector import (
    DomainType, AnalysisLens, detect_domain
)


# Universal MECE templates
MECE_TEMPLATES = {
    DomainType.TECHNICAL_ENGINEERING: {
        'optimization': [
            "Problem Formulation & Objective Functions",
            "Constraint Handling Mechanisms",
            "Search & Convergence Methods",
            "Solution Quality & Validation"
        ],
        'system_design': [
            "System Architecture & Components",
            "Data Flow & Processing Pipeline",
            "Scalability & Performance",
            "Reliability & Error Handling"
        ],
        'algorithm': [
            "Problem Definition & Requirements",
            "Algorithm Design & Complexity",
            "Implementation Techniques",
            "Performance Evaluation"
        ],
        'default': [
            "Technical Requirements & Constraints",
            "Solution Approach & Methods",
            "Implementation Strategy",
            "Validation & Performance Metrics"
        ]
    },
    
    DomainType.NATURAL_SCIENCES: {
        'default': [
            "Theoretical Framework & Foundations",
            "Experimental Methods & Design",
            "Data Analysis & Interpretation",
            "Implications & Future Directions"
        ]
    },
    
    DomainType.MEDICAL_HEALTH: {
        'default': [
            "Clinical Presentation & Assessment",
            "Diagnostic Workup & Testing",
            "Treatment Options & Protocols",
            "Prognosis & Outcomes"
        ]
    },
    
    DomainType.BUSINESS_ECONOMICS: {
        'strategy': [
            "Market Position & Competitive Landscape",
            "Operational Efficiency & Capabilities",
            "Revenue Model & Financial Structure",
            "Strategic Positioning & Growth"
        ],
        'operations': [
            "Process Design & Workflow",
            "Resource Allocation & Optimization",
            "Quality & Performance Management",
            "Technology & Automation"
        ],
        'default': [
            "Market Analysis & Trends",
            "Financial Performance & Drivers",
            "Operational Considerations",
            "Strategic Implications"
        ]
    },
    
    DomainType.MATHEMATICS: {
        'default': [
            "Mathematical Foundations & Definitions",
            "Theoretical Analysis & Proofs",
            "Computational Methods",
            "Applications & Examples"
        ]
    },
    
    DomainType.SOCIAL_POLICY: {
        'default': [
            "Stakeholder Analysis & Impact",
            "Policy Framework & Mechanisms",
            "Implementation Considerations",
            "Outcomes & Evaluation"
        ]
    },
    
    DomainType.LAW_GOVERNANCE: {
        'default': [
            "Legal Framework & Precedent",
            "Regulatory Requirements",
            "Compliance Mechanisms",
            "Implications & Risks"
        ]
    },
    
    DomainType.ARTS_HUMANITIES: {
        'default': [
            "Historical Context & Background",
            "Critical Analysis & Interpretation",
            "Cultural Significance",
            "Contemporary Relevance"
        ]
    },
    
    DomainType.INTERDISCIPLINARY: {
        'default': [
            "Disciplinary Foundations",
            "Integration Points & Synergies",
            "Cross-Domain Methods",
            "Emergent Capabilities"
        ]
    },
    
    DomainType.GENERAL: {
        'default': [
            "Current State & Context",
            "Key Challenges & Constraints",
            "Potential Solutions & Approaches",
            "Implementation Considerations"
        ]
    }
}


def generate_mece_reasons(brief: str, domain: DomainType = None, 
                         context: Dict = None) -> List[Dict[str, any]]:
    """
    Generate domain-appropriate MECE categories.
    Automatically detects domain if not provided.
    """
    # Detect domain if not provided
    if domain is None or context is None:
        domain, context = detect_domain(brief)
    
    # Get subdomain
    subdomain = context.get('subdomain')
    
    # Select appropriate template
    domain_templates = MECE_TEMPLATES.get(domain, MECE_TEMPLATES[DomainType.GENERAL])
    
    # For technical domain, use subdomain if available
    if domain == DomainType.TECHNICAL_ENGINEERING and subdomain:
        categories = domain_templates.get(subdomain, domain_templates['default'])
    else:
        # Get default template for domain
        if isinstance(domain_templates, dict):
            categories = domain_templates.get('default', list(domain_templates.values())[0])
        else:
            categories = domain_templates
    
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


def get_search_strategy(domain: DomainType) -> str:
    """
    Determine search strategy based on domain.
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


__all__ = [
    'generate_mece_reasons',
    'get_search_strategy',
    'MECE_TEMPLATES'
]
