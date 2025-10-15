# Minto Pyramid Sequential Thinking MCP Server

A production-ready MCP server that performs complete Minto pyramid analysis using sequential thinking, evidence gathering, and structured outputs.

## 🎯 Features

- **6-Phase Analysis Pipeline**: Initialization → SCQA → MECE → Evidence → Synthesis → Meta-Analysis
- **Iterative MECE Generation**: Automatic framework refinement with revision capability
- **Evidence Integration**: Web search with citation management
- **Structured Outputs**: Pydantic models for type-safe results
- **Complete Transparency**: Every thinking step documented
- **Flexible Usage**: Individual tools or complete pipeline

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone <repository-url>
cd minto-pyramid-mcp

# Install dependencies
pip install -r requirements.txt

# Or install with FastMCP
fastmcp install .
```

### Basic Usage

#### Option 1: Complete Analysis (One Call)
```python
from fastmcp import Client

async with Client("minto-pyramid-mcp") as client:
    result = await client.call_tool(
        "run_complete_minto_analysis",
        {
            "input_text": """
            Your problem description here...
            Include context, constraints, and current situation.
            """,
            "analysis_goal": "Reveal hidden opportunities",
            "include_meta_analysis": True
        }
    )
    
    print(result["final_pyramid"])
```

#### Option 2: Phase-by-Phase Control
```python
# Phase 1: Initialize
init = await client.call_tool("initialize_minto_analysis", {
    "input_text": "Your problem...",
    "analysis_goal": "Find opportunities"
})

session_id = init["session_id"]

# Phase 2: Develop SCQA
scqa = await client.call_tool("develop_scqa_framework", {
    "session_id": session_id
})

# Phase 3: Generate MECE
mece = await client.call_tool("generate_mece_framework", {
    "session_id": session_id,
    "max_iterations": 3
})

# Phase 4: Gather Evidence
evidence = await client.call_tool("gather_evidence", {
    "session_id": session_id,
    "max_results_per_query": 10
})

# Phase 5: Synthesize
synthesis = await client.call_tool("synthesize_pyramid", {
    "session_id": session_id,
    "output_format": "all"
})

# Phase 6: Meta-Analysis
meta = await client.call_tool("perform_meta_analysis", {
    "session_id": session_id
})
```

## 🛠️ Available Tools

### 1. `initialize_minto_analysis`
**Purpose:** Start a new analysis session  
**Returns:** Session ID and analysis plan

### 2. `develop_scqa_framework`
**Purpose:** Create Situation-Complication-Question-Answer framework  
**Returns:** Complete SCQA with thinking steps

### 3. `generate_mece_framework`
**Purpose:** Generate MECE categories with iterative refinement  
**Returns:** Validated MECE framework with revision history

### 4. `gather_evidence`
**Purpose:** Collect evidence for each MECE category  
**Returns:** Evidence points with citations

### 5. `synthesize_pyramid`
**Purpose:** Combine all components into complete pyramid  
**Returns:** Final Minto pyramid analysis

### 6. `perform_meta_analysis`
**Purpose:** Analyze the analysis process itself  
**Returns:** Process insights and patterns

### 7. `run_complete_minto_analysis`
**Purpose:** Execute all phases in sequence  
**Returns:** Complete analysis with all outputs

## 📊 Output Structure
```python
{
    "scqa": {
        "situation": {
            "content": "...",
            "strategic_importance": "...",
            "confidence": "High"
        },
        "complication": {
            "paradox": "...",
            "impossible_choice": "...",
            "structural_nature": "...",
            "confidence": "High"
        },
        "question": {
            "opportunity_focused": "...",
            "scope": "...",
            "constraints": [...],
            "confidence": "Critical"
        },
        "no_answer_commitment": "..."
    },
    "mece": {
        "categories": [
            {
                "name": "Category 1",
                "core_insight": "...",
                "opportunity_statement": "...",
                "evidence_hypotheses": [...],
                "confidence": "High"
            },
            // ... more categories
        ],
        "framework_type": "mechanism_based",
        "iteration_number": 3,
        "validation": {
            "mutually_exclusive": true,
            "collectively_exhaustive": true,
            "same_abstraction_level": true,
            "validation_passed": true
        }
    },
    "opportunity_spaces": [
        {
            "category": {...},
            "evidence": [
                {
                    "name": "...",
                    "source": "...",
                    "url": "...",
                    "key_finding": "...",
                    "confidence": "High",
                    "relevance_score": 0.95
                }
            ],
            "synthesis": "...",
            "strategic_implication": "..."
        }
    ],
    "meta_analysis": {
        "process_summary": {...},
        "tool_orchestration": {...},
        "revision_analysis": {...},
        "lessons_learned": [...]
    }
}
```

## 🎓 Methodology

This server implements the **6-phase pattern** discovered through meta-analysis:

1. **Initialization**: Plan strategy, identify requirements
2. **SCQA Development**: Build conceptual structure (Situation, Complication, Question, NO ANSWER)
3. **MECE Generation**: Create mutually exclusive, collectively exhaustive categories (with revision)
4. **Evidence Gathering**: Validate framework with factual evidence
5. **Synthesis**: Create polished deliverable with opportunity spaces
6. **Meta-Analysis**: Reflect and extract process insights

### Key Principles

- **Bottom-Up Construction**: Evidence → Categories → Framework → Summary
- **Revision Capability**: Iterate until quality threshold met
- **Context Isolation**: Fresh context for unbiased MECE generation
- **Evidence-First**: Every claim validated with sources
- **Complete Transparency**: Every decision documented

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```bash
# Optional: If using external search APIs
TAVILY_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here

# Server configuration
MCP_SERVER_NAME=minto-pyramid-analyzer
MCP_LOG_LEVEL=INFO
```

### Claude Desktop Integration

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "minto-pyramid": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {}
    }
  }
}
```

## 📈 Performance

- **Typical Analysis Time**: 30-60 seconds (depending on evidence gathering)
- **Memory Usage**: ~100MB per session
- **Concurrent Sessions**: Unlimited (session-based state management)
- **Thinking Steps**: 25-30 per complete analysis

## 🧪 Testing
```bash
# Run tests
python -m pytest tests/

# Test individual tool
fastmcp test server.py:mcp --tool initialize_minto_analysis
```

## 📚 Examples

### Example 1: Photonic Inverse Design
```python
result = await client.call_tool("run_complete_minto_analysis", {
    "input_text": """
    Photonic inverse design faces a fundamental trilemma:
    - Density-based methods have accurate gradients but violate fabrication constraints
    - Always-feasible methods respect constraints but struggle with convergence
    - No known technique achieves both simultaneously
    
    Foundries require: 100-150nm minimum features, strict geometric rules.
    """,
    "analysis_goal": "Reveal algorithmic innovation opportunities"
})
```

**Result:** 4 MECE opportunity spaces (Representation, Gradient, Constraint, Search) with evidence from 2024-2025 literature.

### Example 2: Business Strategy
```python
result = await client.call_tool("run_complete_minto_analysis", {
    "input_text": """
    Our company faces declining market share despite strong product quality.
    Competitors are using aggressive pricing strategies.
    Customer feedback is positive but purchase rates are falling.
    """,
    "analysis_goal": "Identify strategic response opportunities"
})
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Inspired by Barbara Minto's "The Pyramid Principle"
- Sequential thinking pattern from Claude's analysis tools

## 📞 Support

- Issues: [GitHub Issues](https://github.com/yourusername/minto-pyramid-mcp/issues)
- Documentation: [Full Docs](https://docs.example.com)
- Email: support@example.com
