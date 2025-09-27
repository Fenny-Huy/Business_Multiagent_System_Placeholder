#!/usr/bin/env python3
"""
Complete Multi-Agent System using LangGraph's Pre-built Functions

This script demonstrates a business intelligence multi-agent system using:
- create_react_agent for worker agents
- create_supervisor for orchestration
- LangGraph tools for external integrations

"""

import os
from typing import List, Dict, Any, Union
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing_extensions import TypedDict
import json

# Import official LangChain Google GenAI
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_GOOGLE_GENAI_AVAILABLE = True
    print("✓ langchain-google-genai package available")
except ImportError:
    LANGCHAIN_GOOGLE_GENAI_AVAILABLE = False
    print("❌ langchain-google-genai package not available")

# Import existing ChromaDB and sentiment analysis tools
try:
    from tools.business_search_tool import BusinessSearchTool
    from tools.review_search_tool import ReviewSearchTool
    from tools.sentiment_analysis_tool import SentimentAnalysisTool
    TOOLS_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Custom tools not available. Using mock implementations.")
    TOOLS_AVAILABLE = False

# Environment setup
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

# Initialize external tools if available
if TOOLS_AVAILABLE:
    try:
        business_tool = BusinessSearchTool()
        review_tool = ReviewSearchTool()
        sentiment_tool = SentimentAnalysisTool()
        print("✓ All external tools initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize external tools: {e}")
        TOOLS_AVAILABLE = False

# --- Step 1: Define LangGraph Tools ---

