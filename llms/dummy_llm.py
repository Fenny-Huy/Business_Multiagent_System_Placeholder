# dummy_llm.py
class DummyLLM:
    """A simple LLM stub for testing multiagent workflows."""
    def __init__(self, name):
        self.name = name
    def generate(self, prompt, **kwargs):
        return f"[{self.name} LLM] Response to: {prompt}"