# 🏛️ Minto Pyramid Logic MCP Server

> Transform complex, scattered thoughts into crystal-clear, logically organized pyramids using Minto's Pyramid Principle

## 🎯 What This Does

This MCP server applies **Minto's Pyramid Principle** to help you:
- Break down complex problems using SCQA (Situation-Complication-Question-Answer)
- Create MECE (Mutually Exclusive, Collectively Exhaustive) categories
- Gather and organize evidence systematically
- Build logical pyramid structures
- Identify hidden opportunities in challenges

## 🚀 Quick Start

### Local Testing
```bash
# Install FastMCP
pip install fastmcp

# Run the server
fastmcp dev server.py
```

### Deploy to FastMCP Cloud
1. Push this repository to GitHub
2. Go to https://fastmcp.cloud
3. Sign in with GitHub
4. Click "New Project" and select this repo
5. FastMCP Cloud automatically deploys!

Your server will be available at: `https://minto-pyramid.fastmcp.app/mcp`

## 🛠️ Tools Available

### SCQA Framework
- `analyze_situation` - Establish baseline context
- `identify_complication` - Find paradoxes and tensions
- `formulate_transformation_question` - Generate transformative questions

### MECE Decomposition
- `generate_mece_categories` - Create mutually exclusive categories
- `validate_mece_structure` - Validate MECE compliance

### Evidence & Analysis
- `gather_category_evidence` - Collect supporting evidence
- `create_source_attribution_table` - Document sources

### Pyramid Construction
- `build_pyramid_structure` - Assemble complete pyramid
- `validate_pyramid_rules` - Check Minto's 3 rules

### Opportunity Identification
- `reframe_challenges_as_opportunities` - Transform problems into possibilities

### Reporting
- `generate_minto_report` - Create comprehensive reports
- `generate_decision_flow_diagram` - Visualize the analysis flow

### Core Thinking
- `minto_sequential_thinking` - Advanced sequential reasoning engine

## 📊 Features

- **Complexity Score**: 85/100
- **Thinking Pattern**: Complex Multi-Dimensional
- **Agent Strategy**: Full Sequence (7 agents)
- **18+ Specialized Tools**
- **6-Phase Analysis Protocol**
- **Context Isolation for Unbiased MECE Generation**
- **Full Transparency & Attribution**

## 🔌 Connect From

### Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "minto": {
      "url": "https://minto-pyramid.fastmcp.app/mcp",
      "auth": {"type": "oauth"}
    }
  }
}
```

### Python
```python
from fastmcp import Client

async with Client("https://minto-pyramid.fastmcp.app/mcp") as client:
    result = await client.call_tool("analyze_situation", {
        "context": "Your context here",
        "domain": "business"
    })
```

### n8n
- Server URL: `https://minto-pyramid.fastmcp.app/mcp/sse`
- Auth: Bearer Token
- Transport: SSE

## 📈 Performance

| Operation | Target Time |
|-----------|-------------|
| Tool call | < 500ms |
| SCQA analysis | 2-3 sec |
| MECE generation | 5-10 sec |
| Complete pyramid | 30-60 sec |
| Report generation | 10-20 sec |

## 🎓 Methodology

Based on Barbara Minto's "The Pyramid Principle":
1. **Start with the answer** (or transformative question)
2. **Group ideas** into MECE categories
3. **Logical sequencing** - time, structure, or importance
4. **Evidence-based** - every claim supported
5. **Bottom-up construction** - evidence drives structure

## 📞 Support

- **Documentation**: See this README
- **FastMCP Cloud**: https://docs.fastmcp.com
- **Issues**: Use GitHub Issues in this repo

## 📝 License

MIT License - Feel free to use and modify!

---

**Built with FastMCP** | **Complexity: 85/100** | **18+ Tools**

Transform complex thinking into structured pyramids! 🚀
