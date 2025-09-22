# retrieval_agent.py
from llms.dummy_llm import DummyLLM
from tools.fixed_data_tool import FixedDataTool

class RetrievalAgent:
    def __init__(self):
        self.llm = DummyLLM("RetrievalAgent")
        self.tool = FixedDataTool()
    def act(self, state):
        query = state.get("user_query", "default query")
        data = self.tool(query)
        state["retrieved_data"] = data
        state["retrieval_log"] = self.llm.generate(f"Retrieved data for query: {query}")
        return state
