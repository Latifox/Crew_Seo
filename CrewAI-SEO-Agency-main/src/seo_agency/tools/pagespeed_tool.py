"""
Google PageSpeed Insights Tool

This tool provides access to Google PageSpeed Insights API for analyzing web page
performance, accessibility, SEO, and best practices.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional, Union

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class PageSpeedToolInput(BaseModel):
    """Input for querying Google PageSpeed Insights."""
    url: str = Field(..., description="The URL to analyze with PageSpeed Insights")
    strategy: str = Field(
        default="mobile", 
        description="The strategy to use: 'mobile' or 'desktop'"
    )
    category: Optional[List[str]] = Field(
        default=None,
        description="Categories to measure: 'performance', 'accessibility', 'best-practices', 'seo', 'pwa'"
    )


class GooglePageSpeedTool(BaseTool):
    """Tool for accessing Google PageSpeed Insights API."""
    
    name: str = "Google PageSpeed Insights Tool"
    description: str = """
    Use this tool to analyze web page performance, accessibility, SEO, and best practices.
    It returns detailed metrics about a web page and suggestions for improvement.
    This is useful for technical SEO audits and performance optimization.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Google PageSpeed Insights Tool.
        
        Args:
            api_key: The Google PageSpeed Insights API key. 
                If not provided, will try to use environment variable.
        """
        super().__init__()
        self._api_key = api_key
    
    def _get_api_key(self) -> str:
        """Get the API key from instance variable or environment."""
        if self._api_key:
            return self._api_key
        
        api_key = os.getenv("GOOGLE_PAGE_SPEED_API_KEY")
        if not api_key:
            raise ValueError(
                "Google PageSpeed API key not provided. Either pass it to the constructor "
                "or set the GOOGLE_PAGE_SPEED_API_KEY environment variable."
            )
        
        return api_key
    
    def _analyze_url(self, url: str, strategy: str = 'mobile', category: Optional[List[str]] = None) -> str:
        """
        Analyze a URL with Google PageSpeed Insights.
        
        Args:
            url: The URL to analyze
            strategy: 'mobile' or 'desktop'
            category: List of categories to analyze
            
        Returns:
            Formatted analysis results
        """
        api_key = self._get_api_key()
        
        # Build request URL
        request_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}"
        
        if category:
            for cat in category:
                request_url += f"&category={cat}"
        
        request_url += f"&key={api_key}"
        
        try:
            response = requests.get(request_url)
            response.raise_for_status()
            data = response.json()
            
            # Format the results
            result = self._format_results(data, strategy)
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Error analyzing URL: {str(e)}"
    
    def _format_results(self, data: Dict[str, Any], strategy: str) -> str:
        """
        Format the PageSpeed Insights results into a readable format.
        
        Args:
            data: The JSON response from the API
            strategy: The strategy used ('mobile' or 'desktop')
            
        Returns:
            Formatted results as a string
        """
        try:
            url = data.get('id', 'Unknown URL')
            lighthouse_result = data.get('lighthouseResult', {})
            categories = lighthouse_result.get('categories', {})
            audits = lighthouse_result.get('audits', {})
            
            # Format as markdown
            result = f"# PageSpeed Insights Analysis for {url}\n\n"
            result += f"Strategy: {strategy.capitalize()}\n\n"
            
            # Overall scores
            result += "## Overall Scores\n\n"
            
            for category_key, category_data in categories.items():
                score = int(category_data.get('score', 0) * 100)
                result += f"- {category_data.get('title', category_key)}: {score}/100\n"
            
            # Field data
            if 'loadingExperience' in data:
                load_exp = data['loadingExperience']
                if 'metrics' in load_exp:
                    result += "\n## Real User Metrics\n\n"
                    metrics = load_exp['metrics']
                    
                    for metric_key, metric_data in metrics.items():
                        # Clean up metric name
                        metric_name = metric_key.replace('CUMULATIVE_', '').replace('_', ' ').title()
                        percentile = metric_data.get('percentile', 'N/A')
                        
                        if 'LAYOUT_SHIFT' in metric_key:
                            value = f"{percentile/100:.2f}"
                        elif percentile >= 1000:
                            value = f"{percentile/1000:.1f}s"
                        else:
                            value = f"{percentile}ms"
                            
                        result += f"- {metric_name}: {value}\n"
            
            # Top opportunities for improvement
            result += "\n## Top Improvement Opportunities\n\n"
            
            # Get opportunities and sort by impact
            opportunities = []
            for audit_id, audit_data in audits.items():
                if audit_data.get('details', {}).get('type') == 'opportunity':
                    opportunities.append(audit_data)
            
            # Sort by waste bytes or potential savings
            opportunities = sorted(
                opportunities, 
                key=lambda x: x.get('details', {}).get('overallSavingsMs', 0) or 
                              x.get('details', {}).get('overallSavingsBytes', 0) or 0,
                reverse=True
            )
            
            # Take top 5
            for opportunity in opportunities[:5]:
                title = opportunity.get('title', 'Unknown')
                description = opportunity.get('description', '')
                
                # Try to get savings
                savings_ms = opportunity.get('details', {}).get('overallSavingsMs', None)
                savings_bytes = opportunity.get('details', {}).get('overallSavingsBytes', None)
                
                savings_text = ""
                if savings_ms:
                    savings_text += f"Potential time saving: {savings_ms}ms. "
                if savings_bytes:
                    savings_text += f"Potential size saving: {savings_bytes/1024:.1f}KB."
                
                result += f"### {title}\n"
                result += f"{description}\n"
                if savings_text:
                    result += f"**{savings_text}**\n"
                result += "\n"
            
            # SEO-specific audits if available
            seo_audits = {}
            for audit_id, audit_data in audits.items():
                if 'seo' in audit_id:
                    seo_audits[audit_id] = audit_data
            
            if seo_audits:
                result += "\n## SEO Audits\n\n"
                for audit_id, audit_data in seo_audits.items():
                    title = audit_data.get('title', audit_id)
                    score = audit_data.get('score', None)
                    description = audit_data.get('description', '')
                    
                    status = "✅ Passed" if score == 1 else "❌ Failed" if score == 0 else "⚠️ Warning"
                    
                    result += f"### {title}: {status}\n"
                    result += f"{description}\n\n"
            
            return result
        
        except Exception as e:
            return f"Error formatting results: {str(e)}\n\nRaw data: {json.dumps(data, indent=2)}"
    
    def _run(self, tool_input: str) -> str:
        """
        Execute the Google PageSpeed Insights tool.
        
        Args:
            tool_input: JSON string containing the tool input.
            
        Returns:
            Tool execution result.
        """
        try:
            # Parse the tool input
            input_dict = json.loads(tool_input)
            
            url = input_dict.get("url")
            if not url:
                return "Error: URL is required."
            
            strategy = input_dict.get("strategy", "mobile")
            if strategy not in ["mobile", "desktop"]:
                return "Error: Strategy must be either 'mobile' or 'desktop'."
            
            category = input_dict.get("category")
            
            # Analyze the URL
            return self._analyze_url(url, strategy, category)
        
        except json.JSONDecodeError:
            return "Error: Invalid JSON input."
        except Exception as e:
            return f"Error executing Google PageSpeed Insights tool: {str(e)}"