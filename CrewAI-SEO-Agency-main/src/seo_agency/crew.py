"""
SEO Agency Crew - Core orchestration module

This module defines the SEO Agency Crew, including all agents and tasks for
comprehensive SEO services.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
# Import agent configurations
from src.seo_agency.configurations import AGENT_CONFIGS

# Import string-based task definitions
from src.seo_agency.string_based_tasks import (
    KEYWORD_RESEARCH_DESCRIPTION, KEYWORD_RESEARCH_OUTPUT,
    COMPETITOR_ANALYSIS_DESCRIPTION, COMPETITOR_ANALYSIS_OUTPUT,
    CONTENT_STRATEGY_DESCRIPTION, CONTENT_STRATEGY_OUTPUT,
    TECHNICAL_AUDIT_DESCRIPTION, TECHNICAL_AUDIT_OUTPUT,
    ONPAGE_OPTIMIZATION_DESCRIPTION, ONPAGE_OPTIMIZATION_OUTPUT,
    BACKLINK_STRATEGY_DESCRIPTION, BACKLINK_STRATEGY_OUTPUT,
    CONTENT_CREATION_DESCRIPTION, CONTENT_CREATION_OUTPUT,
    ANALYTICS_REPORTING_DESCRIPTION, ANALYTICS_REPORTING_OUTPUT,
    SEO_AGENCY_REPORT_DESCRIPTION, SEO_AGENCY_REPORT_OUTPUT
)

# Handle knowledge sources for different versions of CrewAI
try:
    # For newer versions that use file_paths
    from crewai.datasources import FileDataSource as DirectoryKnowledgeSource
    from crewai.datasources import TextDataSource as StringKnowledgeSource
except ImportError:
    try:
        # For versions that still use knowledge module
        from crewai.datasources import DirectoryKnowledgeSource, StringKnowledgeSource
    except ImportError:
        # Fallback to our own implementation
        class DirectoryKnowledgeSource:
            def __init__(self, file_paths=None, path=None, description=None, metadata=None):
                # Support both new (file_paths) and old (path) parameter names
                self.file_paths = file_paths
                self.path = path
                self.description = description
                self.metadata = metadata or {}
                
        class StringKnowledgeSource:
            def __init__(self, content, description=None, metadata=None):
                self.content = content
                self.description = description
                self.metadata = metadata or {}

# Import crewai tools properly with fallbacks for different versions
try:
    # Try to import tools from crewai_tools
    from crewai_tools import SerperDevTool
    from crewai_tools.file_tools import FileReadTool, DirectoryReadTool
    from src.seo_agency.tools import FileWriteTool, GoogleSearchConsoleTool, ContentAnalysisTool, GooglePageSpeedTool, GoogleAnalyticsTool
except ImportError:
    try:
        # Try alternative import path
        from crewai_tools import SerperDevTool
        from crewai_tools.files import FileReadTool, DirectoryReadTool
        from src.seo_agency.tools import FileWriteTool, GoogleSearchConsoleTool, ContentAnalysisTool, GooglePageSpeedTool, GoogleAnalyticsTool
    except ImportError:
        # Final fallback to basic class definitions
        print("Warning: CrewAI tools not available. Using simple implementations.")
        
        # Import base tool class
        from crewai.tools import BaseTool
        
        # Define SerperDevTool
        class SerperDevTool(BaseTool):
            def __init__(self, api_key=None):
                super().__init__(
                    name="SerperDevTool",
                    description="Search the web for information",
                    return_direct=False
                )
                self.api_key = api_key or os.getenv("SERPER_API_KEY")
            
            def _run(self, query: str) -> str:
                return f"Results for: {query}"
        
        # Define FileReadTool
        class FileReadTool(BaseTool):
            def __init__(self):
                super().__init__(
                    name="FileReadTool",
                    description="Read the contents of a file",
                    return_direct=False
                )
            
            def _run(self, file_path: str) -> str:
                try:
                    with open(file_path, 'r') as f:
                        return f.read()
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            
        # Define DirectoryReadTool
        class DirectoryReadTool(BaseTool):
            def __init__(self):
                super().__init__(
                    name="DirectoryReadTool",
                    description="List the contents of a directory",
                    return_direct=False
                )
            
            def _run(self, directory_path: str) -> str:
                try:
                    return str(os.listdir(directory_path))
                except Exception as e:
                    return f"Error reading directory: {str(e)}"
        
        # Import our custom tools but ensure they inherit from BaseTool
        from src.seo_agency.tools import FileWriteTool, GoogleSearchConsoleTool, ContentAnalysisTool, GooglePageSpeedTool, GoogleAnalyticsTool

# Try to implement a simple YAML-to-JSON conversion utility for CrewAI configurations
try:
    from crewai.utilities.project_utils import load_yaml
    # If successful, log it
    print("Successfully imported YAML utilities from CrewAI")
except ImportError:
    print("YAML utilities not available in this CrewAI version")

@CrewBase
class SEOAgencyCrew:
    """
    SEO Agency Crew - A team of specialized agents for comprehensive SEO services.
    
    This crew handles all aspects of SEO including keyword research, competitor analysis,
    content strategy, technical audits, and more.
    """
    
    def __init__(self) -> None:
        """Initialize the SEO Agency Crew."""
        
        # Initialize configuration
        self.agents_config = AGENT_CONFIGS
        
        # Initialize knowledge sources to None by default
        self.seo_best_practices = None
        self.algorithm_updates = None
        self.search_tool = None
        self.file_read_tool = None
        self.file_write_tool = None
        self.directory_read_tool = None
        self.search_console_tool = None
        self.content_analysis_tool = None
        self.pagespeed_tool = None
        self.analytics_tool = None
        self.firecrawl_tool = None  # Add the FireCrawl tool
        self.openlit_available = False
        
        try:
            # Initialize tools
            self.search_tool = SerperDevTool()
            self.file_read_tool = FileReadTool()
            self.file_write_tool = FileWriteTool()
            self.directory_read_tool = DirectoryReadTool()
            
            # Initialize Google tools with proper fallbacks
            try:
                self.search_console_tool = GoogleSearchConsoleTool()
                self.content_analysis_tool = ContentAnalysisTool()
                self.pagespeed_tool = GooglePageSpeedTool()
                self.analytics_tool = GoogleAnalyticsTool()
                print("✅ All Google tools initialized successfully")
            except Exception as e:
                print(f"⚠️  Some Google tools could not be initialized: {str(e)}")
                # Fallbacks already set to None above
            
            # Initialize FireCrawl tool
            try:
                from src.seo_agency.tools.firecrawl_tool import FireCrawlTool
                self.firecrawl_tool = FireCrawlTool()
                print("✅ FireCrawl tool initialized successfully")
            except Exception as e:
                print(f"⚠️  FireCrawl tool could not be initialized: {str(e)}")
                # Fallback already set to None above
            
            # Initialize knowledge sources - more robust handling for different CrewAI versions
            try:
                # Try importing from the latest location
                try:
                    from crewai.datasources import FileDataSource
                    
                    # Use the latest datasource approach
                    self.seo_best_practices = FileDataSource(
                        name="SEO Best Practices",
                        description="SEO best practices and guidelines for 2025",
                        files=["knowledge/seo_best_practices.txt"]
                    )
                    
                    self.algorithm_updates = FileDataSource(
                        name="Algorithm Updates",
                        description="Latest Google algorithm updates and their implications",
                        files=["knowledge/google_algorithm_updates.txt"]
                    )
                    
                except (ImportError, AttributeError):
                    # Try alternative import paths
                    try:
                        from crewai.tools import FileDataSource
                        
                        self.seo_best_practices = FileDataSource(
                            name="SEO Best Practices",
                            description="SEO best practices and guidelines for 2025",
                            files=["knowledge/seo_best_practices.txt"]
                        )
                        
                        self.algorithm_updates = FileDataSource(
                            name="Algorithm Updates",
                            description="Latest Google algorithm updates and their implications",
                            files=["knowledge/google_algorithm_updates.txt"]
                        )
                    except ImportError:
                        # Knowledge sources already set to None above
                        print("Warning: Knowledge sources could not be initialized. Working with limited knowledge.")
            except Exception as e:
                # If all attempts fail, knowledge sources already set to None above
                print(f"Warning: Knowledge sources initialization failed: {str(e)}. Working with limited knowledge.")
            
            # Initialize task outputs storage
            self.task_outputs = {}
            
            # Check if OpenLIT is available
            try:
                import openlit
                self.openlit_available = True
            except ImportError:
                pass
        except Exception as e:
            print(f"⚠️  Error initializing tools: {str(e)}")
            # Tools already set to None above
        
    @before_kickoff
    def prepare_environment(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare the environment before starting the crew.
        
        Args:
            inputs: Input parameters for the crew.
            
        Returns:
            The updated inputs dictionary.
        """
        # Save inputs for task creation
        self.current_inputs = inputs
        
        # Ensure output directory exists
        output_dir = inputs.get('output_dir', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Starting SEO Agency for website: {inputs.get('website', 'Not specified')}")
        print(f"Industry/Niche: {inputs.get('niche', 'Not specified')}")
        
        if inputs.get('specific_focus'):
            print(f"Specific Focus: {inputs['specific_focus']}")
            
        print("\nInitializing agents and tasks...\n")
        
        # Record OpenLIT span for this crew run if available
        try:
            import openlit
            from openlit.span import Span
            
            # Create a top-level span for this crew run
            with Span(
                name="seo_agency_crew_run",
                attributes={
                    "website": inputs.get('website', 'Not specified'),
                    "niche": inputs.get('niche', 'Not specified'),
                    "specific_focus": inputs.get('specific_focus', ''),
                    "output_dir": output_dir,
                    "tasks": inputs.get('tasks', 'full_strategy')
                }
            ):
                print("OpenLIT monitoring active for this crew run")
        except (ImportError, Exception) as e:
            # If OpenLIT is not available or there's an error, continue without it
            print(f"OpenLIT monitoring not available or error: {e}")
        
        return inputs
    
    @after_kickoff
    def process_results(self, result: Any) -> Any:
        """
        Process the results after the crew execution.
        
        Args:
            result: The result from the crew execution.
            
        Returns:
            The processed result.
        """
        print("\nSEO Agency tasks completed successfully!")
        print("All reports have been saved to the output directory.")
        
        # Record completion in OpenLIT if available
        try:
            import openlit
            from openlit.span import Span
            
            with Span(
                name="seo_agency_results_processing",
                attributes={
                    "result_length": len(str(result)) if result else 0,
                    "result_type": type(result).__name__,
                    "status": "success"
                }
            ):
                print("Results recorded in OpenLIT monitoring")
        except (ImportError, Exception):
            # If OpenLIT is not available or there's an error, continue without it
            pass
        
        return result
    
    # Agent definitions
    @agent
    def seo_manager(self) -> Agent:
        """Create the SEO Manager agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool,
                    self.directory_read_tool, self.search_console_tool,
                    self.analytics_tool, self.pagespeed_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Create the agent with proper parameters
        config = self.agents_config['seo_manager']
        
        # Use role and other parameters directly if config is not compatible
        return Agent(
            role=config.get('role', "SEO Manager"), 
            goal=config.get('goal', "Manage SEO strategy"),
            backstory=config.get('backstory', "Experienced SEO professional"),
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            allow_delegation=True,
            verbose=True
        )
        
    @agent
    def keyword_researcher(self) -> Agent:
        """Create the Keyword Research Specialist agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Create the agent config
        config = self.agents_config.get('keyword_researcher', {})
        
        # Create the agent using the config
        return Agent(
            role=config.get('role', "Senior Keyword Research Specialist"),
            goal=config.get('goal', "Identify high-potential keywords for SEO"),
            backstory=config.get('backstory', "Expert in keyword research and analysis"),
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            allow_delegation=False,
            verbose=True
        )
    
    @agent
    def competitor_analyst(self) -> Agent:
        """Create the Competitor Analysis Expert agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        if self.algorithm_updates is not None:
            knowledge_sources.append(self.algorithm_updates)
        
        # Create the agent config
        config = self.agents_config.get('competitor_analyst', {})
        
        # Create the agent with safe defaults
        return Agent(
            role=config.get('role', "Expert SEO Competitor Analyst"),
            goal=config.get('goal', "Analyze competitors to identify opportunities"),
            backstory=config.get('backstory', "Strategic analyst who uncovers competitor strategies"),
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=False,
            verbose=True
        )
    
    @agent
    def content_strategist(self) -> Agent:
        """Create the Content Strategy Director agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool, self.content_analysis_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        if self.algorithm_updates is not None:
            knowledge_sources.append(self.algorithm_updates)
        
        # Create the agent config
        config = self.agents_config.get('content_strategist', {})
        
        # Create the agent with safe defaults
        return Agent(
            role=config.get('role', "Lead Content Strategy Director"),
            goal=config.get('goal', "Develop comprehensive content strategies"),
            backstory=config.get('backstory', "Visionary content strategist with expertise in SEO"),
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=True,
            verbose=True
        )
    
    @agent
    def onpage_optimizer(self) -> Agent:
        """Create the On-Page SEO Optimization Expert agent."""
        # Filter out None values from tools and knowledge sources
        tools = []
        for tool in [
            self.search_tool, 
            self.file_read_tool, 
            self.file_write_tool, 
            self.content_analysis_tool,
            self.firecrawl_tool,  # Add the FireCrawl tool
            self.pagespeed_tool  # Add PageSpeed tool for performance analysis
        ]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        
        # Create the agent with the filtered tools and knowledge sources
        return Agent(
            config=self.agents_config['onpage_optimizer'],
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=False,
            verbose=True
        )
    
    @agent
    def technical_auditor(self) -> Agent:
        """Create the Technical SEO Audit Specialist agent."""
        # Filter out None values from tools and knowledge sources
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool, self.search_console_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        if self.algorithm_updates is not None:
            knowledge_sources.append(self.algorithm_updates)
        
        # Create the agent with the filtered tools and knowledge sources
        return Agent(
            config=self.agents_config['technical_auditor'],
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=False,
            verbose=True
        )
    
    @agent
    def backlink_strategist(self) -> Agent:
        """Create the Backlink Acquisition and Strategy Expert agent."""
        # Filter out None values from tools and knowledge sources
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        
        # Create the agent with the filtered tools and knowledge sources
        return Agent(
            config=self.agents_config['backlink_strategist'],
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=False,
            verbose=True
        )
        
    @agent
    def analytics_reporter(self) -> Agent:
        """Create the Analytics Reporter agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool, 
                    self.analytics_tool, self.search_console_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        
        # Create the agent with proper parameters
        config = self.agents_config.get('analytics_reporter', {})
        
        # Use role and other parameters directly
        return Agent(
            role=config.get('role', "Analytics Reporting Specialist"),
            goal=config.get('goal', "Generate comprehensive analytics reports and insights"),
            backstory=config.get('backstory', "You are an experienced analytics specialist who excels at extracting meaningful insights from data. "
                               "You have a deep understanding of web analytics, user behavior, and SEO performance metrics."),
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=False,
            verbose=True
        )
    
    @agent
    def content_creator(self) -> Agent:
        """Create the SEO Content Creator agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool, self.content_analysis_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.seo_best_practices is not None:
            knowledge_sources.append(self.seo_best_practices)
        if self.algorithm_updates is not None:
            knowledge_sources.append(self.algorithm_updates)
        
        # Important: Per requirements, we MUST use Anthropic's Claude model for content creation
        # This provides more creative, engaging content than other models
        try:
            return Agent(
                config=self.agents_config['content_creator'],
                llm="anthropic/claude-3-7-sonnet-20250219",  # REQUIRED: Claude for content creation
                tools=tools,
                knowledge_sources=knowledge_sources if knowledge_sources else None,
                allow_delegation=False,
                verbose=True
            )
        except TypeError as e:
            # Alternative initialization for newer CrewAI versions
            print(f"Trying alternative Agent initialization for Content Creator: {str(e)}")
            return Agent(
                config=self.agents_config['content_creator'],
                llm="anthropic/claude-3-7-sonnet-20250219",  # REQUIRED: Claude for content creation
                tools=tools,
                allow_delegation=False,
                verbose=True
            )
    
    @agent
    def analytics_specialist(self) -> Agent:
        """Create the SEO Analytics and Reporting Specialist agent."""
        # Filter out None values from tools
        tools = []
        for tool in [self.search_tool, self.file_read_tool, self.file_write_tool, self.search_console_tool]:
            if tool is not None:
                tools.append(tool)
        
        # Filter out None values from knowledge sources
        knowledge_sources = []
        if self.algorithm_updates is not None:
            knowledge_sources.append(self.algorithm_updates)
        
        # Create the agent with the filtered tools and knowledge sources
        return Agent(
            config=self.agents_config['analytics_specialist'],
            llm="openai/gpt-4o-2024-08-06",
            tools=tools,
            knowledge_sources=knowledge_sources if knowledge_sources else None,
            allow_delegation=False,
            verbose=True
        )
    
    # Task definitions
    @task
    def keyword_research_task(self) -> Task:
        """Create the keyword research task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        focus_text = f"Focus on {inputs.get('specific_focus')}." if inputs.get('specific_focus') else ""
        
        description = KEYWORD_RESEARCH_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry'),
            focus_text=focus_text
        )
        
        return Task(
            description=description,
            expected_output=KEYWORD_RESEARCH_OUTPUT,
            output_file='output/keyword_research_report.md'
        )
    
    @task
    def competitor_analysis_task(self) -> Task:
        """Create the competitor analysis task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        focus_text = f"Focus on {inputs.get('specific_focus')}." if inputs.get('specific_focus') else ""
        
        description = COMPETITOR_ANALYSIS_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry'),
            focus_text=focus_text
        )
        
        return Task(
            description=description,
            expected_output=COMPETITOR_ANALYSIS_OUTPUT,
            output_file='output/competitor_analysis_report.md'
        )
    
    @task
    def content_strategy_task(self) -> Task:
        """Create the content strategy task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        focus_text = f"Focus on {inputs.get('specific_focus')}." if inputs.get('specific_focus') else ""
        
        description = CONTENT_STRATEGY_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry'),
            focus_text=focus_text
        )
        
        return Task(
            description=description,
            expected_output=CONTENT_STRATEGY_OUTPUT,
            output_file='output/content_strategy_plan.md'
        )
    
    @task
    def technical_audit_task(self) -> Task:
        """Create the technical SEO audit task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        
        description = TECHNICAL_AUDIT_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry')
        )
        
        return Task(
            description=description,
            expected_output=TECHNICAL_AUDIT_OUTPUT,
            human_input=True,  # Enable human review for technical audits
            output_file='output/technical_audit_report.md'
        )
    
    @task
    def onpage_optimization_task(self) -> Task:
        """Create the on-page optimization task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        focus_text = f"Focus on {inputs.get('specific_focus')}." if inputs.get('specific_focus') else ""
        
        description = ONPAGE_OPTIMIZATION_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry'),
            focus_text=focus_text
        )
        
        return Task(
            description=description,
            expected_output=ONPAGE_OPTIMIZATION_OUTPUT,
            output_file='output/onpage_optimization_report.md'
        )
    
    @task
    def backlink_strategy_task(self) -> Task:
        """Create the backlink strategy task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        focus_text = f"Focus on {inputs.get('specific_focus')}." if inputs.get('specific_focus') else ""
        
        description = BACKLINK_STRATEGY_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry'),
            focus_text=focus_text
        )
        
        return Task(
            description=description,
            expected_output=BACKLINK_STRATEGY_OUTPUT,
            output_file='output/backlink_strategy_plan.md'
        )
    
    @task
    def content_creation_task(self) -> Task:
        """Create the content creation task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        focus_text = f"Focus on {inputs.get('specific_focus')}." if inputs.get('specific_focus') else ""
        
        # Get the special content prompt if available
        content_prompt = inputs.get('content_prompt', '')
        
        # Create an enhanced description that includes the special content prompt
        description = CONTENT_CREATION_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry'),
            focus_text=focus_text
        )
        
        # Append the content prompt to the description
        if content_prompt:
            description += f"\n\nIMPORTANT: Follow these specific content creation guidelines:\n{content_prompt}"
        
        return Task(
            description=description,
            expected_output=CONTENT_CREATION_OUTPUT,
            human_input=True,  # Enable human review
            agent=self.content_creator(),  # Explicitly assign the content_creator agent to ensure it uses Claude
            output_file='output/created_content.md'
        )
    
    @task
    def analytics_reporting_task(self) -> Task:
        """Create the analytics and reporting task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        
        description = ANALYTICS_REPORTING_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry')
        )
        
        return Task(
            description=description,
            expected_output=ANALYTICS_REPORTING_OUTPUT,
            output_file='output/analytics_reporting_framework.md'
        )
    
    @task
    def seo_agency_report_task(self) -> Task:
        """Create the final SEO agency report task."""
        # Format task description with input values
        inputs = self._get_current_inputs()
        
        description = SEO_AGENCY_REPORT_DESCRIPTION.format(
            website=inputs.get('website', 'the target website'),
            niche=inputs.get('niche', 'the target industry')
        )
        
        return Task(
            description=description,
            expected_output=SEO_AGENCY_REPORT_OUTPUT,
            human_input=True,  # Enable human review for the final report
            output_file='output/seo_strategy_report.md'
        )
    
    def _get_current_inputs(self) -> Dict[str, Any]:
        """
        Helper method to get current inputs.
        Returns default values if no inputs are available.
        """
        # This is a best effort to get inputs that may not be available during initialization
        try:
            inputs = getattr(self, 'current_inputs', {}) or {}
            if not inputs:
                # Fallback to empty dict with defaults
                inputs = {
                    'website': 'the target website',
                    'niche': 'the target industry',
                    'specific_focus': ''
                }
            return inputs
        except:
            # Ultimate fallback
            return {
                'website': 'the target website',
                'niche': 'the target industry',
                'specific_focus': ''
            }
    
    def _configure_agent_monitoring(self, agent, role):
        """
        Configure OpenLIT monitoring for an agent if available.
        
        Args:
            agent: The agent to configure
            role: The role of the agent
            
        Returns:
            The configured agent
        """
        if not self.openlit_available:
            return agent
            
        try:
            import openlit
            from openlit.modules.crewai import instrument_crewai
            
            # Configure OpenLIT to track this agent
            instrument_crewai()
            
            # Add OpenLIT custom attributes to the agent for better tracking
            agent.openlit_attributes = {
                "agent.role": role,
                "agent.llm": agent.llm.model_name if hasattr(agent.llm, 'model_name') else str(agent.llm),
                "agent.delegation": str(agent.allow_delegation),
                "agent.tools_count": len(agent.tools) if hasattr(agent, 'tools') else 0,
            }
            
            return agent
        except Exception as e:
            print(f"Warning: Unable to configure OpenLIT monitoring for agent {role}: {e}")
            return agent
    
    @crew
    def crew(self) -> Crew:
        """
        Create the SEO Agency Crew with all agents and tasks.
        
        Returns:
            A configured Crew instance ready to execute SEO tasks.
        """
        # Create and monitor manager agent
        manager = self._configure_agent_monitoring(self.seo_manager(), "seo_manager")
        
        # Create regular agents (excluding manager)
        regular_agents = [
            self._configure_agent_monitoring(self.keyword_researcher(), "keyword_researcher"),
            self._configure_agent_monitoring(self.competitor_analyst(), "competitor_analyst"),
            self._configure_agent_monitoring(self.content_strategist(), "content_strategist"),
            self._configure_agent_monitoring(self.onpage_optimizer(), "onpage_optimizer"),
            self._configure_agent_monitoring(self.technical_auditor(), "technical_auditor"),
            self._configure_agent_monitoring(self.backlink_strategist(), "backlink_strategist"),
            self._configure_agent_monitoring(self.content_creator(), "content_creator"),
            self._configure_agent_monitoring(self.analytics_specialist(), "analytics_specialist")
        ]
        
        return Crew(
            agents=regular_agents,  # Manager agent is NOT included in the agents list
            tasks=[
                self.keyword_research_task(),
                self.competitor_analysis_task(),
                self.content_strategy_task(),
                self.technical_audit_task(),
                self.onpage_optimization_task(),
                self.backlink_strategy_task(),
                self.content_creation_task(),
                self.analytics_reporting_task(),
                self.seo_agency_report_task()
            ],
            process=Process.hierarchical,  # Use hierarchical process
            manager_agent=manager,  # Use the monitored manager agent
            verbose=True,
            memory=True,  # Enable memory for context retention
            planning=True,  # Enable planning
            memory_config={
                "provider": "openai",  # Use OpenAI for embeddings
                "config": {
                    "model": "text-embedding-3-small"  # Use a smaller, cost-effective model for embeddings
                }
            }
        )
    
    # Helper methods for running individual task groups
    def run_keyword_research(self, inputs: Dict[str, Any]) -> Any:
        """Run only the keyword research task."""
        # Apply OpenLIT monitoring
        keyword_researcher = self._configure_agent_monitoring(
            self.keyword_researcher(), "keyword_researcher"
        )
        
        # Create a crew with OpenLIT monitoring
        try:
            import openlit
            from openlit.span import Span
            
            with Span(
                name="keyword_research_run",
                attributes={
                    "website": inputs.get('website', 'Not specified'),
                    "niche": inputs.get('niche', 'Not specified')
                }
            ):
                crew = Crew(
                    agents=[keyword_researcher],
                    tasks=[self.keyword_research_task()],
                    process=Process.sequential,
                    verbose=True
                )
                return crew.kickoff(inputs=inputs)
        except (ImportError, Exception):
            # Fallback without OpenLIT span if not available
            crew = Crew(
                agents=[keyword_researcher],
                tasks=[self.keyword_research_task()],
                process=Process.sequential,
                verbose=True
            )
            return crew.kickoff(inputs=inputs)
    
    def run_content_strategy(self, inputs: Dict[str, Any]) -> Any:
        """Run content strategy related tasks."""
        # Apply OpenLIT monitoring to all agents
        keyword_researcher = self._configure_agent_monitoring(
            self.keyword_researcher(), "keyword_researcher"
        )
        competitor_analyst = self._configure_agent_monitoring(
            self.competitor_analyst(), "competitor_analyst"
        )
        content_strategist = self._configure_agent_monitoring(
            self.content_strategist(), "content_strategist"
        )
        
        # Create a crew with OpenLIT monitoring
        try:
            import openlit
            from openlit.span import Span
            
            with Span(
                name="content_strategy_run",
                attributes={
                    "website": inputs.get('website', 'Not specified'),
                    "niche": inputs.get('niche', 'Not specified'),
                    "specific_focus": inputs.get('specific_focus', ''),
                    "agent_count": 3,
                    "task_count": 3
                }
            ):
                crew = Crew(
                    agents=[
                        keyword_researcher,
                        competitor_analyst,
                        content_strategist
                    ],
                    tasks=[
                        self.keyword_research_task(),
                        self.competitor_analysis_task(),
                        self.content_strategy_task()
                    ],
                    process=Process.sequential,
                    verbose=True
                )
                return crew.kickoff(inputs=inputs)
        except (ImportError, Exception):
            # Fallback without OpenLIT span if not available
            crew = Crew(
                agents=[
                    keyword_researcher,
                    competitor_analyst,
                    content_strategist
                ],
                tasks=[
                    self.keyword_research_task(),
                    self.competitor_analysis_task(),
                    self.content_strategy_task()
                ],
                process=Process.sequential,
                verbose=True
            )
            return crew.kickoff(inputs=inputs)
    
    def run_technical_seo(self, inputs: Dict[str, Any]) -> Any:
        """Run technical SEO related tasks."""
        # Apply OpenLIT monitoring to all agents
        technical_auditor = self._configure_agent_monitoring(
            self.technical_auditor(), "technical_auditor"
        )
        onpage_optimizer = self._configure_agent_monitoring(
            self.onpage_optimizer(), "onpage_optimizer"
        )
        
        # Create a crew with OpenLIT monitoring
        try:
            import openlit
            from openlit.span import Span
            
            with Span(
                name="technical_seo_run",
                attributes={
                    "website": inputs.get('website', 'Not specified'),
                    "niche": inputs.get('niche', 'Not specified'),
                    "specific_focus": inputs.get('specific_focus', ''),
                    "agent_count": 2,
                    "task_count": 2
                }
            ):
                crew = Crew(
                    agents=[
                        technical_auditor,
                        onpage_optimizer
                    ],
                    tasks=[
                        self.technical_audit_task(),
                        self.onpage_optimization_task()
                    ],
                    process=Process.sequential,
                    verbose=True
                )
                return crew.kickoff(inputs=inputs)
        except (ImportError, Exception):
            # Fallback without OpenLIT span if not available
            crew = Crew(
                agents=[
                    technical_auditor,
                    onpage_optimizer
                ],
                tasks=[
                    self.technical_audit_task(),
                    self.onpage_optimization_task()
                ],
                process=Process.sequential,
                verbose=True
            )
            return crew.kickoff(inputs=inputs)