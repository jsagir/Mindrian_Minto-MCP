"""
Minto Pyramid Logic Reasoning Engine v3.1
Implements Barbara Minto's Pyramid Principle with Sequential Thinking

Core Principles:
1. SCQA Introduction (Situation-Complication-Question-Answer)
2. MECE Decomposition (Mutually Exclusive, Collectively Exhaustive)
3. Vertical Q&A Dialogue (each level answers question above)
4. Horizontal Logic (deductive OR inductive)
5. Logical Ordering (deductive/chronological/structural/comparative)
6. Cognitive Load (3-4 categories ideal)
7. Top-Down Communication (summary before details)
"""

# Domain Detection
from .domain_detector import (
    DomainType,
    AnalysisLens,
    detect_domain,
    is_academic_source,
    is_business_source,
    generate_search_queries
)

# MECE Generation
from .mece_generator import (
    generate_mece_reasons,
    get_search_strategy,
    explain_mece_choice,
    MECE_TEMPLATES
)

# Planning
from .plan import (
    plan_pyramid_with_thinking,
    REASONING_STATE
)

# MECE Validation
from .mece_validator import validate_mece_structure

# Execution
from .execution import execute_evidence_gathering

# Synthesis
from .synthesis import synthesize_deliverable

# Critique
from .critique import critique_pyramid_quality

__version__ = "3.1.0"
__author__ = "Minto Pyramid Logic MCP"

__all__ = [
    # Domain Detection
    'DomainType',
    'AnalysisLens',
    'detect_domain',
    'is_academic_source',
    'is_business_source',
    'generate_search_queries',
    
    # MECE Generation
    'generate_mece_reasons',
    'get_search_strategy',
    'explain_mece_choice',
    'MECE_TEMPLATES',
    
    # Core Pipeline
    'plan_pyramid_with_thinking',
    'validate_mece_structure',
    'execute_evidence_gathering',
    'synthesize_deliverable',
    'critique_pyramid_quality',
    
    # State
    'REASONING_STATE',
]

# Minto Principles (for reference)
MINTO_PRINCIPLES = {
    "three_rules": {
        "1": "Ideas at any level must ALWAYS be summaries of ideas grouped below",
        "2": "Ideas in each grouping must ALWAYS be the SAME KIND of idea",
        "3": "Ideas in each grouping must ALWAYS be LOGICALLY ORDERED"
    },
    "logical_orders": [
        "Deductive (argument: A + B → C)",
        "Chronological (time: first, second, third)",
        "Structural (space: Boston, New York, Washington)",
        "Comparative (importance: most important to least)"
    ],
    "mece_principle": {
        "mutually_exclusive": "No overlaps (avoid double-counting)",
        "collectively_exhaustive": "No gaps (avoid missing information)"
    },
    "cognitive_load": "3-4 categories ideal (mind holds 7±2 items)",
    "scqa_structure": {
        "situation": "Context the reader knows",
        "complication": "What changed or went wrong",
        "question": "What question does this raise?",
        "answer": "The governing thought (main message)"
    }
}
