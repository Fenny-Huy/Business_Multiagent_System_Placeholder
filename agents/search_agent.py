# agents/search_agent.py
from typing import Dict, Any, List
from langchain.tools import Tool
from agents.base_agent import BaseAgent
from tools.review_search_tool import ReviewSearchTool
from tools.business_search_tool import BusinessSearchTool


class SearchAgent(BaseAgent):
    """Agent specialized in searching and retrieving information from databases"""
    
    def __init__(self, chroma_host: str = "localhost"):
        """Initialize search agent
        
        Args:
            chroma_host: ChromaDB server host
        """
        # Initialize tools
        self.review_search_tool = ReviewSearchTool(host=chroma_host, port=8001)
        self.business_search_tool = BusinessSearchTool(host=chroma_host, port=8000)
        
        # Create LangChain tools
        tools = [
            Tool(
                name="search_reviews",
                description="Search for relevant reviews based on semantic similarity. Input can be a string (query), or a dict with 'query', optional 'k', and optional 'business_id'.",
                func=self.review_search_tool
            ),
            Tool(
                name="search_businesses",
                description="Search for businesses by name, category, location, or description. Input can be a string (query) or dict with 'query' and optional 'k'.",
                func=self.business_search_tool
            )
        ]
        
        super().__init__(
            agent_name="SearchAgent",
            description="Specialized in finding and retrieving relevant reviews and business information from databases",
            tools=tools
        )
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for the search agent"""
        return """You are a Search Agent specialized in finding and retrieving information from databases.

Your primary responsibilities:
1. Search for relevant reviews based on user queries
2. Find businesses by name, category, location, or description
3. Filter search results based on specific criteria (e.g., business_id)
4. Provide accurate and relevant search results

Available tools:
- search_reviews: Find reviews using semantic similarity search
- search_businesses: Find businesses using various search criteria

When searching:
- Use specific and relevant search terms
- Consider different search strategies if initial results are not satisfactory
- Always provide the most relevant and helpful results
- Include context and metadata in your responses

Be thorough but concise in your responses."""
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process search requests from the state"""
        user_query = state.get("user_query", "")
        search_type = state.get("search_type", "auto")  # auto, reviews, businesses
        
        results = {}
        
        # Determine search strategy
        if search_type == "reviews" or "review" in user_query.lower():
            # Search for reviews
            review_results = self.review_search_tool(user_query)
            results["reviews"] = review_results
            
        elif search_type == "businesses" or any(word in user_query.lower() for word in ["restaurant", "business", "place", "shop"]):
            # Search for businesses
            business_results = self.business_search_tool(user_query)
            results["businesses"] = business_results
            
        else:
            # Auto mode - search both
            review_results = self.review_search_tool(user_query)
            business_results = self.business_search_tool(user_query)
            results["reviews"] = review_results
            results["businesses"] = business_results
        
        # Update state with search results
        updated_state = state.copy()
        updated_state["search_results"] = results
        updated_state["last_agent"] = self.agent_name
        
        return updated_state