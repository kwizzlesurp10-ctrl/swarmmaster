"""Configuration management for SwarmMaster."""

import os
from typing import Optional


class SwarmConfig:
    """Configuration class for SwarmMaster settings."""
    
    # Model configuration
    DEFAULT_MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct"
    DEFAULT_MAX_TOKENS = 4096
    DEFAULT_TEMPERATURE = 0.7
    
    # Available models (can be extended)
    AVAILABLE_MODELS = [
        "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "google/gemma-7b-it",
    ]
    
    @staticmethod
    def get_model() -> str:
        """Get the model identifier from environment or default."""
        return os.getenv("SWARM_MODEL", SwarmConfig.DEFAULT_MODEL)
    
    @staticmethod
    def get_token() -> Optional[str]:
        """Get the Hugging Face token from environment."""
        return os.getenv("HF_TOKEN")
    
    @staticmethod
    def get_max_tokens() -> int:
        """Get max tokens from environment or default."""
        max_tokens = os.getenv("SWARM_MAX_TOKENS")
        if max_tokens:
            try:
                return int(max_tokens)
            except ValueError:
                return SwarmConfig.DEFAULT_MAX_TOKENS
        return SwarmConfig.DEFAULT_MAX_TOKENS
    
    @staticmethod
    def get_temperature() -> float:
        """Get temperature from environment or default."""
        temperature = os.getenv("SWARM_TEMPERATURE")
        if temperature:
            try:
                return float(temperature)
            except ValueError:
                return SwarmConfig.DEFAULT_TEMPERATURE
        return SwarmConfig.DEFAULT_TEMPERATURE
    
    @staticmethod
    def validate_token() -> tuple[bool, Optional[str]]:
        """
        Validate that HF_TOKEN is set.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        token = SwarmConfig.get_token()
        if not token:
            return False, "HF_TOKEN not set. Please configure your Hugging Face token."
        return True, None

