---
description: Search real-time stock market information using Exa neural search
name: exa-stock-search
tags:
  - web-search
  - stocks
  - market-research
  - finance
author: Exa Search Integration
---

# Exa Stock Search Skill

🔍 Search real-time stock market information, news, and analysis using Exa's neural search technology.

## Features

- **Stock News** - Get latest news for any stock ticker
- **Market Analysis** - Analyze market trends and insights
- **Company Research** - Find company information and earnings
- **Deep Research** - Perform thorough multi-step research

## Usage

### Search Stock News
Get latest developments about a specific stock:
```
Search for news about Apple (AAPL)
```

### Market Analysis
Analyze market trends and sectors:
```
Analyze AI tech stocks market trends
```

### Company Research
Research company information:
```
Research Microsoft company information
```

### Deep Research
Perform thorough research on topics:
```
Deep research on quantum computing companies
```

## Capabilities Provided

### Tools Available

1. **search_stock_news** - Search for stock news by ticker symbol
   - Input: Stock ticker (e.g., "AAPL", "GOOGL", "TSLA")
   - Returns: Latest news articles, URLs, and highlights

2. **search_market_analysis** - Get market analysis and trends
   - Input: Market topic (e.g., "AI stocks", "renewable energy")
   - Returns: Analysis articles and insights

3. **search_company_info** - Research company information
   - Input: Company name
   - Returns: Company info, earnings, financials

4. **deep_research** - Perform thorough market research
   - Input: Research query
   - Returns: Comprehensive research with citations

## Configuration

- **Search Type**: Auto (balanced relevance and speed)
- **Content**: Highlights (efficient token usage)
- **Speed**: ~1 second per search
- **Results**: Up to 10 per search

API Key: Set `EXA_API_KEY` in environment variables

## Installation

### For Claude Skill Use

1. Place this file in your VS Code workspace
2. Claude will automatically discover and enable it
3. Use natural language queries like "Search for AAPL news"

### For Standalone Use

```bash
# Install dependencies
pip install -r requirements.txt

# Run examples
python -m src.examples.basic_search

# Or use in your code
from src.stock_searcher import StockSearcher
searcher = StockSearcher()
results = searcher.search_stock_news("AAPL")
```

## Examples

### In Claude

```
user: What's the latest with Tesla stock?
claude: I'll search for recent Tesla news for you.
[Uses search_stock_news("TSLA")]

user: Analyze the AI sector for me
claude: Let me research current AI stock trends.
[Uses search_market_analysis("AI stocks")]
```

### In Python

```python
from src.stock_searcher import StockSearcher

searcher = StockSearcher()

# Stock news
results = searcher.search_stock_news("AAPL", num_results=10)

# Market analysis
results = searcher.search_market_analysis("AI stocks")

# Company info
results = searcher.search_company_info("Microsoft")

# Deep research
results = searcher.search_with_deep_research("semiconductor industry")

# Print formatted results
print(StockSearcher.format_results(results))
```

## Environment Setup

Required environment variables:
```env
EXA_API_KEY=your_api_key_here
```

Optional:
```env
OPENAI_API_KEY=your_key  # For OpenAI examples
ANTHROPIC_API_KEY=your_key  # For Claude examples
```

Get your Exa API key: https://dashboard.exa.ai/api-keys

## Search Configuration

### Search Types

- **auto** (default): Balanced relevance and speed (~1s)
- **fast**: Fastest results (<0.5s)
- **deep**: Thorough research (2-5s)
- **deep-reasoning**: Most comprehensive (5-10s)

### Content Types

- **highlights**: Compact excerpts (recommended, lower tokens)
- **text**: Full article content (higher tokens)

## Data Freshness

Content is automatically refreshed as needed:
- Cached results used when available
- Live crawl performed for real-time data
- Configurable freshness settings

## Limitations

- Requires internet connection
- API rate limits apply (check dashboard)
- Search results depend on Exa's index
- Financial data may be delayed

## Support

- Documentation: https://exa.ai/docs
- API Status: https://status.exa.ai
- Dashboard: https://dashboard.exa.ai

---

**Ready to use!** Ask Claude about any stock, market trend, or company.
