# example_usage.py
"""
Example usage of the Multi-Agent Business Intelligence System
Run this script after setting up ChromaDB servers and API keys
"""

import os
from multiagent_system import MultiAgentSystem
from config.api_keys import APIKeyManager

import dotenv
dotenv.load_dotenv()


def setup_environment():
    """Setup environment and check prerequisites"""
    print("🔧 Setting up environment...")
    
    # Check API key
    api_manager = APIKeyManager()
    gemini_key = api_manager.get_api_key("gemini")
    
    if not gemini_key:
        print("❌ Gemini API key not found!")
        print("Please set GEMINI_API_KEY environment variable or use APIKeyManager")
        return False
    
    print("✅ API key configured")
    return True


def run_examples():
    """Run example queries through the multi-agent system"""
    
    if not setup_environment():
        return
    
    print("🚀 Initializing Multi-Agent System...")
    
    try:
        # Initialize the system
        system = MultiAgentSystem(log_level="INFO")
        print("✅ System initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        print("Make sure ChromaDB servers are running:")
        print("- Reviews: chroma run --host localhost --port 8001 --path ./data/chroma_db")  
        print("- Business: chroma run --host localhost --port 8000 --path ./data/business_chroma_db")
        return
    
    # Example queries to demonstrate different agent capabilities
    example_queries = [
        {
            "query": "Find reviews for pizza restaurants",
            "description": "Tests search functionality for reviews"
        },
        {
            "query": "What do people say about Hernandez Restaurant with business ID Y3041zkdC8kT7o3bBFIBxQ?",
            "description": "Tests specific business search and review analysis"
        },
        {
            "query": "Show me highly rated Italian restaurants and analyze their customer sentiment",
            "description": "Tests business search + sentiment analysis workflow"
        },
        {
            "query": "What are the common themes in negative reviews?",
            "description": "Tests analysis and insight generation"
        }
    ]
    
    print(f"\n📋 Running {len(example_queries)} example queries...\n")
    
    for i, example in enumerate(example_queries, 1):
        query = example["query"]
        description = example["description"]
        
        print(f"{'='*80}")
        print(f"Example {i}: {description}")
        print(f"Query: {query}")
        print('='*80)
        
        try:
            # Process the query
            result = system.process_query(query)
            
            if result["success"]:
                # Display results
                print(f"\n💬 Final Response:")
                print("-" * 50)
                print(result["final_response"])
                
                # Show execution summary
                print(f"\n📊 Execution Summary:")
                print("-" * 50)
                
                search_results = result.get("search_results", {})
                analysis_results = result.get("analysis_results", {})
                
                # Search summary
                if search_results:
                    if "reviews" in search_results:
                        print(f"🔍 Found {len(search_results['reviews'])} reviews")
                    if "businesses" in search_results:
                        print(f"🏪 Found {len(search_results['businesses'])} businesses")
                
                # Analysis summary  
                if analysis_results:
                    if "sentiment_analysis" in analysis_results:
                        sentiment = analysis_results["sentiment_analysis"]
                        print(f"😊 Sentiment: {sentiment.get('positive_percentage', 0)}% positive, {sentiment.get('negative_percentage', 0)}% negative")
                    if "business_analysis" in analysis_results:
                        business = analysis_results["business_analysis"]
                        print(f"⭐ Average rating: {business.get('average_stars', 0)} stars")
                
                # Execution trace
                if result.get("execution_log"):
                    print(f"\n🔄 Agent Execution Log:")
                    for message in result["execution_log"]:
                        print(f"  • {message}")
                
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
        
        print(f"\n{'='*80}\n")
    
    print("✅ All examples completed!")


def interactive_mode():
    """Run in interactive mode for custom queries"""
    
    if not setup_environment():
        return
    
    print("🚀 Starting Interactive Multi-Agent System...")
    
    try:
        system = MultiAgentSystem(log_level="INFO")
        print("✅ System ready! Type your queries below (type 'quit' to exit):")
        
        while True:
            print("\n" + "-"*60)
            user_query = input("💭 Your question: ").strip()
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_query:
                continue
            
            print(f"\n🤔 Processing: {user_query}")
            print("⏳ Working...")
            
            try:
                result = system.process_query(user_query)
                
                if result["success"]:
                    print(f"\n💬 Response:")
                    print(result["final_response"])
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Exception: {e}")
                
    except Exception as e:
        print(f"❌ Failed to start system: {e}")


def main():
    """Main function with menu options"""
    
    print("🤖 Multi-Agent Business Intelligence System")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Run example queries")
        print("2. Interactive mode")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_examples()
        elif choice == "2":
            interactive_mode()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()