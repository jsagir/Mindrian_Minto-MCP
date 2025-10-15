"""
Example usage of the Minto Pyramid MCP Server
"""

import asyncio
from fastmcp import Client

async def example_complete_analysis():
    """Run a complete Minto analysis in one call"""
    
    async with Client("minto-pyramid-mcp") as client:
        result = await client.call_tool(
            "run_complete_minto_analysis",
            {
                "input_text": """
                Software development teams struggle to balance:
                - Code quality vs delivery speed
                - Technical debt vs new features  
                - Team autonomy vs standardization
                
                Traditional approaches force impossible choices.
                """,
                "analysis_goal": "Reveal development process opportunities",
                "include_meta_analysis": True
            }
        )
        
        # Access results
        pyramid = result["final_pyramid"]
        
        print("=== SCQA Framework ===")
        print(f"Question: {pyramid['scqa']['question']['opportunity_focused']}")
        
        print("\n=== MECE Categories ===")
        for category in pyramid['mece']['categories']:
            print(f"- {category['name']}: {category['core_insight']}")
        
        print("\n=== Meta-Analysis ===")
        print(f"Total thoughts: {pyramid['meta_analysis']['process_summary']['total_thoughts']}")
        print(f"Evidence sources: {pyramid['meta_analysis']['process_summary']['total_evidence_sources']}")
        
        return result

async def example_phase_by_phase():
    """Execute analysis phase by phase with control"""
    
    async with Client("minto-pyramid-mcp") as client:
        # Phase 1: Initialize
        init = await client.call_tool("initialize_minto_analysis", {
            "input_text": "Your complex problem here...",
            "analysis_goal": "Find opportunities"
        })
        session_id = init["session_id"]
        print(f"✓ Initialized session: {session_id}")
        
        # Phase 2: SCQA
        scqa = await client.call_tool("develop_scqa_framework", {
            "session_id": session_id
        })
        print(f"✓ SCQA developed: {len(scqa['thinking_steps'])} thinking steps")
        
        # Phase 3: MECE (with iterations)
        mece = await client.call_tool("generate_mece_framework", {
            "session_id": session_id,
            "max_iterations": 3
        })
        print(f"✓ MECE generated: {mece['iterations_required']} iterations")
        
        # Phase 4: Evidence
        evidence = await client.call_tool("gather_evidence", {
            "session_id": session_id,
            "max_results_per_query": 10
        })
        print(f"✓ Evidence gathered: {evidence['total_sources']} sources")
        
        # Phase 5: Synthesis
        synthesis = await client.call_tool("synthesize_pyramid", {
            "session_id": session_id,
            "output_format": "all"
        })
        print(f"✓ Pyramid synthesized")
        
        # Phase 6: Meta-analysis
        meta = await client.call_tool("perform_meta_analysis", {
            "session_id": session_id
        })
        print(f"✓ Meta-analysis complete")
        
        return meta["final_pyramid"]

if __name__ == "__main__":
    print("Example 1: Complete Analysis")
    asyncio.run(example_complete_analysis())
    
    print("\n" + "="*80 + "\n")
    
    print("Example 2: Phase-by-Phase Control")
    asyncio.run(example_phase_by_phase())
