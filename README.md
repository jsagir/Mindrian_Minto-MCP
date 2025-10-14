# 🏛️ Minto Pyramid Logic MCP Server v3.1

Implements Barbara Minto's **Pyramid Principle** with Sequential Thinking for structured reasoning and analysis.

## 📚 What is the Pyramid Principle?

The Pyramid Principle is a communication and reasoning methodology developed by Barbara Minto at McKinsey. It structures thinking in a top-down, hierarchical manner that mirrors how the mind naturally processes information.

### Core Structure: SCQA

**S**ituation → **C**omplication → **Q**uestion → **A**nswer

1. **Situation**: Establish context the reader knows
2. **Complication**: What changed or went wrong
3. **Question**: What question does this raise in the reader's mind?
4. **Answer**: The governing thought (main message)

### Three Sacred Rules

1. **Ideas at any level must ALWAYS be summaries of ideas grouped below**
2. **Ideas in each grouping must ALWAYS be the SAME KIND of idea**
3. **Ideas in each grouping must ALWAYS be LOGICALLY ORDERED**

### MECE Principle

**M**utually **E**xclusive, **C**ollectively **E**xhaustive
- **No overlaps** between categories (avoid double-counting)
- **No gaps** in coverage (avoid missing information)

### Cognitive Load Principle

Limit to **3-4 categories** (mind holds 7±2 items, 3 is ideal)

---

## 🚀 Features

✅ **Universal Domain Detection** - Works for ANY domain (technical, business, medical, etc.)  
✅ **SCQA Introduction** - Engages reader before diving into analysis  
✅ **MECE Validation** - Ensures no overlaps, no gaps  
✅ **Sequential Thinking** - Smart reasoning for structure generation  
✅ **Vertical Q&A Flow** - Each level answers question from above  
✅ **Horizontal Logic** - Deductive OR inductive (never mixed)  
✅ **4 Logical Orders** - Deductive/Chronological/Structural/Comparative  
✅ **Quality Critique** - 8-point validation checklist  

---

## 📦 Installation
```bash
# Clone repository
git clone https://github.com/yourusername/Mindrian_Minto-MCP.git
cd Mindrian_Minto-MCP

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

---

## 🎯 Usage Example

### 1. Plan Pyramid (SCQA + MECE)
```python
result = plan_pyramid(
    brief="How can we develop density-based topology optimization "
          "algorithms for photonic inverse design that enforce "
          "foundry fabrication constraints?",
    audience="researchers"
)

# Returns:
# {
#   "run_id": "abc123",
#   "domain": "technical_engineering",
#   "subdomain": "photonics",
#   "scqa": {
#     "situation": "...",
#     "complication": "...",
#     "question": "...",
#     "answer": "..."
#   },
#   "reasons": [
#     {"title": "Device Design & Geometry", ...},
#     {"title": "Fabrication Constraints & Foundry Rules", ...},
#     {"title": "Performance Optimization & Validation", ...}
#   ],
#   "mece_validation": {"is_mece": true, ...}
# }
```

### 2. Validate MECE
```python
validation = validate_mece(run_id="abc123")

# Returns:
# {
#   "is_mece": true,
#   "mutually_exclusive": true,
#   "collectively_exhaustive": true,
#   "cognitive_load_ok": true,
#   "category_count": 3
# }
```

### 3. Gather Evidence
```python
evidence = run_plan_stage(run_id="abc123", stage="all")

# Returns:
# {
#   "total_evidence": 12,
#   "evidence_by_reason": [
#     {"reason_title": "Device Design", "evidence_count": 4},
#     ...
#   ]
# }
```

### 4. Synthesize Deliverable
```python
deliverable = synthesize_pyramid(run_id="abc123", format="markdown")

# Returns full pyramid structure:
# - SCQA Introduction
# - Governing Thought
# - 3-4 MECE Reasons
# - Supporting Evidence
# - Citations
```

### 5. Quality Critique
```python
critique = critique_pyramid(run_id="abc123")

# Returns:
# {
#   "overall_score": 0.89,
#   "passed": true,
#   "critiques": [
#     {"aspect": "SCQA Completeness", "score": 0.95, ...},
#     {"aspect": "MECE Compliance", "score": 1.0, ...},
#     ...
#   ]
# }
```

---

## 📊 Domain Support

Works automatically for:

| Domain | Example Questions |
|--------|------------------|
| **Technical/Engineering** | Algorithm optimization, system design, photonics, quantum computing, ML/AI |
| **Natural Sciences** | Physics experiments, chemistry synthesis, biological research |
| **Business/Economics** | Strategy, operations, finance, marketing |
| **Medical/Health** | Clinical diagnosis, pharmaceutical development, treatment protocols |
| **Mathematics** | Proof development, computational methods, theoretical analysis |
| **Social/Policy** | Policy analysis, social impact, governance |
| **Law/Governance** | Legal frameworks, compliance, regulatory analysis |
| **Arts/Humanities** | Historical analysis, literary critique, cultural studies |

---

## 🏗️ Architecture
```
server.py                    # FastMCP server (main entry point)
reasoning/
  ├── __init__.py           # Package initialization
  ├── domain_detector.py    # Universal domain detection
  ├── mece_generator.py     # MECE category generation
  ├── mece_validator.py     # MECE compliance validation
  ├── plan.py               # Pyramid planning with sequential thinking
  ├── execution.py          # Evidence gathering
  ├── synthesis.py          # Deliverable generation
  └── critique.py           # Quality validation (8 checkpoints)
```

---

## 🎓 Learning Resources

- **Original Book**: ["The Pyramid Principle" by Barbara Minto](https://www.barbaraminto.com/)
- **MECE Framework**: [McKinsey Problem Solving](https://www.mckinsey.com/)
- **Cognitive Load**: [Miller's Law (7±2)](https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two)

---

## 🤝 Contributing

Contributions welcome! Please:
1. Follow Minto principles in code structure
2. Add tests for new features
3. Update documentation

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- **Barbara Minto** - For the Pyramid Principle methodology
- **McKinsey & Company** - For MECE framework
- **FastMCP** - For MCP server framework

---

**Built with ❤️ following Barbara Minto's timeless principles**
