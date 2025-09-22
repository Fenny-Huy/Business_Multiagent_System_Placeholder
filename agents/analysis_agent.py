# analysis_agent.py
from llms.dummy_llm import DummyLLM
from tools.fixed_analysis_tool import FixedAnalysisTool

class AnalysisAgent:
    def __init__(self):
        self.llm = DummyLLM("AnalysisAgent")
        self.tool = FixedAnalysisTool()
    def act(self, state):
        data = state.get("retrieved_data", {})
        analysis = self.tool(data)
        state["analysis_result"] = analysis
        state["analysis_log"] = self.llm.generate(f"Analyzed data: {data}")
        return state
