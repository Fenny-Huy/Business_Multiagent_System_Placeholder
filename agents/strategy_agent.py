# strategy_agent.py
from llms.dummy_llm import DummyLLM
from tools.fixed_strategy_tool import FixedStrategyTool

class StrategyAgent:
    def __init__(self):
        self.llm = DummyLLM("StrategyAgent")
        self.tool = FixedStrategyTool()
    def act(self, state):
        analysis = state.get("analysis_result", {})
        strategy = self.tool(analysis)
        state["strategy_decision"] = strategy
        state["strategy_log"] = self.llm.generate(f"Strategy based on analysis: {analysis}")
        return state
