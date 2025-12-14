"""Tests for prompt building utilities."""

import pytest
from utils.prompts import build_swarm_prompt, SWARMMASTER_PROMPT


def test_build_swarm_prompt_includes_task():
    """Test that the prompt includes the user task."""
    task = "Design a viral AI tool"
    prompt = build_swarm_prompt(task)
    
    assert task in prompt
    assert "Task:" in prompt


def test_build_swarm_prompt_contains_template():
    """Test that the prompt contains key template elements."""
    task = "Test task"
    prompt = build_swarm_prompt(task)
    
    assert "SwarmMaster" in prompt
    assert "Builder Swarm" in prompt
    assert "Swarm Complete" in prompt
    assert "Agent Role Name" in prompt


def test_build_swarm_prompt_formatting():
    """Test that prompt formatting works correctly."""
    task = "Create a business plan"
    prompt = build_swarm_prompt(task)
    
    # Should not have unformatted placeholders
    assert "{user_task}" not in prompt
    assert task in prompt


def test_build_swarm_prompt_empty_task():
    """Test that empty tasks are handled."""
    task = ""
    prompt = build_swarm_prompt(task)
    
    assert "Task:" in prompt
    assert prompt.endswith("\nTask: \n")


def test_build_swarm_prompt_special_characters():
    """Test that special characters in tasks are handled."""
    task = "Task with 'quotes' and \"double quotes\" and <tags>"
    prompt = build_swarm_prompt(task)
    
    assert task in prompt

