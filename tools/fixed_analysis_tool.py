# fixed_analysis_tool.py
class FixedAnalysisTool:
    """A tool that always returns a fixed analysis result."""
    def __call__(self, data):
        return {"analysis": f"Analysis of {data}"}
