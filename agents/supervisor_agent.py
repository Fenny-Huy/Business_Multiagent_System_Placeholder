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
        
        # Use efficient note-based routing instead of full results
        search_agent_note = state.get("search_agent_note", "")
        analysis_agent_note = state.get("analysis_agent_note", "")
        final_response = state.get("final_response", "")
        
        # Build context for decision making using notes for efficiency
        context_parts = []
        context_parts.append(f"User Query: {user_query}")
        context_parts.append(f"Last Agent: {last_agent}")
        
        # Use concise notes instead of full results
        if search_agent_note:
            context_parts.append(f"Search Agent Note: {search_agent_note}")
        else:
            context_parts.append("Search: Not completed")
            
        if analysis_agent_note:
            context_parts.append(f"Analysis Agent Note: {analysis_agent_note}")
        else:
            context_parts.append("Analysis: Not completed")
        
        # Include actual final response content for quality evaluation
        if final_response:
            response_preview = final_response[:300] + ("..." if len(final_response) > 300 else final_response)
            context_parts.append(f"Current Final Response: {response_preview}")
        else:
            context_parts.append("Final Response: Not completed")
        
        context = "\\n".join(context_parts)
        
        # Create decision prompt
        decision_prompt = f"""Based on the current workflow state, decide which agent should handle the next step:

{context}

Workflow Analysis:
- If Search Agent hasn't run yet (no search note), route to SearchAgent
- If we have search notes but no analysis note, route to AnalysisAgent  
- If we have both search and analysis notes but no final response, route to ResponseAgent
- If we have a final response, evaluate if it's complete and addresses the user query
- If the response seems incomplete, you can route to ResponseAgent again for improvement

The notes provide concise summaries of what each agent accomplished.

Your decision (respond with ONLY the agent name or FINISH):"""
        
        try:
            decision = self.llm._call(decision_prompt).strip()
            
            # Validate decision
            valid_choices = self.available_agents + ["FINISH"]
            if decision not in valid_choices:
                # Default routing logic if LLM gives invalid response
                decision = self._get_fallback_decision(search_agent_note, analysis_agent_note, final_response)
            
        except Exception as e:
            # Fallback routing logic
            decision = self._get_fallback_decision(search_agent_note, analysis_agent_note, final_response)
        
        # Update state with routing decision
        updated_state = state.copy()
        updated_state["next_agent"] = decision
        updated_state["last_agent"] = self.agent_name
        
        return updated_state
    
    def _get_fallback_decision(self, search_agent_note: str, analysis_agent_note: str, final_response: str) -> str:
        """Simple fallback decision logic using note-based approach"""
        if not search_agent_note:
            return "SearchAgent"
        elif search_agent_note and not analysis_agent_note:
            return "AnalysisAgent"
        elif not final_response:
            return "ResponseAgent"
        else:
            return "FINISH"
    
    def route_to_agent(self, state: Dict[str, Any]) -> Literal["SearchAgent", "AnalysisAgent", "ResponseAgent", "FINISH"]:
        """Route to the next agent based on current state"""
        updated_state = self.process(state)
        return updated_state.get("next_agent", "FINISH")