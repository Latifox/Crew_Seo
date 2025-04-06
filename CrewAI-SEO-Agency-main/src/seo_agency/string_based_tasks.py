"""
SEO Agency Task Definitions (String-Based)

This module contains string-based task descriptions and outputs
for CrewAI tasks.
"""

# Keyword Research Task
KEYWORD_RESEARCH_DESCRIPTION = """
Conduct comprehensive keyword research for {website} in the {niche} industry.
{focus_text}
Identify primary keywords, long-tail variations, and question-based queries.
Analyze search volume, competition, and commercial intent.
Organize keywords by user journey stage and prioritize based on potential impact.
Deliver a complete keyword research report with recommendations.
"""

KEYWORD_RESEARCH_OUTPUT = """
A detailed keyword research report in markdown format that includes:
1. Primary keywords with search volumes and competition metrics
2. Long-tail keyword opportunities
3. Question-based queries for content development
4. Keyword grouping by topic and user intent
5. Prioritized list of keywords to target
"""

# Competitor Analysis Task
COMPETITOR_ANALYSIS_DESCRIPTION = """
Analyze top competitors of {website} in the {niche} industry. {focus_text}
Identify at least 5 key competitors based on keyword overlap and market position.
Analyze their domain authority, backlink profile, content strategy, technical SEO, and on-page optimization.
Identify their strengths, weaknesses, and opportunities to outperform them.
Deliver a comprehensive competitor analysis report with actionable insights.
"""

COMPETITOR_ANALYSIS_OUTPUT = """
A detailed competitor analysis report in markdown format that includes:
1. List of top competitors with domain metrics
2. Analysis of competitors' content strategies
3. Technical SEO comparison
4. Backlink profile analysis
5. Content gap analysis
6. Recommendations for outperforming competitors
"""

# Content Strategy Task
CONTENT_STRATEGY_DESCRIPTION = """
Develop a content strategy for {website} in the {niche} industry. {focus_text}
Use the insights from keyword research and competitor analysis to create a comprehensive content plan.
Include content pillars, topic clusters, content formats, and publishing schedule.
Consider user journey stages and search intent in your recommendations.
Provide guidelines for content optimization and promotion.
Deliver a detailed content strategy plan with implementation roadmap.
"""

CONTENT_STRATEGY_OUTPUT = """
A comprehensive content strategy plan in markdown format that includes:
1. Content pillars and topic clusters
2. Content formats and types
3. Publishing schedule and content calendar
4. Content optimization guidelines
5. Content promotion strategies
6. Success metrics and KPIs
"""

# Technical Audit Task
TECHNICAL_AUDIT_DESCRIPTION = """
Conduct a comprehensive technical SEO audit for {website} in the {niche} industry.
Analyze site structure, URL format, page speed, mobile friendliness, indexability, crawlability, and schema markup.
Identify technical issues preventing optimal search performance.
Evaluate internal linking, duplicate content, and canonical usage.
Deliver a technical SEO audit report with prioritized recommendations.
"""

TECHNICAL_AUDIT_OUTPUT = """
A detailed technical SEO audit report in markdown format that includes:
1. Site structure and architecture analysis
2. Page speed and performance assessment
3. Mobile optimization review
4. Indexing and crawlability issues
5. Schema markup implementation recommendations
6. Prioritized list of technical fixes
"""

# On-page Optimization Task
ONPAGE_OPTIMIZATION_DESCRIPTION = """
Develop on-page optimization recommendations for {website} in the {niche} industry. {focus_text}

IMPORTANT: First, use the FireCrawl Website Analyzer tool to scrape and analyze the actual website content. 
Use the following parameters:
1. Use the 'crawl' operation to get multiple pages from the website
2. Set max_pages to 10 to analyze a representative sample
3. Set max_depth to 2 to include important subpages

After scraping the website content, conduct a thorough on-page SEO analysis of the actual HTML content, including:
1. Title tags, meta descriptions, and heading structure
2. Content quality, length, and keyword usage
3. Internal linking structure and anchor text
4. Image optimization (alt tags, compression)
5. Schema markup implementation
6. Mobile responsiveness and user experience
7. Page speed and performance issues

Create specific, actionable guidelines for title tags, meta descriptions, heading structure, content formatting, 
internal linking, and schema markup based on the actual website content.
Provide specific recommendations for optimizing key pages based on target keywords.
Deliver an on-page optimization plan with implementation guidelines based on your actual analysis of the website.
"""

