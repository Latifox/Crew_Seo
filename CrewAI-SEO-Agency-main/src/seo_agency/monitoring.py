"""
SEO Agency Monitoring Module

This module provides monitoring and observability for the SEO Agency using OpenLIT.
"""

import os
import sys
import traceback
from typing import Any, Dict, List, Optional

# Check if openlit is installed, if not, provide guidance for installation
try:
    from openlit import Tracer
    from openlit.constants import ModelVendor
    HAS_OPENLIT = True
except ImportError:
    HAS_OPENLIT = False
    print("OpenLIT is not installed. To use monitoring, install it with: pip install openlit")


class SEOAgencyTracer:
    """
    SEO Agency tracer that provides monitoring and observability using OpenLIT.
    
    This class integrates with OpenLIT to provide visibility into agent operations,
    model usage, and task execution in the SEO Agency.
    """
    
    def __init__(
        self,
        project_id: str = "seo-agency",
        environment: str = "development",
        version: str = "0.1.0"
    ):
        """Initialize the SEO Agency tracer.
        
        Args:
            project_id: The project ID for OpenLIT
            environment: The environment name (e.g., "development", "production")
            version: The version of the application
        """
        self.project_id = project_id
        self.environment = environment
        self.version = version
        self.tracer = None
        
        if not HAS_OPENLIT:
            print("WARNING: OpenLIT is not installed. Monitoring will be disabled.")
            return
        
        try:
            # Initialize the OpenLIT tracer
            self.tracer = Tracer(
                project_id=project_id,
                metadata={
                    "environment": environment,
                    "version": version,
                    "application": "seo-agency"
                }
            )
            print(f"OpenLIT tracer initialized for project: {project_id}")
        except Exception as e:
            print(f"ERROR initializing OpenLIT tracer: {str(e)}")
            traceback.print_exc()
            self.tracer = None
    
    def get_callback(self):
        """Get the OpenLIT callback for CrewAI to use.
        
        Returns:
            The OpenLIT callback or None if OpenLIT is not available
        """
        if self.tracer:
            return self.tracer.get_callback()
        return None
    
    def record_error(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Record an error event.
        
        Args:
            message: The error message
            details: Additional details about the error
        """
        if self.tracer:
            self.tracer.add_event(
                event_type="error",
                message=message,
                metadata=details or {}
            )
    
    def record_custom_event(self, event_type: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Record a custom event.
        
        Args:
            event_type: The type of event
            message: The event message
            metadata: Additional metadata for the event
        """
        if self.tracer:
            self.tracer.add_event(
                event_type=event_type,
                message=message,
                metadata=metadata or {}
            )


# Create a singleton instance of the tracer to be used across the application
seo_agency_tracer = SEOAgencyTracer()