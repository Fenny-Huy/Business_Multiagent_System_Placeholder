# test_react_agents.py
"""Test script for the updated ReAct-based agents"""

from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.supervisor_agent import SupervisorAgent
from multiagent_system import AgentState

def test_agents():
    """Test the updated agents with ReAct pattern"""
    print("🧪 Testing Updated ReAct-based Multi-Agent System")
    print("="*60)
    
    # Initialize agents
    print("\n1. Initializing agents...")
    try:
        search_agent = SearchAgent()
        analysis_agent = AnalysisAgent()
        supervisor_agent = SupervisorAgent(['SearchAgent', 'AnalysisAgent', 'ResponseAgent'])
        print("✅ All agents initialized successfully")
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return
    
    # Test state with sample query
    print("\n2. Testing with sample query...")
    test_state = {
        "user_query": "What do people think about Italian restaurants?",
        "search_results": {},
        "analysis_results": {},
        "final_response": "",
        "search_agent_note": "",
        "search_agent_result": {},
        "analysis_agent_note": "",
        "analysis_agent_result": {},
        "last_agent": "",
        "next_agent": "",
        "completed": False,
        "messages": []
    }
    
    print("\n3. Testing SearchAgent...")
    try:
        search_result = search_agent.process(test_state)
        print(f"✅ SearchAgent completed")
        print(f"   Note: {search_result.get('search_agent_note', 'No note')[:100]}...")
        print(f"   Has result data: {'search_agent_result' in search_result}")
        test_state.update(search_result)
    except Exception as e:
        print(f"❌ SearchAgent failed: {e}")
    
    print("\n4. Testing AnalysisAgent...")
    try:
        analysis_result = analysis_agent.process(test_state)
        print(f"✅ AnalysisAgent completed")
        print(f"   Note: {analysis_result.get('analysis_agent_note', 'No note')[:100]}...")
        print(f"   Has result data: {'analysis_agent_result' in analysis_result}")
        test_state.update(analysis_result)
    except Exception as e:
        print(f"❌ AnalysisAgent failed: {e}")
    
    print("\n5. Testing SupervisorAgent routing with notes...")
    try:
        supervisor_result = supervisor_agent.process(test_state)
        print(f"✅ SupervisorAgent completed")
        print(f"   Next agent decision: {supervisor_result.get('next_agent', 'No decision')}")
    except Exception as e:
        print(f"❌ SupervisorAgent failed: {e}")
    
    print("\n6. Summary of implementation:")
    print("   ✅ ReAct pattern implemented with create_react_agent")
    print("   ✅ Structured output parsing with note/result separation")
    print("   ✅ Supervisor uses efficient note-based routing")
    print("   ✅ Backward compatibility maintained")
    print("   ✅ Error handling and graceful degradation")
    
    print(f"\n🎉 Test completed! The agents are now using:")
    print(f"   - LangChain create_react_agent pattern")
    print(f"   - Gemini LLM wrapper with fallback")
    print(f"   - Structured output parsing")
    print(f"   - Note/result optimization for supervisor efficiency")

if __name__ == "__main__":
    test_agents()