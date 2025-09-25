   # multiagent_system.py
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
import json
import pprint

# Import agents
from agents.supervisor_agent import SupervisorAgent
from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.response_agent import ResponseAgent

# Import config
from config.logging_config import setup_logging, get_logger


class AgentState(TypedDict):
    """State shared between all agents"""
    user_query: str
    search_results: Dict[str, Any]
    analysis_results: Dict[str, Any] 
    final_response: str
    last_agent: str
    next_agent: str
    completed: bool
    messages: List[str]


class MultiAgentSystem:
    """LangGraph-based multi-agent system with supervisor coordination"""
    
    def __init__(self, chroma_host: str = None, log_level: str = "INFO", show_state_changes: bool = True):
        """Initialize the multi-agent system
        
        Args:
            chroma_host: ChromaDB server host (defaults to CHROMA_HOST env var or "localhost")
            log_level: Logging level
            show_state_changes: Whether to display state changes in real-time
        """
        # Setup logging
        setup_logging(log_level=log_level)
        self.logger = get_logger(__name__)
        self.show_state_changes = show_state_changes
        
        # Initialize agents
        self.search_agent = SearchAgent(chroma_host=chroma_host)
        self.analysis_agent = AnalysisAgent()
        self.response_agent = ResponseAgent()
        
        # Available agent names for supervisor
        available_agents = ["SearchAgent", "AnalysisAgent", "ResponseAgent"]
        self.supervisor = SupervisorAgent(available_agents)
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
        
        self.logger.info("✓ Multi-agent system initialized")
    
    def _display_state_change(self, node_name: str, state: AgentState, changes: Dict[str, Any] = None):
        """Display state changes in real-time"""
        if not self.show_state_changes:
            return
            
        print(f"\n{'='*60}")
        print(f"🔄 STATE UPDATE - {node_name}")
        print('='*60)
        
        # Show key state information
        print(f"Last Agent: {state.get('last_agent', 'None')}")
        print(f"Next Agent: {state.get('next_agent', 'None')}")
        print(f"Completed: {state.get('completed', False)}")
        
        # Show search results summary
        search_results = state.get('search_results', {})
        if search_results:
            print(f"\n📊 Search Results:")
            for key, value in search_results.items():
                if isinstance(value, list):
                    print(f"  - {key}: {len(value)} items")
                else:
                    print(f"  - {key}: {type(value).__name__}")
        
        # Show analysis results summary  
        analysis_results = state.get('analysis_results', {})
        if analysis_results:
            print(f"\n🔍 Analysis Results:")
            for key, value in analysis_results.items():
                if isinstance(value, dict):
                    print(f"  - {key}: {list(value.keys())}")
                else:
                    print(f"  - {key}: {type(value).__name__}")
        
        # Show final response preview
        final_response = state.get('final_response', '')
        if final_response:
            preview = final_response[:100] + "..." if len(final_response) > 100 else final_response
            print(f"\n💬 Response Preview: {preview}")
        
        # Show recent messages
        messages = state.get('messages', [])
        if messages:
            print(f"\n📝 Recent Messages:")
            for msg in messages[-3:]:  # Show last 3 messages
                print(f"  - {msg}")
        
        print('='*60)
        input("Press Enter to continue...")  # Pause for user to review
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("SearchAgent", self._search_agent_node)
        workflow.add_node("AnalysisAgent", self._analysis_agent_node)
        workflow.add_node("ResponseAgent", self._response_agent_node)
        
        # Define the routing logic
        workflow.add_conditional_edges(
            "supervisor",
            self._route_to_agent,
            {
                "SearchAgent": "SearchAgent",
                "AnalysisAgent": "AnalysisAgent", 
                "ResponseAgent": "ResponseAgent",
                "FINISH": END
            }
        )
        
        # After each agent, go back to supervisor
        workflow.add_edge("SearchAgent", "supervisor")
        workflow.add_edge("AnalysisAgent", "supervisor")
        workflow.add_edge("ResponseAgent", "supervisor")
        
        # Set entry point
        workflow.set_entry_point("supervisor")
        
        return workflow.compile()
    
    def _supervisor_node(self, state: AgentState) -> AgentState:
        """Supervisor agent node"""
        self.logger.info("Supervisor making routing decision...")
        
        # Show current state before processing
        self._display_state_change("SUPERVISOR (Before)", state)
        
        updated_state = self.supervisor.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        messages.append(f"Supervisor routing to: {updated_state.get('next_agent', 'UNKNOWN')}")
        updated_state["messages"] = messages
        
        # Show state after processing
        self._display_state_change("SUPERVISOR (After)", updated_state)
        
        return updated_state
    
    def _search_agent_node(self, state: AgentState) -> AgentState:
        """Search agent node"""
        self.logger.info("SearchAgent processing...")
        
        # Show current state before processing
        self._display_state_change("SEARCH AGENT (Before)", state)
        
        updated_state = self.search_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        search_results = updated_state.get("search_results", {})
        result_summary = []
        
        if "reviews" in search_results:
            result_summary.append(f"Found {len(search_results['reviews'])} reviews")
        if "businesses" in search_results:
            result_summary.append(f"Found {len(search_results['businesses'])} businesses")
        
        messages.append(f"SearchAgent completed: {', '.join(result_summary) if result_summary else 'No results'}")
        updated_state["messages"] = messages
        
        # Show state after processing
        self._display_state_change("SEARCH AGENT (After)", updated_state)
        
        return updated_state
    
    def _analysis_agent_node(self, state: AgentState) -> AgentState:
        """Analysis agent node"""
        self.logger.info("AnalysisAgent processing...")
        
        # Show current state before processing
        self._display_state_change("ANALYSIS AGENT (Before)", state)
        
        updated_state = self.analysis_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        analysis_results = updated_state.get("analysis_results", {})
        analysis_summary = []
        
        if "sentiment_analysis" in analysis_results:
            sentiment = analysis_results["sentiment_analysis"]
            overall = sentiment.get("overall_sentiment", "Unknown")
            analysis_summary.append(f"Sentiment: {overall}")
        
        if "business_analysis" in analysis_results:
            business = analysis_results["business_analysis"] 
            avg_stars = business.get("average_stars", 0)
            analysis_summary.append(f"Avg rating: {avg_stars} stars")
        
        messages.append(f"AnalysisAgent completed: {', '.join(analysis_summary) if analysis_summary else 'No analysis'}")
        updated_state["messages"] = messages
        
        # Show state after processing
        self._display_state_change("ANALYSIS AGENT (After)", updated_state)
        
        return updated_state
    
    def _response_agent_node(self, state: AgentState) -> AgentState:
        """Response agent node"""
        self.logger.info("ResponseAgent processing...")
        
        # Show current state before processing
        self._display_state_change("RESPONSE AGENT (Before)", state)
        
        updated_state = self.response_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        has_response = bool(updated_state.get("final_response", ""))
        messages.append(f"ResponseAgent completed: {'Generated final response' if has_response else 'No response generated'}")
        updated_state["messages"] = messages
        
        # Show state after processing
        self._display_state_change("RESPONSE AGENT (After)", updated_state)
        
        return updated_state
    
    def _route_to_agent(self, state: AgentState) -> str:
        """Route to the next agent based on supervisor decision"""
        next_agent = state.get("next_agent", "FINISH")
        self.logger.info(f"Routing to: {next_agent}")
        return next_agent
    
    def process_query(self, user_query: str, max_iterations: int = 10) -> Dict[str, Any]:
        """Process a user query through the multi-agent system
        
        Args:
            user_query: User's question or request
            max_iterations: Maximum number of agent iterations
            
        Returns:
            Final results including response and execution details
        """
        self.logger.info(f"Processing query: {user_query}")
        
        # Initialize state
        initial_state = AgentState(
            user_query=user_query,
            search_results={},
            analysis_results={},
            final_response="",
            last_agent="",
            next_agent="",
            completed=False,
            messages=[]
        )
        
        try:
            # Execute the workflow
            result = self.workflow.invoke(initial_state)
            
            self.logger.info("Query processing completed")
            
            return {
                "success": True,
                "query": user_query,
                "final_response": result.get("final_response", ""),
                "search_results": result.get("search_results", {}),
                "analysis_results": result.get("analysis_results", {}),
                "execution_log": result.get("messages", []),
                "completed": result.get("completed", False)
            }
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": user_query,
                "final_response": f"I apologize, but I encountered an error: {str(e)}",
                "execution_log": []
            }


