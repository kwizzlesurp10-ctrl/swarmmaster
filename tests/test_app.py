"""Integration tests for app.py run_swarm function."""

import os
from unittest.mock import patch, MagicMock
import pytest

# Mock gradio before importing app
import sys
sys.modules['gradio'] = MagicMock()

from app import run_swarm
from utils import SwarmConfig


class TestRunSwarm:
    """Test suite for run_swarm function."""
    
    def test_run_swarm_empty_task(self):
        """Test that empty task returns error message."""
        result = list(run_swarm("", "model", 0.7, 4096))
        assert len(result) == 1
        assert "❌" in result[0]
        assert "task" in result[0].lower()
    
    def test_run_swarm_whitespace_only_task(self):
        """Test that whitespace-only task returns error message."""
        result = list(run_swarm("   ", "model", 0.7, 4096))
        assert len(result) == 1
        assert "❌" in result[0]
    
    def test_run_swarm_invalid_temperature(self):
        """Test that invalid temperature returns error message."""
        result = list(run_swarm("test task", "model", 2.5, 4096))
        assert len(result) == 1
        assert "❌" in result[0]
        assert "temperature" in result[0].lower()
    
    def test_run_swarm_invalid_max_tokens(self):
        """Test that invalid max_tokens returns error message."""
        result = list(run_swarm("test task", "model", 0.7, 10000))
        assert len(result) == 1
        assert "❌" in result[0]
        assert "max tokens" in result[0].lower() or "cannot exceed" in result[0].lower()
    
    @patch('app.SwarmConfig.validate_token')
    @patch('app.SwarmClient')
    @patch('app.build_swarm_prompt')
    @patch.dict(os.environ, {"HF_TOKEN": "test-token"})
    def test_run_swarm_missing_token(self, mock_build_prompt, mock_client_class, mock_validate):
        """Test that missing HF_TOKEN returns error message."""
        mock_validate.return_value = (False, "HF_TOKEN not set")
        
        result = list(run_swarm("test task", "model", 0.7, 4096))
        assert len(result) == 1
        assert "HF_TOKEN not set" in result[0]
    
    @patch('app.SwarmConfig.validate_token')
    @patch('app.SwarmClient')
    @patch('app.build_swarm_prompt')
    @patch.dict(os.environ, {"HF_TOKEN": "test-token"})
    def test_run_swarm_success(self, mock_build_prompt, mock_client_class, mock_validate):
        """Test successful swarm execution with mocked API."""
        # Setup mocks
        mock_validate.return_value = (True, None)
        mock_build_prompt.return_value = "formatted prompt"
        
        mock_client = MagicMock()
        mock_client.stream_swarm_response.return_value = [
            "🚀 Deploying",
            "🚀 Deploying Builder Swarm",
            "🚀 Deploying Builder Swarm...\n\nAgent 1: Working",
        ]
        mock_client_class.return_value = mock_client
        
        result = list(run_swarm("test task", "model", 0.7, 4096))
        
        # Verify prompt was built
        mock_build_prompt.assert_called_once_with("test task")
        
        # Verify client was called with correct parameters
        mock_client.stream_swarm_response.assert_called_once_with(
            "formatted prompt",
            max_tokens=4096,
            temperature=0.7,
        )
        
        # Verify output includes deployment message and chunks
        assert len(result) >= 2  # At least deployment message + one chunk
        assert "🚀 Deploying Builder Swarm" in result[0]
    
    @patch('app.SwarmConfig.validate_token')
    @patch('app.SwarmClient')
    @patch('app.build_swarm_prompt')
    @patch.dict(os.environ, {"HF_TOKEN": "test-token"})
    def test_run_swarm_api_error(self, mock_build_prompt, mock_client_class, mock_validate):
        """Test that API errors are caught and returned as error message."""
        from utils.errors import APIError
        
        # Setup mocks
        mock_validate.return_value = (True, None)
        mock_build_prompt.return_value = "formatted prompt"
        
        mock_client = MagicMock()
        mock_client.stream_swarm_response.side_effect = APIError("Connection failed")
        mock_client_class.return_value = mock_client
        
        result = list(run_swarm("test task", "model", 0.7, 4096))
        
        # Should yield deployment message then error
        assert len(result) >= 2
        assert "🚀 Deploying Builder Swarm" in result[0]
        assert "❌" in result[-1]
        assert "API error" in result[-1] or "Connection failed" in result[-1]
    
    @patch('app.SwarmConfig.validate_token')
    @patch('app.SwarmClient')
    @patch('app.build_swarm_prompt')
    @patch.dict(os.environ, {"HF_TOKEN": "test-token"})
    def test_run_swarm_streaming_chunks_accumulate(self, mock_build_prompt, mock_client_class, mock_validate):
        """Test that streaming chunks are yielded correctly."""
        # Setup mocks
        mock_validate.return_value = (True, None)
        mock_build_prompt.return_value = "formatted prompt"
        
        mock_client = MagicMock()
        mock_client.stream_swarm_response.return_value = [
            "Chunk 1",
            "Chunk 1 Chunk 2",
            "Chunk 1 Chunk 2 Chunk 3",
        ]
        mock_client_class.return_value = mock_client
        
        result = list(run_swarm("test task", "model", 0.7, 4096))
        
        # Should have deployment message + 3 chunks
        assert len(result) == 4
        assert result[0] == "🚀 Deploying Builder Swarm...\n\n"
        assert result[1] == "Chunk 1"
        assert result[2] == "Chunk 1 Chunk 2"
        assert result[3] == "Chunk 1 Chunk 2 Chunk 3"

