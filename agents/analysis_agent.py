# agents/analysis_agent.py
from typing import Dict, Any, List
from langchain.tools import Tool
from agents.base_agent import BaseAgent
from tools.sentiment_analysis_tool import SentimentAnalysisTool


class AnalysisAgent(BaseAgent):
    """Agent specialized in analyzing data and extracting insights"""
    
    def __init__(self):
        """Initialize analysis agent"""
        # Initialize tools
        self.sentiment_tool = SentimentAnalysisTool()
        
        # Create LangChain tools
        tools = [
            Tool(
                name="analyze_sentiment",
                description="Analyze sentiment of reviews or text. Input can be a string, list of strings, or dict with 'reviews' key.",
                func=self.sentiment_tool
            )
        ]
        
        super().__init__(
            agent_name="AnalysisAgent", 
            description="Specialized in analyzing data, extracting insights, and performing sentiment analysis",
            tools=tools
        )
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for the analysis agent"""
        return """You are an Analysis Agent specialized in data analysis and insight extraction.

Your primary responsibilities:
1. Perform sentiment analysis on reviews and text data
2. Extract meaningful insights from data patterns
3. Provide statistical summaries and trends
4. Identify key themes and patterns in customer feedback

Available tools:
- analyze_sentiment: Analyze sentiment of text data and reviews

When analyzing:
- Consider both positive and negative aspects
- Look for patterns and trends in the data
- Provide actionable insights based on your analysis
- Use statistical measures to support your conclusions
- Be objective and evidence-based in your assessments

Always provide clear, structured, and insightful analysis."""
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process analysis requests from the state"""
        analysis_results = {}
        
        # Check if there are search results to analyze
        search_results = state.get("search_results", {})
        
        if "reviews" in search_results:
            reviews = search_results["reviews"]
            if reviews and isinstance(reviews, list) and len(reviews) > 0:
                # Extract review texts for sentiment analysis
                review_texts = []
                for review in reviews:
                    if isinstance(review, dict) and "text" in review:
                        review_texts.append(review["text"])
                
                if review_texts:
                    sentiment_analysis = self.sentiment_tool(review_texts)
                    analysis_results["sentiment_analysis"] = sentiment_analysis
        
        # Analyze business data if available
        if "businesses" in search_results:
            businesses = search_results["businesses"]
            if businesses and isinstance(businesses, list):
                # Basic business analysis
                total_businesses = len(businesses)
                avg_stars = 0
                total_reviews = 0
                
                for business in businesses:
                    if isinstance(business, dict):
                        stars = business.get("stars", 0)
                        review_count = business.get("review_count", 0)
                        
                        try:
                            avg_stars += float(stars) if stars else 0
                            total_reviews += int(review_count) if review_count else 0
                        except (ValueError, TypeError):
                            continue
                
                if total_businesses > 0:
                    avg_stars = avg_stars / total_businesses
                    analysis_results["business_analysis"] = {
                        "total_businesses": total_businesses,
                        "average_stars": round(avg_stars, 2),
                        "total_reviews": total_reviews,
                        "avg_reviews_per_business": round(total_reviews / total_businesses, 1)
                    }
        
        # Update state with analysis results
        updated_state = state.copy()
        updated_state["analysis_results"] = analysis_results
        updated_state["last_agent"] = self.agent_name
        
        return updated_state
    
    def analyze_custom_data(self, data: List[str]) -> Dict[str, Any]:
        """Analyze custom text data"""
        return self.sentiment_tool(data)