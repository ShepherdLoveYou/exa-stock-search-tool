---
description: Crisis Investment Research Assistant - Generate structured investment reports using three research frameworks (Mature Company / Growth Company / Web3 Project), cross-validate valuations with 10+ methods, check data freshness, and enforce investment discipline
name: crisis-investment-researcher
tags:
  - investment-research
  - crisis-investing
  - valuation
  - web-search
  - stocks
  - crypto
  - market-research
  - finance
author: Crisis Investment Research System
---

# Crisis Investment Research Assistant

Search real-time information and generate structured investment research reports following the Crisis Investment methodology

## Core Philosophy

**Excess Return = Reversible Crisis of Good Company x Emotionally Mispriced Low Price x Massive Growth Potential x Patience^2**

Three research frameworks for different target types:
- **Mature Company** (成熟公司): 7 major steps with 10-point scoring on People/Business/Results
- **Growth Company** (成长性公司): 14 sections covering market/team/business/financials/valuation
- **Web3 Project** (Web3项目): 15 sections including tokenomics/on-chain/ecosystem/governance

## Features

- **Auto Framework Detection** - Automatically selects mature/growth/web3 framework based on target
- **Report Generation** - Generate structured markdown report skeletons with all required sections
- **Research Query Planning** - Get prioritized search queries to fill report fields
- **10+ Valuation Methods** - DCF, Graham, PE/PB/PS, EV/EBITDA, PEG, DDM, Owner Earnings, Replacement Cost
- **Cross Validation** - Median/mean/spread analysis across all valuation methods
- **Data Freshness Check** - Scan reports for stale data that needs updating
- **Completeness Check** - Find unfilled fields categorized by priority
- **Position Sizing** - Calculate buy ladder (9/7/5 fold) and zone classification
- **Discipline Enforcement** - 不为清单 (Do-Not-Invest Checklist) with 12 rules

## ⚠️ Data Integrity & Anti-Hallucination Rules

**ALL financial data in research reports MUST follow these rules. No exceptions.**

### Rule 1: No Fabricated Numbers
Every financial metric (revenue, net income, EPS, PE, market cap, growth rate, FCF, etc.) MUST come from:
- Exa search results with traceable source URLs
- API responses (FMP, Finnhub, FRED, CoinGecko, DeFiLlama, etc.)
- User-provided documents

**NEVER** generate financial numbers from memory or training data. If data is unavailable, mark as `⚠️ DATA MISSING`.

### Rule 2: Source Attribution Required
Every data point must include: `[Source: XX | Date: YYYY-MM-DD]`
```
Revenue: $38.3B [Source: Exa→SEC 10-Q | Date: 2026-03-15]
PE Ratio: 24.5x [Source: FMP API | Date: 2026-04-01]
TVL: $320M [Source: DeFiLlama API | Date: 2026-04-04]
```

### Rule 3: Cross-Validation Mandatory
Critical financial data must be verified from ≥2 independent sources. If only 1 source: tag `[Single source, not cross-validated]`.

### Rule 4: Freshness Enforcement
- Stock prices: must be ≤1 day old
- Financial statements: must be ≤120 days old  
- News/sentiment: must be ≤3 days old
- Stale data must be flagged: `⚠️ Data may be outdated (N days old)`

### Rule 5: Valuation Input Traceability
For each of the 10+ valuation methods, every input parameter must cite its source. Methods with untraceable inputs must be marked `N/A — input data unavailable` instead of using assumed values.

### Rule 6: Mandatory Report Audit Before Export
Before exporting any report (Markdown or PDF), you MUST run `audit_report_citations` to scan for uncited data points. If hallucination_risk is "high", DO NOT export — go back and fix all uncited financial data. If "medium", flag the issue to the user. Search results now include source tier tags (Tier 1-4) — prefer higher-tier sources for critical data.

### Rule 7: Price Data Must Be Real-Time Verified
Stock prices quoted in reports MUST be verified against ≥2 real-time sources at the time of report generation. If the user provides a price, cross-check it via search. Never assume a price is correct without verification. Tag any unverified price with `⚠️ 未经实时验证`.

