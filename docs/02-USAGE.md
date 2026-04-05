# Complete Usage Guide / 完整使用指南

**Crisis Investment Researcher v0.3.0**

This guide covers every feature of the system: search, research reports, valuation, data freshness, cross-validation, and export.

---

## Table of Contents / 目录

1. [Configuration / 配置](#configuration)
2. [Search / 搜索](#search)
3. [Research Reports / 研究报告](#research-reports)
4. [Valuation Methods / 估值方法](#valuation-methods)
5. [Data Freshness / 数据时效性](#data-freshness)
6. [Data Validation / 数据验证](#data-validation)
7. [Report Export / 报告导出](#report-export)
8. [CLI Reference / 命令行参考](#cli-reference)

---

## Configuration

All settings live in `config.yaml` at the project root. The file uses bilingual comments (Chinese + English).

### config.yaml structure / 配置文件结构

```yaml
# API Keys / API 密钥
api_keys:
  exa: "your-key"          # Required / 必填
  openai: ""                # Optional / 选填
  anthropic: ""             # Optional / 选填

# Search Settings / 搜索设置
search:
  type: "auto"              # auto | fast | deep | deep-reasoning
  num_results: 10           # Default results per search / 每次搜索默认结果数
  max_characters: 4000      # Max chars per result / 每条结果最大字符数
  content_mode: "highlights" # highlights | text

# Data Validation / 数据验证
validation:
  require_source_citations: true
  min_cross_validation_sources: 2
  auto_flag_stale_data: true
  block_export_on_high_risk: true
  freshness_thresholds:
    stock_price: 1           # Days / 天
    financial_statements: 120
    analyst_ratings: 30
    news_sentiment: 3
    # ... (20 categories total, see config.yaml for full list)

# Source Credibility Tiers / 来源可信度分级
source_tiers:
  tier1: ["sec.gov", "hkex.com.hk", "defillama.com", ...]  # Official/Regulatory
  tier2: ["bloomberg.com", "reuters.com", "yahoo.com", ...]  # Mainstream Financial
  tier3: ["investopedia.com", "benzinga.com", ...]            # Analytical Reference
  # Tier 4 = anything not in tier1-3 (needs cross-validation)

# Report Export / 报告导出
export:
  markdown_dir: "research Output/markdown"
  pdf_dir: "research Output/pdf"
  naming_pattern: "{date}_{ticker}_{framework}_{report_id}"
  pdf_engines: ["chromium", "fitz", "text"]

# Network / 网络设置
network:
  timeout: 30
  max_retries: 3
  retry_delay: 1.0
```

### Configuration priority / 配置优先级

Settings are loaded by `src/config.py` in this order (highest priority first):

1. Environment variables (`.env` file or system env)
2. `config.yaml`
3. Built-in defaults

```python
from src.config import (
    get_api_key,
    get_search_config,
    get_validation_config,
    get_freshness_thresholds,
    get_source_tiers,
    get_export_config,
    get_network_config,
)

# Examples / 示例
api_key = get_api_key("exa")
search_cfg = get_search_config()   # {"type": "auto", "num_results": 10, ...}
thresholds = get_freshness_thresholds()  # {"stock_price": 1, ...}
```

---

## Search

The search system is built on the Exa neural search API with automatic retry and exponential backoff.

### StockSearcher (src/search/exa_searcher.py)

```python
from src.search.exa_searcher import StockSearcher

searcher = StockSearcher()

# Stock news / 股票新闻
news = searcher.search_stock_news("AAPL", num_results=5)

# Market analysis / 市场分析
analysis = searcher.search_market_analysis("AI stocks", num_results=5)

# Company info / 公司信息
company = searcher.search_company_info("Microsoft", num_results=5)

# Deep research (uses full text, up to 20000 chars per result)
# 深度研究 (使用全文模式, 每条结果最多 20000 字符)
deep = searcher.search_with_deep_research("semiconductor industry", num_results=5)
```

### Formatted output / 格式化输出

```python
# Text output with source tier tags / 带来源分级标签的文本输出
print(StockSearcher.format_results(news))
```

Output example:

```
============================================================
Stock Ticker: AAPL
Found 5 results
============================================================

1. [Tier 2 (主流财经)] Apple Inc. (AAPL) Stock Price, News...
   URL: https://finance.yahoo.com/quote/AAPL/
   Highlight: Apple reports record Q1 revenue of $124B...

2. [Tier 1 (官方/监管)] Apple Inc. Form 10-Q
   URL: https://sec.gov/cgi-bin/browse-edgar?...
   Highlight: Net sales increased 6% year over year...
```

### Source credibility tiers / 来源可信度分级

Every search result is automatically classified into one of four tiers:

| Tier   | Label / 标签          | Examples / 示例                         |
|--------|-----------------------|----------------------------------------|
| Tier 1 | Official/Regulatory   | sec.gov, hkex.com.hk, defillama.com   |
| Tier 2 | Mainstream Financial  | bloomberg.com, reuters.com, yahoo.com  |
| Tier 3 | Analytical Reference  | investopedia.com, benzinga.com         |
| Tier 4 | Needs verification    | Everything else / 其他来源              |

Tier domains are configurable in `config.yaml` under `source_tiers`.

```python
# Classify a URL / 对URL进行分级
tier_label = searcher.classify_source_tier("https://sec.gov/cgi-bin/...")
# Returns: "Tier 1 (官方/监管)"
```

### Retry logic / 重试逻辑

The searcher uses exponential backoff for transient failures. Configured via `config.yaml`:

- `network.max_retries`: number of retries (default: 3)
- `network.retry_delay`: base delay in seconds (default: 1.0)
- Auth errors (401/403) are never retried.

---

## Research Reports

The system supports three research frameworks, each generating a structured report skeleton.

### InvestmentResearcher (src/core/researcher.py)

```python
from src.core.researcher import InvestmentResearcher
from src.search.exa_searcher import StockSearcher

searcher = StockSearcher()
researcher = InvestmentResearcher(searcher)

# Generate report skeleton -- framework is auto-detected
# 生成报告骨架 -- 框架自动检测
report = researcher.generate_report_skeleton(
    target_name="Apple",
    ticker="AAPL",
    market="us",          # Optional: "us", "hk", "a-share", "crypto"
    framework="",         # Optional: "mature", "growth", "web3" (empty = auto-detect)
)

print(report["framework"])        # "growth"
print(report["report_id"])        # UUID
print(report["unfilled_fields"])  # ["STRATEGIC_POSITIONING", "MARKET_SIZE", ...]
print(report["content"][:200])    # Markdown report with {{PLACEHOLDER}} fields
```

### Three frameworks / 三种框架

| Framework       | Label / 标签  | Target type / 目标类型                | Key sections |
|-----------------|---------------|--------------------------------------|--------------|
| `mature`        | 成熟公司       | Banks, oil, utilities, telecom       | 7 major steps, People/Business/Results 10-point scoring |
| `growth`        | 成长性公司     | Tech, SaaS, high-growth companies    | 14 sections: market/team/business/financials/valuation |
| `web3`          | Web3项目       | DeFi, tokens, DAOs, protocols        | 15 sections: tokenomics/on-chain/ecosystem/governance |

### Auto-detection logic / 自动检测逻辑

The framework is detected from target name and market keywords:

- `"crypto"`, `"defi"`, `"token"`, `"dao"`, `"eth"`, `"sol"`, etc. --> `web3`
- `"bank"`, `"insurance"`, `"energy"`, `"oil"`, `"utility"`, etc. --> `mature`
- Everything else --> `growth`

### Research query planning / 研究查询规划

After generating a skeleton, get prioritized search queries to fill each field:

```python
queries = researcher.get_research_queries(
    target_name="Apple",
    ticker="AAPL",
    framework="growth",
)

for q in queries[:3]:
    print(f"[P{q['priority']}] {q['field']}: {q['query']}")
    # [P1] STRATEGIC_POSITIONING: Apple AAPL company overview strategic positioning
    # [P1] TARGET_USER/PAIN_POINT/SOLUTION: Apple AAPL target users pain points solutions
    # [P1] GROWTH_SPEED: Apple AAPL revenue growth rate YoY quarterly
```

Each query includes:

- `priority`: 1 (highest) to 3 (supplementary)
- `field`: the report placeholder to fill
- `preferred_sources`: recommended source types
- `data_type`: "quantitative" or "qualitative"
- `requires_source_citation`: whether the data must have a source tag

### Do-Not-Invest Checklist / 不为清单

```python
checklist = researcher.get_checklist("growth")
for item in checklist:
    print(f"{item['id']}. {item['rule']}")
    # 1. 终生投资不超30支股票和30支代币
    # 2. 没有买完后踏实睡觉的坚定信心不投
    # ...
```

### Position sizing / 仓位管理

```python
sizing = researcher.get_position_sizing(
    intrinsic_value=200.0,
    current_price=95.0,
)
print(sizing["zone_label"])       # "深水区（长期持有复利增长）"
print(sizing["discount_rate"])    # "47.5%"
print(sizing["buy_ladder"])
# {"9折": {"price": 180.0, "allocation": "30%"},
#  "7折": {"price": 140.0, "allocation": "30%"},
#  "5折": {"price": 100.0, "allocation": "40%"}}
```

---

## Valuation Methods

The system provides 10+ valuation methods, all accessible as static methods.

### ValuationMethods (src/core/valuation.py)

| Method              | Function            | Description / 描述                   |
|---------------------|---------------------|--------------------------------------|
| DCF                 | `dcf()`             | Discounted Cash Flow / 自由现金流折现  |
| Graham              | `graham_formula()`  | Benjamin Graham intrinsic value / 格雷厄姆公式 |
| PE Relative         | `pe_relative()`     | PE ratio valuation / 市盈率对标       |
| PB Relative         | `pb_relative()`     | PB ratio valuation / 市净率对标       |
| PS Relative         | `ps_relative()`     | PS ratio valuation / 市销率对标       |
| EV/EBITDA           | `ev_ebitda()`       | Enterprise value multiple / 企业价值倍数 |
| PEG                 | `peg()`             | PEG ratio / PEG估值法                |
| DDM                 | `ddm()`             | Dividend Discount Model / 股利折现模型 |
| Owner Earnings      | `owner_earnings_valuation()` | Buffett owner earnings / 股东盈余估值 |
| Replacement Cost    | `replacement_cost()`| Liquidation value / 重置成本法        |
| Cross-Validate      | `cross_validate()`  | Aggregate all methods / 交叉验证汇总  |

### Example: DCF valuation / DCF估值示例

```python
from src.core.valuation import ValuationMethods

result = ValuationMethods.dcf(
    fcf_current=8_000_000_000,   # Current free cash flow / 当前自由现金流
    growth_rate=0.15,             # 15% annual growth / 15%年增长率
    terminal_growth=0.03,         # 3% terminal growth / 3%永续增长率
    discount_rate=0.10,           # 10% WACC / 10%折现率
    years=10,                     # Projection period / 预测年数
    shares_outstanding=15_000_000_000,
)
print(result["method"])           # "DCF自由现金流折现"
print(result["per_share_value"])  # Intrinsic value per share / 每股内在价值
```

### Example: Cross-validation / 交叉验证示例

```python
valuations = [
    ValuationMethods.dcf(fcf_current=8e9, growth_rate=0.15, shares_outstanding=15e9),
    ValuationMethods.graham_formula(eps=6.5, growth_rate=0.15),
    ValuationMethods.pe_relative(eps=6.5, industry_pe=25),
    ValuationMethods.peg(eps=6.5, growth_rate=0.15),
]

cross = ValuationMethods.cross_validate(valuations)
print(cross["median"])       # Median valuation / 中位数估值
print(cross["spread"])       # Spread between methods / 方法间离散度
print(cross["confidence"])   # "high" / "medium" / "low"
```

If input parameters lack source citations, the cross-validation result will include a `source_audit` warning.

---

## Data Freshness

The freshness checker validates whether data in a report is still within acceptable age thresholds.

### DataFreshnessChecker (src/core/freshness.py)

```python
from src.core.freshness import DataFreshnessChecker

checker = DataFreshnessChecker()

# Check a single data point / 检查单个数据点
result = checker.check_data_point(
    category="stock_price",
    source="Yahoo Finance",
    date_string="2026-04-03",
)
print(result["status"])        # "fresh" | "aging" | "stale" | "unknown"
print(result["status_label"])  # "fresh - 数据新鲜（1天前）"
```

### Scan a full report / 扫描完整报告

```python
report_content = open("my_report.md").read()
report_check = checker.check_report(report_content)

print(report_check["overall_status"])   # "CURRENT" | "AGING" | "NEEDS_UPDATE" | "NO_DATES"
print(report_check["fresh_count"])      # Number of fresh data points
print(report_check["stale_count"])      # Number of stale data points
```

### Check unfilled fields / 检查未填字段

```python
unfilled = checker.check_unfilled_fields(report_content)
print(unfilled["total_unfilled"])         # Total placeholder count
print(unfilled["completeness_estimate"])  # e.g. "45%"
print(unfilled["critical_unfilled"])      # Fields with VAL_, PRICE, SCORE, etc.
print(unfilled["important_unfilled"])     # Fields with REVENUE, MARGIN, GROWTH, etc.
```

### Audit source citations / 审计来源标注

```python
audit = checker.audit_source_citations(report_content)
print(audit["total_data_points"])     # Number of financial data references found
print(audit["cited_count"])           # How many have proper source tags
print(audit["uncited_count"])         # How many lack citation
print(audit["hallucination_risk"])    # "low" | "medium" | "high"
print(audit["uncited_items"][:3])     # List of uncited data snippets
```

### Freshness threshold categories / 时效性阈值类别

All thresholds are configurable in `config.yaml` under `validation.freshness_thresholds`:

| Category / 类别       | Default / 默认阈值 (days) | Description / 描述            |
|-----------------------|--------------------------|-------------------------------|
| stock_price           | 1                        | Stock/crypto prices / 股价     |
| financial_statements  | 120                      | Income, balance sheet / 财务报表 |
| analyst_ratings       | 30                       | Analyst ratings / 分析师评级    |
| insider_trading       | 14                       | Insider transactions / 内部交易 |
| news_sentiment        | 3                        | News articles / 新闻资讯       |
| market_data           | 1                        | Index, volume / 市场数据       |
| industry_report       | 180                      | Industry research / 行业报告    |
| tvl_data              | 1                        | DeFi TVL / 链上锁仓            |
| protocol_revenue      | 7                        | Protocol fees / 协议收入        |
| token_unlock          | 30                       | Token vesting / 代币解锁        |
| governance_proposal   | 14                       | DAO governance / 治理提案       |
| github_activity       | 7                        | Dev activity / 开发活动         |
| macro_economic        | 30                       | GDP, CPI, rates / 宏观经济     |

(See `config.yaml` for the full list of 20 categories.)

---

## Data Validation

The DataValidator provides cross-validation, source scoring, and confidence assessment for individual data points.

### DataValidator (src/core/validator.py)

```python
from src.core.validator import DataValidator

validator = DataValidator()

# Validate a data point against multiple sources
# 对一个数据点进行多源交叉验证
result = validator.validate_data_point(
    value=38.3,
    label="Revenue (Q1 2026)",
    sources=[
        {"name": "SEC 10-Q", "url": "https://sec.gov/...", "date": "2026-03-15", "value": 38.3},
        {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/...", "date": "2026-03-15", "value": 38.2},
    ],
    tolerance=0.05,  # 5% acceptable deviation / 5%可接受偏差
)

print(result["status"])       # "verified" | "single_source" | "unverified" | "inconsistent"
print(result["confidence"])   # "high" | "medium" | "low"
print(result["citation"])     # "[来源: SEC 10-Q | 日期: 2026-03-15]"
print(result["consistency"])  # "consistent" | "inconsistent"
print(result["max_deviation"])  # "0.3%" -- deviation between sources
```

### Validate search results / 验证搜索结果

```python
scored = validator.validate_search_results([
    {"url": "https://sec.gov/filings/...", "title": "Apple 10-Q"},
    {"url": "https://benzinga.com/...", "title": "Apple Analysis"},
])
print(scored["overall_quality"])    # "high" | "medium" | "low"
print(scored["tier_distribution"])  # {1: 1, 2: 0, 3: 1, 4: 0}
```

### Assess overall report confidence / 评估报告整体置信度

```python
# After validating multiple data points / 验证多个数据点后
assessment = validator.assess_report_confidence(validator.validation_log)
print(assessment["overall_confidence"])  # "high" | "medium" | "low"
print(assessment["verified_ratio"])       # e.g. "80%"
print(assessment["recommendation"])       # Human-readable recommendation
```

### Validation summary / 验证摘要

```python
print(validator.get_validation_summary())
# Output:
# === Data Validation Summary / 数据验证摘要 ===
# Total data points: 12
# Verified (cross-validated): 8
# Single source: 3
# Unverified: 1
# Inconsistent: 0
# Overall confidence: HIGH
```

---

## Report Export

The exporter outputs research reports in Markdown and/or PDF format to separate directories.

### ReportExporter (src/export/exporter.py)

```python
from src.export.exporter import ReportExporter

exporter = ReportExporter()

# Export as both Markdown and PDF / 同时导出 Markdown 和 PDF
paths = exporter.export_both(
    content="# Apple Research Report\n...",
    ticker="AAPL",
    framework="growth",
    report_id="abc123",
)
print(paths["markdown"])  # research Output/markdown/2026-04-04_AAPL_growth_abc123.md
print(paths["pdf"])       # research Output/pdf/2026-04-04_AAPL_growth_abc123.pdf
```

### Export formats / 导出格式

```python
# Markdown only / 仅 Markdown
md_path = exporter.export_markdown(content, ticker, framework, report_id)

# PDF only / 仅 PDF
pdf_path = exporter.export_pdf(content, ticker, framework, report_id)

# Both / 两者都导出
paths = exporter.export_both(content, ticker, framework, report_id)
```

### PDF rendering engine priority / PDF 渲染引擎优先级

The system tries engines in order (configurable in `config.yaml`):

1. **Chromium** (via Playwright) -- best quality, CJK font support
   - Requires: `pip install playwright && playwright install chromium`
2. **fitz** (PyMuPDF) -- good quality, lightweight
   - Requires: `pip install pymupdf`
3. **text** -- plain text fallback, always available

### Output directories / 输出目录

Default paths (relative to project root, configurable in `config.yaml`):

- Markdown: `research Output/markdown/`
- PDF: `research Output/pdf/`

### File naming / 文件命名

Pattern: `{date}_{ticker}_{framework}_{report_id}`

Example: `2026-04-04_AAPL_growth_a1b2c3d4.md`

### Pre-export audit / 导出前审计

When `validation.block_export_on_high_risk` is `true` in `config.yaml`, the MCP server automatically runs a citation audit before export. If hallucination risk is "high", the export is blocked and an error is returned.

---

## CLI Reference

```
python src/claude_skill.py <query> [options]
```

### Arguments / 参数

| Argument     | Required | Description / 描述                              |
|-------------|----------|--------------------------------------------------|
| `query`      | Yes      | Search query or research request / 查询或研究请求  |
| `--json`     | No       | Output in JSON format / JSON格式输出               |
| `--research` | No       | Use research routing mode / 使用研究路由模式        |
| `--results N`| No       | Limit number of results (default: 10) / 限制结果数 |

### Examples / 示例

```powershell
# Stock news search / 股票新闻搜索
python src/claude_skill.py "Apple latest stock news" --results 5

# Market analysis in JSON / JSON格式市场分析
python src/claude_skill.py "Tesla market analysis" --json

# Generate report via research mode / 研究模式生成报告
python src/claude_skill.py "Generate report for AAPL" --research

# Valuation request / 估值请求
python src/claude_skill.py "DCF valuation for Tesla" --research

# Checklist / 投资纪律清单
python src/claude_skill.py "Do-not-invest checklist for growth" --research
```

---

## Related docs / 相关文档

- [Quick start / 快速开始](01-QUICKSTART.md)
- [Claude integration / Claude 集成](03-INTEGRATION.md)
