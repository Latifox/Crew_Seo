"""
SEO Agency Configuration

This module contains the configuration for agents and tasks.
"""

# Agent configurations
AGENT_CONFIGS = {
    "seo_manager": {
        "role": "SEO Manager",
        "goal": "Guide and coordinate the SEO team to develop a comprehensive SEO strategy",
        "backstory": """You are an experienced SEO Manager with over 10 years of experience
        leading SEO strategies for major brands. You have deep expertise in all aspects of SEO,
        from technical SEO to content strategy and link building. You excel at coordinating
        specialists and synthesizing their insights into effective SEO plans."""
    },
    
    "keyword_researcher": {
        "role": "Keyword Research Specialist",
        "goal": "Discover valuable keywords that balance search volume, competition, and relevance",
        "backstory": """You are a data-driven Keyword Research Specialist who excels at finding
        valuable keyword opportunities for businesses. You understand user intent and know how
        to identify keywords with the perfect balance of search volume, competition, and relevance.
        You have a keen eye for long-tail keywords that can drive qualified traffic."""
    },
    
    "competitor_analyst": {
        "role": "Competitor Analysis Expert",
        "goal": "Analyze competing websites to identify their strengths, weaknesses, and SEO strategies",
        "backstory": """You are a strategic Competitor Analysis Expert who specializes in reverse-engineering
        successful SEO strategies. You have a detective's mindset and can quickly identify what makes
        competitors successful in search engines. You've helped numerous businesses outrank their
        competition by finding gaps and opportunities in the market."""
    },
    
    "content_strategist": {
        "role": "Content Strategy Director",
        "goal": "Develop a comprehensive content plan that addresses user needs and search intent",
        "backstory": """You are a Content Strategy Director with experience in creating data-driven
        content plans that drive organic traffic. You understand the intersection of user intent,
        search algorithms, and brand messaging. You know how to create content that ranks well
        while providing genuine value to readers."""
    },
    
    "onpage_optimizer": {
        "role": "On-Page SEO Optimization Expert",
        "goal": "Optimize webpage elements to maximize relevance and user experience",
        "backstory": """You are an On-Page SEO Optimization Expert who knows exactly how to structure
        web pages for maximum search visibility. You understand the technical aspects of page optimization,
        from schema markup to heading structure. You've helped businesses increase their organic
        traffic by making smart, data-driven optimization changes."""
    },
    
    "technical_auditor": {
        "role": "Technical SEO Audit Specialist",
        "goal": "Identify and solve technical issues preventing optimal search performance",
        "backstory": """You are a Technical SEO Audit Specialist with a background in web development
        and SEO. You can spot technical issues that most people miss, from server configuration problems
        to crawlability issues. You've helped websites recover from penalties and achieve dramatic
        improvements in search visibility through technical improvements."""
    },
    
    "backlink_strategist": {
        "role": "Backlink Acquisition and Strategy Expert",
        "goal": "Develop and execute a plan to acquire high-quality, relevant backlinks",
        "backstory": """You are a Backlink Acquisition and Strategy Expert who specializes in
        ethical link building tactics. You know how to analyze link profiles, identify link
        opportunities, and develop strategies that result in natural, high-quality backlinks.
        You've helped websites build authority in highly competitive niches."""
    },
    
    "content_creator": {
        "role": "SEO Content Creator",
        "goal": "Produce engaging, valuable content that satisfies both users and search engines",
        "backstory": """You are a talented SEO Content Creator who knows how to craft content
        that ranks well and engages readers. You understand how to incorporate keywords naturally,
        structure content for readability, and address user intent. Your content consistently
        ranks well and converts visitors into customers."""
    },
    
    "analytics_specialist": {
        "role": "SEO Analytics and Reporting Specialist",
        "goal": "Track, analyze, and report on SEO performance metrics and ROI",
        "backstory": """You are an SEO Analytics and Reporting Specialist with a data-driven mindset.
        You know how to set up tracking, interpret complex data, and derive actionable insights.
        You've helped businesses attribute revenue to SEO efforts and justify increased investment
        in organic search strategies."""
    }
}

