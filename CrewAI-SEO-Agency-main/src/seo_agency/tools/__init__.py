"""
Custom SEO tools for the CrewAI framework.

This module contains custom tools for SEO tasks such as:
- Google Analytics and Search Console data retrieval
- File operations for writing reports
- Content analysis and optimization
- PageSpeed performance testing
- Website crawling and scraping for content analysis
- And more specialized SEO functions
"""

from typing import List

# Import all tools here as they are developed
from .search_console_tool import GoogleSearchConsoleTool
from .content_analysis_tool import ContentAnalysisTool
from .pagespeed_tool import GooglePageSpeedTool
from .google_analytics_tool import GoogleAnalyticsTool
from .file_write_tool import FileWriteTool
from .firecrawl_tool import FireCrawlTool
# from .moz_tool import MozTool
# from .technical_audit_tool import TechnicalAuditTool
# from .backlink_tools import BacklinkTool

def get_all_tools():
    """
    Get all available SEO tools.
    
    Returns:
        List: A list of all available tools.
    """
    tools = [
        # Add tools here as they are developed
        GoogleSearchConsoleTool(),
        ContentAnalysisTool(),
        GooglePageSpeedTool(),
        GoogleAnalyticsTool(),
        FileWriteTool(),
        FireCrawlTool(),
        # MozTool(),
        # TechnicalAuditTool(),
        # BacklinkTool(),
    ]
    return tools
