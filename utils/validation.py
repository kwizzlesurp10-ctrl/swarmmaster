"""Input validation utilities for SwarmMaster."""

from typing import Optional
from .errors import ValidationError


def validate_task(task: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate a user task input.
    
    Args:
        task: The task string to validate.
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not task:
        return False, "Please provide a task to execute."
    
    if not task.strip():
        return False, "Task cannot be empty or only whitespace."
    
    if len(task.strip()) < 3:
        return False, "Task must be at least 3 characters long."
    
    if len(task) > 10000:
        return False, "Task is too long (maximum 10,000 characters)."
    
    return True, None


def validate_model(model: str, available_models: list[str]) -> tuple[bool, Optional[str]]:
    """
    Validate a model identifier.
    
    Args:
        model: The model identifier to validate.
        available_models: List of available model identifiers.
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not model or not model.strip():
        return False, "Model identifier cannot be empty."
    
    if model not in available_models:
        return False, f"Model '{model}' is not in the available models list."
    
    return True, None


def validate_temperature(temperature: float) -> tuple[bool, Optional[str]]:
    """
    Validate temperature parameter.
    
    Args:
        temperature: The temperature value to validate.
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(temperature, (int, float)):
        return False, "Temperature must be a number."
    
    if temperature < 0.0 or temperature > 2.0:
        return False, "Temperature must be between 0.0 and 2.0."
    
    return True, None


def validate_max_tokens(max_tokens: int) -> tuple[bool, Optional[str]]:
    """
    Validate max_tokens parameter.
    
    Args:
        max_tokens: The max_tokens value to validate.
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(max_tokens, int):
        return False, "Max tokens must be an integer."
    
    if max_tokens < 1:
        return False, "Max tokens must be at least 1."
    
    if max_tokens > 8192:
        return False, "Max tokens cannot exceed 8192."
    
    return True, None

