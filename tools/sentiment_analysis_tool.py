# tools/sentiment_analysis_tool.py
from transformers import pipeline
from typing import List, Dict, Any, Union
import json


class SentimentAnalysisTool:
    """Sentiment analysis tool for multi-agent system"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """Initialize sentiment analyzer
        
        Args:
            model_name: HuggingFace model for sentiment analysis
        """
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)
        print(f"✓ Sentiment analyzer initialized with model: {model_name}")
    
    def analyze_reviews(self, reviews: Union[List[str], str]) -> Dict[str, Any]:
        """Analyze sentiment of reviews
        
        Args:
            reviews: List of review texts or single review text
            
        Returns:
            Sentiment analysis results
        """
        # Handle single review
        if isinstance(reviews, str):
            reviews = [reviews]
        
        try:
            # Analyze sentiments
            sentiments = self.sentiment_analyzer(reviews)
            
            # Count sentiments
            sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0}
            total_confidence = {"POSITIVE": 0, "NEGATIVE": 0}
            
            for sentiment in sentiments:
                label = sentiment["label"]
                confidence = sentiment["score"]
                sentiment_counts[label] += 1
                total_confidence[label] += confidence
            
            total = len(sentiments)
            positive_pct = (sentiment_counts["POSITIVE"] / total) * 100 if total > 0 else 0
            negative_pct = (sentiment_counts["NEGATIVE"] / total) * 100 if total > 0 else 0
            
            # Calculate average confidence scores
            avg_positive_confidence = (
                total_confidence["POSITIVE"] / sentiment_counts["POSITIVE"] 
                if sentiment_counts["POSITIVE"] > 0 else 0
            )
            avg_negative_confidence = (
                total_confidence["NEGATIVE"] / sentiment_counts["NEGATIVE"] 
                if sentiment_counts["NEGATIVE"] > 0 else 0
            )
            
            return {
                "total_reviews": total,
                "positive_count": sentiment_counts["POSITIVE"],
                "negative_count": sentiment_counts["NEGATIVE"],
                "positive_percentage": round(positive_pct, 2),
                "negative_percentage": round(negative_pct, 2),
                "avg_positive_confidence": round(avg_positive_confidence, 3),
                "avg_negative_confidence": round(avg_negative_confidence, 3),
                "overall_sentiment": "POSITIVE" if positive_pct > negative_pct else "NEGATIVE",
                "sample_sentiments": sentiments[:5]  # Show first 5 for reference
            }
            
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    def __call__(self, input_data):
        """Make the tool callable with flexible input formats"""
        # Handle JSON string input
        if isinstance(input_data, str):
            if input_data.strip().startswith('[') or input_data.strip().startswith('{'):
                try:
                    parsed = json.loads(input_data)
                    if isinstance(parsed, list):
                        return self.analyze_reviews(parsed)
                    elif isinstance(parsed, dict) and "reviews" in parsed:
                        return self.analyze_reviews(parsed["reviews"])
                    else:
                        return {"error": "Invalid JSON format"}
                except json.JSONDecodeError:
                    # Treat as single review text
                    return self.analyze_reviews([input_data])
            else:
                # Single review text
                return self.analyze_reviews([input_data])
        
        # Handle list input
        elif isinstance(input_data, list):
            return self.analyze_reviews(input_data)
        
        # Handle dictionary input
        elif isinstance(input_data, dict):
            if "reviews" in input_data:
                return self.analyze_reviews(input_data["reviews"])
            else:
                return {"error": "Dictionary must contain 'reviews' key"}
        
        return {"error": f"Invalid input format: {type(input_data)}"}