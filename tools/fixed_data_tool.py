# fixed_data_tool.py
class FixedDataTool:
    """A tool that always returns a fixed dataset."""
    def __call__(self, query=None):
        return {"data": ["item1", "item2", "item3"], "query": query}
