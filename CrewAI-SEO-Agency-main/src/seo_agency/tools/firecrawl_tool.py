"""
FireCrawl Tool

This tool provides website scraping and crawling capabilities using FireCrawl.
It allows for extracting content from websites for SEO analysis.
"""

import os
from typing import Dict, Any, Optional, Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import json

try:
    # Try to import FireCrawl tools from crewai_tools
    from crewai_tools import FirecrawlScrapeWebsiteTool, FirecrawlCrawlWebsiteTool
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False
    print("FireCrawl tools not available. Install with: pip install firecrawl-py crewai[tools]")


class WebsiteScrapeInput(BaseModel):
    """Input schema for website scraping."""
    url: str = Field(..., description="The URL to scrape")
    only_main_content: bool = Field(
        default=True, 
        description="Only extract the main content, filtering out navigation, footers, etc."
    )
    include_html: bool = Field(
        default=False,
        description="Include the raw HTML in the response"
    )


class WebsiteCrawlInput(BaseModel):
    """Input schema for website crawling."""
    url: str = Field(..., description="The base URL to crawl")
    max_pages: int = Field(
        default=10,
        description="Maximum number of pages to crawl"
    )
    max_depth: int = Field(
        default=2,
        description="Maximum depth to crawl (1 is just the base URL)"
    )
    include_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to include in the crawl"
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to exclude from the crawl"
    )


class FireCrawlTool(BaseTool):
    """Tool for scraping and crawling websites using FireCrawl."""
    
    name: str = "FireCrawl Website Analyzer"
    description: str = """
    Analyze websites by scraping and crawling their content. This tool can extract content from
    webpages for SEO analysis, including text content, headings, and structure. It can also
    crawl entire websites to discover and analyze multiple pages.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the FireCrawl Tool."""
        super().__init__()
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        
        if not FIRECRAWL_AVAILABLE:
            print("Warning: FireCrawl tools not available. Some functionality will be limited.")
            self.scrape_tool = None
            self.crawl_tool = None
        else:
            # Initialize the FireCrawl tools
            self.scrape_tool = FirecrawlScrapeWebsiteTool(api_key=self.api_key)
            self.crawl_tool = FirecrawlCrawlWebsiteTool(api_key=self.api_key)
    
    def scrape_website(self, url: str, only_main_content: bool = True, include_html: bool = False) -> str:
        """
        Scrape a single webpage and return its content.
        
        Args:
            url: The URL to scrape
            only_main_content: Only extract the main content (default: True)
            include_html: Include the raw HTML in the response (default: False)
            
        Returns:
            The extracted content as markdown
        """
        if not FIRECRAWL_AVAILABLE or not self.scrape_tool:
            return f"Error: FireCrawl tools not available. Could not scrape {url}"
        
        page_options = {
            "onlyMainContent": only_main_content,
            "includeHtml": include_html
        }
        
        try:
            # Use the FireCrawl scrape tool
            result = self.scrape_tool.run(url=url, page_options=page_options)
            return result
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
    
    def crawl_website(
        self, 
        url: str, 
        max_pages: int = 10, 
        max_depth: int = 2,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> str:
        """
        Crawl a website and return the content of multiple pages.
        
        Args:
            url: The base URL to crawl
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum depth to crawl
            include_patterns: URL patterns to include
            exclude_patterns: URL patterns to exclude
            
        Returns:
            The extracted content from multiple pages
        """
        if not FIRECRAWL_AVAILABLE or not self.crawl_tool:
            return f"Error: FireCrawl tools not available. Could not crawl {url}"
        
        crawler_options = {
            "limit": max_pages,
            "maxDepth": max_depth
        }
        
        if include_patterns:
            crawler_options["includes"] = include_patterns
        
        if exclude_patterns:
            crawler_options["excludes"] = exclude_patterns
        
        page_options = {
            "onlyMainContent": True
        }
        
        try:
            # Use the FireCrawl crawl tool
            result = self.crawl_tool.run(
                url=url, 
                crawler_options=crawler_options,
                page_options=page_options
            )
            return result
        except Exception as e:
            return f"Error crawling {url}: {str(e)}"
    
    def _run(self, tool_input: str) -> str:
        """
        Run the tool with the provided input.
        
        Args:
            tool_input: A JSON string containing the tool input
            
        Returns:
            The extracted content
        """
        try:
            # Parse the input JSON
            input_dict = json.loads(tool_input)
            
            # Determine the operation (scrape or crawl)
            operation = input_dict.get("operation", "scrape")
            
            if operation == "scrape":
                # Extract scrape parameters
                url = input_dict.get("url")
                only_main_content = input_dict.get("only_main_content", True)
                include_html = input_dict.get("include_html", False)
                
                # Perform the scrape
                return self.scrape_website(url, only_main_content, include_html)
            
            elif operation == "crawl":
                # Extract crawl parameters
                url = input_dict.get("url")
                max_pages = input_dict.get("max_pages", 10)
                max_depth = input_dict.get("max_depth", 2)
                include_patterns = input_dict.get("include_patterns")
                exclude_patterns = input_dict.get("exclude_patterns")
                
                # Perform the crawl
                return self.crawl_website(
                    url, 
                    max_pages, 
                    max_depth,
                    include_patterns,
                    exclude_patterns
                )
            
            else:
                return f"Error: Unknown operation '{operation}'. Use 'scrape' or 'crawl'."
        
        except json.JSONDecodeError:
            return "Error: Invalid JSON input."
        except KeyError as e:
            return f"Error: Missing required parameter {str(e)}."
        except Exception as e:
            return f"Error: {str(e)}" 