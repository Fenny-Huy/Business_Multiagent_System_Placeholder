# agents/analysis_agent.py
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from llm_wrapper import get_llm
from tools.sentiment_analysis_tool import SentimentAnalysisTool
import json


class AnalysisAgent:
    """Agent specialized in sentiment analysis and data insights using create_react_agent"""
    
    def __init__(self):
        """Initialize analysis agent with ReAct pattern"""
        self.agent_name = "AnalysisAgent"
        
        # Initialize external tools
        self.sentiment_tool = SentimentAnalysisTool()
        
        # Create LangChain tools
        self.tools = [
            Tool(
                name="analyze_sentiment",
                description="Analyze sentiment in customer reviews and feedback. Input can be a string, list of strings, or text separated by '|'.",
                func=self.sentiment_tool
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
        
        print(f"✓ AnalysisAgent initialized with ReAct pattern")

    def _create_react_prompt(self) -> PromptTemplate:
        """Create the ReAct prompt template for AnalysisAgent"""
        return PromptTemplate.from_template("""
You are an analysis expert in a business intelligence system.
Your role is to analyze data provided by other agents and extract actionable insights.

TOOLS:
------
You have access to the following tools:

{tools}

TOOL INPUT FORMATS:
- analyze_sentiment: Analyze sentiment in customer reviews and feedback
  Input: string (single review), list of strings (multiple reviews), or text separated by '|'
  Example: "Great food but slow service" or ["Great food", "Bad service", "Nice ambiance"]

ANALYSIS GUIDELINES:
1. Use analyze_sentiment tool to process all review data provided
2. Calculate overall sentiment percentages and confidence scores
3. Identify key positive and negative themes from the sentiment analysis
4. Look for patterns and trends in customer feedback
5. Provide quantified metrics and specific insights
6. Always include structured JSON results in your Final Answer

OUTPUT FORMAT:
Your Final Answer must include structured sections for easy parsing:

ANALYSIS_NOTE: [Brief 1-2 sentence summary for supervisor]

ANALYSIS_RESULT:
```json
{{
  "sentiment_analysis": {{
    "overall_sentiment": "positive/negative/neutral",
    "confidence_score": 0.85,
    "positive_percentage": 60,
    "negative_percentage": 25,
    "neutral_percentage": 15
  }},
  "key_insights": [
    "insight 1",
    "insight 2"
  ],
  "themes": {{
    "positive_themes": ["theme1", "theme2"],
    "negative_themes": ["theme1", "theme2"]
  }},
  "summary": "Brief description of analysis results",
  "total_reviews_analyzed": 100
}}
```

DETAILED_RESPONSE: [Comprehensive analysis in readable format]

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: [Use the structured format above with ANALYSIS_NOTE, ANALYSIS_RESULT JSON, and DETAILED_RESPONSE]

Begin!

Question: {input}
Thought: {agent_scratchpad}""")

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
        """Process analysis requests using the ReAct agent"""
        search_results = state.get("search_results", {})
        user_query = state.get("user_query", "")
        
        # Create the task description with available data
        task = f"""Analyze data related to: "{user_query}"

Available Data to Analyze:
- Business Data: {len(search_results.get('businesses', []))} businesses found
- Review Data: {len(search_results.get('reviews', []))} reviews found

Search Results Data:
{json.dumps(search_results, indent=2)}

Please analyze this data and provide sentiment analysis, key insights, and statistical summaries."""
        
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
            updated_state["analysis_agent_note"] = note
            updated_state["analysis_agent_result"] = structured_result
            updated_state["last_agent"] = self.agent_name
            
            # Maintain backward compatibility with legacy analysis_results field
            analysis_results = structured_result.get("analysis_data", structured_result)
            updated_state["analysis_results"] = analysis_results
            
            # Add summary to messages
            messages = updated_state.get("messages", [])
            messages.append(note)
            updated_state["messages"] = messages
            
            return updated_state
            
        except Exception as e:
            error_msg = f"Error in {self.agent_name}: {str(e)}"
            print(f"❌ {error_msg}")
            
            updated_state = state.copy()
            updated_state["analysis_agent_note"] = f"AnalysisAgent encountered an error: {str(e)}"
            updated_state["analysis_agent_result"] = {"error": str(e)}
            updated_state["analysis_results"] = {"error": str(e)}
            updated_state["last_agent"] = self.agent_name
            
            return updated_state

    def _parse_structured_output(self, agent_output: str) -> tuple[str, Dict[str, Any]]:
        """Parse the structured output from the agent"""
        import re
        
        # Extract the note
        note_match = re.search(r'ANALYSIS_NOTE:\s*(.*?)(?=\n\n|ANALYSIS_RESULT:)', agent_output, re.DOTALL)
        note = note_match.group(1).strip() if note_match else f"AnalysisAgent completed analysis task"
        
        # Extract the JSON result
        json_match = re.search(r'ANALYSIS_RESULT:\s*```json\s*(.*?)\s*```', agent_output, re.DOTALL)
        
        structured_result = {"full_output": agent_output}
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                structured_result["analysis_data"] = json_data
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse JSON from agent output: {e}")
                structured_result["parse_error"] = str(e)
        
        # Extract detailed response
        detailed_match = re.search(r'DETAILED_RESPONSE:\s*(.*)', agent_output, re.DOTALL)
        if detailed_match:
            structured_result["detailed_response"] = detailed_match.group(1).strip()
        
        return note, structured_result
