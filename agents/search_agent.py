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
                name="get_business_id",
                description="Get the business_id for a given business name (exact match). Input should be a string (business name).",
                func=lambda name: (
                    print(f"[TOOL CALLED] get_business_id with input: {name}") or
                    self.business_search_tool.get_business_id(name)
            )
            ),
            Tool(
                name="business_fuzzy_search",
                description="Fuzzy search for businesses by name. Input can be a string (query) or a dict with 'query' and optional 'top_n'. The input query is used to search the business record with the business name most similar to the input query. Returns a list of similar business records.",
                func=lambda input: (
                    print(f"[TOOL CALLED] fuzzy_search with input: {input}") or
                    (self.business_search_tool.fuzzy_search(input) if isinstance(input, str)
                    else self.business_search_tool.fuzzy_search(input.get('query', ''), top_n=input.get('top_n', 5)))
                )
            ),
            Tool(
                name="search_businesses",
                description="Semantic search for businesses. Return a business record. Input should be a string (query/description) or a dict with 'query' and optional 'k'. Input query represent any information about the business",
                func=lambda input: (
                    print(f"[TOOL CALLED] search_businesses with input: {input}") or
                    (self.business_search_tool.search_businesses(input, k=5) if isinstance(input, str)
                    else self.business_search_tool.search_businesses(input.get("query", ""), k=input.get("k", 5)))
                )

            ),
            Tool(
                name="get_business_info",
                description="Get general info for a business_id. Input should be a string (business_id).",
                func=lambda input: (
                    print(f"[TOOL CALLED] get_business_info with input: {input}") or
                    self.business_search_tool.get_business_info(
                        input if isinstance(input, str) else input.get("business_id", "")
                    )
                )
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

GUIDELINES:
- Use the tools to gather relevant information about businesses and reviews
- Process the user's query thoroughly and systematically
- Preserve the exact structure and format of each tool's output
- Do not modify, simplify, or restructure the tool outputs
- If tools return no data or errors, include this information as is
- Document each tool you use and the reason you used it

REASONING APPROACH:
1. Analyze the user's query to understand what information is needed
2. Select appropriate tools to retrieve the necessary data
3. Execute the tools in a logical sequence
4. Compile the results in a structured format that preserves all information

REQUIRED OUTPUT FORMAT:
Your Final Answer MUST be structured as a valid JSON object with the following format:

```json
{{
  "note": "Brief 1-2 sentence summary of what you found",
  "result": {{
    "tool_outputs": {{
      "tool_name_1": [exact raw output from the first tool you used],
      "tool_name_2": [exact raw output from the second tool you used],
      ...
    }},
    "query_processed": "The query you processed",
    "reasoning_summary": "Brief explanation of your search strategy"
  }}
}}
```

Include the EXACT raw outputs from each tool under the appropriate tool name.
Do NOT reformat, restructure, or modify the tool outputs in any way.

REQUIRED EXECUTION FORMAT:
Follow this exact format when executing your search:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: ```json
{
  "note": "Brief summary of findings",
  "result": {
    "tool_outputs": {
      "tool_name_1": [exact output from tool 1],
      "tool_name_2": [exact output from tool 2]
    },
    "query_processed": "Query I processed",
    "reasoning_summary": "How I approached this search"
  }
}
```

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
        task = f"""Find relevant information about: "{user_query}"
        
Please search for business information related to this query. Use the appropriate search tools to gather comprehensive information:
1. If the query is for a specific business by name, try to identify the business_id
2. If the query is more general, search for relevant businesses
3. Gather detailed information about any businesses you find"""
        
        try:
            # Execute the ReAct agent
            result = self.agent_executor.invoke({
                "input": task
            })
            
            # Extract the response
            agent_output = result.get("output", "")
            
            # Parse the structured output according to the new format
            note, structured_result = self._parse_structured_output(agent_output)
            
            # Update state with both note and detailed results
            updated_state = state.copy()
            updated_state["search_agent_note"] = note
            updated_state["search_agent_result"] = structured_result
            updated_state["last_agent"] = self.agent_name
            
            # Maintain backward compatibility with legacy search_results field
            search_results = structured_result.get("search_results", {
                "businesses": [],
                "reviews": []
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
        
        # Extract JSON from the agent output
        json_match = re.search(r'```json\s*(.*?)\s*```', agent_output, re.DOTALL)
        
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                
                # Extract note and result from the JSON structure
                note = json_data.get("note", "SearchAgent completed search task")
                result = json_data.get("result", {})
                
                # Store the full output for reference
                result["full_agent_output"] = agent_output
                
                # Create a backward compatible structure for search_results
                search_results = {}
                
                # Extract data from tool outputs for backward compatibility
                tool_outputs = result.get("tool_outputs", {})
                
                # Extract businesses and reviews from tool outputs
                businesses = []
                reviews = []
                
                # Look for business data in tool outputs
                for tool_name, output in tool_outputs.items():
                    # Get business data from business search tools
                    if "business" in tool_name.lower() and isinstance(output, list):
                        businesses.extend(output)
                    elif isinstance(output, dict) and "businesses" in output:
                        businesses.extend(output["businesses"])
                    
                    # Get review data from review search tools
                    if "review" in tool_name.lower() and isinstance(output, list):
                        reviews.extend(output)
                    elif isinstance(output, dict) and "reviews" in output:
                        reviews.extend(output["reviews"])
                
                # Add to structured result for backward compatibility
                search_results["businesses"] = businesses
                search_results["reviews"] = reviews
                result["search_results"] = search_results
                
                # Debug logging
                print(f"✅ Successfully parsed structured output")
                print(f"  - Note: {note[:50]}...")
                print(f"  - Tool outputs found: {list(tool_outputs.keys())}")
                print(f"  - Businesses found: {len(businesses)}")
                print(f"  - Reviews found: {len(reviews)}")
                
                return note, result
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse JSON from agent output: {e}")
                print(f"⚠️ JSON snippet that failed parsing: {json_match.group(1)[:100]}...")
                return f"SearchAgent encountered error: {e}", {"error": str(e), "full_output": agent_output}
        else:
            # Fallback if no JSON found - this shouldn't happen if agent follows instructions
            print("⚠️ No JSON structure found in agent output")
            print(f"⚠️ Agent output: {agent_output[:200]}...")
            return "SearchAgent completed task (no structured output)", {"full_output": agent_output}
        