@tool
def review_search_tool(query: str, business_id: str = None, max_results: int = 5) -> str:
    """
    Searches a vector database for relevant customer reviews based on a query.
    Use this to understand customer opinions and experiences.
    
    Args:
        query: Search query to find relevant reviews
        business_id: Optional specific business ID to filter reviews
        max_results: Maximum number of reviews to return (default: 5)
    
    Returns:
        JSON string containing review results
    """
    print(f"🔍 TOOL CALL: review_search_tool(query='{query}', business_id='{business_id}', max_results={max_results})")
    
    if TOOLS_AVAILABLE:
        try:
            results = review_tool.search_reviews(query=query, k=max_results, business_id=business_id)
            return json.dumps({
                "tool": "review_search",
                "query": query,
                "business_id": business_id,
                "results_count": len(results),
                "reviews": results
            }, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Review search failed: {str(e)}"})
    else:
        # Mock implementation
        mock_reviews = [
            {
                "review_id": "mock_1",
                "text": "The pasta was divine, best I've had outside of Italy. Service was exceptional.",
                "stars": 5,
                "business_id": "luigi_123",
                "date": "2024-01-15",
                "score": 0.95
            },
            {
                "review_id": "mock_2", 
                "text": "Ambiance was romantic, but the service was incredibly slow on a Friday night.",
                "stars": 3,
                "business_id": "luigi_123",
                "date": "2024-01-10",
                "score": 0.85
            },
            {
                "review_id": "mock_3",
                "text": "A bit pricey, but the quality of the ingredients justifies the cost.",
                "stars": 4,
                "business_id": "luigi_123", 
                "date": "2024-01-08",
                "score": 0.80
            }
        ]
        
        if "italian" in query.lower() or "luigi" in query.lower():
            return json.dumps({
                "tool": "review_search",
                "query": query,
                "results_count": len(mock_reviews),
                "reviews": mock_reviews
            }, indent=2)
        else:
            return json.dumps({
                "tool": "review_search",
                "query": query,
                "results_count": 0,
                "reviews": []
            }, indent=2)

@tool 
def business_search_tool(business_name: str = None, query: str = None, max_results: int = 5) -> str:
    """
    Retrieves specific business details from a database including ratings, address, categories.
    Use this to get factual data about businesses.
    
    Args:
        business_name: Specific business name to search for
        query: General search query (category, location, etc.)
        max_results: Maximum number of businesses to return (default: 5)
    
    Returns:
        JSON string containing business results
    """
    search_term = business_name or query or ""
    print(f"🏢 TOOL CALL: business_search_tool(business_name='{business_name}', query='{query}', max_results={max_results})")
    
    if TOOLS_AVAILABLE:
        try:
            results = business_tool.search_businesses(query=search_term, k=max_results)
            return json.dumps({
                "tool": "business_search",
                "search_term": search_term,
                "results_count": len(results),
                "businesses": results
            }, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Business search failed: {str(e)}"})
    else:
        # Mock implementation
        mock_businesses = [
            {
                "business_id": "luigi_123",
                "name": "Luigi's Pizzeria", 
                "categories": "Italian, Pizza, Restaurants",
                "address": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "stars": 4.5,
                "review_count": 250,
                "description": "Authentic Italian restaurant with traditional recipes",
                "score": 0.92
            },
            {
                "business_id": "mario_456",
                "name": "Mario's Italian Kitchen",
                "categories": "Italian, Restaurants", 
                "address": "456 Oak Ave",
                "city": "San Francisco",
                "state": "CA",
                "stars": 4.2,
                "review_count": 180,
                "description": "Family-owned Italian restaurant specializing in pasta",
                "score": 0.88
            }
        ]
        
        if "luigi" in search_term.lower() or "italian" in search_term.lower():
            return json.dumps({
                "tool": "business_search",
                "search_term": search_term,
                "results_count": len(mock_businesses),
                "businesses": mock_businesses
            }, indent=2)
        else:
            return json.dumps({
                "tool": "business_search", 
                "search_term": search_term,
                "results_count": 0,
                "businesses": []
            }, indent=2)

@tool
def sentiment_analysis_tool(text_data: str) -> str:
    """
    Analyzes the sentiment of given text (reviews, comments, etc.).
    Use this to understand customer sentiment from review text.
    
    Args:
        text_data: Text to analyze, can be a single review or JSON array of reviews
    
    Returns:
        JSON string containing sentiment analysis results
    """
    print(f"💭 TOOL CALL: sentiment_analysis_tool(text='{text_data[:50]}...')")
    
    if TOOLS_AVAILABLE:
        try:
            # Try to parse as JSON first
            try:
                parsed_data = json.loads(text_data)
                if isinstance(parsed_data, list):
                    texts = parsed_data
                elif isinstance(parsed_data, dict) and "reviews" in parsed_data:
                    texts = [review.get("text", "") for review in parsed_data["reviews"]]
                else:
                    texts = [text_data]
            except json.JSONDecodeError:
                texts = [text_data]
            
            results = sentiment_tool.analyze_reviews(texts)
            return json.dumps({
                "tool": "sentiment_analysis",
                "analysis": results
            }, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Sentiment analysis failed: {str(e)}"})
    else:
        # Mock implementation
        positive_keywords = ["divine", "exceptional", "quality", "great", "excellent", "amazing"]
        negative_keywords = ["slow", "pricey", "terrible", "awful", "bad", "disappointing"]
        
        text_lower = text_data.lower()
        positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
        
        if positive_count > negative_count:
            overall_sentiment = "POSITIVE"
            confidence = 0.85
        elif negative_count > positive_count:
            overall_sentiment = "NEGATIVE" 
            confidence = 0.80
        else:
            overall_sentiment = "NEUTRAL"
            confidence = 0.60
            
        return json.dumps({
            "tool": "sentiment_analysis",
            "analysis": {
                "overall_sentiment": overall_sentiment,
                "confidence": confidence,
                "positive_indicators": positive_count,
                "negative_indicators": negative_count,
                "summary": f"Detected {overall_sentiment.lower()} sentiment with {confidence:.0%} confidence"
            }
        }, indent=2)

# --- Step 2: Initialize LLM ---

# No need for custom LLM wrapper - using official LangChain integration

class MockLLM:
    """Mock LLM for testing when real LLM is not available"""
    
    def invoke(self, messages):
        """Mock invoke method"""
        if isinstance(messages, list) and messages:
            last_message = messages[-1]
            content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            # Simple routing logic for supervisor
            if "supervisor" in content.lower():
                if "search completed: false" in content.lower():
                    return AIMessage(content="SEARCHAGENT")
                elif "analysis completed: false" in content.lower():
                    return AIMessage(content="ANALYSISAGENT")
                elif "response completed: false" in content.lower():
                    return AIMessage(content="RESPONSEAGENT")
                else:
                    return AIMessage(content="FINISH")
            
            # Mock agent responses
            return AIMessage(content=f"Mock response based on: {content[:50]}...")
        
        return AIMessage(content="Mock response")

def get_llm():
    """Initialize and return the LLM"""
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ Warning: GEMINI_API_KEY or GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key: export GEMINI_API_KEY='your_key_here'")
        print("Using mock LLM for demonstration...")
        return MockLLM()
    
    # Try official LangChain Google GenAI integration
    if LANGCHAIN_GOOGLE_GENAI_AVAILABLE:
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                temperature=0.1,
                max_retries=2,
                google_api_key=api_key
            )
            print("✓ Official LangChain Google GenAI LLM initialized successfully")
            return llm
        except Exception as e:
            print(f"❌ Failed to initialize ChatGoogleGenerativeAI: {e}")
    
    print("⚠️ No compatible LLM found. Using mock LLM for demonstration...")
    return MockLLM()

# --- Step 3: Create Worker Agents with create_react_agent ---

def create_agents(llm):
    """Create all worker agents using create_react_agent"""
    
    # SearchAgent - specializes in finding business data and reviews
    search_agent = create_react_agent(
        llm,
        tools=[review_search_tool, business_search_tool],
        name="SearchAgent",
        prompt="""You are a research specialist in a business intelligence system. 
Your primary role is to gather comprehensive information using your search tools.

INSTRUCTIONS:
1. Use business_search_tool to find business information (ratings, addresses, categories)
2. Use review_search_tool to find customer reviews and opinions
3. Always search broadly first, then narrow down if needed
4. Provide detailed, structured information from your searches
5. If searching for a specific business, try different variations of the name

Be thorough and methodical in your research."""
    )
    
    # AnalysisAgent - specializes in analyzing data, especially sentiment
    analysis_agent = create_react_agent(
        llm,
        tools=[sentiment_analysis_tool],
        name="AnalysisAgent", 
        prompt="""You are an analysis expert in a business intelligence system.
Your role is to analyze data provided by other agents, especially performing sentiment analysis.

INSTRUCTIONS:
1. Use sentiment_analysis_tool to analyze customer review text
2. Look for patterns in customer feedback
3. Provide clear summaries of sentiment trends
4. Identify key positive and negative themes
5. Quantify sentiment where possible (percentages, confidence scores)

Focus on extracting actionable insights from the data."""
    )
    
    # ResponseAgent - synthesizes final answers
    response_agent = create_react_agent(
        llm,
        tools=[], 
        name="ResponseAgent",
        prompt="""You are the final response synthesizer in a business intelligence system.
Your task is to create comprehensive, well-structured answers for users.

INSTRUCTIONS:
1. Synthesize information from search results and analysis
2. Structure your response clearly with headers and bullet points
3. Include specific data points (ratings, review counts, sentiment percentages)
4. Provide actionable insights and recommendations
5. Address the user's original question directly
6. Keep responses informative but concise

Create responses that are professional, helpful, and easy to understand."""
    )
    
    return search_agent, analysis_agent, response_agent

# --- Step 4: Define State and Create Manual Supervisor ---

class SupervisorState(TypedDict):
    """State for the supervisor workflow"""
    messages: List[HumanMessage | AIMessage | SystemMessage]
    next_agent: str
    search_completed: bool
    analysis_completed: bool
    response_completed: bool

def supervisor_node(state: SupervisorState, llm) -> SupervisorState:
    """Supervisor node that decides which agent to call next"""
    
    # Get the conversation so far
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    # Create supervisor prompt
    supervisor_prompt = f"""You are a supervisor managing a business intelligence multi-agent system.
Your team consists of three specialist agents that work together to answer user queries.

AVAILABLE AGENTS:
- SearchAgent: Finds business data and customer reviews using search tools
- AnalysisAgent: Analyzes data, especially sentiment analysis of reviews  
- ResponseAgent: Creates final comprehensive answers for users

CURRENT STATE:
- Search completed: {state.get('search_completed', False)}
- Analysis completed: {state.get('analysis_completed', False)}  
- Response completed: {state.get('response_completed', False)}

WORKFLOW STRATEGY:
1. Start with SearchAgent to gather relevant business and review data
2. If reviews are found, use AnalysisAgent to analyze sentiment and trends
3. Finally, use ResponseAgent to synthesize everything into a final answer
4. Only finish when you have sufficient information to provide a complete response

Based on the current state and conversation, decide which agent should act next.
Respond with ONLY the agent name: SearchAgent, AnalysisAgent, ResponseAgent, or FINISH.

Current conversation:
{last_message.content if last_message else "No messages yet"}
"""
    
    # Get supervisor decision using proper message format for ChatGoogleGenerativeAI
    try:
        # For ChatGoogleGenerativeAI, we need HumanMessage, not SystemMessage
        human_message = HumanMessage(content=supervisor_prompt)
        response = llm.invoke([human_message])
        decision = response.content.strip().upper()
    except Exception as e:
        print(f"⚠️ LLM error in supervisor: {e}")
        # Fallback logic based on state
        if not state.get('search_completed', False):
            decision = "SEARCHAGENT"
        elif not state.get('analysis_completed', False):
            decision = "ANALYSISAGENT"
        elif not state.get('response_completed', False):
            decision = "RESPONSEAGENT"
        else:
            decision = "FINISH"
    
    # Validate decision
    if decision not in ["SEARCHAGENT", "ANALYSISAGENT", "RESPONSEAGENT", "FINISH"]:
        decision = "SEARCHAGENT"  # Default fallback
    
    # Update state
    state["next_agent"] = decision
    state["messages"].append(AIMessage(content=f"Supervisor decision: {decision}"))
    
    return state

def route_to_agent(state: SupervisorState) -> str:
    """Route to the appropriate agent based on supervisor decision"""
    next_agent = state.get("next_agent", "FINISH")
    if next_agent == "SEARCHAGENT":
        return "search_agent"
    elif next_agent == "ANALYSISAGENT":
        return "analysis_agent"
    elif next_agent == "RESPONSEAGENT":
        return "response_agent"
    else:
        return END

def create_supervisor_system(llm):
    """Create the complete supervisor system with manual supervisor"""
    
    # Create worker agents
    search_agent, analysis_agent, response_agent = create_agents(llm)
    
    # Create supervisor workflow
    workflow = StateGraph(SupervisorState)
    
    # Add supervisor node
    workflow.add_node("supervisor", lambda state: supervisor_node(state, llm))
    
    # Add agent nodes
    def search_node(state: SupervisorState) -> SupervisorState:
        print("\n🔍 SearchAgent executing...")
        try:
            result = search_agent.invoke({"messages": state["messages"]})
            # Get new messages from the agent
            new_messages = result["messages"][len(state["messages"]):]
            state["messages"].extend(new_messages)
            state["search_completed"] = True
            print(f"✅ SearchAgent completed. Added {len(new_messages)} new messages.")
        except Exception as e:
            print(f"❌ SearchAgent error: {e}")
            state["messages"].append(AIMessage(content=f"SearchAgent encountered an error: {str(e)}"))
            state["search_completed"] = True
        return state
    
    def analysis_node(state: SupervisorState) -> SupervisorState:
        print("\n📊 AnalysisAgent executing...")
        try:
            # Create a specific prompt for analysis if we have search results
            current_messages = state["messages"].copy()
            
            # Add a prompt to help the analysis agent understand what to do
            analysis_prompt = HumanMessage(content="""
Based on the business search results above, please analyze the sentiment and trends in the customer reviews. 
Look for patterns in customer feedback and provide insights about the business reputation.
Use the sentiment_analysis_tool to analyze any review text you find.
""")
            current_messages.append(analysis_prompt)
            
            result = analysis_agent.invoke({"messages": current_messages})
            # Get new messages from the agent (excluding our added prompt)
            new_messages = result["messages"][len(current_messages):]
            state["messages"].extend(new_messages)
            state["analysis_completed"] = True
            print(f"✅ AnalysisAgent completed. Added {len(new_messages)} new messages.")
        except Exception as e:
            print(f"❌ AnalysisAgent error: {e}")
            state["messages"].append(AIMessage(content=f"AnalysisAgent encountered an error: {str(e)}"))
            state["analysis_completed"] = True
        return state
    
    def response_node(state: SupervisorState) -> SupervisorState:
        print("\n📝 ResponseAgent executing...")
        try:
            # Create a specific prompt for final response synthesis
            current_messages = state["messages"].copy()
            
            response_prompt = HumanMessage(content="""
Please create a comprehensive final answer based on all the search results and analysis above.
Synthesize the business information, customer reviews, and any sentiment analysis into a clear, 
helpful response for the user. Structure your response with clear sections and bullet points.
""")
            current_messages.append(response_prompt)
            
            result = response_agent.invoke({"messages": current_messages})
            # Get new messages from the agent (excluding our added prompt)
            new_messages = result["messages"][len(current_messages):]
            state["messages"].extend(new_messages)
            state["response_completed"] = True
            print(f"✅ ResponseAgent completed. Added {len(new_messages)} new messages.")
        except Exception as e:
            print(f"❌ ResponseAgent error: {e}")
            state["messages"].append(AIMessage(content=f"ResponseAgent encountered an error: {str(e)}"))
            state["response_completed"] = True
        return state
    
    workflow.add_node("search_agent", search_node)
    workflow.add_node("analysis_agent", analysis_node)
    workflow.add_node("response_agent", response_node)
    
    # Add routing logic
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "search_agent": "search_agent",
            "analysis_agent": "analysis_agent",
            "response_agent": "response_agent",
            END: END
        }
    )
    
    # After each agent, go back to supervisor
    workflow.add_edge("search_agent", "supervisor")
    workflow.add_edge("analysis_agent", "supervisor") 
    workflow.add_edge("response_agent", "supervisor")
    
    # Set entry point
    workflow.set_entry_point("supervisor")
    
    return workflow.compile()