ONPAGE_OPTIMIZATION_OUTPUT = """
A comprehensive on-page optimization plan in markdown format that includes:
1. Website content analysis (based on actual scraped content)
2. Title tag and meta description evaluation and recommendations
3. Heading structure analysis and improvements
4. Content optimization analysis and guidelines
5. Internal linking assessment and strategy
6. Schema markup evaluation and implementation guide
7. Page-specific optimization recommendations based on actual pages found
8. Technical on-page issues discovered during analysis
"""

# Backlink Strategy Task
BACKLINK_STRATEGY_DESCRIPTION = """
Develop a backlink acquisition strategy for {website} in the {niche} industry. {focus_text}
Identify high-quality link building opportunities through competitor analysis, content gap analysis, and industry research.
Create strategies for guest posting, resource link building, broken link building, and digital PR.
Provide guidelines for outreach and relationship building.
Deliver a comprehensive backlink strategy with implementation timeline.
"""

BACKLINK_STRATEGY_OUTPUT = """
A detailed backlink strategy plan in markdown format that includes:
1. Link building opportunity analysis
2. Outreach templates and guidelines
3. Content creation recommendations for link acquisition
4. Digital PR strategies
5. Implementation timeline and resource requirements
6. Success metrics and tracking recommendations
"""

# Content Creation Task
CONTENT_CREATION_DESCRIPTION = """
Create high-quality SEO content for {website} in the {niche} industry. {focus_text}
Use the insights from keyword research and content strategy to create engaging, optimized content.
Ensure content addresses user intent, incorporates target keywords naturally, and provides genuine value.
Structure content for readability and engagement with proper heading hierarchy, short paragraphs, and bulleted lists.
Deliver polished, publication-ready content with optimization recommendations.
"""

CONTENT_CREATION_OUTPUT = """
IMPORTANT: Include the FULL publication-ready content in this markdown file. Do not just provide a summary.

The output should include:
1. SEO-optimized headline and subheadings
2. Well-structured content with proper heading hierarchy (at least 1000 words)
3. Naturally incorporated target keywords
4. Internal and external linking recommendations (specified inline)
5. Meta title and description suggestions

The complete article should be publication-ready, written in an engaging, conversational style that follows the special content creation guidelines.
"""

# Analytics Reporting Task
ANALYTICS_REPORTING_DESCRIPTION = """
Develop an SEO analytics and reporting framework for {website} in the {niche} industry.
Define key performance indicators (KPIs) and metrics to track SEO performance.
Create a reporting structure with recommended tools and data sources.
Provide guidelines for data analysis and insight generation.
Develop a dashboard template for ongoing performance monitoring.
Deliver a comprehensive analytics and reporting framework with implementation guidelines.
"""

ANALYTICS_REPORTING_OUTPUT = """
A detailed SEO analytics and reporting framework in markdown format that includes:
1. Key performance indicators (KPIs) and metrics definitions
2. Reporting structure and frequency recommendations
3. Tool selection and implementation guidelines
4. Dashboard template design
5. Analysis and insight generation process
6. Performance benchmarking methodology
"""

# SEO Agency Report Task
SEO_AGENCY_REPORT_DESCRIPTION = """
Synthesize all SEO findings and recommendations for {website} in the {niche} industry into a comprehensive strategy report.
Integrate insights from keyword research, competitor analysis, content strategy, technical audit, on-page optimization, and backlink strategy.
Prioritize recommendations based on potential impact and implementation difficulty.
Create an executive summary with key findings and expected outcomes.
Deliver a comprehensive SEO strategy report with implementation roadmap.
"""

SEO_AGENCY_REPORT_OUTPUT = """
A comprehensive SEO strategy report in markdown format that includes:
1. Executive summary with key findings and recommendations
2. Integrated strategy across all SEO disciplines
3. Prioritized implementation roadmap
4. Resource requirements and timeline
5. Expected outcomes and success metrics
6. Ongoing maintenance and optimization recommendations
"""