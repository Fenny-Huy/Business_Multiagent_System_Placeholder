# llm/gemini_llm.py
import google.generativeai as genai
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
import os
import logging
import time
from dataclasses import dataclass


@dataclass
class GeminiConfig:
    """Configuration for Gemini model"""
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.3
    max_output_tokens: int = 2048
    top_p: float = 0.95
    top_k: int = 40


class GeminiLLM(LLM):
    """Custom LangChain LLM wrapper for Google's Gemini API"""
    
    # Declare fields for Pydantic
    config: Any
    api_key: Any
    model: Any
    _generation_config: Any
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[GeminiConfig] = None, **kwargs):
        """Initialize Gemini LLM
        
        Args:
            api_key: Google API key for Gemini. If None, will look for GEMINI_API_KEY env var
            config: GeminiConfig object for model configuration
            **kwargs: Additional LangChain LLM parameters
        """
        # Prepare configuration
        config_obj = config or GeminiConfig()
        api_key_val = api_key or os.getenv('GEMINI_API_KEY')
        
        if not api_key_val:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Initialize the Gemini components first
        try:
            # Configure the API
            genai.configure(api_key=api_key_val)
            
            # Initialize the model
            model_obj = genai.GenerativeModel(config_obj.model_name)
            
            # Configure generation parameters
            generation_config = genai.GenerationConfig(
                temperature=config_obj.temperature,
                max_output_tokens=config_obj.max_output_tokens,
                top_p=config_obj.top_p,
                top_k=config_obj.top_k,
            )
            
            logging.info(f"✓ Gemini LLM initialized with model: {config_obj.model_name}")
            
        except Exception as e:
            logging.error(f"Failed to initialize Gemini LLM: {e}")
            raise
        
        # Initialize parent LangChain LLM with the fields
        super().__init__(
            config=config_obj,
            api_key=api_key_val,
            model=model_obj,
            _generation_config=generation_config,
            **kwargs
        )
        
        # Ensure the attributes are properly set as instance variables
        self.config = config_obj
        self.api_key = api_key_val
        self.model = model_obj
        self._generation_config = generation_config

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Generate response using Gemini API
        
        Args:
            prompt: The input prompt
            stop: Stop sequences
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            # Track generation time for monitoring
            start_time = time.time()
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=self._generation_config
            )
            
            # Get the generated text
            generated_text = response.text
            
            # Handle stop sequences if provided
            if stop:
                for stop_seq in stop:
                    if stop_seq in generated_text:
                        generated_text = generated_text.split(stop_seq)[0]
                        break
            
            # Log generation metrics
            generation_time = time.time() - start_time
            logging.info(f"Gemini generation completed in {generation_time:.2f}s")
            
            return generated_text.strip()
            
        except Exception as e:
            error_msg = f"Gemini generation error: {str(e)}"
            logging.error(error_msg)
            
            # Return a graceful error message instead of raising
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Return identifying parameters for the LLM"""
        return {
            "model_name": self.config.model_name,
            "temperature": self.config.temperature,
            "max_output_tokens": self.config.max_output_tokens,
            "top_p": self.config.top_p,
            "top_k": self.config.top_k,
        }