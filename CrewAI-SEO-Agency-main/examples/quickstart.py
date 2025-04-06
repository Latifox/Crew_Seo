#!/usr/bin/env python
"""
SEO Agency Quickstart Example

This script demonstrates how to use the autonomous SEO agency
for a simple SEO analysis and content creation workflow.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for imports to work
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from seo_agency.crew import SEOAgencyCrew


def check_environment():
    """Check that necessary environment variables are set."""
    required_env_vars = ["OPENAI_API_KEY"]
    
    # Optional but recommended
    recommended_env_vars = [
        "SERPER_API_KEY",
        "MOZ_API_KEY",
        "GOOGLE_ANALYTICS_API_KEY",
        "GOOGLE_SEARCH_CONSOLE_API_KEY"
    ]
    
    missing_required = [var for var in required_env_vars if not os.getenv(var)]
    missing_recommended = [var for var in recommended_env_vars if not os.getenv(var)]
    
    if missing_required:
        print(f"Error: Missing required environment variables: {', '.join(missing_required)}")
        print("Please add them to your .env file.")
        sys.exit(1)
    
    if missing_recommended:
        print(f"Warning: Missing recommended environment variables: {', '.join(missing_recommended)}")
        print("Some functionality may be limited.")


def run_keyword_research_example():
    """Run a simple keyword research example."""
    print("\n=== Running Keyword Research Example ===\n")
    
    crew = SEOAgencyCrew()
    
    inputs = {
        "website": "example-tech-blog.com",
        "niche": "artificial intelligence",
        "specific_focus": "AI for small businesses",
        "output_dir": "output"
    }
    
    result = crew.run_keyword_research(inputs)
    
    print("\nKeyword Research completed!")
    print(f"Results saved to: output/keyword_research_report.md")
    
    return result


def run_content_creation_example():
    """Run a simple content creation example."""
    print("\n=== Running Content Creation Example ===\n")
    
    # First we need to simulate having keyword research results
    # In a real scenario, you would run the keyword research task first
    
    # Create sample keyword research output file
    os.makedirs("output", exist_ok=True)
    with open("output/keyword_research_report.md", "w") as f:
        f.write("""# Keyword Research Report for example-tech-blog.com

## Primary Keywords

| Keyword | Search Volume | Competition | Search Intent |
|---------|--------------|-------------|---------------|
| ai for small business | 2,400 | Medium | Commercial |
| small business ai tools | 1,900 | Medium | Commercial |
| artificial intelligence for small companies | 1,300 | Low | Informational |
| affordable ai solutions | 1,100 | High | Transactional |
| ai automation for small business | 950 | Medium | Commercial |

## Secondary Keywords
[Additional keywords listed here...]

## Recommendations
1. Focus content creation on "ai for small business" and "small business ai tools" as primary targets.
2. Create comprehensive guides around "artificial intelligence for small companies" to capture informational intent.
3. Develop comparison content for "affordable ai solutions" to target transactional searches.
""")
    
    crew = SEOAgencyCrew()
    
    inputs = {
        "website": "example-tech-blog.com",
        "niche": "artificial intelligence",
        "specific_focus": "AI for small businesses",
        "content_topic": "How AI is Transforming Small Business Operations",
        "output_dir": "output"
    }
    
    # Initialize agents for this specific task
    content_creator = crew.content_creator()
    
    # Create a standalone task for content creation
    from crewai import Task
    
    content_task = Task(
        description=f"""
            Create high-quality, SEO-optimized content for {inputs['website']} about {inputs['content_topic']}.
            Target keyword: ai for small business.
            The content should be engaging, valuable to small business owners, and properly optimized for search engines.
            
            Create deeply engaging tech/business content that feels like a genuine human conversation. Use storytelling
            techniques that draw readers in, making complex topics feel personal and relatable. Incorporate conversational
            nuances like rhetorical questions, subtle humor, and authentic emotional connections. Share insights as if
            you're a knowledgeable friend explaining something fascinating over coffee. Use vivid, conversational language
            that makes technical or business information feel alive and compelling. Prioritize human connection over
            rigid information delivery, weaving personal perspectives and real-world context into every explanation.
            Balance professional credibility with warm, approachable storytelling that makes readers feel like they're
            part of an intimate, enlightening dialogue.
        """,
        expected_output="A complete, SEO-optimized article about AI for small businesses, formatted as markdown.",
        agent=content_creator,
        output_file="output/ai_small_business_article.md"
    )
    
    # Run the content creation task
    from crewai import Crew
    
    single_task_crew = Crew(
        agents=[content_creator],
        tasks=[content_task],
        verbose=True
    )
    
    result = single_task_crew.kickoff()
    
    print("\nContent Creation completed!")
    print(f"Results saved to: output/ai_small_business_article.md")
    
    return result


def main():
    """Run the quickstart examples."""
    print("=== SEO Agency Quickstart Example ===")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check that necessary environment variables are set
    check_environment()
    
    # Run keyword research example
    run_keyword_research_example()
    
    # Run content creation example
    run_content_creation_example()
    
    print("\n=== All Examples Completed ===")
    print("Check the 'output' directory for results!")


if __name__ == "__main__":
    main()