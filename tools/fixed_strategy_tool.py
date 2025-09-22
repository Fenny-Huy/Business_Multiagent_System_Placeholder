# fixed_strategy_tool.py
class FixedStrategyTool:
    """A tool that always returns a fixed strategy decision."""
    def __call__(self, analysis):
        return {"strategy": f"Strategy based on {analysis}"}
