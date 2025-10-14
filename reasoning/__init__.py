"""
Minto Pyramid Logic Reasoning Engine v3.1
Domain-aware MECE decomposition and evidence synthesis
"""

from .domain_detector import (
    DomainType,
    AnalysisLens,
    detect_domain,
    is_academic_source,
    is_business_source,
    generate_search_queries
)

from .mece_generator import (
    generate_mece_reasons,
    get_search_strategy,
    MECE_TEMPLATES
)

__version__ = "3.1.0"

__all__ = [
    'DomainType',
    'AnalysisLens',
    'detect_domain',
    'is_academic_source',
    'is_business_source',
    'generate_search_queries',
    'generate_mece_reasons',
    'get_search_strategy',
    'MECE_TEMPLATES'
]
