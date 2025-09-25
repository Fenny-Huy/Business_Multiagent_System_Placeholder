# tools/business_search_tool.py
import chromadb
import json
from typing import List, Dict, Any, Optional
import os

import dotenv
dotenv.load_dotenv()
class BusinessSearchTool:
    """ChromaDB-based business search tool for multi-agent system"""
    
    def __init__(self, host: str = None, port: int = 8000):
        """Initialize ChromaDB connection
        
        Args:
            host: ChromaDB server host (defaults to CHROMA_HOST env var or "localhost")
            port: ChromaDB server port
        """
        if host is None:
            host = os.getenv("CHROMA_HOST", "localhost")
        
        self.client = chromadb.HttpClient(host=host, port=port)
        try:
            self.collection = self.client.get_collection("yelp_businesses")
            print(f"✓ Connected to ChromaDB collection: yelp_businesses")
        except Exception as e:
            print(f"⚠️ Warning: Could not connect to ChromaDB: {e}")
            self.collection = None
    
    def search_businesses(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant businesses
        
        Args:
            query: Search query (business name, category, location, etc.)
            k: Number of results to return
            
        Returns:
            List of business documents with metadata
        """
        if not self.collection:
            return [{"error": "ChromaDB collection not available"}]
        
        try:
            # Query the collection
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            # Process results
            processed_results = []
            if results and 'ids' in results and len(results['ids']) > 0:
                for i in range(len(results['ids'][0])):
                    metadata = results['metadatas'][0][i] if 'metadatas' in results else {}
                    text = results['documents'][0][i] if 'documents' in results else ""
                    distance = results['distances'][0][i] if 'distances' in results else 0
                    
                    # Convert distance to similarity score
                    similarity_score = 1.0 - distance
                    
                    processed_results.append({
                        "business_id": metadata.get("business_id", ""),
                        "name": metadata.get("name", ""),
                        "categories": metadata.get("categories", ""),
                        "address": metadata.get("address", ""),
                        "city": metadata.get("city", ""),
                        "state": metadata.get("state", ""),
                        "stars": metadata.get("stars", ""),
                        "review_count": metadata.get("review_count", ""),
                        "description": text,
                        "score": float(similarity_score)
                    })
            
            return processed_results
            
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    def get_business_by_id(self, business_id: str) -> Dict[str, Any]:
        """Get specific business by ID
        
        Args:
            business_id: Business ID to retrieve
            
        Returns:
            Business data or error
        """
        if not self.collection:
            return {"error": "ChromaDB collection not available"}
        
        try:
            # Query with business_id filter
            results = self.collection.query(
                query_texts=[""],
                n_results=1,
                where={"business_id": business_id}
            )
            
            if results and 'ids' in results and len(results['ids'][0]) > 0:
                metadata = results['metadatas'][0][0]
                text = results['documents'][0][0]
                
                return {
                    "business_id": metadata.get("business_id", ""),
                    "name": metadata.get("name", ""),
                    "categories": metadata.get("categories", ""),
                    "address": metadata.get("address", ""),
                    "city": metadata.get("city", ""),
                    "state": metadata.get("state", ""),
                    "stars": metadata.get("stars", ""),
                    "review_count": metadata.get("review_count", ""),
                    "description": text
                }
            
            return {"error": f"Business not found: {business_id}"}
            
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}
    
    def __call__(self, input_data):
        """Make the tool callable with flexible input formats"""
        # Handle JSON string input
        if isinstance(input_data, str):
            if input_data.strip().startswith('{'):
                try:
                    parsed = json.loads(input_data)
                    if "business_id" in parsed:
                        return self.get_business_by_id(parsed["business_id"])
                    else:
                        return self.search_businesses(
                            query=parsed.get("query", ""),
                            k=parsed.get("k", 5)
                        )
                except json.JSONDecodeError:
                    # Treat as plain string query
                    return self.search_businesses(query=input_data, k=5)
            else:
                return self.search_businesses(query=input_data, k=5)
        
        # Handle dictionary input
        elif isinstance(input_data, dict):
            if "business_id" in input_data:
                return self.get_business_by_id(input_data["business_id"])
            else:
                return self.search_businesses(
                    query=input_data.get("query", ""),
                    k=input_data.get("k", 5)
                )
        
        return {"error": f"Invalid input format: {type(input_data)}"}