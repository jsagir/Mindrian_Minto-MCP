# 🏛️ Minto Pyramid Logic MCP Server v3.0

> **Reasoning Orchestrator:** Research-grade sequential thinking engine implementing Pyramid Principle as a first-class execution framework

## 🎯 What's New in v3.0

### **From Tools to Orchestrator**

**v2.0** provided individual tools (search, analyze, validate)  
**v3.0** orchestrates them into a **complete reasoning pipeline** with:

- ✅ **Explicit Planning Stage** - Generate ReasoningPlan before execution
- ✅ **MECE Validation** - Automated scoring and quality gates
- ✅ **Evidence Orchestration** - Parallel search with provenance tracking
- ✅ **Contradiction Detection** - NLI-based consistency checks
- ✅ **Critique Loops** - Systematic evaluation and revision
- ✅ **State Management** - Full run history and artifacts
- ✅ **Metrics & Observability** - Quality scores and tracing

---

## 🏗️ Architecture: 5-Stage Pipeline

```
1. PLAN          →  2. EXECUTE      →  3. SYNTHESIZE  →  4. CRITIQUE     →  5. FINALIZE
plan_pyramid        run_plan_stage      synthesize_       critique_          finalize_
                                        pyramid           pyramid_tool       pyramid

├─ Brief          ├─ Tavily Search  ├─ MECE Check   ├─ Rubric Eval   ├─ Export
├─ Governing      ├─ Evidence       ├─ Citation     ├─ Revision Plan  ├─ Markdown
   Thoughts          Collection         Stitching   ├─ Quality Score  ├─ JSON
├─ MECE Reasons   ├─ Confidence     ├─ Pyramid      └─ Recommendations └─ Artifacts
├─ Evidence Tasks    Scoring           Format
└─ Risk List      └─ Provenance
```

---

## 🚀 Quick Start

### **1. Deploy (Same as Before)**

```bash
cd Desktop\minto-pyramid-mcp
git add .
git commit -m "v3.0: Reasoning Orchestrator"
git push origin main
```

FastMCP Cloud auto-deploys in 2-3 minutes.

### **2. Connect to Claude Desktop**

```json
{
  "mcpServers": {
    "minto-pyramid": {
      "url": "https://PyramidlogicMINTOmindrian.fastmcp.app/mcp"
    }
  }
}
```

### **3. Run Complete Analysis**

```
Use the full_pyramid_analysis prompt with:

Brief: "Our revenue grew 60% but profit margin dropped from 28% to 14%. 
Customer acquisition cost tripled. Analyze this paradox."

Audience: board_of_directors
```

**Claude will automatically orchestrate all 5 stages!**

---

## 🛠️ The 5 Orchestrator Tools

### **1. `plan_pyramid`** - Strategic Planning

```python
plan_pyramid(
    brief="Your business challenge",
    audience="executives",
    constraints={"timeframe": "Q1 2025"}
)
```

**Returns:**
- `run_id` - Unique identifier for this analysis
- `governing_thoughts` - 3 hypothesis candidates
- `reasons` - MECE categories (4-6)
- `evidence_tasks` - Tavily search tasks per reason
- `mece_score` - Quality metric (0.0-1.0)
- `risks` - Identified assumptions and gaps

**Use when:** Starting a new analysis

---

### **2. `run_plan_stage`** - Evidence Gathering

```python
run_plan_stage(
    run_id="abc123",
    stage="all"  # or "reason_1", "reason_2", etc.
)
```

**Does:**
- Executes all Tavily searches in parallel
- Collects evidence with URLs and confidence scores
- Tracks provenance (query, rank, timestamp)
- Normalizes results for citation

**Returns:**
- Evidence collected per reason
- Average confidence scores
- Total evidence count

**Use when:** Collecting supporting evidence

---

### **3. `synthesize_pyramid`** - Document Generation

```python
synthesize_pyramid(
    run_id="abc123",
    include_critique=True
)
```

**Quality Gates:**
- ✅ MECE score ≥ 0.75
- ✅ Evidence count ≥ 2× reasons
- ✅ No critical contradictions

**Returns:**
- Complete Markdown deliverable
- Executive summary (governing thought)
- MECE reasons with evidence
- Full citation list with hyperlinks
- Quality metrics

