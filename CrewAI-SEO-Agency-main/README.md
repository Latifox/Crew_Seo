# AI-Powered SEO Agency

An advanced, autonomous SEO agency built with CrewAI, providing comprehensive SEO analysis and strategy generation through a team of specialized AI agents.

## 🚀 Overview

This system creates professional-grade SEO recommendations by analyzing websites within specific industries or niches. It leverages a hierarchical crew of AI agents, each with specialized knowledge and tools, to generate:

- Keyword research and opportunity analysis
- Competitor analysis with actionable insights
- Content strategy and topic recommendations
- Technical SEO audit with prioritized fixes
- On-page optimization guidelines based on actual website content
- Backlink acquisition strategy
- SEO-optimized content creation
- Analytics reporting framework
- Comprehensive SEO strategy reports

## ✨ Key Features

- **Hierarchical AI Agent Structure**: Manager agent coordinates specialized agents for each SEO domain
- **Real Website Content Analysis**: FireCrawl integration for accurate on-page analysis
- **Multiple LLM Support**: OpenAI for analytical tasks, Claude for content creation
- **Long & Short-Term Memory**: Agents maintain context throughout the analysis
- **Knowledge Integration**: Specialized knowledge sources for SEO best practices
- **Multi-Tool Integration**: Google Search Console, Analytics, PageSpeed, SERP, and more
- **Comprehensive Reporting**: Detailed markdown reports for all aspects of SEO

## 📋 Project Structure

```
.
├── .env                # Environment variables (API keys)
├── pyproject.toml      # Python project configuration
├── knowledge/          # SEO knowledge base
│   ├── google_algorithm_updates.txt  # Algorithm information
│   └── seo_best_practices.txt        # SEO best practices
├── google/             # Google API credentials
│   └── secret.json     # Service account credentials
├── src/                # Source code
│   └── seo_agency/     # SEO agency implementation
│       ├── config/     # Agent and task configurations
│       ├── tools/      # Custom SEO tools
│       ├── crew.py     # Agent and crew definitions
│       ├── main.py     # Main entry point
│       └── ...         # Supporting modules
├── output/             # Generated reports
├── docs/               # Documentation (CrewAI docs)
└── examples/           # Example code
```

## 🛠️ Installation

### Prerequisites

- Python 3.9+ 
- Git
- API keys for:
  - OpenAI (for analytical tasks)
  - Anthropic (for content creation)
  - SERPER (for search capabilities)
  - MOZ (for backlink analysis)
  - Google (for PageSpeed Insights)
  - FireCrawl (for website crawling and scraping)
  - Google Service Account (for Analytics and Search Console)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CrewAI-SEO-Production
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Create a `.env` file with your API keys (see `.env.example` for a template)

4. Place Google service account credentials in `google/secret.json`

## 🚀 Usage

Run the SEO agency with the following command:

```bash
python -m src.seo_agency.main --website "example.com" --niche "Your Industry" --specific-focus "Your Focus Area" --verbose
```

### Command-line Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `--website` | The website to analyze | Yes |
| `--niche` | Industry or niche (e.g., "health", "finance") | Yes |
| `--specific-focus` | Specific focus area within the niche | No |
| `--content-topic` | Topic for content creation task | No |
| `--tasks` | Specific tasks to run (default: full_strategy) | No |
| `--output-dir` | Directory to store output reports | No |
| `--verbose` | Enable verbose output | No |

### Available Tasks

- `keyword_research`: Generate keyword opportunities
- `competitor_analysis`: Analyze competitor websites
- `content_strategy`: Develop content strategy recommendations
- `technical_audit`: Perform technical SEO audit
- `onpage_optimization`: Create on-page optimization recommendations
- `backlink_strategy`: Develop a backlink acquisition strategy
- `content_creation`: Generate SEO-optimized content
- `analytics_reporting`: Create an analytics reporting framework
- `full_strategy`: Run all tasks (default)

### Examples

```bash
# Run full SEO strategy for a health website
python -m src.seo_agency.main --website "healthylifestyle.com" --niche "Health and Wellness" --specific-focus "Nutrition" --verbose

# Generate only content for a tech website
python -m src.seo_agency.main --website "techblog.com" --niche "Technology" --content-topic "AI Applications" --tasks content_creation --verbose

# Run technical audit and on-page optimization
python -m src.seo_agency.main --website "ecommerce.com" --niche "E-commerce" --tasks technical_audit onpage_optimization --verbose
```

## 📈 Output

The system generates detailed markdown reports in the `output/` directory:

- `keyword_research_report.md`: Keyword opportunities and analysis
- `competitor_analysis_report.md`: Competitor insights and strategies
- `content_strategy_plan.md`: Content strategy recommendations
- `technical_audit_report.md`: Technical SEO issues and fixes
- `onpage_optimization_report.md`: On-page SEO recommendations
- `backlink_strategy_plan.md`: Backlink acquisition strategies
- `created_content.md`: SEO-optimized content
- `analytics_reporting_framework.md`: Analytics setup recommendations
- `seo_strategy_report.md`: Comprehensive SEO strategy

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
SERPER_API_KEY=your_serper_key
MOZ_API_KEY=your_moz_key
GOOGLE_API_KEY=your_google_key
GOOGLE_PAGE_SPEED_API_KEY=your_pagespeed_key
FIRECRAWL_API_KEY=your_firecrawl_key

# Google Service Account Settings
# The service account JSON file should be placed in the google/secret.json location
GOOGLE_SERVICE_ACCOUNT=your-service-account@project.iam.gserviceaccount.com

# Configuration
LOG_LEVEL=INFO
```

### Agent Configuration

Agent configurations can be modified in `src/seo_agency/configurations.py` or in the YAML files under `src/seo_agency/config/`.

## 🧩 System Architecture

### Agent Hierarchy

- **SEO Manager**: Coordinates all other agents (uses OpenAI)
- **Specialized Agents**:
  - Keyword Researcher
  - Competitor Analyst
  - Content Strategist
  - Technical Auditor
  - On-Page Optimizer
  - Backlink Strategist
  - Content Creator (uses Claude)
  - Analytics Specialist

### Tools Integration

- **Search Tools**: SERP API for web search
- **Google Tools**: PageSpeed, Search Console, Analytics 
- **Website Analysis**: FireCrawl for crawling and content extraction
- **File Operations**: Reading and writing reports

### Knowledge Sources

The system uses specialized knowledge sources for SEO best practices and Google algorithm updates, stored as text files in the `knowledge/` directory.

### Memory System

The crew utilizes both long-term and short-term memory through CrewAI's memory system, configured with OpenAI embeddings.

## 🔍 Recent Improvements

- Added FireCrawl integration for actual website content analysis
- Enhanced content creation with Claude and specialized prompts
- Implemented hierarchical crew structure with manager delegation
- Fixed memory integration for better context retention
- Added comprehensive error handling and fallbacks
- Improved task descriptions and output formats
- Enhanced Google tools integration
- Fixed import paths and module structure

## 📝 Contributing

Contributions are welcome! Here's how you can extend the system:

- Add new agents in `src/seo_agency/crew.py`
- Create new tools in `src/seo_agency/tools/`
- Modify task definitions in `src/seo_agency/string_based_tasks.py`
- Update configurations in `src/seo_agency/configurations.py`