# Task configurations
TASK_CONFIGS = {
    "keyword_research_task": {
        "description": """Conduct comprehensive keyword research for {website} in the {niche} industry.
        Focus on {specific_focus} if specified. Identify primary keywords, long-tail variations,
        and question-based queries. Analyze search volume, competition, and commercial intent.
        Organize keywords by user journey stage and prioritize based on potential impact.
        Deliver a complete keyword research report with recommendations.""",
        "expected_output": """A detailed keyword research report in markdown format that includes:
        1. Primary keywords with search volumes and competition metrics
        2. Long-tail keyword opportunities
        3. Question-based queries for content development
        4. Keyword grouping by topic and user intent
        5. Prioritized list of keywords to target
        """
    },
    
    "competitor_analysis_task": {
        "description": """Analyze top competitors of {website} in the {niche} industry, with focus on {specific_focus} if specified.
        Identify at least 5 key competitors based on keyword overlap and market position.
        Analyze their domain authority, backlink profile, content strategy, technical SEO, and on-page optimization.
        Identify their strengths, weaknesses, and opportunities to outperform them.
        Deliver a comprehensive competitor analysis report with actionable insights.""",
        "expected_output": """A detailed competitor analysis report in markdown format that includes:
        1. List of top competitors with domain metrics
        2. Analysis of competitors' content strategies
        3. Technical SEO comparison
        4. Backlink profile analysis
        5. Content gap analysis
        6. Recommendations for outperforming competitors
        """
    },
    
    "content_strategy_task": {
        "description": """Develop a content strategy for {website} in the {niche} industry, focusing on {specific_focus} if specified.
        Use the insights from keyword research and competitor analysis to create a comprehensive content plan.
        Include content pillars, topic clusters, content formats, and publishing schedule.
        Consider user journey stages and search intent in your recommendations.
        Provide guidelines for content optimization and promotion.
        Deliver a detailed content strategy plan with implementation roadmap.""",
        "expected_output": """A comprehensive content strategy plan in markdown format that includes:
        1. Content pillars and topic clusters
        2. Content formats and types
        3. Publishing schedule and content calendar
        4. Content optimization guidelines
        5. Content promotion strategies
        6. Success metrics and KPIs
        """
    },
    
    "technical_audit_task": {
        "description": """Conduct a comprehensive technical SEO audit for {website} in the {niche} industry.
        Analyze site structure, URL format, page speed, mobile friendliness, indexability, crawlability, and schema markup.
        Identify technical issues preventing optimal search performance.
        Evaluate internal linking, duplicate content, and canonical usage.
        Deliver a technical SEO audit report with prioritized recommendations.""",
        "expected_output": """A detailed technical SEO audit report in markdown format that includes:
        1. Site structure and architecture analysis
        2. Page speed and performance assessment
        3. Mobile optimization review
        4. Indexing and crawlability issues
        5. Schema markup implementation recommendations
        6. Prioritized list of technical fixes
        """
    },
    
    "onpage_optimization_task": {
        "description": """Develop on-page optimization recommendations for {website} in the {niche} industry, focusing on {specific_focus} if specified.
        Create guidelines for title tags, meta descriptions, heading structure, content formatting, internal linking, and schema markup.
        Provide specific recommendations for optimizing key pages based on target keywords.
        Deliver an on-page optimization plan with implementation guidelines.""",
        "expected_output": """A comprehensive on-page optimization plan in markdown format that includes:
        1. Title tag and meta description templates
        2. Heading structure recommendations
        3. Content optimization guidelines
        4. Internal linking strategy
        5. Schema markup implementation guide
        6. Page-specific optimization recommendations
        """
    },
    
    "backlink_strategy_task": {
        "description": """Develop a backlink acquisition strategy for {website} in the {niche} industry, focusing on {specific_focus} if specified.
        Identify high-quality link building opportunities through competitor analysis, content gap analysis, and industry research.
        Create strategies for guest posting, resource link building, broken link building, and digital PR.
        Provide guidelines for outreach and relationship building.
        Deliver a comprehensive backlink strategy with implementation timeline.""",
        "expected_output": """A detailed backlink strategy plan in markdown format that includes:
        1. Link building opportunity analysis
        2. Outreach templates and guidelines
        3. Content creation recommendations for link acquisition
        4. Digital PR strategies
        5. Implementation timeline and resource requirements
        6. Success metrics and tracking recommendations
        """
    },
    
    "content_creation_task": {
        "description": """Create high-quality SEO content for {website} in the {niche} industry, focusing on {specific_focus} if specified.
        Use the insights from keyword research and content strategy to create engaging, optimized content.
        Ensure content addresses user intent, incorporates target keywords naturally, and provides genuine value.
        Structure content for readability and engagement with proper heading hierarchy, short paragraphs, and bulleted lists.
        Deliver polished, publication-ready content with optimization recommendations.""",
        "expected_output": """Publication-ready content in markdown format that includes:
        1. SEO-optimized headline and subheadings
        2. Well-structured content with proper heading hierarchy
        3. Naturally incorporated target keywords
        4. Internal and external linking recommendations
        5. Meta title and description suggestions
        """
    },
    
    "analytics_reporting_task": {
        "description": """Develop an SEO analytics and reporting framework for {website} in the {niche} industry.
        Define key performance indicators (KPIs) and metrics to track SEO performance.
        Create a reporting structure with recommended tools and data sources.
        Provide guidelines for data analysis and insight generation.
        Develop a dashboard template for ongoing performance monitoring.
        Deliver a comprehensive analytics and reporting framework with implementation guidelines.""",
        "expected_output": """A detailed SEO analytics and reporting framework in markdown format that includes:
        1. Key performance indicators (KPIs) and metrics definitions
        2. Reporting structure and frequency recommendations
        3. Tool selection and implementation guidelines
        4. Dashboard template design
        5. Analysis and insight generation process
        6. Performance benchmarking methodology
        """
    },
    
    "seo_agency_report_task": {
        "description": """Synthesize all SEO findings and recommendations for {website} in the {niche} industry into a comprehensive strategy report.
        Integrate insights from keyword research, competitor analysis, content strategy, technical audit, on-page optimization, and backlink strategy.
        Prioritize recommendations based on potential impact and implementation difficulty.
        Create an executive summary with key findings and expected outcomes.
        Deliver a comprehensive SEO strategy report with implementation roadmap.""",
        "expected_output": """A comprehensive SEO strategy report in markdown format that includes:
        1. Executive summary with key findings and recommendations
        2. Integrated strategy across all SEO disciplines
        3. Prioritized implementation roadmap
        4. Resource requirements and timeline
        5. Expected outcomes and success metrics
        6. Ongoing maintenance and optimization recommendations
        """
    }
}