**Use when:** Ready to generate output

---

### **4. `critique_pyramid_tool`** - Quality Evaluation

```python
critique_pyramid_tool(
    run_id="abc123"
)
```

**Evaluates:**
1. **Pyramid Fidelity** - MECE compliance, structure
2. **Evidence Sufficiency** - Coverage and confidence
3. **Consistency** - Contradiction detection

**Returns:**
- Per-aspect scores (0.0-1.0)
- Findings and recommendations
- Revision plan if needed
- Overall quality gate (pass/fail)

**Use when:** Validating before finalization

---

### **5. `finalize_pyramid`** - Export

```python
finalize_pyramid(
    run_id="abc123",
    export_format="both"  # markdown, json, or both
)
```

**Exports:**
- **Markdown:** Full formatted report with citations
- **JSON:** Structured data for programmatic use
- **Metrics:** Quality scores and statistics

**Use when:** Analysis complete and validated

---

## 📊 Complete Workflow Example

```
User: "Analyze declining profit margins in our SaaS business"

Claude orchestrates:

1️⃣ plan_pyramid(brief="declining profit margins SaaS")
   → run_id: "a1b2c3"
   → 4 MECE reasons
   → 8 evidence tasks
   → MECE score: 0.85 ✓

2️⃣ run_plan_stage(run_id="a1b2c3", stage="all")
   → Tavily searches: 8 queries
   → Evidence collected: 24 items
   → Avg confidence: 0.82

3️⃣ synthesize_pyramid(run_id="a1b2c3")
   → Quality gates: PASS ✓
   → Citations: 24 sources
   → Output: 2,500 word report

4️⃣ critique_pyramid_tool(run_id="a1b2c3")
   → Pyramid fidelity: 0.85
   → Evidence sufficiency: 0.88
   → Consistency: 0.92
   → Overall: 0.88 (PASS) ✓

5️⃣ finalize_pyramid(run_id="a1b2c3", format="both")
   → Markdown ✓
   → JSON ✓
   → Artifacts exported ✓

Output includes:
✅ Executive summary
✅ 4 MECE reasons with evidence
✅ 24 cited sources with hyperlinks
✅ Opportunities identified
✅ Strategic recommendations
✅ Quality metrics
```

---

## 📚 Resources (Access Run Artifacts)

```
pyramid://runs/{run_id}/plan         # ReasoningPlan JSON
pyramid://runs/{run_id}/evidence     # All evidence items
pyramid://runs/{run_id}/deliverable  # Final markdown
pyramid://runs/{run_id}/metrics      # Quality scores
```

**Example:**
```
Show me pyramid://runs/a1b2c3/metrics
```

---

## 🎯 Key Concepts

### **ReasoningPlan**
Structured execution plan with:
- Governing thought hypotheses
- MECE reasons
- Evidence tasks (dependencies, acceptance criteria)
- Risk list
- Execution sequence

### **MECE Validation**
Automated check for:
- **Mutually Exclusive:** No overlaps between reasons
- **Collectively Exhaustive:** No gaps in coverage
- **Same Level:** Consistent abstraction

Scored 0.0-1.0, must be ≥0.75 to synthesize.

### **Evidence Provenance**
Every evidence item tracks:
- Source query
- Search engine
- Rank position
- Timestamp
- Confidence score
- URL for citation

### **Critique Loop**
Systematic evaluation against rubric:
1. Pyramid fidelity (MECE, top-down)
2. Evidence sufficiency (coverage, confidence)
3. Consistency (contradictions)

Returns revision plan if quality gates fail.

---

## 💡 Why This Architecture?

### **Problem:** LLMs are non-deterministic and stateless
- Forget context between calls
- Inconsistent reasoning paths
- No validation or quality control
- Poor evidence tracking

### **Solution:** Explicit reasoning scaffold
- ✅ Deterministic stages with checkpoints
- ✅ State persistence across calls
- ✅ Automated quality gates
- ✅ Full provenance and citations
- ✅ Measurable outputs

### **Benefit:** Reproducible, auditable analysis
- Run same brief twice → same structure
- Trace every decision
- Validate quality objectively
- Iterate with targeted revisions

