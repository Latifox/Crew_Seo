"""
File Write Tool

This tool provides a way to write content to files for SEO reports and other outputs.
It follows the BaseTool interface for CrewAI 0.108.0+.
"""

import os
from typing import Dict, Any, Optional, Type
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class FileWriteInput(BaseModel):
    """Input schema for FileWriteTool."""
    file_path: str = Field(..., description="The path to the file to write to")
    content: str = Field(..., description="The content to write to the file")

class FileWriteTool(BaseTool):
    """Tool for writing content to a file."""
    
    name: str = "File Write Tool"
    description: str = "Use this tool to write content to a file."
    args_schema: Type[BaseModel] = FileWriteInput
    
    def _run(self, file_path: str, content: str) -> str:
        """
        Write content to a file.
        
        Args:
            file_path: The path to the file to write to
            content: The content to write to the file
            
        Returns:
            A string confirming the content was written successfully
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Content successfully written to {file_path}"
    
    def run(self, tool_input: Dict[str, Any]) -> str:
        """
        Run the tool with the input provided.
        
        Args:
            tool_input: Dictionary containing file_path and content keys
            
        Returns:
            A string confirming the content was written successfully
        """
        # Parse and validate the input
        parsed_input = FileWriteInput(**tool_input)
        
        # Execute the tool with validated input
        return self._run(
            file_path=parsed_input.file_path,
            content=parsed_input.content
        ) 