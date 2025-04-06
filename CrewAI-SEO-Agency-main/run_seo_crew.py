#!/usr/bin/env python
"""
SEO Crew Runner

This script runs the complete SEO Agency crew with all agents and tasks,
ensuring proper authentication for Google services.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("seo_crew.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SEOCrew")

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SEO Crew - Run the complete SEO agency with all agents"
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
    required_keys = [
        "OPENAI_API_KEY", 
        "SERPER_API_KEY",
        "GOOGLE_SERVICE_ACCOUNT"
    ]
    
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.error(f"Missing required API keys: {', '.join(missing_keys)}")
        logger.error("Please add them to your .env file.")
        sys.exit(1)
    
    # Verify Google service account file exists
    google_creds_file = os.path.join(os.getcwd(), 'google', 'secret.json')
    if not os.path.exists(google_creds_file):
        logger.error(f"Google service account file not found at: {google_creds_file}")
        logger.error("Please ensure the secret.json file is available in the google directory.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Set additional environment variables for Google authentication
    os.environ["GOOGLE_CREDENTIALS_PATH"] = google_creds_file
    
    logger.info("✅ Environment setup complete")
    logger.info(f"✅ Using Google service account: {os.getenv('GOOGLE_SERVICE_ACCOUNT')}")
    logger.info(f"✅ Using credentials file: {google_creds_file}")

def run_seo_crew(args: argparse.Namespace) -> None:
    """Run the SEO crew with all agents."""
    website = args.website
    niche = args.niche
    focus = args.focus
    output_dir = args.output_dir
    
    logger.info(f"Starting SEO analysis for {website}")
    logger.info(f"Industry/Niche: {niche}")
    logger.info(f"Specific focus: {focus}")
    
    try:
        # Import the SEO Agency Crew
        from src.seo_agency.crew import SEOAgencyCrew
        
        # Create the SEO Agency Crew instance
        seo_crew = SEOAgencyCrew()
        
        # Prepare inputs for the crew
        inputs = {
            "website": website,
            "niche": niche,
            "specific_focus": focus,
            "output_dir": output_dir
        }
        
        # Run the crew with all agents
        logger.info("Starting SEO Agency Crew with all agents...")
        result = seo_crew.crew().kickoff(inputs=inputs)
        
        logger.info("SEO analysis completed successfully")
        logger.info(f"Results saved to {output_dir}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error running SEO crew: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

def main() -> None:
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up environment
    setup_environment()
    
    print("\n" + "=" * 70)
    print(f"SEO CREW ANALYSIS FOR {args.website}")
    print(f"Niche: {args.niche}")
    print(f"Focus: {args.focus}")
    print("=" * 70 + "\n")
    
    # Run SEO analysis
    run_seo_crew(args)
    
    print("\n" + "=" * 70)
    print("SEO ANALYSIS COMPLETE")
    print(f"Check output directory for detailed reports: {args.output_dir}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main() 