---

## 🔬 Quality Metrics

### **MECE Score**
```
Score = 1.0 - (overlap_penalty + gap_penalty)
Pass threshold: ≥ 0.75
```

### **Evidence Sufficiency**
```
Score = (evidence_count / (reasons × 2)) × avg_confidence
Pass threshold: ≥ 0.70
```

### **Contradiction Score**
```
Score = contradiction_count × severity_weight
Pass threshold: ≤ 0.30
```

### **Overall Quality**
```
Overall = (pyramid_fidelity + evidence + consistency) / 3
Pass threshold: ≥ 0.75
```

---

## 🧪 Testing

### **Simple Test:**
```
Use plan_pyramid to analyze: "Our customer churn increased from 5% to 18%"
```

### **Full Pipeline:**
```
Use the full_pyramid_analysis prompt with:
Brief: "Revenue up 60%, profits down to 14%"
Audience: executives
```

### **Check Artifacts:**
```
After running, show me:
- pyramid://runs/{run_id}/metrics
- pyramid://runs/{run_id}/deliverable
```

---

## 🆚 Comparison: v2.0 vs v3.0

| Feature | v2.0 | v3.0 |
|---------|------|------|
| **Architecture** | Individual tools | 5-stage pipeline |
| **Planning** | Manual | Automated ReasoningPlan |
| **MECE** | Manual check | Automated scoring |
| **Evidence** | Ad-hoc search | Orchestrated with provenance |
| **Quality** | Subjective | Measured with gates |
| **State** | Stateless | Persistent RunState |
| **Iteration** | Manual | Critique loop |
| **Observability** | Logs only | Metrics + artifacts |
| **Reproducibility** | Low | High |

---

## 🔮 What's Next (Future Enhancements)

### **Phase 2:**
- [ ] Multi-agent mode (Planner, Researcher, Critic, Writer)
- [ ] Counter-argument generation per reason
- [ ] Source diversity constraints
- [ ] Automatic ablation testing

### **Phase 3:**
- [ ] Neo4j GraphRAG integration
- [ ] Embeddings for semantic MECE validation
- [ ] Real NLI model for contradictions
- [ ] OpenTelemetry tracing

### **Phase 4:**
- [ ] LangFlow node wrapper
- [ ] PDF export with diagrams
- [ ] Multi-run comparison
- [ ] Parallel hypothesis testing

---

## 📞 Support

**GitHub:** https://github.com/jsagir/Mindrian_Minto-MCP  
**Server:** https://PyramidlogicMINTOmindrian.fastmcp.app/mcp  
**Version:** 3.0.0  
**Status:** 🟢 Live

---

## 🎓 For Developers

### **Extending the Orchestrator:**

1. **Add new quality gates:**
   ```python
   # In reasoning/metrics.py
   def custom_quality_check(plan: ReasoningPlan) -> float:
       # Your logic
       return score
   ```

2. **Add new evidence sources:**
   ```python
   # In reasoning/execution.py
   async def execute_custom_task(task: EvidenceTask):
       # Your API integration
       return evidence_items
   ```

3. **Customize synthesis:**
   ```python
   # In reasoning/pyramid.py
   def custom_deliverable_format(plan, evidence):
       # Your template
       return formatted_output
   ```

---

## 🏆 Built For

This is the **prototype for Lawrence's distributed intelligence vision:**

✅ **Workflows as Intelligence** - Each MCP = specialized reasoning  
✅ **Composable** - Chain MCPs together  
✅ **Auditable** - Full provenance and metrics  
✅ **Reproducible** - Same input → same structure  
✅ **Scalable** - Run 1000s of analyses

**If this works, we can build MCPs for:**
- Market research workflows
- Competitive analysis  
- OKR frameworks
- Growth strategies
- Customer research
- Product strategy
- Financial analysis
- Risk assessment

**Each becomes a specialized "intelligence" that Claude orchestrates.**

---

**🚀 Deploy now and start building the intelligence layer!**

```bash
git add .
git commit -m "v3.0: Full Reasoning Orchestrator"
git push
```

Your enhanced server will be live in 3 minutes! 🎉
