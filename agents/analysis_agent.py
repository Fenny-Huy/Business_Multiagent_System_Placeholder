# agents/analysis_agent.py
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from llm_wrapper import get_llm
import json


class AnalysisAgent:
    """Agent specialized in sentiment analysis and data insights using create_react_agent"""
    

    def __init__(self):
        """Initialize analysis agent with ReAct pattern and custom tools for business info and reviews."""
        self.agent_name = "AnalysisAgent"

        # Placeholders for extracted data (set in process)
        self.business_info_dict = None
        self.reviews_dict = None

        # Create LangChain tools (will be updated in process)
        self.tools = [
            Tool(
                name="get_business_field",
                description="Get a specific field value for a business ID from get_business_info. Input: '<business_id>|<field>'",
                func=self._get_business_field
            ),
            Tool(
                name="get_reviews_for_business",
                description="Get all reviews for a business ID from search_reviews. Input: '<business_id>'",
                func=self._get_reviews_for_business
            ),
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
            max_iterations=10
        )

        print(f"✓ AnalysisAgent initialized with ReAct pattern and custom tools")

    def _create_react_prompt(self) -> PromptTemplate:
        """Create the ReAct prompt template for AnalysisAgent (single analysis_results output)."""
        return PromptTemplate.from_template("""
You are an analysis expert in a business intelligence system.
Your role is to analyze data provided by other agents and extract actionable insights.

TOOLS:
------
You have access to the following tools:

{tools}

ANALYSIS GUIDELINES:
1. Use the tools to retrieve only the necessary business info fields or reviews for your analysis. Do not request the entire dataset at once.
2. Provide quantified metrics and specific insights.
3. Always output your final answer as a single JSON object.

OUTPUT FORMAT:
Your Final Answer must be a single JSON object, for example:
```json
{{
    "key_insights": ["..."],
    "summary": "..."
}}
```

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer:
```json
{{
    "key_insights": ["..."],
    "summary": "..."
}}
```

Begin!

Question: {input}
Thought: {agent_scratchpad}""")

    def get_system_prompt(self) -> str:
        """Return the system prompt for the analysis agent"""
        return """You are an Analysis Agent specialized in data analysis and insight extraction.

Your primary responsibilities:
1. Extract meaningful insights from data patterns
2. Identify key themes and patterns in customer feedback

Available tools:
- get_business_field: Get a specific field value for a business ID
- get_reviews_for_business: Get all reviews for a business ID

When analyzing:
- Look for patterns and trends in the data
- Provide actionable insights based on your analysis
- Be objective and evidence-based in your assessments

Always provide clear, structured, and insightful analysis."""
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process analysis requests using the ReAct agent, with pre-extracted business info and reviews and custom tools. Only sets analysis_results."""
        results = state.get("search_agent_result", {})
        search_results = results.get("tool_outputs", {})
        user_query = state.get("user_query", "")

        print(f"search_results: {search_results}")

        # --- Pre-extract get_business_info and search_reviews as dicts ---
        def _unwrap_tool(tool_key):
            value = search_results.get(tool_key)
            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
                return value[0]
            return value if isinstance(value, dict) else None

        self.business_info_dict = _unwrap_tool("get_business_info")
        self.reviews_dict = _unwrap_tool("search_reviews")

        # Compose available data summary for the prompt
        available_tools = []
        if self.business_info_dict:
            available_tools.append("get_business_info")
        if self.reviews_dict:
            available_tools.append("search_reviews")
        print (f"Available tools: {available_tools}")
        business_ids = list(self.business_info_dict.keys()) if self.business_info_dict else []
        review_business_ids = list(self.reviews_dict.keys()) if self.reviews_dict else []
        print (f"business_ids: {business_ids}, review_business_ids: {review_business_ids}")
        data_summary = f"Available data: {', '.join(available_tools) if available_tools else 'None'}\n"
        if business_ids:
            data_summary += f"Business IDs: {business_ids}\n"
            # Add available fields for each business id
            for bid in business_ids:
                info = self.business_info_dict.get(bid)
                if isinstance(info, dict):
                    fields = list(info.keys())
                    print (f"Fields for {bid}: {fields}")
                    data_summary += f"Fields for {bid}: {fields}\n"
            
        if review_business_ids:
            data_summary += f"Review Business IDs: {review_business_ids}\n"

        # Create the task description with available data summary
        task = f"""Analyze data related to: "{user_query}"

{data_summary}
Please use the available tools to retrieve only the necessary business info fields or reviews for your analysis. Do not request the entire dataset at once. Use the tools to:
- Get a specific field for a business
- Get reviews for a business
"""

        try:
            # Execute the ReAct agent
            result = self.agent_executor.invoke({
                "input": task
            })

            # Extract the response
            agent_output = result.get("output", "")

            # Parse the structured output (expecting a single JSON block as final answer)
            analysis_results = self._parse_analysis_results(agent_output)
            print(f"analysis_results: {analysis_results}")

            # Update state with only analysis_results
            updated_state = state.copy()
            updated_state["analysis_results"] = analysis_results
            updated_state["last_agent"] = self.agent_name

            # Add summary to messages
            messages = updated_state.get("messages", [])
            messages.append("Analysis complete.")
            updated_state["messages"] = messages

            return updated_state

        except Exception as e:
            error_msg = f"Error in {self.agent_name}: {str(e)}"
            print(f"❌ {error_msg}")

            updated_state = state.copy()
            updated_state["analysis_results"] = {"error": str(e)}
            updated_state["last_agent"] = self.agent_name

            return updated_state

    # --- Custom tool implementations ---
    def _get_business_field(self, input_str):
        # Input format: '<business_id>|<field>'
        if not self.business_info_dict:
            return None
        try:
            business_id, field = input_str.split("|", 1)
            info = self.business_info_dict.get(business_id)
            if isinstance(info, dict):
                return info.get(field)
        except Exception:
            return None
        return None

    def _get_reviews_for_business(self, business_id):
        if self.reviews_dict and isinstance(self.reviews_dict, dict):
            return self.reviews_dict.get(business_id, [])
        return []

    def _parse_analysis_results(self, agent_output: str) -> dict:
        """Parse the final JSON object from the agent output (as per prompt)."""
        import re
        # Look for the last JSON code block in the output
        matches = list(re.finditer(r'```json\s*(.*?)\s*```', agent_output, re.DOTALL))
        if matches:
            last_json = matches[-1].group(1)
            try:
                return json.loads(last_json)
            except Exception as e:
                print(f"⚠️ Failed to parse JSON from agent output: {e}")
                return {"parse_error": str(e), "raw_output": agent_output}
        return {"parse_error": "No JSON found in output", "raw_output": agent_output}
