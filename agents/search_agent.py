# agents/search_agent.py
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from llm_wrapper import get_llm
from tools.business_search_tool import BusinessSearchTool
from tools.review_search_tool import ReviewSearchTool
import json
import os

import dotenv
dotenv.load_dotenv()


class SearchAgent:
    """Agent specialized in searching and retrieving information from databases using create_react_agent"""
    
    def __init__(self, chroma_host: str = None):
        """Initialize search agent
        
        Args:
            chroma_host: ChromaDB server host (defaults to CHROMA_HOST env var or "localhost")
        """
        self.agent_name = "SearchAgent"
        
        # Use environment variable if no host is provided
        if chroma_host is None:
            chroma_host = os.getenv("CHROMA_HOST", "localhost")
            print(f"✓ Using ChromaDB host from env: {chroma_host}")
        
        # Initialize external tools
        self.review_search_tool = ReviewSearchTool(host=chroma_host, port=8001)
        self.business_search_tool = BusinessSearchTool(host=chroma_host, port=8000)
        
        # Create LangChain tools
        self.tools = [
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
        
        # Initialize LLM
        self.llm = get_llm()
        
        # Create ReAct agent
        self.prompt = self._create_react_prompt()
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
        
        print(f"✓ SearchAgent initialized with ReAct pattern")

    def _create_react_prompt(self) -> PromptTemplate:
        """Create the ReAct prompt template for SearchAgent"""
        return PromptTemplate.from_template("""
You are a business review search agent with access to a vector database of reviews and business information.
Your mission is to find relevant reviews and business data to help answer user queries.

TOOLS:
------
You have access to the following tools:

{tools}

TOOL INPUT FORMATS:
- search_reviews: Search for relevant reviews based on semantic similarity. 
  Input: string (query) or dict with 'query' (string), optional 'k' (int), optional 'business_id' (string)
  Example: "Find reviews about pizza" or {{"query": "pizza", "k": 5}}
  
- search_businesses: Search for businesses by name, category, location, or description.
  Input: string (query) or dict with 'query' (string) and optional 'k' (int)
  Example: "vegan restaurant" or {{"query": "vegan restaurant", "k": 5}}

STRICT GUIDELINES:
- Only use actual tool outputs in your reasoning - never invent data
- If tools return no data, explicitly state information is unavailable
- Always include complete tool results in your Final Answer
- Use proper JSON format when providing dict inputs to tools

REASONING PATTERN:
1. Analyze what type of information is needed from the question
2. Use search_businesses to find basic business information first
3. Use search_reviews to find customer feedback and opinions
4. Provide comprehensive results with both business data and review insights

OUTPUT FORMAT:
Your Final Answer must include structured sections for easy parsing:

SEARCH_NOTE: [Brief 1-2 sentence summary for supervisor]

SEARCH_RESULT:
```json
{{
  "businesses": [list of business objects from your search],
  "reviews": [list of review objects from your search],
  "summary": "Brief description of search results",
  "query_processed": "The query you processed",
  "total_businesses": number,
  "total_reviews": number
}}
```

DETAILED_RESPONSE: [Comprehensive findings in readable format]

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: [Use the structured format above with SEARCH_NOTE, SEARCH_RESULT JSON, and DETAILED_RESPONSE]

Begin!

Question: {input}
Thought: {agent_scratchpad}""")

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
        """Process search requests using the ReAct agent"""
        user_query = state.get("user_query", "")
        
        # Create the task description
        task = f"""Find relevant information for: "{user_query}"
        
Please search for businesses and reviews related to this query. Use both search_businesses and search_reviews tools to gather comprehensive information."""
        
        try:
            # Execute the ReAct agent
            result = self.agent_executor.invoke({
                "input": task
            })
            
            # Extract the response
            agent_output = result.get("output", "")
            
            # Parse the structured output
            note, structured_result = self._parse_structured_output(agent_output)
            
            # Update state with both note and detailed results
            updated_state = state.copy()
            updated_state["search_agent_note"] = note
            updated_state["search_agent_result"] = structured_result
            updated_state["last_agent"] = self.agent_name
            
            # Maintain backward compatibility with legacy search_results field
            search_results = structured_result.get("search_data", {
                "businesses": structured_result.get("businesses", []),
                "reviews": structured_result.get("reviews", [])
            })
            updated_state["search_results"] = search_results
            
            # Add summary to messages
            messages = updated_state.get("messages", [])
            messages.append(note)
            updated_state["messages"] = messages
            
            return updated_state
            
        except Exception as e:
            error_msg = f"Error in {self.agent_name}: {str(e)}"
            print(f"❌ {error_msg}")
            
            updated_state = state.copy()
            updated_state["search_agent_note"] = f"SearchAgent encountered an error: {str(e)}"
            updated_state["search_agent_result"] = {"error": str(e)}
            updated_state["search_results"] = {"businesses": [], "reviews": [], "error": str(e)}
            updated_state["last_agent"] = self.agent_name
            
            return updated_state

    def _parse_structured_output(self, agent_output: str) -> tuple[str, Dict[str, Any]]:
        """Parse the structured output from the agent"""
        import re
        
        # Extract the note
        note_match = re.search(r'SEARCH_NOTE:\s*(.*?)(?=\n\n|SEARCH_RESULT:)', agent_output, re.DOTALL)
        note = note_match.group(1).strip() if note_match else f"SearchAgent completed search task"
        
        # Extract the JSON result
        json_match = re.search(r'SEARCH_RESULT:\s*```json\s*(.*?)\s*```', agent_output, re.DOTALL)
        
        structured_result = {"full_output": agent_output}
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                structured_result["search_data"] = json_data
                # Also maintain backward compatibility
                structured_result["businesses"] = json_data.get("businesses", [])
                structured_result["reviews"] = json_data.get("reviews", [])
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse JSON from agent output: {e}")
                structured_result["parse_error"] = str(e)
        
        # Extract detailed response
        detailed_match = re.search(r'DETAILED_RESPONSE:\s*(.*)', agent_output, re.DOTALL)
        if detailed_match:
            structured_result["detailed_response"] = detailed_match.group(1).strip()
        
        return note, structured_result