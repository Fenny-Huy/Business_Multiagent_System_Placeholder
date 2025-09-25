   # multiagent_system.py
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing_extensions import TypedDict

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
    
    def __init__(self, chroma_host: str = "localhost", log_level: str = "INFO"):
        """Initialize the multi-agent system
        
        Args:
            chroma_host: ChromaDB server host
            log_level: Logging level
        """
        # Setup logging
        setup_logging(log_level=log_level)
        self.logger = get_logger(__name__)
        
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
        updated_state = self.supervisor.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        messages.append(f"Supervisor routing to: {updated_state.get('next_agent', 'UNKNOWN')}")
        updated_state["messages"] = messages
        
        return updated_state
    
    def _search_agent_node(self, state: AgentState) -> AgentState:
        """Search agent node"""
        self.logger.info("SearchAgent processing...")
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
        
        return updated_state
    
    def _analysis_agent_node(self, state: AgentState) -> AgentState:
        """Analysis agent node"""
        self.logger.info("AnalysisAgent processing...")
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
        
        return updated_state
    
    def _response_agent_node(self, state: AgentState) -> AgentState:
        """Response agent node"""
        self.logger.info("ResponseAgent processing...")
        updated_state = self.response_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        has_response = bool(updated_state.get("final_response", ""))
        messages.append(f"ResponseAgent completed: {'Generated final response' if has_response else 'No response generated'}")
        updated_state["messages"] = messages
        
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
    # Initialize system
    system = MultiAgentSystem(chroma_host="localhost")
    
    # Example queries
    test_queries = [
        "Find reviews for Italian restaurants",
        "What do people say about Hernandez Restaurant?", 
        "Show me businesses with good ratings in the food category"
    ]
    
    for query in test_queries:
        print(f"\\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        result = system.process_query(query)
        
        if result["success"]:
            print(f"\\nFinal Response:")
            print(result["final_response"])
            
            print(f"\\nExecution Log:")
            for message in result["execution_log"]:
                print(f"- {message}")
        else:
            print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()