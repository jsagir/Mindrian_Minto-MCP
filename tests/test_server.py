"""
Unit tests for Minto Pyramid MCP Server
"""

import pytest
from fastmcp.testing import TestTransport
from server import mcp

@pytest.fixture
async def client():
    """Create a test client"""
    transport = TestTransport()
    # In production, would properly initialize client
    yield transport

@pytest.mark.asyncio
async def test_initialize_analysis(client):
    """Test session initialization"""
    result = await mcp.call_tool(
        "initialize_minto_analysis",
        {"input_text": "Test problem", "analysis_goal": "Test"}
    )
    
    assert "session_id" in result
    assert result["status"] == "initialized"
    assert len(result["phases_planned"]) == 6

@pytest.mark.asyncio
async def test_scqa_development(client):
    """Test SCQA framework generation"""
    # Initialize first
    init = await mcp.call_tool(
        "initialize_minto_analysis",
        {"input_text": "Test problem"}
    )
    
    # Develop SCQA
    result = await mcp.call_tool(
        "develop_scqa_framework",
        {"session_id": init["session_id"]}
    )
    
    assert "scqa" in result
    assert result["scqa"]["framework_complete"] == True
    assert len(result["thinking_steps"]) == 5

@pytest.mark.asyncio
async def test_mece_generation(client):
    """Test MECE framework with revisions"""
    # Setup
    init = await mcp.call_tool("initialize_minto_analysis", {"input_text": "Test"})
    await mcp.call_tool("develop_scqa_framework", {"session_id": init["session_id"]})
    
    # Generate MECE
    result = await mcp.call_tool(
        "generate_mece_framework",
        {"session_id": init["session_id"], "max_iterations": 3}
    )
    
    assert "mece" in result
    assert result["mece"]["validation"]["validation_passed"] == True
    assert result["iterations_required"] <= 3

@pytest.mark.asyncio
async def test_complete_analysis(client):
    """Test end-to-end analysis"""
    result = await mcp.call_tool(
        "run_complete_minto_analysis",
        {
            "input_text": "Test problem for complete analysis",
            "include_meta_analysis": True
        }
    )
    
    assert result["status"] == "Complete"
    assert result["phases_executed"] == 6
    assert "final_pyramid" in result
    
    pyramid = result["final_pyramid"]
    assert "scqa" in pyramid
    assert "mece" in pyramid
    assert "opportunity_spaces" in pyramid
    assert "meta_analysis" in pyramid
