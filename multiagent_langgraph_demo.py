# multiagent_langgraph_demo.py
"""
A minimal LangGraph multiagent system using GeminiLLM and dummy tools.
"""
from langgraph.graph import StateGraph, node
from gemini_llm import GeminiLLM, GeminiConfig

from tools.fixed_data_tool import FixedDataTool
from tools.fixed_analysis_tool import FixedAnalysisTool
from tools.fixed_strategy_tool import FixedStrategyTool
import os

# Shared state class
def make_initial_state(user_query):
    return {"user_query": user_query}

# Agent classes
class RetrievalAgent:
    def __init__(self, llm, tool):
        self.llm = llm
        self.tool = tool
    def act(self, state):
        query = state.get("user_query", "default query")
        data = self.tool(query)
        state["retrieved_data"] = data
        state["retrieval_log"] = self.llm._call(f"Retrieved data for query: {query}")
        return state

class AnalysisAgent:
    def __init__(self, llm, tool):
        self.llm = llm
        self.tool = tool
    def act(self, state):
        data = state.get("retrieved_data", {})
        analysis = self.tool(data)
        state["analysis_result"] = analysis
        state["analysis_log"] = self.llm._call(f"Analyzed data: {data}")
        return state

class StrategyAgent:
    def __init__(self, llm, tool):
        self.llm = llm
        self.tool = tool
    def act(self, state):
        analysis = state.get("analysis_result", {})
        strategy = self.tool(analysis)
        state["strategy_decision"] = strategy
        state["strategy_log"] = self.llm._call(f"Strategy based on analysis: {analysis}")
        return state

# Instantiate agents
gemini_llm = GeminiLLM(api_key=os.getenv("GEMINI_API_KEY"), config=GeminiConfig())
retrieval_agent = RetrievalAgent(gemini_llm, FixedDataTool())
analysis_agent = AnalysisAgent(gemini_llm, FixedAnalysisTool())
strategy_agent = StrategyAgent(gemini_llm, FixedStrategyTool())

# LangGraph nodes
@node
def retrieval_node(state):
    return retrieval_agent.act(state)

@node
def analysis_node(state):
    return analysis_agent.act(state)

@node
def strategy_node(state):
    return strategy_agent.act(state)

# Build LangGraph workflow
graph = StateGraph()
graph.add_node("retrieval", retrieval_node)
graph.add_node("analysis", analysis_node)
graph.add_node("strategy", strategy_node)
# Define transitions
graph.add_edge("retrieval", "analysis")
graph.add_edge("analysis", "strategy")
# Set entry and exit
graph.set_entry("retrieval")
graph.set_exit("strategy")

# Run demo
if __name__ == "__main__":
    user_query = "What is the best strategy for the given data?"
    initial_state = make_initial_state(user_query)
    final_state = graph.run(initial_state)
    print("\n=== Final State ===")
    for k, v in final_state.items():
        print(f"{k}: {v}")
