"""
Expert Domain Detection System
Based on Domain Explorer methodology with multi-lens analysis
"""

from typing import Dict, List, Tuple, Optional
import re
from enum import Enum


class DomainType(Enum):
    """Primary domain classifications"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    SCIENTIFIC = "scientific"
    MEDICAL = "medical"
    LEGAL = "legal"
    SOCIAL = "social"
    INTERDISCIPLINARY = "interdisciplinary"
    GENERAL = "general"


class TechnicalSubdomain(Enum):
    """Technical problem classifications"""
    ALGORITHM = "algorithm"
    OPTIMIZATION = "optimization"
    SYSTEM_DESIGN = "system_design"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    HARDWARE = "hardware"
    SOFTWARE = "software"
    AI_ML = "ai_ml"
    PHOTONICS = "photonics"
    QUANTUM = "quantum"
    DISTRIBUTED = "distributed"


class AnalysisLens(Enum):
    """Domain Explorer analysis lenses"""
    DISCIPLINARY = "disciplinary"      # Academic/professional fields
    STAKEHOLDER = "stakeholder"        # Who's affected
    SYSTEM = "system"                  # Components and interactions
    TEMPORAL = "temporal"              # Time dimensions
    SCALE = "scale"                    # Micro/meso/macro levels


# Comprehensive domain keyword taxonomy
DOMAIN_KEYWORDS = {
    DomainType.TECHNICAL: {
        'core': [
            'algorithm', 'optimization', 'computational', 'simulation',
            'architecture', 'implementation', 'system', 'design',
            'performance', 'efficiency', 'throughput', 'latency',
            'scalability', 'distributed', 'parallel', 'concurrent'
        ],
        'hardware': [
            'fabrication', 'semiconductor', 'photonic', 'optical',
            'electronic', 'device', 'circuit', 'transistor',
            'wafer', 'lithography', 'etching', 'deposition'
        ],
        'software': [
            'code', 'programming', 'software', 'framework',
            'library', 'api', 'protocol', 'interface',
            'data structure', 'compiler', 'runtime'
        ],
        'ml_ai': [
            'neural network', 'deep learning', 'machine learning',
            'training', 'inference', 'model', 'gradient',
            'backpropagation', 'transformer', 'embedding'
        ],
        'optimization': [
            'topology optimization', 'inverse design', 'constraint',
            'objective function', 'convergence', 'gradient descent',
            'binarization', 'penalty method', 'adjoint method'
        ],
        'photonics': [
            'photonic', 'optical', 'waveguide', 'resonator',
            'silicon photonics', 'inverse design', 'mode',
            'electromagnetic', 'maxwell', 'fdtd'
        ],
        'quantum': [
            'quantum', 'qubit', 'entanglement', 'superposition',
            'quantum computing', 'quantum error correction',
            'topological', 'hamiltonian'
        ]
    },
    
    DomainType.SCIENTIFIC: {
        'physics': [
            'electromagnetic', 'quantum mechanics', 'thermodynamics',
            'optics', 'mechanics', 'relativity', 'field theory'
        ],
        'chemistry': [
            'molecular', 'chemical', 'reaction', 'synthesis',
            'catalyst', 'polymer', 'spectroscopy'
        ],
        'biology': [
            'biological', 'genetic', 'protein', 'cell',
            'organism', 'evolution', 'ecosystem'
        ],
        'materials': [
            'material science', 'crystallography', 'metallurgy',
            'composite', 'nanomaterial', 'thin film'
        ]
    },
    
    DomainType.BUSINESS: {
        'financial': [
            'revenue', 'profit', 'margin', 'ebitda', 'roi',
            'valuation', 'investment', 'funding', 'cash flow',
            'dividend', 'shareholder', 'equity', 'debt'
        ],
        'operational': [
            'operational', 'efficiency', 'productivity', 'supply chain',
            'logistics', 'inventory', 'manufacturing', 'quality'
        ],
        'strategic': [
            'strategy', 'competitive', 'positioning', 'market share',
            'differentiation', 'competitive advantage', 'moat'
        ],
        'marketing': [
            'customer', 'market', 'brand', 'acquisition', 'retention',
            'churn', 'conversion', 'engagement', 'persona'
        ],
        'growth': [
            'growth', 'expansion', 'scaling', 'penetration',
            'market entry', 'addressable market', 'tam sam som'
        ]
    },
    
    DomainType.MEDICAL: {
        'clinical': [
            'patient', 'diagnosis', 'treatment', 'therapy',
            'clinical', 'prognosis', 'symptom', 'syndrome'
        ],
        'pharmaceutical': [
            'drug', 'pharmaceutical', 'medication', 'dosage',
            'pharmacology', 'compound', 'trial', 'efficacy'
        ],
        'surgical': [
            'surgery', 'surgical', 'procedure', 'operation',
            'invasive', 'laparoscopic', 'endoscopic'
        ],
        'diagnostic': [
            'diagnostic', 'imaging', 'radiology', 'pathology',
            'biopsy', 'biomarker', 'screening'
        ]
    },
    
    DomainType.LEGAL: {
        'core': [
            'law', 'legal', 'regulation', 'statute', 'legislation',
            'compliance', 'contract', 'liability', 'jurisdiction',
            'precedent', 'judicial', 'court', 'litigation'
        ],
        'ip': [
            'patent', 'trademark', 'copyright', 'intellectual property',
            'infringement', 'licensing', 'trade secret'
        ]
    },
    
    DomainType.SOCIAL: {
        'policy': [
            'policy', 'governance', 'regulation', 'public',
            'government', 'legislative', 'political'
        ],
        'societal': [
            'social', 'cultural', 'community', 'societal',
            'demographic', 'population', 'inequality', 'equity'
        ],
        'environmental': [
            'environmental', 'sustainability', 'climate',
            'ecosystem', 'conservation', 'renewable'
        ]
    }
}


# Technical subdomain patterns
TECHNICAL_SUBDOMAIN_PATTERNS = {
    TechnicalSubdomain.ALGORITHM: [
        'algorithm', 'complexity', 'search', 'sort', 'graph',
        'dynamic programming', 'greedy', 'divide and conquer'
    ],
    TechnicalSubdomain.OPTIMIZATION: [
        'optimization', 'minimize', 'maximize', 'constraint',
        'objective', 'gradient', 'convergence', 'penalty',
        'lagrangian', 'topology optimization', 'inverse design'
    ],
    TechnicalSubdomain.SYSTEM_DESIGN: [
        'system design', 'distributed', 'architecture',
        'microservice', 'scalability', 'load balancing',
        'caching', 'database', 'consistency'
    ],
    TechnicalSubdomain.HARDWARE: [
        'hardware', 'circuit', 'fpga', 'asic', 'vlsi',
        'semiconductor', 'fabrication', 'lithography'
    ],
    TechnicalSubdomain.PHOTONICS: [
        'photonic', 'optical', 'waveguide', 'silicon photonics',
        'inverse design', 'topology optimization', 'foundry',
        'fabrication constraint', 'mode', 'resonator'
    ],
    TechnicalSubdomain.AI_ML: [
        'neural network', 'deep learning', 'machine learning',
        'transformer', 'attention', 'embedding', 'training',
        'inference', 'model', 'llm', 'generative'
    ],
    TechnicalSubdomain.QUANTUM: [
        'quantum', 'qubit', 'quantum computing', 'superposition',
        'entanglement', 'quantum error correction', 'topological'
    ]
}


def detect_domain(brief: str) -> Tuple[DomainType, Dict[str, any]]:
    """
    Expert domain detection using multi-lens analysis.
    
    Returns:
        (primary_domain, analysis_context)
    
    Context includes:
        - subdomain: Specific technical/business subdomain
        - lenses: Which analysis lenses are most relevant
        - keywords_found: Matched keywords for validation
        - confidence: Detection confidence score
        - is_interdisciplinary: Whether multiple domains detected
    """
    brief_lower = brief.lower()
    
    # Score each domain
    domain_scores = {}
    keyword_matches = {}
    
    for domain_type, categories in DOMAIN_KEYWORDS.items():
        score = 0
        matches = []
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in brief_lower:
                    score += 1
                    matches.append(keyword)
        
        domain_scores[domain_type] = score
        keyword_matches[domain_type] = matches
    
    # Get top domains
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    primary_domain = sorted_domains[0][0] if sorted_domains[0][1] > 0 else DomainType.GENERAL
    
    # Check if interdisciplinary (multiple high scores)
    is_interdisciplinary = len([d for d, s in sorted_domains if s >= 3]) > 1
    
    # Detect subdomain for technical questions
    subdomain = None
    if primary_domain == DomainType.TECHNICAL:
        subdomain = classify_technical_subdomain(brief_lower)
    
    # Determine relevant analysis lenses
    relevant_lenses = determine_analysis_lenses(brief_lower, primary_domain)
    
    # Calculate confidence
    max_score = sorted_domains[0][1]
    confidence = min(max_score / 10.0, 1.0)  # Normalize to 0-1
    
    context = {
        'subdomain': subdomain,
        'lenses': relevant_lenses,
        'keywords_found': keyword_matches[primary_domain],
        'confidence': confidence,
        'is_interdisciplinary': is_interdisciplinary,
        'secondary_domains': [d.value for d, s in sorted_domains[1:3] if s > 0],
        'domain_scores': {d.value: s for d, s in sorted_domains if s > 0}
    }
    
    return primary_domain, context


def classify_technical_subdomain(brief_lower: str) -> TechnicalSubdomain:
    """
    Classify specific technical subdomain for specialized templates.
    """
    subdomain_scores = {}
    
    for subdomain, keywords in TECHNICAL_SUBDOMAIN_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in brief_lower)
        subdomain_scores[subdomain] = score
    
    max_subdomain = max(subdomain_scores.items(), key=lambda x: x[1])
    return max_subdomain[0] if max_subdomain[1] > 0 else TechnicalSubdomain.ALGORITHM


def determine_analysis_lenses(brief: str, domain: DomainType) -> List[AnalysisLens]:
    """
    Determine which Domain Explorer lenses are most relevant.
    
    Analysis lenses:
    - Disciplinary: Academic/professional field perspective
    - Stakeholder: Who's affected, who cares
    - System: Components, interactions, boundaries
    - Temporal: Historical context, current state, future trajectory
    - Scale: Micro/meso/macro levels
    """
    lenses = []
    brief_lower = brief.lower()
    
    # Disciplinary lens - relevant for academic/technical questions
    disciplinary_indicators = [
        'research', 'academic', 'scientific', 'theoretical',
        'field', 'discipline', 'domain', 'area of study'
    ]
    if any(ind in brief_lower for ind in disciplinary_indicators):
        lenses.append(AnalysisLens.DISCIPLINARY)
    
    # Stakeholder lens - relevant for business/social questions
    stakeholder_indicators = [
        'customer', 'user', 'stakeholder', 'impact', 'affect',
        'benefit', 'harm', 'people', 'organization', 'community'
    ]
    if any(ind in brief_lower for ind in stakeholder_indicators):
        lenses.append(AnalysisLens.STAKEHOLDER)
    
    # System lens - relevant for technical/complex problems
    system_indicators = [
        'system', 'component', 'architecture', 'design',
        'interaction', 'integration', 'interface', 'dependency'
    ]
    if any(ind in brief_lower for ind in system_indicators):
        lenses.append(AnalysisLens.SYSTEM)
    
    # Temporal lens - relevant when time/evolution matters
    temporal_indicators = [
        'historical', 'evolution', 'trend', 'future', 'trajectory',
        'forecast', 'predict', 'timeline', 'roadmap', 'phase'
    ]
    if any(ind in brief_lower for ind in temporal_indicators):
        lenses.append(AnalysisLens.TEMPORAL)
    
    # Scale lens - relevant for multi-level analysis
    scale_indicators = [
        'micro', 'macro', 'meso', 'individual', 'organizational',
        'societal', 'global', 'local', 'scale', 'level'
    ]
    if any(ind in brief_lower for ind in scale_indicators):
        lenses.append(AnalysisLens.SCALE)
    
    # Default lenses based on domain
    if not lenses:
        if domain == DomainType.TECHNICAL:
            lenses = [AnalysisLens.SYSTEM, AnalysisLens.DISCIPLINARY]
        elif domain == DomainType.BUSINESS:
            lenses = [AnalysisLens.STAKEHOLDER, AnalysisLens.TEMPORAL]
        elif domain == DomainType.SCIENTIFIC:
            lenses = [AnalysisLens.DISCIPLINARY, AnalysisLens.SCALE]
        else:
            lenses = [AnalysisLens.DISCIPLINARY]
    
    return lenses


def get_search_domains(domain: DomainType, subdomain: Optional[TechnicalSubdomain] = None) -> List[str]:
    """
    Return appropriate academic/research domains for search queries.
    """
    search_domains = {
        DomainType.TECHNICAL: {
            TechnicalSubdomain.PHOTONICS: [
                'arxiv.org', 'opg.optica.org', 'nature.com/nphoton',
                'ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=50',
                'aip.scitation.org/journal/apl'
            ],
            TechnicalSubdomain.QUANTUM: [
                'arxiv.org/list/quant-ph', 'nature.com/nphys',
                'journals.aps.org/pra', 'quantum-journal.org'
            ],
            TechnicalSubdomain.AI_ML: [
                'arxiv.org/list/cs.LG', 'arxiv.org/list/cs.AI',
                'proceedings.mlr.press', 'openreview.net',
                'neurips.cc', 'icml.cc'
            ],
            TechnicalSubdomain.OPTIMIZATION: [
                'arxiv.org/list/math.OC', 'link.springer.com/journal/10107',
                'pubsonline.informs.org/journal/opre'
            ],
            'default': [
                'arxiv.org', 'ieeexplore.ieee.org', 'dl.acm.org',
                'sciencedirect.com', 'springer.com'
            ]
        },
        DomainType.SCIENTIFIC: [
            'nature.com', 'science.org', 'pnas.org',
            'sciencedirect.com', 'rsc.org', 'acs.org'
        ],
        DomainType.MEDICAL: [
            'pubmed.ncbi.nlm.nih.gov', 'nejm.org', 'thelancet.com',
            'jamanetwork.com', 'bmj.com'
        ],
        DomainType.BUSINESS: [
            'mckinsey.com', 'bcg.com', 'hbr.org',
            'strategy-business.com', 'sloanreview.mit.edu'
        ],
        DomainType.LEGAL: [
            'scholar.google.com', 'ssrn.com', 'heinonline.org'
        ]
    }
    
    if domain == DomainType.TECHNICAL and subdomain:
        return search_domains[domain].get(subdomain, search_domains[domain]['default'])
    
    return search_domains.get(domain, ['scholar.google.com'])


def is_academic_source(url: str) -> bool:
    """Check if URL is from academic/research source."""
    academic_domains = [
        'arxiv.org', 'ieee.org', 'nature.com', 'science.org',
        'sciencedirect.com', 'springer.com', 'wiley.com',
        'acm.org', 'osa.org', 'optica.org', 'aps.org',
        'semanticscholar.org', 'scholar.google.com',
        'researchgate.net', 'pubmed.ncbi.nlm.nih.gov',
        'pnas.org', 'cell.com', 'thelancet.com', 'nejm.org',
        'aip.org', 'acs.org', 'rsc.org', 'iop.org'
    ]
    return any(domain in url.lower() for domain in academic_domains)


def is_business_source(url: str) -> bool:
    """Check if URL is from business/industry source."""
    business_domains = [
        'mckinsey.com', 'bcg.com', 'bain.com', 'deloitte.com',
        'pwc.com', 'ey.com', 'kpmg.com', 'accenture.com',
        'forbes.com', 'fortune.com', 'bloomberg.com', 'wsj.com',
        'ft.com', 'economist.com', 'hbr.org', 'sloanreview.mit.edu',
        'techcrunch.com', 'venturebeat.com', 'crunchbase.com'
    ]
    return any(domain in url.lower() for domain in business_domains)


def generate_domain_specific_queries(brief: str, domain: DomainType, 
                                     subdomain: Optional[TechnicalSubdomain] = None) -> List[str]:
    """
    Generate expert search queries based on domain and problem type.
    """
    queries = []
    brief_clean = brief[:100]  # First 100 chars
    
    if domain == DomainType.TECHNICAL:
        if subdomain == TechnicalSubdomain.PHOTONICS:
            queries = [
                f"photonic inverse design {brief_clean}",
                f"topology optimization photonics fabrication",
                f"silicon photonics design constraints",
                f"adjoint method photonic optimization",
                f"FDTD inverse design photonic devices"
            ]
        elif subdomain == TechnicalSubdomain.OPTIMIZATION:
            queries = [
                f"topology optimization {brief_clean}",
                f"constrained optimization methods",
                f"gradient-based optimization convergence",
                f"penalty methods constraint handling",
                f"binarization techniques optimization"
            ]
        elif subdomain == TechnicalSubdomain.AI_ML:
            queries = [
                f"deep learning {brief_clean}",
                f"neural network architecture",
                f"training optimization techniques",
                f"model performance benchmarks"
            ]
        else:
            queries = [
                f"{brief_clean} research paper",
                f"{brief_clean} algorithm methods",
                f"{brief_clean} state of the art",
                f"{brief_clean} technical review"
            ]
    
    elif domain == DomainType.BUSINESS:
        queries = [
            f"{brief_clean} market analysis",
            f"{brief_clean} business strategy",
            f"{brief_clean} industry trends",
            f"{brief_clean} competitive landscape"
        ]
    
    elif domain == DomainType.SCIENTIFIC:
        queries = [
            f"{brief_clean} scientific review",
            f"{brief_clean} research findings",
            f"{brief_clean} experimental results"
        ]
    
    else:
        queries = [f"{brief_clean} research", f"{brief_clean} analysis"]
    
    return queries


# Export main functions
__all__ = [
    'DomainType',
    'TechnicalSubdomain',
    'AnalysisLens',
    'detect_domain',
    'classify_technical_subdomain',
    'determine_analysis_lenses',
    'get_search_domains',
    'is_academic_source',
    'is_business_source',
    'generate_domain_specific_queries'
]
