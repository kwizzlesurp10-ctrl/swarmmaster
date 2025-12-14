"""Tests for validation utilities."""

import pytest
from utils.validation import (
    validate_task,
    validate_temperature,
    validate_max_tokens,
    validate_model,
)


class TestValidateTask:
    """Test suite for task validation."""
    
    def test_validate_task_valid(self):
        """Test validation of valid tasks."""
        is_valid, error = validate_task("Design a viral AI tool")
        assert is_valid is True
        assert error is None
    
    def test_validate_task_empty(self):
        """Test validation of empty task."""
        is_valid, error = validate_task("")
        assert is_valid is False
        assert error is not None
        assert "task" in error.lower() or "empty" in error.lower() or "whitespace" in error.lower()
    
    def test_validate_task_whitespace_only(self):
        """Test validation of whitespace-only task."""
        is_valid, error = validate_task("   ")
        assert is_valid is False
        assert "whitespace" in error.lower()
    
    def test_validate_task_too_short(self):
        """Test validation of task that's too short."""
        is_valid, error = validate_task("ab")
        assert is_valid is False
        assert "at least 3" in error.lower()
    
    def test_validate_task_too_long(self):
        """Test validation of task that's too long."""
        long_task = "a" * 10001
        is_valid, error = validate_task(long_task)
        assert is_valid is False
        assert "too long" in error.lower()
    
    def test_validate_task_none(self):
        """Test validation of None task."""
        is_valid, error = validate_task(None)
        assert is_valid is False
        assert error is not None


class TestValidateTemperature:
    """Test suite for temperature validation."""
    
    def test_validate_temperature_valid(self):
        """Test validation of valid temperatures."""
        is_valid, error = validate_temperature(0.7)
        assert is_valid is True
        assert error is None
        
        is_valid, error = validate_temperature(0.0)
        assert is_valid is True
        
        is_valid, error = validate_temperature(2.0)
        assert is_valid is True
    
    def test_validate_temperature_too_low(self):
        """Test validation of temperature that's too low."""
        is_valid, error = validate_temperature(-0.1)
        assert is_valid is False
        assert "between 0.0 and 2.0" in error
    
    def test_validate_temperature_too_high(self):
        """Test validation of temperature that's too high."""
        is_valid, error = validate_temperature(2.1)
        assert is_valid is False
        assert "between 0.0 and 2.0" in error
    
    def test_validate_temperature_invalid_type(self):
        """Test validation of non-numeric temperature."""
        is_valid, error = validate_temperature("0.7")
        assert is_valid is False
        assert "number" in error.lower()


class TestValidateMaxTokens:
    """Test suite for max_tokens validation."""
    
    def test_validate_max_tokens_valid(self):
        """Test validation of valid max_tokens."""
        is_valid, error = validate_max_tokens(4096)
        assert is_valid is True
        assert error is None
        
        is_valid, error = validate_max_tokens(1)
        assert is_valid is True
        
        is_valid, error = validate_max_tokens(8192)
        assert is_valid is True
    
    def test_validate_max_tokens_too_low(self):
        """Test validation of max_tokens that's too low."""
        is_valid, error = validate_max_tokens(0)
        assert is_valid is False
        assert "at least 1" in error.lower()
    
    def test_validate_max_tokens_too_high(self):
        """Test validation of max_tokens that's too high."""
        is_valid, error = validate_max_tokens(8193)
        assert is_valid is False
        assert "cannot exceed 8192" in error
    
    def test_validate_max_tokens_invalid_type(self):
        """Test validation of non-integer max_tokens."""
        is_valid, error = validate_max_tokens("4096")
        assert is_valid is False
        assert "integer" in error.lower()


class TestValidateModel:
    """Test suite for model validation."""
    
    def test_validate_model_valid(self):
        """Test validation of valid model."""
        available = ["model1", "model2", "model3"]
        is_valid, error = validate_model("model1", available)
        assert is_valid is True
        assert error is None
    
    def test_validate_model_not_in_list(self):
        """Test validation of model not in available list."""
        available = ["model1", "model2"]
        is_valid, error = validate_model("model3", available)
        assert is_valid is False
        assert "not in the available models list" in error
    
    def test_validate_model_empty(self):
        """Test validation of empty model."""
        available = ["model1"]
        is_valid, error = validate_model("", available)
        assert is_valid is False
        assert "cannot be empty" in error.lower()

