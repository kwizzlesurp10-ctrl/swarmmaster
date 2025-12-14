"""Export utilities for SwarmMaster results."""

from datetime import datetime
from typing import Optional


def format_export_content(task: str, response: str, model: str, metadata: Optional[dict] = None) -> str:
    """
    Format swarm results for export.
    
    Args:
        task: The original task.
        response: The swarm response.
        model: The model used.
        metadata: Optional metadata dictionary.
        
    Returns:
        Formatted string ready for export.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    export_lines = [
        "=" * 80,
        "SwarmMaster Export",
        "=" * 80,
        f"Generated: {timestamp}",
        f"Model: {model}",
    ]
    
    if metadata:
        for key, value in metadata.items():
            export_lines.append(f"{key}: {value}")
    
    export_lines.extend([
        "",
        "=" * 80,
        "TASK",
        "=" * 80,
        task,
        "",
        "=" * 80,
        "SWARM RESPONSE",
        "=" * 80,
        response,
        "",
        "=" * 80,
    ])
    
    return "\n".join(export_lines)


def export_to_file(content: str, filename: Optional[str] = None) -> str:
    """
    Generate a filename for export.
    
    Args:
        content: The content to export.
        filename: Optional custom filename.
        
    Returns:
        Suggested filename.
    """
    if filename:
        return filename
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"swarmmaster_export_{timestamp}.txt"

