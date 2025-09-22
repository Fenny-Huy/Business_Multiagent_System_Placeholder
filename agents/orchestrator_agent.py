# orchestrator_agent.py
from agents.retrieval_agent import RetrievalAgent
from agents.analysis_agent import AnalysisAgent
from agents.strategy_agent import StrategyAgent

class OrchestratorAgent:
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.analysis_agent = AnalysisAgent()
        self.strategy_agent = StrategyAgent()
    def run(self, user_query):
        state = {"user_query": user_query}
        print("[Orchestrator] Starting workflow...")
        state = self.retrieval_agent.act(state)
        print("[Orchestrator] Retrieval done.")
        state = self.analysis_agent.act(state)
        print("[Orchestrator] Analysis done.")
        state = self.strategy_agent.act(state)
        print("[Orchestrator] Strategy done.")
        return state
