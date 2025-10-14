## 🎯 Domain-Aware Reasoning (v3.1)

### Automatic Domain Detection

The system now automatically detects question domains and applies appropriate frameworks:

| Domain | Detection Keywords | MECE Template | Search Strategy |
|--------|-------------------|---------------|-----------------|
| **Technical** | algorithm, optimization, fabrication, photonic, neural network | Problem Formulation, Solution Approach, Implementation, Validation | arXiv, IEEE, Nature, ScienceDirect |
| **Business** | revenue, profit, market, customer, strategy | Market Position, Operational Efficiency, Revenue Model, Strategic Positioning | Tavily, McKinsey, Forbes, HBR |
| **Medical** | patient, diagnosis, treatment, clinical | Clinical Presentation, Diagnostic Workup, Differential, Treatment | PubMed, NEJM, medical journals |
| **General** | (default) | Current State, Challenges, Solutions, Implementation | General web search |

### Example: Technical Question
```python
plan_pyramid(
    brief="How can we develop density-based topology optimization "
          "algorithms for photonic inverse design that strictly enforce "
          "foundry fabrication constraints?"
)
```

**Output:**
- Domain: `technical`
- MECE Reasons:
  1. Problem Formulation & Requirements
  2. Solution Approach & Methods
  3. Implementation Strategy
  4. Validation & Performance Metrics
- Search Strategy: `academic` (arXiv, IEEE, Nature)
- Evidence: 20+ academic papers from photonics journals

### Example: Business Question
```python
plan_pyramid(
    brief="Revenue grew 60% but profit margin dropped from 28% to 14%. "
          "Customer acquisition cost tripled."
)
```

**Output:**
- Domain: `business`
- MECE Reasons:
  1. Revenue Drivers
  2. Cost Structure
  3. Pricing Strategy
  4. Market Dynamics
- Search Strategy: `business` (Tavily, industry reports)
- Evidence: 20+ business sources

### Quality Gates

All pyramids now pass through 4 quality checks:

1. **Pyramid Fidelity** (≥0.75): MECE compliance
2. **Evidence Sufficiency** (≥0.70): Coverage and confidence
3. **Consistency** (≥0.70): No contradictions
4. **Semantic Relevance** (≥0.70): Evidence matches domain ✨ NEW

If semantic relevance fails, the system recommends adjusting search queries or regenerating MECE categories.
