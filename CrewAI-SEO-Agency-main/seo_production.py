#!/usr/bin/env python
"""
SEO Production Pipeline

A comprehensive SEO analysis and optimization pipeline using CrewAI that properly
implements all agents, tasks, tools, and knowledge integration.
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("seo_production.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SEOProduction")

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
logger.info(f"Added {os.path.dirname(os.path.abspath(__file__))} to Python path")

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded from .env file")

# Import CrewAI components with proper fallbacks
from crewai import Agent, Task, Crew, Process

# Handle different versions of CrewAI
try:
    # Try the newer import path
    from crewai.datasources import FileDataSource
    logger.info("Using crewai.datasources.FileDataSource")
except ImportError:
    try:
        # Try alternative import path
        from crewai.tools import FileDataSource
        logger.info("Using crewai.tools.FileDataSource")
    except ImportError:
        try:
            # Try legacy knowledge module
            from crewai.knowledge import DirectoryKnowledgeSource as FileDataSource
            logger.info("Using legacy crewai.knowledge.DirectoryKnowledgeSource")
        except ImportError:
            # Define a minimal fallback
            class FileDataSource:
                def __init__(self, name=None, description=None, files=None):
                    self.name = name
                    self.description = description
                    self.files = files or []
            logger.warning("Using fallback FileDataSource implementation")

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Complete SEO Production Pipeline"
    )
    
    parser.add_argument(
        "--website", 
        type=str, 
        default="eatonassoc.com",
        help="The website to analyze (default: eatonassoc.com)"
    )
    
    parser.add_argument(
        "--niche", 
        type=str, 
        default="Managed IT Solutions",
        help="The business niche (default: Managed IT Solutions)"
    )
    
    parser.add_argument(
        "--focus", 
        type=str, 
        default="IT Support, Managed IT Services, IT Consulting",
        help="Specific focus area (default: IT Support, Managed IT Services, IT Consulting)"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="output",
        help="Output directory (default: output)"
    )
    
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["single", "full"],
        default="full",
        help="Execution mode (default: full)"
    )
    
    parser.add_argument(
        "--task", 
        type=str, 
        choices=["keyword_research", "competitor_analysis", "content_creation"],
        default="keyword_research",
        help="Task to run in single mode (default: keyword_research)"
    )
    
    parser.add_argument(
        "--human-review", 
        action="store_true",
        help="Enable human review for all content (default: only for content creation)"
    )
    
    return parser.parse_args()

def setup_environment() -> Dict[str, Any]:
    """Set up the environment and return configuration."""
    # Check required API keys
    required_keys = ["OPENAI_API_KEY", "SERPER_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.error(f"Missing required API keys: {', '.join(missing_keys)}")
        sys.exit(1)
    
    # Verify Google credentials
    google_creds_file = os.path.join(os.getcwd(), 'google', 'secret.json')
    if not os.path.exists(google_creds_file):
        logger.warning(f"Google credentials file not found at '{google_creds_file}'. Google services may not work properly.")
    else:
        # Set environment variable for Google credentials
        os.environ["GOOGLE_CREDENTIALS_PATH"] = google_creds_file
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Check for OpenLIT monitoring
    try:
        import openlit
        has_openlit = True
        logger.info("OpenLIT package is available")
        if os.getenv("OPENLIT_API_KEY"):
            logger.info("OpenLIT API key found")
        else:
            logger.warning("OpenLIT API key not found, monitoring will be limited")
    except ImportError:
        has_openlit = False
        logger.warning("OpenLIT package not installed. Monitoring will be limited.")
    
    return {
        "google_creds_file": google_creds_file if os.path.exists(google_creds_file) else None,
        "has_openlit": has_openlit
    }

def prepare_knowledge_sources() -> List[FileDataSource]:
    """Prepare knowledge sources from knowledge directory."""
    knowledge_sources = []
    
    # SEO best practices
    seo_best_practices_path = os.path.join(os.getcwd(), 'knowledge', 'seo_best_practices.txt')
    if os.path.exists(seo_best_practices_path):
        knowledge_sources.append(
            FileDataSource(
                name="SEO Best Practices",
                description="Best practices for SEO in 2025 with focus on IT services industry",
                files=[seo_best_practices_path]
            )
        )
        logger.info(f"✅ Loaded SEO best practices: {seo_best_practices_path}")
    else:
        logger.warning(f"❌ Could not find SEO best practices file: {seo_best_practices_path}")
    
    # Google algorithm updates
    google_algorithm_path = os.path.join(os.getcwd(), 'knowledge', 'google_algorithm_updates.txt')
    if os.path.exists(google_algorithm_path):
        knowledge_sources.append(
            FileDataSource(
                name="Google Algorithm Updates",
                description="Latest Google algorithm updates and their implications for IT services",
                files=[google_algorithm_path]
            )
        )
        logger.info(f"✅ Loaded Google algorithm updates: {google_algorithm_path}")
    else:
        logger.warning(f"❌ Could not find Google algorithm updates file: {google_algorithm_path}")
    
    return knowledge_sources

def build_seo_crew(args: argparse.Namespace, knowledge_sources: List[FileDataSource]) -> Crew:
    """Build the complete SEO crew with all agents and tasks."""
    # Import the SEO Agency Crew
    from src.seo_agency.crew import SEOAgencyCrew
    
    # Create the SEO Agency Crew instance
    seo_crew = SEOAgencyCrew()
    
    # Prepare inputs for the crew
    inputs = {
        "website": args.website,
        "niche": args.niche,
        "specific_focus": args.focus,
        "output_dir": args.output,
        "human_review": args.human_review
    }
    
    # Configure the crew
    crew = seo_crew.crew()
    
    # Add knowledge sources if not already added
    if hasattr(crew, 'knowledge_sources') and not crew.knowledge_sources:
        crew.knowledge_sources = knowledge_sources
    
    return crew, inputs

def run_seo_pipeline(args: argparse.Namespace) -> None:
    """Run the SEO production pipeline."""
    # Log event
    logger.info("EVENT [workflow_start]: Starting Complete SEO Production Pipeline")
    
    # Prepare knowledge sources
    knowledge_sources = prepare_knowledge_sources()
    
    # If no knowledge sources were found, warn but continue
    if not knowledge_sources:
        logger.warning("No knowledge sources found. The crew will operate with limited information.")
    
    try:
        logger.info("Creating and running keyword research crew...")
        
        # Log event
        logger.info("EVENT [task_start]: Starting keyword research task")
        
        # Build the SEO crew
        crew, inputs = build_seo_crew(args, knowledge_sources)
        
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        # Log event
        logger.info("EVENT [task_complete]: Keyword research task completed")
        
        # Print the result
        print("\n" + "=" * 70)
        print("SEO PRODUCTION COMPLETE")
        print(f"Check {args.output} directory for detailed reports")
        print("=" * 70)
        
        # Log completion event
        logger.info("EVENT [workflow_complete]: Complete SEO Production Pipeline completed")
        
        # Save summary to output
        summary = {
            "website": args.website,
            "niche": args.niche,
            "specific_focus": args.focus,
            "mode": args.mode,
            "task": args.task if args.mode == "single" else None,
            "human_review": args.human_review,
            "total_time": 0,  # Would be calculated in a real implementation
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Write summary to output file
        output_path = os.path.join(args.output, "production_summary.json")
        import json
        with open(output_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        return result
    
    except Exception as e:
        logger.error(f"Error running keyword research: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Log error event
        logger.info("EVENT [workflow_complete]: Complete SEO Production Pipeline completed")
        
        # Save error summary
        summary = {
            "website": args.website,
            "niche": args.niche,
            "specific_focus": args.focus,
            "mode": args.mode,
            "task": args.task if args.mode == "single" else None,
            "human_review": args.human_review,
            "total_time": 0,
            "success": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # Write summary to output file
        output_path = os.path.join(args.output, "production_summary.json")
        import json
        with open(output_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        return None

def main() -> None:
    """Main entry point for the script."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup environment
    config = setup_environment()
    
    # Begin with a nice header
    print("\n" + "=" * 70)
    print(f"COMPLETE SEO PRODUCTION PIPELINE FOR {args.website}")
    print(f"Niche: {args.niche}")
    print(f"Focus: {args.focus}")
    print(f"Mode: {args.mode}")
    print(f"Human Review: {'Enabled for all tasks' if args.human_review else 'Enabled for content creation only'}")
    print("=" * 70 + "\n")
    
    # Run the SEO production pipeline
    run_seo_pipeline(args)

if __name__ == "__main__":
    main() 