# --- Step 5: Main Execution Functions ---

def run_query_with_streaming(supervisor, query: str):
    """Run a query with streaming output to see the workflow"""
    print(f"\n{'='*60}")
    print(f"🎯 QUERY: {query}")
    print('='*60)
    
    # Prepare initial state
    initial_state = SupervisorState(
        messages=[HumanMessage(content=query)],
        next_agent="",
        search_completed=False,
        analysis_completed=False,
        response_completed=False
    )
    
    print("🔄 Starting workflow with streaming...\n")
    
    # Stream the execution to see each step
    step_count = 0
    for event in supervisor.stream(initial_state, stream_mode="values"):
        step_count += 1
        messages = event.get("messages", [])
        
        if messages and len(messages) > step_count:
            last_message = messages[-1]
            
            print(f"📋 STEP {step_count}:")
            
            # Handle different message types
            if hasattr(last_message, 'content'):
                content = last_message.content
                if isinstance(content, str):
                    print(f"Response: {content[:200]}{'...' if len(content) > 200 else ''}")
                elif isinstance(content, list):
                    for item in content:
                        if hasattr(item, 'get') and item.get('type') == 'tool_use':
                            print(f"Tool Call: {item.get('name', 'unknown')}({item.get('input', {})})")
                        else:
                            print(f"Content: {str(item)[:100]}{'...' if len(str(item)) > 100 else ''}")
            
            print("-" * 40)
    
    # Get final result
    print("\n🏁 Getting final result...")
    final_result = supervisor.invoke(initial_state)
    final_messages = final_result["messages"]
    
    # Find the ResponseAgent's comprehensive answer (not supervisor decisions or agent errors)
    for message in reversed(final_messages):
        if (hasattr(message, 'content') and 
            not message.content.startswith("Supervisor decision:") and
            not message.content.startswith("I am sorry, I do not have access") and
            len(message.content.strip()) > 50):  # Look for substantial responses
            return message.content
    
    # Fallback: look for any meaningful non-supervisor message
    for message in reversed(final_messages):
        if (hasattr(message, 'content') and 
            not message.content.startswith("Supervisor decision:") and
            len(message.content.strip()) > 10):
            return message.content
    
    return "No final response generated"

