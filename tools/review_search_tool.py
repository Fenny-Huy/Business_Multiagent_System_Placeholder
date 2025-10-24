# tools/review_search_tool.py
import chromadb
import json
from typing import List, Dict, Any, Optional
import os

import dotenv
dotenv.load_dotenv()

class ReviewSearchTool:
    """ChromaDB-based review search tool for multi-agent system"""
    
    def __init__(self, host: str = None, port: int = 8001):
        """Initialize ChromaDB connection
        
        Args:
            host: ChromaDB server host (defaults to CHROMA_HOST env var or "localhost")
            port: ChromaDB server port
        """
        if host is None:
            host = os.getenv("CHROMA_HOST", "localhost")
        
        self.client = chromadb.HttpClient(host=host, port=port)
        try:
            self.collection = self.client.get_collection("yelp_reviews")
            print(f"✓ Connected to ChromaDB collection: yelp_reviews")
        except Exception as e:
            print(f"⚠️ Warning: Could not connect to ChromaDB: {e}")
            self.collection = None
    
    def search_reviews(self, query: str, k: int = 5, business_id: Optional[str] = None) -> Dict[str, list]:
        """Search for relevant reviews and group them by business_id.
        Returns a dict: {business_id: [review_dict, ...], ...}
        """
        if not self.collection:
            return {"error": "ChromaDB collection not available"}
        try:
            # Set up filter for business_id if provided
            where_filter = {"business_id": business_id} if business_id else None
            # Query the collection
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=where_filter
            )
            # Group reviews by business_id
            grouped = {}
            if results and 'ids' in results and len(results['ids']) > 0:
                for i in range(len(results['ids'][0])):
                    metadata = results['metadatas'][0][i] if 'metadatas' in results else {}
                    text = results['documents'][0][i] if 'documents' in results else ""
                    distance = results['distances'][0][i] if 'distances' in results else 0
                    similarity_score = 1.0 - distance
                    bid = metadata.get("business_id", "")
                    review = {
                        "text": text,
                        "stars": metadata.get("stars", ""),
                        "date": metadata.get("date", ""),
                        "score": float(similarity_score)
                    }
                    if bid not in grouped:
                        grouped[bid] = []
                    grouped[bid].append(review)
            return grouped
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}
    
    def __call__(self, input_data):
        """Make the tool callable with flexible input formats"""
        # Handle JSON string input
        if isinstance(input_data, str):
            if input_data.strip().startswith('{'):
                try:
                    parsed = json.loads(input_data)
                    return self.search_reviews(
                        query=parsed.get("query", ""),
                        k=parsed.get("k", 5),
                        business_id=parsed.get("business_id")
                    )
                except json.JSONDecodeError:
                    # Treat as plain string query
                    return self.search_reviews(query=input_data, k=5)
            else:
                return self.search_reviews(query=input_data, k=5)
        
        # Handle dictionary input
        elif isinstance(input_data, dict):
            return self.search_reviews(
                query=input_data.get("query", ""),
                k=input_data.get("k", 5),
                business_id=input_data.get("business_id")
            )
        
        return [{"error": f"Invalid input format: {type(input_data)}"}]