# Example usage and testing
def main():
    """Example usage of the multi-agent system"""
    print("🤖 Multi-Agent System with Real-Time State Monitoring")
    print("="*60)
    
    # Ask user for monitoring preference
    monitor_choice = input("Enable real-time state monitoring? (y/n, default=y): ").lower()
    show_monitoring = monitor_choice != 'n'
    
    # Initialize system - will use CHROMA_HOST from .env file
    system = MultiAgentSystem(show_state_changes=show_monitoring)
    
    print("\n🎯 Choose mode:")
    print("1. Interactive chat mode")
    print("2. Run example queries")
    
    mode = input("Enter choice (1/2, default=1): ").strip()
    
    if mode == "2":
        # Run example queries
        test_queries = [
            "Find reviews for Italian restaurants",
            "What do people say about Hernandez Restaurant?", 
            "Show me businesses with good ratings in the food category"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print('='*60)
            
            result = system.process_query(query)
            
            if result["success"]:
                print(f"\n✅ Final Response:")
                print(result["final_response"])
                
                if not show_monitoring:  # Only show execution log if not monitoring
                    print(f"\n📋 Execution Log:")
                    for message in result["execution_log"]:
                        print(f"  - {message}")
            else:
                print(f"❌ Error: {result['error']}")
                
            if query != test_queries[-1]:  # Don't pause after last query
                input("\nPress Enter to continue to next query...")
    else:
        # Interactive chat mode
        print("\n💬 Interactive Chat Mode")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', '']:
                    print("👋 Goodbye!")
                    break
                
                print(f"\n🤖 Processing: {user_input}")
                result = system.process_query(user_input)
                
                if result["success"]:
                    print(f"\n🎯 System: {result['final_response']}")
                else:
                    print(f"❌ Error: {result['error']}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()