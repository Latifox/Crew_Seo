"""
SEO Agency Test Mock

This module contains simplified versions of the SEO Agency components for testing purposes.
"""

from typing import Dict, Any

# Mock classes for testing
class MockTask:
    def __init__(self, human_input=False):
        self.human_input = human_input

class MockAgent:
    def __init__(self, role='Mock Agent'):
        self.role = role

class MockCrew:
    def __init__(self, 
                 process='hierarchical', 
                 manager_agent=None, 
                 memory=False,
                 memory_config=None,
                 planning=False):
        self.process = process
        self.manager_agent = manager_agent
        self.memory = memory
        self.memory_config = memory_config
        self.planning = planning

class MockSEOAgencyCrew:
    """Simplified version of SEOAgencyCrew for testing purposes."""
    
    def __init__(self):
        """Initialize the SEO Agency Crew mock."""
        self._init_mocks()
    
    def _init_mocks(self):
        """Initialize mock objects."""
        # Create mock SEO manager agent
        self._seo_manager = MockAgent(role="SEO Manager")
        
        # Create mock tasks with human input configuration
        self._content_creation_task = MockTask(human_input=True)
        self._technical_audit_task = MockTask(human_input=True)
        self._final_report_task = MockTask(human_input=True)
        
        # Create mock crew with our configuration
        self._crew = MockCrew(
            process='hierarchical',
            manager_agent=self._seo_manager,
            memory=True,
            memory_config={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            },
            planning=True
        )
    
    # Agent methods
    def seo_manager(self):
        """Return the SEO manager agent."""
        return self._seo_manager
    
    # Task methods
    def content_creation_task(self):
        """Return the content creation task."""
        return self._content_creation_task
    
    def technical_audit_task(self):
        """Return the technical audit task."""
        return self._technical_audit_task
    
    def seo_agency_report_task(self):
        """Return the final report task."""
        return self._final_report_task
    
    # Crew method
    def crew(self):
        """Return the SEO Agency crew."""
        return self._crew