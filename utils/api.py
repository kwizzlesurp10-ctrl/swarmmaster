"""API utilities for Hugging Face Inference Client."""

import os
from typing import Generator, Optional
from huggingface_hub import InferenceClient

from .errors import APIError


class SwarmClient:
    """Wrapper for Hugging Face InferenceClient with SwarmMaster-specific logic."""
    
    def __init__(self, model: str, token: Optional[str] = None) -> None:
        """
        Initialize the SwarmClient.
        
        Args:
            model: The model identifier to use.
            token: Optional Hugging Face token. If None, uses HF_TOKEN env var.
        """
        self.model = model
        self.token = token or os.getenv("HF_TOKEN")
        self.client = InferenceClient(model=model, token=self.token)
    
    def stream_swarm_response(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        """
        Stream responses from the model for a swarm task.
        
        Args:
            prompt: The full prompt to send to the model.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            
        Yields:
            Accumulated response chunks as strings.
            
        Raises:
            Exception: If the API call fails.
        """
        accumulated = ""
        try:
            for message in self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                stream=True,
                temperature=temperature,
            ):
                chunk = message.choices[0].delta.content or ""
                if chunk:
                    accumulated += chunk
                    yield accumulated
        except Exception as e:
            raise APIError(f"Failed to stream response: {str(e)}") from e

