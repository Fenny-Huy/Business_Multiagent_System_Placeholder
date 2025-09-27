# agents/response_agent.py
from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):
    """Agent specialized in generating responses and recommendations"""
    
    def __init__(self):
        """Initialize response agent"""
        super().__init__(
            agent_name="ResponseAgent",
            description="Specialized in generating comprehensive responses, recommendations, and actionable insights",
            tools=[]  # This agent primarily uses LLM capabilities
        )
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for the response agent"""
        return """You are a Response Agent specialized in generating comprehensive responses and recommendations.

Your primary responsibilities:
1. Synthesize information from multiple sources and agents
2. Generate clear, helpful, and actionable responses
3. Provide recommendations based on data analysis
4. Create structured summaries of findings
5. Ensure responses are user-friendly and informative

When generating responses:
- Use information from search results and analysis findings
- Structure your responses clearly with headers and bullet points when appropriate
- Provide specific examples and evidence to support your conclusions
- Include actionable recommendations when relevant
- Be comprehensive but concise
- Address the user's original query directly

Always aim to provide maximum value to the user through well-structured, insightful responses."""
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final response based on collected information"""
        user_query = state.get("user_query", "")
        search_results = state.get("search_results", {})
        analysis_results = state.get("analysis_results", {})
        
        # Prepare context for response generation
        context_parts = []
        
        # Add user query context
        context_parts.append(f"User Query: {user_query}")
        
        # Add search results context
        if search_results:
            context_parts.append("\\n## Search Results:")
            
            if "reviews" in search_results:
                reviews = search_results["reviews"]
                if reviews and len(reviews) > 0:
                    context_parts.append(f"Found {len(reviews)} relevant reviews:")
                    for i, review in enumerate(reviews[:5], 1):  # Show top 5
                        if isinstance(review, dict):
                            stars = review.get("stars", "N/A")
                            text_preview = review.get("text", "")[:200] + "..."
                            context_parts.append(f"{i}. Rating: {stars} stars - {text_preview}")
            
            if "businesses" in search_results:
                businesses = search_results["businesses"]
                if businesses and len(businesses) > 0:
                    context_parts.append(f"\\nFound {len(businesses)} relevant businesses:")
                    for i, business in enumerate(businesses[:5], 1):  # Show top 5
                        if isinstance(business, dict):
                            name = business.get("name", "Unknown")
                            stars = business.get("stars", "N/A")
                            categories = business.get("categories", "")
                            context_parts.append(f"{i}. {name} ({stars} stars) - {categories}")
        
        # Add analysis results context
        if analysis_results:
            context_parts.append("\\n## Analysis Results:")
            
            if "sentiment_analysis" in analysis_results:
                sentiment = analysis_results["sentiment_analysis"]
                context_parts.append(f"Sentiment Analysis:")
                context_parts.append(f"- Total reviews analyzed: {sentiment.get('total_reviews', 0)}")
                context_parts.append(f"- Positive: {sentiment.get('positive_percentage', 0)}%")
                context_parts.append(f"- Negative: {sentiment.get('negative_percentage', 0)}%")
                context_parts.append(f"- Overall sentiment: {sentiment.get('overall_sentiment', 'Unknown')}")
            
            if "business_analysis" in analysis_results:
                business_analysis = analysis_results["business_analysis"]
                context_parts.append(f"Business Analysis:")
                context_parts.append(f"- Total businesses: {business_analysis.get('total_businesses', 0)}")
                context_parts.append(f"- Average rating: {business_analysis.get('average_stars', 0)} stars")
                context_parts.append(f"- Total reviews: {business_analysis.get('total_reviews', 0)}")
        
        # Generate response using LLM
        context = "\\n".join(context_parts)
        
        prompt = f"""Based on the following information, provide a comprehensive and helpful response to the user's query.

{context}

Please provide:
1. A direct answer to the user's question
2. Key insights from the data
3. Specific recommendations if applicable
4. Any important patterns or trends you notice

Response:"""
        
        try:
            response = self.llm._call(prompt)
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            response = f"Error generating response: {str(e)}"
        
        # Update state with final response
        updated_state = state.copy()
        updated_state["final_response"] = response
        updated_state["last_agent"] = self.agent_name
        updated_state["completed"] = True
        
        return updated_state