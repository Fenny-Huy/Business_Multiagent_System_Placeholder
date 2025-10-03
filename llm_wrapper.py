# llm_wrapper.py
import os
from typing import Optional
from llm.gemini_llm import GeminiLLM, GeminiConfig

def get_llm(model_name: str = "gemini-2.0-flash", temperature: float = 0.3):
    """Get LLM instance with proper configuration
    
    Args:
        model_name: The model name to use
        temperature: Temperature for generation
        
    Returns:
        Configured LLM instance
    """
    try:
        # Create configuration
        config = GeminiConfig(
            model_name=model_name,
            temperature=temperature,
            max_output_tokens=2048,
            top_p=0.95,
            top_k=40
        )
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("⚠️ Warning: No Gemini API key found. Using mock LLM.")
            return MockLLM()
        
        # Create and return Gemini LLM
        llm = GeminiLLM(api_key=api_key, config=config)
        print(f"✅ Gemini LLM initialized with model: {model_name}")
        return llm
        
    except Exception as e:
        print(f"❌ Error initializing Gemini LLM: {e}")
        print("Using mock LLM instead.")
        return MockLLM()


class MockLLM:
    """Mock LLM for testing when real LLM is not available"""
    
    def _call(self, prompt: str, **kwargs) -> str:
        """Mock LLM call"""
        if "SearchAgent" in prompt or "search" in prompt.lower():
            return "SearchAgent"
        elif "AnalysisAgent" in prompt or "analysis" in prompt.lower():
            return "AnalysisAgent"
        elif "ResponseAgent" in prompt or "response" in prompt.lower():
            return "ResponseAgent"
        else:
            return "FINISH"
    
    def invoke(self, messages, **kwargs):
        """Mock invoke method for compatibility"""
        if hasattr(messages, '__iter__') and messages:
            prompt = str(messages[0].content if hasattr(messages[0], 'content') else messages[0])
        else:
            prompt = str(messages)
        
        class MockResponse:
            def __init__(self, content):
                self.content = content
        
        return MockResponse(self._call(prompt))