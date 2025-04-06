#!/usr/bin/env python
"""
Simplified SEO Crew Runner

This script runs a simplified version of the SEO analysis with a custom FileWriteTool
implementation that is compatible with CrewAI 0.108.0.
"""

import os
import sys
import logging
from typing import Dict, Any, List
from pathlib import Path
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("simplified_crew.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SimplifiedCrew")

# Import CrewAI components
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Define a custom FileWriteTool that follows CrewAI 0.108.0 BaseTool interface
class FileWriteInput(BaseModel):
    """Input for writing to a file."""
    file_path: str = Field(..., description="The path to the file to write to")
    content: str = Field(..., description="The content to write to the file")

class FileWriteTool(BaseTool):
    """Tool for writing content to a file."""
    
    name: str = "File Write Tool"
    description: str = "Use this tool to write content to a file."
    
    def _run(self, file_path: str, content: str) -> str:
        """Write content to a file."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        return f"Content successfully written to {file_path}"
    
    def run(self, tool_input: Dict[str, Any]) -> str:
        """Run the tool with the input provided."""
        try:
            # Parse input with validation
            parsed_input = FileWriteInput(**tool_input)
            
            # Execute the tool with validated input
            return self._run(
                file_path=parsed_input.file_path,
                content=parsed_input.content
            )
        except Exception as e:
            return f"Error writing to file: {str(e)}"

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Simplified SEO Crew - Run a simplified SEO analysis"
    )
    
    parser.add_argument(
        "--website", 
        type=str, 
        default="https://eatonassoc.com",
        help="The website to analyze and optimize"
    )
    
    parser.add_argument(
        "--niche", 
        type=str, 
        default="Managed IT Solutions",
        help="The industry or niche of the website"
    )
    
    parser.add_argument(
        "--focus", 
        type=str, 
        default="IT Support, Managed IT Services, IT Consulting",
        help="Specific focus areas within the niche"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="output",
        help="Directory to store output reports"
    )
    
    return parser.parse_args()

def setup_environment() -> None:
    """Load environment variables and set up the environment."""
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    required_keys = ["OPENAI_API_KEY", "SERPER_API_KEY"]
    
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.error(f"Missing required API keys: {', '.join(missing_keys)}")
        logger.error("Please add them to your .env file.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    logger.info("✅ Environment setup complete")

def run_simplified_crew(args: argparse.Namespace) -> None:
    """Run a simplified SEO analysis with our fixed tools."""
    website = args.website
    niche = args.niche
    focus = args.focus
    output_dir = args.output_dir
    
    logger.info(f"Starting simplified SEO analysis for {website}")
    logger.info(f"Industry/Niche: {niche}")
    logger.info(f"Specific focus: {focus}")
    
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Initialize tools
    serper_tool = SerperDevTool()
    file_tool = FileWriteTool()
    
    # Create the agents
    keyword_researcher = Agent(
        role=f"SEO Keyword Research Specialist for {niche}",
        goal=f"Discover the most valuable keywords for {website} in the {niche} industry",
        backstory=f"""You're a data-driven keyword research expert with 10+ years of experience in SEO. 
            You have an exceptional ability to uncover valuable search terms that competitors have missed.
            You understand search intent deeply and can identify patterns in user behavior. 
            Your keyword research has helped numerous businesses increase their organic traffic by over 200%.""",
        tools=[serper_tool]
    )
    
    competitor_analyst = Agent(
        role=f"Expert SEO Competitor Analyst for {niche}",
        goal=f"Thoroughly analyze competitors to identify their strengths, weaknesses, and untapped opportunities",
        backstory=f"""You're a strategic competitor analysis specialist with a background in both SEO and market research.
            You've helped Fortune 500 companies outmaneuver their competition by finding overlooked opportunities.
            Your analytical skills allow you to reverse-engineer successful strategies and identify critical gaps.
            You're known for your comprehensive reports that turn complex competitive landscapes into actionable insights.""",
        tools=[serper_tool]
    )
    
    content_strategist = Agent(
        role=f"Lead Content Strategy Director for {niche}",
        goal=f"Develop comprehensive content strategies that align with SEO goals and provide exceptional value to users",
        backstory=f"""You're a visionary content strategist who has overseen content operations for major digital publications.
            Your expertise lies in creating scalable content frameworks that drive both engagement and conversions.
            You understand how to balance search engine requirements with user experience and brand voice.
            Your strategies have helped companies establish thought leadership and dominate their niches.""",
        tools=[serper_tool, file_tool]
    )
    
    # Define the tasks
    keyword_research_task = Task(
        description=f"""Conduct comprehensive keyword research for {website} in the {niche} industry with focus on {focus}.
            Identify primary keywords (high volume, high competition), secondary keywords (medium volume, medium competition),
            and long-tail opportunities (lower volume, lower competition).
            Analyze search intent for these keywords and categorize them accordingly.
            Prioritize keywords based on relevance, search volume, competition, and conversion potential.
            Provide a detailed report with your findings and recommendations.""",
        agent=keyword_researcher,
        expected_output="A comprehensive keyword research report with categorized keywords and recommendations."
    )
    
    competitor_analysis_task = Task(
        description=f"""Identify the top 5 competitors for {website} in the {niche} industry for the following areas: {focus}.
            Analyze their SEO strategies, including keyword targeting, content strategies, backlink profiles, and technical setup.
            Determine their strengths and weaknesses, and identify opportunities for {website} to gain competitive advantage.
            Focus on actionable insights that can be implemented quickly.
            Include a detailed breakdown of each competitor's strategy and a comparative analysis.""",
        agent=competitor_analyst,
        expected_output="A detailed competitor analysis report with actionable insights."
    )
    
    content_strategy_task = Task(
        description=f"""Based on the keyword research and competitor analysis, develop a comprehensive content strategy for {website}.
            The strategy should outline content themes, topics, formats, and publication frequency.
            Include recommendations for optimizing existing content and creating new high-value content.
            Provide specific content ideas with target keywords, search intent, and outline suggestions.
            The strategy should align with the business focus areas: {focus}.""",
        agent=content_strategist,
        context=[keyword_research_task, competitor_analysis_task],
        expected_output="A detailed content strategy document with specific recommendations and content ideas.",
        output_file=f"{output_dir}/simplified_content_strategy.md"
    )
    
    # Create the crew
    seo_crew = Crew(
        agents=[keyword_researcher, competitor_analyst, content_strategist],
        tasks=[keyword_research_task, competitor_analysis_task, content_strategy_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Run the crew
    result = seo_crew.kickoff()
    
    logger.info("Simplified SEO analysis completed")
    logger.info(f"Results saved to {output_dir}/simplified_content_strategy.md")
    
    return result

def main() -> None:
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up environment
    setup_environment()
    
    print("\n" + "=" * 70)
    print(f"SIMPLIFIED SEO ANALYSIS FOR {args.website}")
    print(f"Niche: {args.niche}")
    print(f"Focus: {args.focus}")
    print("=" * 70 + "\n")
    
    # Run SEO analysis
    run_simplified_crew(args)
    
    print("\n" + "=" * 70)
    print("SIMPLIFIED SEO ANALYSIS COMPLETE")
    print(f"Check output directory for detailed reports: {args.output_dir}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main() 