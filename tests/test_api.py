"""Tests for SwarmClient API utilities."""

import os
from unittest.mock import Mock, patch, MagicMock
import pytest
from utils.api import SwarmClient


class TestSwarmClient:
    """Test suite for SwarmClient class."""
    
    def test_init_with_token(self):
        """Test initialization with explicit token."""
        with patch('utils.api.InferenceClient') as mock_client:
            client = SwarmClient(model="test-model", token="test-token")
            
            assert client.model == "test-model"
            assert client.token == "test-token"
            mock_client.assert_called_once_with(model="test-model", token="test-token")
    
    def test_init_without_token_uses_env(self):
        """Test initialization falls back to HF_TOKEN env var."""
        with patch('utils.api.InferenceClient') as mock_client:
            with patch.dict(os.environ, {"HF_TOKEN": "env-token"}):
                client = SwarmClient(model="test-model", token=None)
                
                assert client.token == "env-token"
                mock_client.assert_called_once_with(model="test-model", token="env-token")
    
    def test_stream_swarm_response_accumulates_chunks(self):
        """Test that streaming responses accumulate correctly."""
        # Mock the chat_completion response
        mock_message1 = MagicMock()
        mock_message1.choices = [MagicMock()]
        mock_message1.choices[0].delta.content = "Hello"
        
        mock_message2 = MagicMock()
        mock_message2.choices = [MagicMock()]
        mock_message2.choices[0].delta.content = " World"
        
        mock_message3 = MagicMock()
        mock_message3.choices = [MagicMock()]
        mock_message3.choices[0].delta.content = "!"
        
        with patch('utils.api.InferenceClient') as mock_client_class:
            mock_client = Mock()
            mock_client.chat_completion.return_value = [
                mock_message1,
                mock_message2,
                mock_message3,
            ]
            mock_client_class.return_value = mock_client
            
            client = SwarmClient(model="test-model", token="test-token")
            chunks = list(client.stream_swarm_response("test prompt"))
            
            assert len(chunks) == 3
            assert chunks[0] == "Hello"
            assert chunks[1] == "Hello World"
            assert chunks[2] == "Hello World!"
    
    def test_stream_swarm_response_handles_empty_chunks(self):
        """Test that empty chunks are skipped."""
        mock_message1 = MagicMock()
        mock_message1.choices = [MagicMock()]
        mock_message1.choices[0].delta.content = "Hello"
        
        mock_message2 = MagicMock()
        mock_message2.choices = [MagicMock()]
        mock_message2.choices[0].delta.content = ""  # Empty chunk
        
        mock_message3 = MagicMock()
        mock_message3.choices = [MagicMock()]
        mock_message3.choices[0].delta.content = " World"
        
        with patch('utils.api.InferenceClient') as mock_client_class:
            mock_client = Mock()
            mock_client.chat_completion.return_value = [
                mock_message1,
                mock_message2,
                mock_message3,
            ]
            mock_client_class.return_value = mock_client
            
            client = SwarmClient(model="test-model", token="test-token")
            chunks = list(client.stream_swarm_response("test prompt"))
            
            # Should only yield non-empty chunks
            assert len(chunks) == 2
            assert chunks[0] == "Hello"
            assert chunks[1] == "Hello World"
    
    def test_stream_swarm_response_passes_parameters(self):
        """Test that API parameters are passed correctly."""
        with patch('utils.api.InferenceClient') as mock_client_class:
            mock_client = Mock()
            mock_client.chat_completion.return_value = []
            mock_client_class.return_value = mock_client
            
            client = SwarmClient(model="test-model", token="test-token")
            list(client.stream_swarm_response(
                "test prompt",
                max_tokens=2048,
                temperature=0.9,
            ))
            
            mock_client.chat_completion.assert_called_once()
            call_kwargs = mock_client.chat_completion.call_args[1]
            assert call_kwargs["max_tokens"] == 2048
            assert call_kwargs["temperature"] == 0.9
            assert call_kwargs["stream"] is True
            assert call_kwargs["messages"] == [{"role": "user", "content": "test prompt"}]
    
    def test_stream_swarm_response_raises_exception(self):
        """Test that exceptions are propagated."""
        with patch('utils.api.InferenceClient') as mock_client_class:
            mock_client = Mock()
            mock_client.chat_completion.side_effect = Exception("API Error")
            mock_client_class.return_value = mock_client
            
            client = SwarmClient(model="test-model", token="test-token")
            
            with pytest.raises(Exception, match="API Error"):
                list(client.stream_swarm_response("test prompt"))