def run_example_queries(supervisor):
    """Run a set of example queries to demonstrate the system"""
    
    example_queries = [
        "What do people think about Luigi's Pizzeria?",
        "Find reviews for Italian restaurants and analyze the sentiment",
        "Show me information about businesses with good ratings in the restaurant category"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n🚀 EXAMPLE {i}/{len(example_queries)}")
        
        try:
            result = run_query_with_streaming(supervisor, query)
            
            print(f"\n✅ FINAL ANSWER:")
            print(f"{result}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        if i < len(example_queries):
            input(f"\n⏸️  Press Enter to continue to example {i+1}...")

def interactive_mode(supervisor):
    """Run interactive chat mode"""
    print(f"\n{'='*60}")
    print("💬 INTERACTIVE MODE")
    print("Type your questions about businesses and reviews.")
    print("Type 'quit', 'exit', or 'bye' to end.")
    print('='*60)
    
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', '']:
                print("👋 Goodbye!")
                break
            
            result = run_query_with_streaming(supervisor, user_input)
            print(f"\n🤖 Assistant: {result}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# --- Step 6: Main Function ---

def main():
    """Main execution function"""
    print("🤖 LangGraph Multi-Agent Business Intelligence System")
    print("="*60)
    print("Using create_react_agent and create_supervisor")
    print("="*60)
    
    # Initialize LLM
    llm = get_llm()
    if not llm:
        print("❌ Cannot proceed without LLM. Please check your Google API key.")
        return
    
    # Create supervisor system
    print("\n🔧 Creating multi-agent system...")
    try:
        supervisor = create_supervisor_system(llm)
        print("✅ Multi-agent system created successfully!")
    except Exception as e:
        print(f"❌ Failed to create system: {e}")
        return
    
    # Choose mode
    print(f"\n🎯 Choose mode:")
    print("1. Run example queries")
    print("2. Interactive chat mode")
    print("3. Single query test")
    
    choice = input("\nEnter choice (1/2/3, default=1): ").strip() or "1"
    
    if choice == "1":
        run_example_queries(supervisor)
    elif choice == "2":
        interactive_mode(supervisor)
    elif choice == "3":
        query = input("\n🧑 Enter your query: ").strip()
        if query:
            result = run_query_with_streaming(supervisor, query)
            print(f"\n✅ FINAL ANSWER:\n{result}")
    else:
        print("Invalid choice. Running example queries...")
        run_example_queries(supervisor)

if __name__ == "__main__":
    # Check for core LangGraph package
    try:
        import langgraph
        print("✓ LangGraph package available")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install: pip install -U langgraph")
        exit(1)
    
    # Check for LangChain Google GenAI
    if not LANGCHAIN_GOOGLE_GENAI_AVAILABLE:
        print("⚠️ LangChain Google GenAI not available. Install with: pip install langchain-google-genai")
        print("Will use mock LLM for demonstration...")
    
    main()
