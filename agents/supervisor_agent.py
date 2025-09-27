# agents/supervisor_agent.py
from typing import Dict, Any, List, Literal
from agents.base_agent import BaseAgent


class SupervisorAgent(BaseAgent):
    """Supervisor agent that coordinates other agents in the multi-agent system"""
    
    def __init__(self, available_agents: List[str]):
        """Initialize supervisor agent
        
        Args:
            available_agents: List of available agent names
        """
        self.available_agents = available_agents
        
        super().__init__(
            agent_name="SupervisorAgent",
            description="Coordinates and routes tasks between specialized agents",
            tools=[]
        )
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for the supervisor agent"""
        return f"""You are a Supervisor Agent that coordinates a team of specialized agents to handle user queries.

Available agents:
{chr(10).join([f"- {agent}" for agent in self.available_agents])}

Your responsibilities:
1. Analyze the user query to understand what type of task is needed
2. Decide which agent should handle the next step
3. Route the task to the appropriate agent
4. Determine when the task is complete

Agent capabilities:
- SearchAgent: Finds reviews and business information from databases
- AnalysisAgent: Performs sentiment analysis and data insights
- ResponseAgent: Generates final comprehensive responses
- FINISH: Complete the task and return results to user

Decision guidelines:
- If the user wants to find specific reviews or businesses -> SearchAgent
- If there's data that needs analysis (sentiment, patterns) -> AnalysisAgent  
- If you need to generate a final response or summary -> ResponseAgent
- If the task is complete and user has their answer -> FINISH

Always choose the most appropriate next step based on the current state and what's needed to fully answer the user's query.

You must respond with ONLY the name of the next agent (SearchAgent, AnalysisAgent, ResponseAgent) or FINISH."""
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the next agent to route to"""
        user_query = state.get("user_query", "")
        last_agent = state.get("last_agent", "")
        search_results = state.get("search_results", {})
        analysis_results = state.get("analysis_results", {})
        final_response = state.get("final_response", "")
        
        # Build context for decision making
        context_parts = []
        context_parts.append(f"User Query: {user_query}")
        context_parts.append(f"Last Agent: {last_agent}")
        context_parts.append(f"Has Search Results: {'Yes' if search_results else 'No'}")
        context_parts.append(f"Has Analysis Results: {'Yes' if analysis_results else 'No'}")
        
        # Include actual final response content for quality evaluation
        if final_response:
            response_preview = final_response[:200] + "..." if len(final_response) > 200 else final_response
            context_parts.append(f"Current Final Response: {response_preview}")
        else:
            context_parts.append("Has Final Response: No")
        
        context = "\\n".join(context_parts)
        
        # Create decision prompt
        decision_prompt = f"""Based on the current state, decide which agent should handle the next step:

{context}

Current State Analysis:
- If no search has been done yet, route to SearchAgent
- If we have search results but no analysis, route to AnalysisAgent
- If we have data but no final response, route to ResponseAgent
- If we have a final response, review it:
  * Does it appear to be a complete response that addresses the user query?
  * If the response seems incomplete or problematic, you can route to ResponseAgent again

When you've reviewed the information, decide on the next step.

Your decision (respond with ONLY the agent name or FINISH):"""
        
        try:
            decision = self.llm._call(decision_prompt).strip()
            
            # Validate decision
            valid_choices = self.available_agents + ["FINISH"]
            if decision not in valid_choices:
                # Default routing logic if LLM gives invalid response
                decision = self._get_fallback_decision(search_results, analysis_results, final_response)
            
        except Exception as e:
            # Fallback routing logic
            decision = self._get_fallback_decision(search_results, analysis_results, final_response)
        
        # Update state with routing decision
        updated_state = state.copy()
        updated_state["next_agent"] = decision
        updated_state["last_agent"] = self.agent_name
        
        return updated_state
    
    def _get_fallback_decision(self, search_results: Dict[str, Any], analysis_results: Dict[str, Any], final_response: str) -> str:
        """Simple fallback decision logic"""
        if not search_results:
            return "SearchAgent"
        elif search_results and not analysis_results:
            return "AnalysisAgent"
        elif not final_response:
            return "ResponseAgent"
        else:
            return "FINISH"
    
    def route_to_agent(self, state: Dict[str, Any]) -> Literal["SearchAgent", "AnalysisAgent", "ResponseAgent", "FINISH"]:
        """Route to the next agent based on current state"""
        updated_state = self.process(state)
        return updated_state.get("next_agent", "FINISH")