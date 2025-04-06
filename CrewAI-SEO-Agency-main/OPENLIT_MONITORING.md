# OpenLIT Monitoring Integration for CrewAI

This document describes how OpenLIT monitoring has been integrated with the CrewAI SEO Agency project.

## Overview

[OpenLIT](https://github.com/openlit/openlit) is an open-source monitoring solution for AI applications. It provides comprehensive tracing and metrics for LLM applications, making it easy to track costs, performance, and behavior of AI agents.

The SEO Agency project now has full OpenLIT integration, enabling:

- Automatic tracing of LLM API calls (OpenAI, Anthropic, etc.)
- Event tracking for crew and agent operations
- Performance monitoring and cost tracking
- Visualization of agent interactions and task sequences

## Setup

The integration is already configured in the codebase. To use it:

1. Make sure the OpenLIT server is running:
   ```bash
   # The server is running at http://localhost:3000
   # Default login: user@openlit.io / openlituser
   ```

2. Ensure your `.env` file contains the OpenLIT API key:
   ```
   OPENLIT_API_KEY=your_openlit_api_key
   ```

3. Run the SEO Agency as normal - monitoring data will be automatically sent to OpenLIT:
   ```bash
   python run_seo_agency.py --website example.com --niche "technology blog"
   ```

## Testing the Integration

You can run a simple test to verify the OpenLIT integration is working:

```bash
python test_openlit_integration.py
```

This will:
- Initialize OpenLIT
- Record test events
- Make a sample OpenAI API call that will be traced
- Verify the monitoring setup

## Dashboard Access

OpenLIT provides a web dashboard to view monitoring data:

- **URL**: http://localhost:3000
- **Default Login**:
  - Email: user@openlit.io
  - Password: openlituser

## How It Works

The integration works at multiple levels:

1. **Application Level**: OpenLIT is initialized in `run_seo_agency.py`
2. **Event Tracking**: Custom events are tracked through `src/seo_agency/events.py`
3. **Agent Monitoring**: Agents are automatically monitored through OpenLIT's CrewAI integration
4. **API Call Tracing**: LLM API calls are automatically traced by OpenLIT

## Features Enabled

- **Cost Tracking**: Track spending on OpenAI and Anthropic calls
- **Performance Monitoring**: Measure latency and token usage
- **Task Visualization**: See the flow of tasks through the crew
- **Error Detection**: Identify and debug failures in agent execution
- **Token Usage**: Monitor token consumption for optimization opportunities

## Future Enhancements

Future improvements could include:
- Custom dashboards for specific SEO metrics
- Alert configurations for budget limits
- Integration with additional observability platforms
- Enhanced reporting capabilities