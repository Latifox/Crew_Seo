#!/usr/bin/env python
"""
SEO Agency - Main entry point

This script runs the autonomous SEO agency, coordinating the various agents
and tasks for SEO optimization.
"""

import argparse
import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv

from src.seo_agency.crew import SEOAgencyCrew


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SEO Agency - An autonomous SEO agency using CrewAI"
    )
    
    parser.add_argument(
        "--website", 
        type=str, 
        required=True,
        help="The website to analyze and optimize"
    )
    
    parser.add_argument(
        "--niche", 
        type=str, 
        required=True,
        help="The industry or niche of the website (e.g., 'health', 'finance', 'technology')"
    )
    
    parser.add_argument(
        "--specific-focus", 
        type=str, 
        default="",
        help="Optional specific focus area within the niche"
    )
    
    parser.add_argument(
        "--content-topic", 
        type=str, 
        default="",
        help="Topic for content creation task (if running content creation)"
    )
    
    parser.add_argument(
        "--tasks", 
        type=str, 
        nargs="+",
        choices=[
            "keyword_research",
            "competitor_analysis",
            "content_strategy",
            "technical_audit",
            "onpage_optimization",
            "backlink_strategy",
            "content_creation",
            "analytics_reporting",
            "full_strategy"
        ],
        default=["full_strategy"],
        help="Specific SEO tasks to run (default: full_strategy)"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="output",
        help="Directory to store output reports"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def setup_environment() -> None:
    """Load environment variables and set up the environment."""
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    required_keys = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "SERPER_API_KEY",
        "MOZ_API_KEY", 
        "GOOGLE_API_KEY",
        "GOOGLE_SERVICE_ACCOUNT",
        # Note: Google Analytics and Search Console use service account in .env
        # and secret.json file in /google directory
    ]
    
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        print("Please add them to your .env file.")
        sys.exit(1)


def prepare_inputs(args: argparse.Namespace) -> Dict[str, Any]:
    """Prepare input parameters for the crew."""
    # User's special content creation prompt
    content_prompt = """
    Create deeply engaging tech/business content that feels like a genuine human conversation. Use storytelling
    techniques that draw readers in, making complex topics feel personal and relatable. Incorporate conversational
    nuances like rhetorical questions, subtle humor, and authentic emotional connections. Share insights as if
    you're a knowledgeable friend explaining something fascinating over coffee. Use vivid, conversational language
    that makes technical or business information feel alive and compelling. Prioritize human connection over
    rigid information delivery, weaving personal perspectives and real-world context into every explanation.
    Balance professional credibility with warm, approachable storytelling that makes readers feel like they're
    part of an intimate, enlightening dialogue.
    """
    
    # Build a more comprehensive inputs dictionary
    inputs = {
        "website": args.website,
        "niche": args.niche,
        "specific_focus": args.specific_focus,
        "content_topic": args.content_topic,
        "content_prompt": content_prompt,
        "output_dir": args.output_dir
    }
    
    # If content topic is provided, add it to the specific focus for content creation
    if args.content_topic:
        if inputs["specific_focus"]:
            inputs["specific_focus"] += f" with particular emphasis on {args.content_topic}"
        else:
            inputs["specific_focus"] = f"with focus on {args.content_topic}"
    
    return inputs


def run_seo_tasks(args: argparse.Namespace, inputs: Dict[str, Any]) -> None:
    """Run the specified SEO tasks with the given inputs."""
    crew = SEOAgencyCrew()
    
    if "full_strategy" in args.tasks:
        # Run the full SEO strategy
        result = crew.crew().kickoff(inputs=inputs)
        print("\n=== Full SEO Strategy Complete ===")
        print(f"Final report available at: {os.path.join(args.output_dir, 'seo_strategy_report.md')}")
    else:
        # Run individual tasks
        for task_name in args.tasks:
            task_method = getattr(crew, f"{task_name}_task", None)
            if not task_method:
                print(f"Warning: Task '{task_name}' not found, skipping.")
                continue
                
            print(f"\n=== Running {task_name.replace('_', ' ').title()} ===")
            task = task_method()
            # Execute the individual task
            # This will depend on how we implement the crew class
            # For now, we'll just print a placeholder
            print(f"Task {task_name} executed.")


def main() -> None:
    """Main entry point for the SEO agency."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up environment
    setup_environment()
    
    # Prepare inputs for the crew
    inputs = prepare_inputs(args)
    
    # Run specified SEO tasks
    run_seo_tasks(args, inputs)


if __name__ == "__main__":
    main()