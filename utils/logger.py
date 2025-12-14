"""Structured logging utilities for SwarmMaster."""

import logging
import sys
from typing import Optional
from datetime import datetime


class SwarmLogger:
    """Structured logger for SwarmMaster that avoids logging secrets."""
    
    _logger: Optional[logging.Logger] = None
    
    @staticmethod
    def _get_logger() -> logging.Logger:
        """Get or create the logger instance."""
        if SwarmLogger._logger is None:
            logger = logging.getLogger("swarmmaster")
            logger.setLevel(logging.INFO)
            
            # Avoid duplicate handlers
            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logging.INFO)
                
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            
            SwarmLogger._logger = logger
        
        return SwarmLogger._logger
    
    @staticmethod
    def log_swarm_start(task: str, model: str) -> None:
        """Log the start of a swarm execution."""
        logger = SwarmLogger._get_logger()
        logger.info(f"Swarm started - Model: {model}, Task length: {len(task)} chars")
    
    @staticmethod
    def log_swarm_complete(task: str, response_length: int) -> None:
        """Log the completion of a swarm execution."""
        logger = SwarmLogger._get_logger()
        logger.info(f"Swarm completed - Response length: {response_length} chars")
    
    @staticmethod
    def log_error(error_type: str, error_message: str, task: Optional[str] = None) -> None:
        """Log an error without exposing sensitive information."""
        logger = SwarmLogger._get_logger()
        task_info = f", Task length: {len(task)} chars" if task else ""
        logger.error(f"Error - Type: {error_type}, Message: {error_message[:100]}{task_info}")
    
    @staticmethod
    def log_config_change(setting: str, old_value: Optional[str] = None, new_value: Optional[str] = None) -> None:
        """Log configuration changes (without sensitive values)."""
        logger = SwarmLogger._get_logger()
        # Sanitize values to avoid logging tokens
        if "token" in setting.lower():
            old_value = "***" if old_value else None
            new_value = "***" if new_value else None
        logger.info(f"Config changed - {setting}: {old_value} -> {new_value}")

