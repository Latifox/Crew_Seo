"""
SEO Agency Task Functions

This module contains functions for task descriptions and expected outputs.
"""

from typing import Dict, Any


# Keyword Research Task
def keyword_research_description(inputs: Dict[str, Any]) -> str:
    """Generate keyword research task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    specific_focus = inputs.get('specific_focus', '')
    
    focus_text = f"Focus on {specific_focus}." if specific_focus else ""
    
    return f"""Conduct comprehensive keyword research for {website} in the {niche} industry.
    {focus_text}
    Identify primary keywords, long-tail variations, and question-based queries.
    Analyze search volume, competition, and commercial intent.
    Organize keywords by user journey stage and prioritize based on potential impact.
    Deliver a complete keyword research report with recommendations."""


def keyword_research_output() -> str:
    """Expected output for keyword research task."""
    return """A detailed keyword research report in markdown format that includes:
    1. Primary keywords with search volumes and competition metrics
    2. Long-tail keyword opportunities
    3. Question-based queries for content development
    4. Keyword grouping by topic and user intent
    5. Prioritized list of keywords to target
    """


# Competitor Analysis Task
def competitor_analysis_description(inputs: Dict[str, Any]) -> str:
    """Generate competitor analysis task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    specific_focus = inputs.get('specific_focus', '')
    
    focus_text = f"with focus on {specific_focus}" if specific_focus else ""
    
    return f"""Analyze top competitors of {website} in the {niche} industry {focus_text}.
    Identify at least 5 key competitors based on keyword overlap and market position.
    Analyze their domain authority, backlink profile, content strategy, technical SEO, and on-page optimization.
    Identify their strengths, weaknesses, and opportunities to outperform them.
    Deliver a comprehensive competitor analysis report with actionable insights."""


def competitor_analysis_output() -> str:
    """Expected output for competitor analysis task."""
    return """A detailed competitor analysis report in markdown format that includes:
    1. List of top competitors with domain metrics
    2. Analysis of competitors' content strategies
    3. Technical SEO comparison
    4. Backlink profile analysis
    5. Content gap analysis
    6. Recommendations for outperforming competitors
    """


# Content Strategy Task
def content_strategy_description(inputs: Dict[str, Any]) -> str:
    """Generate content strategy task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    specific_focus = inputs.get('specific_focus', '')
    
    focus_text = f"focusing on {specific_focus}" if specific_focus else ""
    
    return f"""Develop a content strategy for {website} in the {niche} industry, {focus_text}.
    Use the insights from keyword research and competitor analysis to create a comprehensive content plan.
    Include content pillars, topic clusters, content formats, and publishing schedule.
    Consider user journey stages and search intent in your recommendations.
    Provide guidelines for content optimization and promotion.
    Deliver a detailed content strategy plan with implementation roadmap."""


def content_strategy_output() -> str:
    """Expected output for content strategy task."""
    return """A comprehensive content strategy plan in markdown format that includes:
    1. Content pillars and topic clusters
    2. Content formats and types
    3. Publishing schedule and content calendar
    4. Content optimization guidelines
    5. Content promotion strategies
    6. Success metrics and KPIs
    """


# Technical Audit Task
def technical_audit_description(inputs: Dict[str, Any]) -> str:
    """Generate technical audit task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    
    return f"""Conduct a comprehensive technical SEO audit for {website} in the {niche} industry.
    Analyze site structure, URL format, page speed, mobile friendliness, indexability, crawlability, and schema markup.
    Identify technical issues preventing optimal search performance.
    Evaluate internal linking, duplicate content, and canonical usage.
    Deliver a technical SEO audit report with prioritized recommendations."""


def technical_audit_output() -> str:
    """Expected output for technical audit task."""
    return """A detailed technical SEO audit report in markdown format that includes:
    1. Site structure and architecture analysis
    2. Page speed and performance assessment
    3. Mobile optimization review
    4. Indexing and crawlability issues
    5. Schema markup implementation recommendations
    6. Prioritized list of technical fixes
    """