### Data Source Priority (by credibility)
1. **Tier 1**: SEC/CSRC/HKEX filings, exchange data, central bank data (FRED), on-chain data (DeFiLlama/Etherscan)
2. **Tier 2**: Structured API data (FMP/Finnhub/Tushare/AKShare/CoinGecko)
3. **Tier 3**: News articles and analyst reports (via Exa search)
4. **Tier 4**: Social media, forums (require verification)
5. **FORBIDDEN**: Claude's own memory/training data for any financial numbers

## Usage

### Generate Research Report
```
Generate a crisis investment research report for Apple (AAPL)
```

### Auto-detect and research Web3
```
Generate research report for Uniswap (UNI) in crypto market
```

### Get Research Queries
```
What data do I need to fill the report for Tesla (TSLA)?
```

### Calculate Valuations
```
Calculate DCF valuation for AAPL with FCF=100B, growth=15%, discount=10%
```

### Cross-Validate
```
Cross validate these valuations: [150, 165, 140, 180, 155]
```

### Check Data Freshness
```
Check if the data in this research report is still current
```

### Position Sizing
```
Calculate position sizing: intrinsic value $200, current price $95
```

### Do-Not-Invest Checklist
```
Run the do-not-invest discipline check for growth company
```

## Capabilities Provided

### Tools Available

1. **search_stock_news** - Search for stock news by ticker symbol
2. **search_market_analysis** - Get market analysis and trends
3. **search_company_info** - Research company information
4. **deep_research** - Perform thorough market research
5. **generate_research_report** - Generate report skeleton with correct framework
6. **get_research_queries** - Get prioritized queries to fill report
7. **check_report_freshness** - Validate data timeliness
8. **check_unfilled_fields** - Find missing data in reports
9. **calculate_valuation** - Run specific valuation method
10. **get_position_sizing** - Calculate buy zones and ladders
11. **get_do_not_invest_checklist** - Return discipline rules
12. **audit_report_citations** - Audit report for uncited data points, detect hallucination risk
13. **export_report** - Export report to Markdown/PDF/both with Chromium rendering
14. **validate_data_point** - Cross-validate a data point against multiple sources with confidence scoring

## Research Frameworks

### Mature Company (7 Steps)
1. Target Introduction
2. Crisis Detection (self-rescue / restructure / external rescue)
3. Opportunity Assessment (People 10pt / Business 10pt / Results 10pt)
4. Buy Timing (10+ valuation methods, must be below 50% of intrinsic value)
5. Sell Timing
6. Disruption Risk
7. Position Principles

### Growth Company (14 Sections)
I-XIV covering: Introduction, Market Size, Team, Business, Industry Value, Competitiveness, Competitors, Profitability, Capital Management, Financial Health, Disruption Risk, Buy Timing, Sell Timing, Position Principles

### Web3 Project (15 Sections)
I-XV covering: Introduction, Market Size, Team, Business, Industry Value, Innovation, Competitiveness, Ecosystem Health, Token Economics, Financial Health, Competitors, Buy Timing, Sell Timing, Disruption Risk, Position Principles

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
3. Use natural language queries to generate research reports

### For Standalone Use

```bash
pip install -r requirements.txt

# Generate a report skeleton
python -c "
from src.core.researcher import InvestmentResearcher
r = InvestmentResearcher()
report = r.generate_report_skeleton('Apple', 'AAPL', 'us')
print(report['content'][:500])
"
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
from src.search.exa_searcher import StockSearcher

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
- Every data point is timestamped and validated against freshness thresholds

## Report Output Requirements

### Every research report must end with a Data Audit Summary:
```
═══ Data Audit Summary ═══
Sources used:    Exa search: N items | API data: N items | User-provided: N items
Cross-validated: N items verified | N items single-source | N items missing
Data freshness:  Newest: YYYY-MM-DD | Oldest: YYYY-MM-DD
Hallucination risk: [List any data points that could not be verified]
Confidence level: HIGH / MEDIUM / LOW (with justification)
```

## Limitations

- Requires internet connection
- API rate limits apply (check dashboard)
- Search results depend on Exa's index
- Financial data may be delayed — always check timestamps
- Real-time prices may not be available
- Claude's training data has a cutoff date — NEVER use memorized financial numbers
- Single-source data should be treated as unverified
## Support

- Documentation: https://exa.ai/docs
- API Status: https://status.exa.ai
- Dashboard: https://dashboard.exa.ai

---

**Ready to use!** Ask Claude about any stock, market trend, or company.