# On-Page Optimization Task
def onpage_optimization_description(inputs: Dict[str, Any]) -> str:
    """Generate on-page optimization task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    specific_focus = inputs.get('specific_focus', '')
    
    focus_text = f"focusing on {specific_focus}" if specific_focus else ""
    
    return f"""Develop on-page optimization recommendations for {website} in the {niche} industry, {focus_text}.
    Create guidelines for title tags, meta descriptions, heading structure, content formatting, internal linking, and schema markup.
    Provide specific recommendations for optimizing key pages based on target keywords.
    Deliver an on-page optimization plan with implementation guidelines."""


def onpage_optimization_output() -> str:
    """Expected output for on-page optimization task."""
    return """A comprehensive on-page optimization plan in markdown format that includes:
    1. Title tag and meta description templates
    2. Heading structure recommendations
    3. Content optimization guidelines
    4. Internal linking strategy
    5. Schema markup implementation guide
    6. Page-specific optimization recommendations
    """


# Backlink Strategy Task
def backlink_strategy_description(inputs: Dict[str, Any]) -> str:
    """Generate backlink strategy task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    specific_focus = inputs.get('specific_focus', '')
    
    focus_text = f"focusing on {specific_focus}" if specific_focus else ""
    
    return f"""Develop a backlink acquisition strategy for {website} in the {niche} industry, {focus_text}.
    Identify high-quality link building opportunities through competitor analysis, content gap analysis, and industry research.
    Create strategies for guest posting, resource link building, broken link building, and digital PR.
    Provide guidelines for outreach and relationship building.
    Deliver a comprehensive backlink strategy with implementation timeline."""


def backlink_strategy_output() -> str:
    """Expected output for backlink strategy task."""
    return """A detailed backlink strategy plan in markdown format that includes:
    1. Link building opportunity analysis
    2. Outreach templates and guidelines
    3. Content creation recommendations for link acquisition
    4. Digital PR strategies
    5. Implementation timeline and resource requirements
    6. Success metrics and tracking recommendations
    """


# Content Creation Task
def content_creation_description(inputs: Dict[str, Any]) -> str:
    """Generate content creation task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    specific_focus = inputs.get('specific_focus', '')
    
    focus_text = f"focusing on {specific_focus}" if specific_focus else ""
    
    return f"""Create high-quality SEO content for {website} in the {niche} industry, {focus_text}.
    Use the insights from keyword research and content strategy to create engaging, optimized content.
    Ensure content addresses user intent, incorporates target keywords naturally, and provides genuine value.
    Structure content for readability and engagement with proper heading hierarchy, short paragraphs, and bulleted lists.
    Deliver polished, publication-ready content with optimization recommendations."""


def content_creation_output() -> str:
    """Expected output for content creation task."""
    return """Publication-ready content in markdown format that includes:
    1. SEO-optimized headline and subheadings
    2. Well-structured content with proper heading hierarchy
    3. Naturally incorporated target keywords
    4. Internal and external linking recommendations
    5. Meta title and description suggestions
    """


# Analytics Reporting Task
def analytics_reporting_description(inputs: Dict[str, Any]) -> str:
    """Generate analytics reporting task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    
    return f"""Develop an SEO analytics and reporting framework for {website} in the {niche} industry.
    Define key performance indicators (KPIs) and metrics to track SEO performance.
    Create a reporting structure with recommended tools and data sources.
    Provide guidelines for data analysis and insight generation.
    Develop a dashboard template for ongoing performance monitoring.
    Deliver a comprehensive analytics and reporting framework with implementation guidelines."""


def analytics_reporting_output() -> str:
    """Expected output for analytics reporting task."""
    return """A detailed SEO analytics and reporting framework in markdown format that includes:
    1. Key performance indicators (KPIs) and metrics definitions
    2. Reporting structure and frequency recommendations
    3. Tool selection and implementation guidelines
    4. Dashboard template design
    5. Analysis and insight generation process
    6. Performance benchmarking methodology
    """


# SEO Agency Report Task
def seo_agency_report_description(inputs: Dict[str, Any]) -> str:
    """Generate SEO agency report task description."""
    website = inputs.get('website', 'the target website')
    niche = inputs.get('niche', 'the target industry')
    
    return f"""Synthesize all SEO findings and recommendations for {website} in the {niche} industry into a comprehensive strategy report.
    Integrate insights from keyword research, competitor analysis, content strategy, technical audit, on-page optimization, and backlink strategy.
    Prioritize recommendations based on potential impact and implementation difficulty.
    Create an executive summary with key findings and expected outcomes.
    Deliver a comprehensive SEO strategy report with implementation roadmap."""


def seo_agency_report_output() -> str:
    """Expected output for SEO agency report task."""
    return """A comprehensive SEO strategy report in markdown format that includes:
    1. Executive summary with key findings and recommendations
    2. Integrated strategy across all SEO disciplines
    3. Prioritized implementation roadmap
    4. Resource requirements and timeline
    5. Expected outcomes and success metrics
    6. Ongoing maintenance and optimization recommendations
    """