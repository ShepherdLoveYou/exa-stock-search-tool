# API Reference / API 参考文档

v0.3.0 -- Crisis Investment Researcher

Complete class, method, and parameter documentation for all modules.
所有模块的类、方法和参数的完整文档。

---

## Module Overview / 模块总览

```
src/
|-- config.py                  # Centralized config loader / 集中配置加载器
|-- claude_skill.py            # CLI entry point / CLI 入口
|-- search/
|   +-- exa_searcher.py        # StockSearcher / 搜索引擎
|-- core/
|   |-- researcher.py          # InvestmentResearcher / 投研引擎
|   |-- valuation.py           # ValuationMethods / 估值方法集合
|   |-- freshness.py           # DataFreshnessChecker / 数据时效性检查器
|   +-- validator.py           # DataValidator / 数据验证器
|-- server/
|   |-- mcp_server.py          # ExaMCPServer (14 tools) / MCP 服务器
|   +-- skill_router.py        # UnifiedSkillRouter / 统一路由
+-- export/
    |-- exporter.py            # ReportExporter (Markdown + PDF) / 报告导出
    +-- naming.py              # ReportNaming / 文件命名
```

---

## Config Functions / 配置函数

Location / 位置: `src/config.py`

Centralized configuration loader. All modules read settings through these
functions instead of accessing `.env` or YAML directly.

Priority: environment variables > config.yaml > built-in defaults.
优先级: 环境变量 > config.yaml > 内置默认值。

### load_config

```python
load_config(force_reload: bool = False) -> Dict
```

Load and cache the merged configuration from `.env` and `config.yaml`.
Call with `force_reload=True` to re-read files.

### get_api_key

```python
get_api_key(name: str = "exa") -> str
```

Get an API key by logical name.

**Parameters / 参数**:

| Name   | Type | Default | Description                                           |
|--------|------|---------|-------------------------------------------------------|
| `name` | str  | "exa"   | Key name: `"exa"`, `"openai"`, or `"anthropic"`      |

**Returns / 返回**: `str` -- the API key value.

**Raises / 异常**: `ValueError` if the key is not found in env, config.yaml, or system env.

**Resolution order / 查找顺序**:

1. Environment variable (e.g., `EXA_API_KEY`)
2. `config.yaml` -> `api_keys` -> `{name}`

### get_search_config

```python
get_search_config() -> Dict
```

Return search-related settings. Keys in the returned dict:

| Key              | Type | Default      | Description                          |
|------------------|------|--------------|--------------------------------------|
| `type`           | str  | "auto"       | Search type                          |
| `num_results`    | int  | 10           | Default number of results            |
| `max_characters` | int  | 4000         | Max characters per result            |
| `content_mode`   | str  | "highlights" | "highlights" or "text"               |

### get_validation_config

```python
get_validation_config() -> Dict
```

Return data validation settings from `config.yaml` -> `validation`.
Includes `require_source_citations`, `min_cross_validation_sources`,
`auto_flag_stale_data`, `block_export_on_high_risk`.

### get_freshness_thresholds

```python
get_freshness_thresholds() -> Dict[str, int]
```

Return freshness thresholds (in days) for all 20 data categories.
Custom values from `config.yaml` are merged over built-in defaults.

### get_source_tiers

```python
get_source_tiers() -> Dict[str, List[str]]
```

Return source credibility tier domain lists. Keys: `"tier1"`, `"tier2"`, `"tier3"`.
Each value is a list of domain strings.

### get_export_config

```python
get_export_config() -> Dict
```

Return export settings. Keys: `markdown_dir`, `pdf_dir`, `naming_pattern`, `pdf_engines`.

### get_network_config

```python
get_network_config() -> Dict
```

Return network settings. Keys: `timeout` (int), `max_retries` (int), `retry_delay` (float).

### get_project_root

```python
get_project_root() -> Path
```

Return the absolute path to the project root directory.

---

## StockSearcher

Location / 位置: `src/search/exa_searcher.py`

Exa API search client with automatic retry (exponential backoff), config-driven
parameters, and source credibility classification.

### Constructor / 构造函数

```python
from src.search.exa_searcher import StockSearcher

searcher = StockSearcher(api_key=None)
```

| Parameter | Type          | Default | Description                                 |
|-----------|---------------|---------|---------------------------------------------|
| `api_key` | str or None   | None    | Exa API key. If None, loaded from config.   |

All search parameters (type, num_results, max_characters, content_mode) and
network parameters (max_retries, retry_delay, timeout) are read from `config.py`.

### search_stock_news

```python
search_stock_news(ticker: str, num_results: int = 0, include_highlights: bool = True) -> Dict
```

Search for latest news about a specific stock ticker.

**Parameters / 参数**:

| Name                 | Type | Default | Description                                    |
|----------------------|------|---------|------------------------------------------------|
| `ticker`             | str  | --      | Stock ticker symbol (e.g., "AAPL", "TSLA")    |
| `num_results`        | int  | 0       | Number of results. 0 = use config default.     |
| `include_highlights` | bool | True    | Include content highlights in results.         |

**Returns / 返回**: `Dict` with keys `ticker`, `query`, `total_results`, `results`.

### search_market_analysis

```python
search_market_analysis(topic: str, num_results: int = 0) -> Dict
```

Search for market analysis and industry trends on a given topic.

| Name          | Type | Default | Description                    |
|---------------|------|---------|--------------------------------|
| `topic`       | str  | --      | Market topic (e.g., "AI stocks") |
| `num_results` | int  | 0       | Number of results.             |

**Returns / 返回**: `Dict` with keys `topic`, `query`, `total_results`, `results`.

### search_company_info

```python
search_company_info(company_name: str, num_results: int = 0) -> Dict
```

Search for company information and earnings reports.

| Name           | Type | Default | Description                        |
|----------------|------|---------|------------------------------------|
| `company_name` | str  | --      | Company name (e.g., "Microsoft")   |
| `num_results`  | int  | 0       | Number of results.                 |

**Returns / 返回**: `Dict` with keys `company`, `query`, `total_results`, `results`.

### search_with_deep_research

```python
search_with_deep_research(query: str, num_results: int = 0) -> Dict
```

Execute a deep research search. Uses `type="deep"` and up to 20,000 characters
of full text per result.

| Name          | Type | Default | Description           |
|---------------|------|---------|-----------------------|
| `query`       | str  | --      | Research query.       |
| `num_results` | int  | 0       | Number of results.    |

**Returns / 返回**: `Dict` with keys `query`, `search_type`, `total_results`, `results`.

### classify_source_tier

```python
classify_source_tier(url: str) -> str
```

Classify a URL into a reliability tier based on domain matching.

| Name  | Type | Description    |
|-------|------|----------------|
| `url` | str  | URL to classify |

**Returns / 返回**: One of:
- `"Tier 1 (官方/监管)"` -- Official / Regulatory (e.g., sec.gov, etherscan.io)
- `"Tier 2 (主流财经)"` -- Mainstream financial (e.g., bloomberg.com, yahoo finance)
- `"Tier 3 (分析参考)"` -- Analytical reference (e.g., investopedia.com)
- `"Tier 4 (需交叉验证)"` -- Unrecognized, needs cross-validation

Tier domain lists are loaded from `config.yaml` -> `source_tiers`, with fallback to
built-in defaults.

### format_results (classmethod)

```python
@classmethod
format_results(cls, results: Dict, max_items: int = 5) -> str
```

Format search results into a human-readable text string with tier labels.

| Name        | Type | Default | Description                     |
|-------------|------|---------|---------------------------------|
| `results`   | Dict | --      | Search result dict.             |
| `max_items` | int  | 5       | Maximum items to display.       |

**Returns / 返回**: `str` -- formatted multi-line text.

---

## UnifiedSkillRouter

Location / 位置: `src/server/skill_router.py`

Intelligent router that interprets natural language queries and dispatches to
search, research, valuation, freshness, or export handlers. Merges the old
`ExaSkillRouter` (search-only) with investment research routing.

### Constructor / 构造函数

```python
from src.server.skill_router import UnifiedSkillRouter

router = UnifiedSkillRouter(api_key=None)
```

| Parameter | Type        | Default | Description                          |
|-----------|-------------|---------|--------------------------------------|
| `api_key` | str or None | None    | Exa API key. If None, loaded from config. |

Internally creates instances of `StockSearcher`, `InvestmentResearcher`,
`DataValidator`, and `ReportExporter`.

### route

```python
route(user_input: str) -> Dict
```

Top-level dispatcher. Analyzes `user_input` and delegates to the appropriate handler.

**Intent detection order / 意图检测顺序**:

1. Report generation -- keywords: "report", "research", "投研", "报告", "框架", etc.
2. Freshness check -- keywords: "freshness", "stale", "时效", "过期", etc.
3. Valuation request -- keywords: "valuation", "dcf", "估值", "内在价值", etc.
4. Checklist request -- keywords: "checklist", "不为清单", "纪律", etc.
5. Position sizing -- keywords: "position", "sizing", "仓位", "建仓", etc.
6. General search -- fallback

**Returns / 返回**: `Dict` with an `"action"` key and action-specific data.

### search

```python
search(query: str, num_results: int = 10) -> Dict
```

Detect the search type from the query and call the matching `StockSearcher` method.

| Name          | Type | Default | Description                     |
|---------------|------|---------|---------------------------------|
| `query`       | str  | --      | Natural language search query.  |
| `num_results` | int  | 10      | Number of results.              |

**Returns / 返回**: `Dict` -- search results from the appropriate search method.

### search_and_format

```python
search_and_format(query: str, num_results: int = 10, max_display: int = 5) -> str
```

Execute search and return formatted text with source tier labels.

| Name          | Type | Default | Description                     |
|---------------|------|---------|---------------------------------|
| `query`       | str  | --      | Search query.                   |
| `num_results` | int  | 10      | Number of results to fetch.     |
| `max_display` | int  | 5       | Maximum items in formatted output. |

**Returns / 返回**: `str` -- formatted multi-line text.

### search_as_json

```python
search_as_json(query: str, num_results: int = 10) -> str
```

Execute search and return a JSON string.

| Name          | Type | Default | Description              |
|---------------|------|---------|--------------------------|
| `query`       | str  | --      | Search query.            |
| `num_results` | int  | 10      | Number of results.       |

**Returns / 返回**: `str` -- JSON string with keys `query`, `total_results`, `results`.

### detect_search_type

```python
detect_search_type(query: str) -> Dict
```

Detect the intended search type from a natural language query using regex patterns.

**Returns / 返回**: `Dict` with keys:

| Key          | Type  | Description                                                     |
|--------------|-------|-----------------------------------------------------------------|
| `type`       | str   | `"stock_news"`, `"market_analysis"`, `"company_info"`, or `"deep_research"` |
| `query`      | str   | Extracted search subject                                        |
| `confidence` | float | Detection confidence (0.0 -- 1.0)                               |

---

## InvestmentResearcher

Location / 位置: `src/core/researcher.py`

Core investment research engine implementing the Crisis Investment methodology.
Supports three frameworks: Mature Company, Growth Company, and Web3 Project.

### Constructor / 构造函数

```python
from src.core.researcher import InvestmentResearcher

researcher = InvestmentResearcher(searcher=None)
```

| Parameter  | Type                  | Default | Description                        |
|------------|-----------------------|---------|------------------------------------|
| `searcher` | StockSearcher or None | None    | Searcher instance for data queries |

### detect_framework

```python
detect_framework(target: str, market: str = "") -> str
```

Auto-detect which research framework to use based on the target name and market.

| Name     | Type | Default | Description                                  |
|----------|------|---------|----------------------------------------------|
| `target` | str  | --      | Company or project name                      |
| `market` | str  | ""      | Market hint: "crypto", "hk", "a-share", etc. |

**Returns / 返回**: `str` -- one of `"mature"`, `"growth"`, `"web3"`.

Detection logic:
- Web3 keywords (crypto, defi, token, protocol, etc.) -> `"web3"`
- Mature company keywords (bank, insurance, energy, utility, etc.) -> `"mature"`
- Default -> `"growth"`

### generate_report_skeleton

```python
generate_report_skeleton(
    target_name: str,
    ticker: str,
    market: str = "",
    framework: str = "",
) -> Dict
```

Generate a pre-filled report skeleton from a Markdown template.

| Name          | Type | Default | Description                                    |
|---------------|------|---------|------------------------------------------------|
| `target_name` | str  | --      | Company or project name                        |
| `ticker`      | str  | --      | Stock ticker or token symbol                   |
| `market`      | str  | ""      | Market hint (auto-detected if empty)           |
| `framework`   | str  | ""      | Force a framework. Empty = auto-detect.        |

**Returns / 返回**: `Dict` with keys:

| Key               | Type      | Description                                |
|-------------------|-----------|--------------------------------------------|
| `report_id`       | str       | UUID for the report                        |
| `framework`       | str       | Detected or forced framework               |
| `target_name`     | str       | Company/project name                       |
| `ticker`          | str       | Ticker symbol                              |
| `market`          | str       | Market designation                         |
| `created_at`      | str       | ISO timestamp                              |
| `content`         | str       | Markdown content with `{{PLACEHOLDER}}` fields |
| `unfilled_fields` | List[str] | List of placeholder names still to fill    |

### get_research_queries

```python
get_research_queries(target_name: str, ticker: str, framework: str) -> List[Dict]
```

Generate a prioritized list of search queries to fill report placeholders.

**Returns / 返回**: `List[Dict]` sorted by priority (1 = highest). Each item:

| Key                     | Type | Description                                    |
|-------------------------|------|------------------------------------------------|
| `query`                 | str  | Suggested Exa search query                     |
| `field`                 | str  | Target placeholder name in the report          |
| `priority`              | int  | 1 (highest) to 3 (lowest)                      |
| `preferred_sources`     | list | Recommended source types                       |
| `data_type`             | str  | "quantitative" or "qualitative"                |
| `requires_source_citation` | bool | Whether the field needs a `[来源: ...]` tag  |
| `cross_validation`      | str  | Cross-validation instruction (if applicable)   |

The list includes common queries (5 items), framework-specific queries
(13 for mature, 11 for growth, 14 for web3), and valuation queries (5 items).

### get_checklist

```python
get_checklist(framework: str) -> List[Dict]
```

Return the "Do Not Invest" discipline checklist (10 rules).

| Name        | Type | Description                               |
|-------------|------|-------------------------------------------|
| `framework` | str  | "mature", "growth", or "web3"             |

**Returns / 返回**: `List[Dict]` with keys `id`, `rule`, `check_field`.

### get_position_sizing

```python
get_position_sizing(intrinsic_value: float, current_price: float) -> Dict
```

Calculate position sizing zone and buy ladder based on discount to intrinsic value.

| Name              | Type  | Description                         |
|-------------------|-------|-------------------------------------|
| `intrinsic_value` | float | Calculated intrinsic value per share |
| `current_price`   | float | Current market price                |

**Returns / 返回**: `Dict` with keys:

| Key                    | Type | Description                                          |
|------------------------|------|------------------------------------------------------|
| `intrinsic_value`      | float | Input intrinsic value                               |
| `current_price`        | float | Input current price                                 |
| `discount_rate`        | str  | Current price / intrinsic value as percentage        |
| `zone`                 | str  | "deep_water", "shallow_water", or "waiting"          |
| `zone_label`           | str  | Chinese description of the zone                     |
| `max_single_position`  | str  | Maximum allocation for a single position             |
| `buy_ladder`           | Dict | Three-tier entry prices at 90%, 70%, 50% of intrinsic value |

---

## ValuationMethods

Location / 位置: `src/core/valuation.py`

Collection of static valuation calculation utilities. Supports 10+ methods
for cross-validation as required by the Crisis Investment framework.
All methods are `@staticmethod` -- no instance state required.

### dcf

```python
@staticmethod
dcf(
    fcf_current: float,
    growth_rate: float,
    terminal_growth: float = 0.03,
    discount_rate: float = 0.10,
    years: int = 10,
    shares_outstanding: float = 1.0,
) -> Dict
```

Discounted Cash Flow valuation.
自由现金流折现估值。

| Parameter            | Type  | Default | Description                        |
|----------------------|-------|---------|------------------------------------|
| `fcf_current`        | float | --      | Current free cash flow             |
| `growth_rate`        | float | --      | Annual FCF growth rate (e.g., 0.15 = 15%) |
| `terminal_growth`    | float | 0.03    | Terminal growth rate               |
| `discount_rate`      | float | 0.10    | Discount rate (WACC)               |
| `years`              | int   | 10      | Projection period in years         |
| `shares_outstanding` | float | 1.0     | Shares outstanding (for per-share) |

**Returns / 返回**: `Dict` with `total_enterprise_value`, `per_share_value`, `assumptions`.

### graham_formula

```python
@staticmethod
graham_formula(eps: float, growth_rate: float, aaa_yield: float = 0.045) -> Dict
```

Benjamin Graham intrinsic value formula: V = EPS x (8.5 + 2g) x 4.4 / Y.
格雷厄姆公式。

| Parameter    | Type  | Default | Description                          |
|--------------|-------|---------|--------------------------------------|
| `eps`        | float | --      | Earnings per share                   |
| `growth_rate`| float | --      | Expected growth rate (e.g., 0.15)    |
| `aaa_yield`  | float | 0.045   | AAA corporate bond yield             |

**Returns / 返回**: `Dict` with `per_share_value`, `assumptions`.

### pe_relative

```python
@staticmethod
pe_relative(eps: float, industry_pe: float, premium: float = 1.0) -> Dict
```

PE ratio relative valuation.
市盈率对标估值。

| Parameter     | Type  | Default | Description                  |
|---------------|-------|---------|------------------------------|
| `eps`         | float | --      | Earnings per share           |
| `industry_pe` | float | --     | Industry average PE ratio    |
| `premium`     | float | 1.0     | Premium/discount factor      |

**Returns / 返回**: `Dict` with `per_share_value`, `assumptions`.

### pb_relative

```python
@staticmethod
pb_relative(bvps: float, industry_pb: float) -> Dict
```

PB ratio relative valuation.
市净率对标估值。

| Parameter     | Type  | Description                     |
|---------------|-------|---------------------------------|
| `bvps`        | float | Book value per share            |
| `industry_pb` | float | Industry average PB ratio       |

**Returns / 返回**: `Dict` with `per_share_value`, `assumptions`.

### ps_relative

```python
@staticmethod
ps_relative(revenue_per_share: float, industry_ps: float) -> Dict
```

PS ratio relative valuation.
市销率对标估值。

| Parameter           | Type  | Description                  |
|---------------------|-------|------------------------------|
| `revenue_per_share` | float | Revenue per share            |
| `industry_ps`       | float | Industry average PS ratio    |

**Returns / 返回**: `Dict` with `per_share_value`, `assumptions`.

### ev_ebitda

```python
@staticmethod
ev_ebitda(
    ebitda: float,
    industry_multiple: float,
    net_debt: float,
    shares_outstanding: float,
) -> Dict
```

EV/EBITDA enterprise value valuation.
企业价值倍数估值。

| Parameter            | Type  | Description                             |
|----------------------|-------|-----------------------------------------|
| `ebitda`             | float | EBITDA                                  |
| `industry_multiple`  | float | Industry average EV/EBITDA multiple     |
| `net_debt`           | float | Total debt minus cash                   |
| `shares_outstanding` | float | Shares outstanding                      |

**Returns / 返回**: `Dict` with `enterprise_value`, `equity_value`, `per_share_value`, `assumptions`.

### peg

```python
@staticmethod
peg(eps: float, growth_rate: float, target_peg: float = 1.0) -> Dict
```

PEG ratio valuation.
PEG 估值法。

| Parameter    | Type  | Default | Description                       |
|--------------|-------|---------|-----------------------------------|
| `eps`        | float | --      | Earnings per share                |
| `growth_rate`| float | --      | Expected growth rate (e.g., 0.20) |
| `target_peg` | float | 1.0     | Target PEG ratio (1.0 = fair)     |

**Returns / 返回**: `Dict` with `per_share_value`, `fair_pe`, `assumptions`.

### ddm

```python
@staticmethod
ddm(
    dividend_per_share: float,
    growth_rate: float,
    required_return: float = 0.10,
) -> Dict
```

Dividend Discount Model (Gordon Growth Model).
股利折现模型。

| Parameter            | Type  | Default | Description                  |
|----------------------|-------|---------|------------------------------|
| `dividend_per_share` | float | --      | Current dividend per share   |
| `growth_rate`        | float | --      | Dividend growth rate         |
| `required_return`    | float | 0.10    | Required rate of return      |

**Returns / 返回**: `Dict` with `per_share_value`, `assumptions`.
Returns `per_share_value: None` if `required_return <= growth_rate`.

### owner_earnings_valuation

```python
@staticmethod
owner_earnings_valuation(
    owner_earnings: float,
    growth_rate: float,
    discount_rate: float = 0.10,
    shares_outstanding: float = 1.0,
) -> Dict
```

Warren Buffett owner earnings valuation.
股东盈余估值法。

| Parameter            | Type  | Default | Description                     |
|----------------------|-------|---------|---------------------------------|
| `owner_earnings`     | float | --      | Owner earnings (net income + D&A - capex) |
| `growth_rate`        | float | --      | Growth rate                     |
| `discount_rate`      | float | 0.10    | Discount rate                   |
| `shares_outstanding` | float | 1.0     | Shares outstanding              |

**Returns / 返回**: `Dict` with `total_value`, `per_share_value`, `assumptions`.

### replacement_cost

```python
@staticmethod
replacement_cost(
    total_assets: float,
    intangibles: float,
    liabilities: float,
    shares: float,
) -> Dict
```

Replacement/liquidation cost valuation.
重置成本法。

| Parameter     | Type  | Description                         |
|---------------|-------|-------------------------------------|
| `total_assets`| float | Total assets                        |
| `intangibles` | float | Intangible assets to exclude        |
| `liabilities` | float | Total liabilities                   |
| `shares`      | float | Shares outstanding                  |

**Returns / 返回**: `Dict` with `net_asset_value`, `per_share_value`, `assumptions`.

### cross_validate

```python
@staticmethod
cross_validate(valuations: List[Dict]) -> Dict
```

Cross-validate multiple valuation results. Computes median, mean, range,
confidence level, and source citation audit.

| Parameter    | Type       | Description                                 |
|--------------|------------|---------------------------------------------|
| `valuations` | List[Dict] | List of valuation result dicts from any of the methods above |

**Returns / 返回**: `Dict` with keys:

| Key              | Type      | Description                                   |
|------------------|-----------|-----------------------------------------------|
| `method_count`   | int       | Number of valid valuations                    |
| `median`         | float     | Median per-share value                        |
| `mean`           | float     | Mean per-share value                          |
| `min`            | float     | Minimum value                                 |
| `max`            | float     | Maximum value                                 |
| `spread`         | str       | Value spread as percentage                    |
| `confidence`     | str       | "high" (<30% spread), "medium", or "low"      |
| `all_values`     | List      | Sorted list of all per-share values           |
| `source_audit`   | Dict      | Present only if some methods lack source citations |

Confidence is downgraded if >50% of valuation methods lack `input_sources`.

---

## DataFreshnessChecker

Location / 位置: `src/core/freshness.py`

Validates the timeliness of data used in investment research reports.
Supports 20 data categories with configurable freshness thresholds.

### Constructor / 构造函数

```python
from src.core.freshness import DataFreshnessChecker

checker = DataFreshnessChecker(reference_date=None)
```

| Parameter        | Type              | Default | Description                         |
|------------------|-------------------|---------|-------------------------------------|
| `reference_date` | datetime or None  | None    | Reference date. Defaults to now.    |

Thresholds are loaded from `config.yaml` via `get_freshness_thresholds()`.

### check_data_point

```python
check_data_point(
    category: str,
    source: str,
    data_date: Optional[datetime] = None,
    date_string: Optional[str] = None,
) -> Dict
```

Check a single data point for freshness.

| Parameter     | Type              | Description                                      |
|---------------|-------------------|--------------------------------------------------|
| `category`    | str               | Data category (e.g., "stock_price", "tvl_data")  |
| `source`      | str               | Source description                                |
| `data_date`   | datetime or None  | Parsed date of the data                          |
| `date_string` | str or None       | Date string to auto-parse (alternative to data_date) |

**Returns / 返回**: `Dict` with `category`, `source`, `status`, `age_days`,
`threshold_days`, `recommendation`, `status_label`.

Status values: `"fresh"`, `"aging"` (1x--2x threshold), `"stale"` (>2x threshold), `"unknown"`.

### check_report

```python
check_report(report_content: str) -> Dict
```

Scan a full report for date references, infer their categories, and assess
overall data freshness.

| Parameter         | Type | Description                          |
|-------------------|------|--------------------------------------|
| `report_content`  | str  | Full Markdown report content         |

**Returns / 返回**: `Dict` with keys:

| Key                | Type | Description                                           |
|--------------------|------|-------------------------------------------------------|
| `overall_status`   | str  | "CURRENT", "AGING", "NEEDS_UPDATE", or "NO_DATES"    |
| `overall_label`    | str  | Chinese summary of the overall status                 |
| `total_data_points`| int  | Number of date references found                       |
| `fresh_count`      | int  | Count of fresh data points                            |
| `aging_count`      | int  | Count of aging data points                            |
| `stale_count`      | int  | Count of stale data points                            |
| `findings`         | list | Detailed per-item results                             |

Recognized date formats: `YYYY-MM-DD`, `YYYY年M月D日`, `M/D/YYYY`, `Q1 2025`, `FY2025`, `2025 Q1`.

### check_unfilled_fields

```python
check_unfilled_fields(report_content: str) -> Dict
```

Scan for `{{PLACEHOLDER}}` fields still remaining in a report.

| Parameter        | Type | Description                  |
|------------------|------|------------------------------|
| `report_content` | str  | Markdown report content      |

**Returns / 返回**: `Dict` with keys:

| Key                     | Type      | Description                              |
|-------------------------|-----------|------------------------------------------|
| `total_unfilled`        | int       | Total unfilled placeholder count         |
| `completeness_estimate` | str       | Estimated completion percentage          |
| `critical_unfilled`     | List[str] | VAL_, INTRINSIC, PRICE, SCORE, DECISION fields |
| `important_unfilled`    | List[str] | REVENUE, MARGIN, GROWTH, FCF, etc.       |
| `supplementary_unfilled`| List[str] | Remaining non-critical fields            |
| `all_unfilled`          | List[str] | Complete sorted list                     |

### audit_source_citations

```python
audit_source_citations(report_content: str) -> Dict
```

Scan a filled report for financial data points that lack proper source citations.
Detects `[来源: ...]` and `(Source: ...)` tags.

| Parameter        | Type | Description                  |
|------------------|------|------------------------------|
| `report_content` | str  | Markdown report content      |

**Returns / 返回**: `Dict` with keys:

| Key                  | Type      | Description                                        |
|----------------------|-----------|----------------------------------------------------|
| `total_data_points`  | int       | Count of numeric/financial data references found   |
| `cited_count`        | int       | How many have a nearby citation tag                |
| `uncited_count`      | int       | How many lack citation                             |
| `citation_rate`      | str       | Percentage of cited data points                    |
| `hallucination_risk` | str       | "low", "medium", "high", or "unknown"              |
| `uncited_items`      | List[Dict]| Up to 30 uncited data snippets for manual review   |
| `recommendation`     | str       | Chinese-language action recommendation             |

---

## DataValidator

Location / 位置: `src/core/validator.py`

Cross-validation, source tier scoring, and confidence assessment for financial data.

### Constructor / 构造函数

```python
from src.core.validator import DataValidator

validator = DataValidator(source_tiers=None)
```

| Parameter      | Type           | Default | Description                                  |
|----------------|----------------|---------|----------------------------------------------|
| `source_tiers` | Dict or None   | None    | Custom tier domain mapping. None = load from config. |

### validate_data_point

```python
validate_data_point(
    value: Any,
    label: str,
    sources: List[Dict],
    tolerance: float = 0.05,
) -> Dict
```

Validate a single data point against multiple sources.

**Parameters / 参数**:

| Name        | Type       | Default | Description                                              |
|-------------|------------|---------|----------------------------------------------------------|
| `value`     | Any        | --      | The reported value                                       |
| `label`     | str        | --      | Data label (e.g., "Revenue", "PE Ratio")                 |
| `sources`   | List[Dict] | --      | Source dicts with keys: `name`, `url`, `date`, `value`   |
| `tolerance` | float      | 0.05    | Acceptable relative difference between sources (5%)       |

**Returns / 返回**: `Dict` with keys:

| Key              | Type | Description                                     |
|------------------|------|-------------------------------------------------|
| `label`          | str  | Data label                                      |
| `value`          | Any  | Reported value                                  |
| `status`         | str  | "verified", "single_source", "unverified", or "inconsistent" |
| `confidence`     | str  | "high", "medium", or "low"                      |
| `source_count`   | int  | Number of sources provided                      |
| `best_tier`      | int  | Tier of the most credible source (1--4)         |
| `consistency`    | str  | "consistent" or "inconsistent"                  |
| `max_deviation`  | str  | Maximum deviation between source values         |
| `citation`       | str  | Generated citation tag: `[来源: XX | 日期: YYYY-MM-DD]` |
| `sources`        | list | Scored and sorted source list                   |
| `warning`        | str  | Present only if sources disagree                |

**Confidence rules**:
- **high**: 2+ sources, best tier <= 2, consistent
- **medium**: 2+ consistent sources (any tier), or 1 source with tier <= 2
- **low**: 1 source with tier > 2, or inconsistent sources

### validate_search_results

```python
validate_search_results(results: List[Dict]) -> Dict
```

Score and rank a batch of search results by source credibility.

| Name      | Type       | Description                                      |
|-----------|------------|--------------------------------------------------|
| `results` | List[Dict] | Search result dicts, each having `url` and `title` |

**Returns / 返回**: `Dict` with keys:

| Key                 | Type | Description                                |
|---------------------|------|--------------------------------------------|
| `total_results`     | int  | Total number of results                    |
| `tier_distribution` | Dict | Count per tier: `{1: n, 2: n, 3: n, 4: n}` |
| `high_quality_ratio`| str  | (Tier 1 + Tier 2) / total as percentage    |
| `overall_quality`   | str  | "high" (>=50%), "medium" (>=20%), "low"    |
| `scored_results`    | list | Results sorted by tier (most credible first) |
| `recommendation`    | str  | Action recommendation                      |

### assess_report_confidence

```python
assess_report_confidence(validation_results: List[Dict]) -> Dict
```

Aggregate multiple `validate_data_point()` results into an overall confidence score.

| Name                 | Type       | Description                             |
|----------------------|------------|-----------------------------------------|
| `validation_results` | List[Dict] | List of validate_data_point() results   |

**Returns / 返回**: `Dict` with keys:

| Key                    | Type      | Description                           |
|------------------------|-----------|---------------------------------------|
| `overall_confidence`   | str       | "high", "medium", "low", or "unknown" |
| `total_data_points`    | int       | Total validated points                |
| `verified_count`       | int       | Cross-validated points                |
| `single_source_count`  | int       | Single-source points                  |
| `unverified_count`     | int       | Unverified points                     |
| `inconsistent_count`   | int       | Inconsistent points                   |
| `verified_ratio`       | str       | Percentage of verified points         |
| `unverified_labels`    | List[str] | Labels of unverified data points      |
| `inconsistent_labels`  | List[str] | Labels of inconsistent data points    |
| `recommendation`       | str       | Action recommendation                 |

### classify_source

```python
classify_source(url: str) -> int
```

Classify a URL into a reliability tier (1 = most reliable, 4 = needs verification).

| Name  | Type | Description     |
|-------|------|-----------------|
| `url` | str  | URL to classify |

**Returns / 返回**: `int` -- tier number 1 through 4.

---

## ReportExporter

Location / 位置: `src/export/exporter.py`

Export research reports in Markdown and PDF formats to separate output directories.
PDF rendering tries engines in order: Chromium (playwright) -> fitz (pymupdf) -> plain text.

### Constructor / 构造函数

```python
from src.export.exporter import ReportExporter

exporter = ReportExporter(md_dir=None, pdf_dir=None)
```

| Parameter | Type          | Default                          | Description                      |
|-----------|---------------|----------------------------------|----------------------------------|
| `md_dir`  | Path or None  | `research Output/markdown`       | Markdown output directory        |
| `pdf_dir` | Path or None  | `research Output/pdf`            | PDF output directory             |

### export_markdown

```python
export_markdown(
    content: str,
    ticker: str,
    framework: str,
    report_id: str,
    naming_pattern: Optional[str] = None,
) -> Path
```

Save report content as a Markdown file.

| Parameter        | Type        | Default | Description                              |
|------------------|-------------|---------|------------------------------------------|
| `content`        | str         | --      | Full Markdown report content             |
| `ticker`         | str         | --      | Stock ticker or token symbol             |
| `framework`      | str         | --      | "mature", "growth", or "web3"            |
| `report_id`      | str         | --      | UUID for the report                      |
| `naming_pattern` | str or None | None    | Custom pattern. None = use config default. |

**Returns / 返回**: `Path` to the saved `.md` file.

File name example: `20260404_AAPL_growth_a1b2c3d4.md`

### export_pdf

```python
export_pdf(
    content: str,
    ticker: str,
    framework: str,
    report_id: str,
    naming_pattern: Optional[str] = None,
) -> Path
```

Convert Markdown content to PDF. Engine fallback chain:

1. **Chromium** (playwright) -- best quality, full CSS, page numbers. Requires
   `pip install playwright && playwright install chromium`.
2. **fitz** (pymupdf) -- good quality, CJK font support. Included in requirements.txt.
3. **Plain text** -- last resort; writes text lines to PDF via pymupdf or raw text.

Parameters are identical to `export_markdown`.

**Returns / 返回**: `Path` to the saved `.pdf` file.

### export_both

```python
export_both(
    content: str,
    ticker: str,
    framework: str,
    report_id: str,
    naming_pattern: Optional[str] = None,
) -> Dict[str, Path]
```

Export as both Markdown and PDF in a single call.
Parameters are identical to `export_markdown`.

**Returns / 返回**: `Dict` with keys `"markdown"` and `"pdf"`, values are `Path` objects.

---

## ExaMCPServer

Location / 位置: `src/server/mcp_server.py`

MCP (Model Context Protocol) server exposing 14 tools for search, research,
valuation, validation, freshness checking, and export.

### Constructor / 构造函数

```python
from src.server.mcp_server import ExaMCPServer

server = ExaMCPServer(api_key=None)
```

Internally creates instances of `StockSearcher`, `InvestmentResearcher`,
`DataFreshnessChecker`, `DataValidator`, and `ReportExporter`.

### 14 MCP Tools / 14 个 MCP 工具

| # | Tool Name                     | Description / 说明                                    | Required Params                          |
|---|-------------------------------|-------------------------------------------------------|------------------------------------------|
| 1 | `search_stock_news`           | Search latest news for a stock ticker / 搜索股票新闻    | `ticker`                                 |
| 2 | `search_market_analysis`      | Search market analysis and trends / 搜索市场分析        | `topic`                                  |
| 3 | `search_company_info`         | Search company information / 搜索公司信息               | `company_name`                           |
| 4 | `deep_research`               | Deep research search / 深度研究搜索                     | `query`                                  |
| 5 | `generate_research_report`    | Generate report skeleton / 生成投研报告骨架             | `target_name`, `ticker`                  |
| 6 | `get_research_queries`        | Get prioritized search queries / 获取优先搜索查询       | `target_name`, `ticker`, `framework`     |
| 7 | `check_report_freshness`      | Check data freshness / 检查数据时效性                   | `report_content`                         |
| 8 | `check_unfilled_fields`       | Check unfilled placeholders / 检查未填字段              | `report_content`                         |
| 9 | `calculate_valuation`         | Calculate intrinsic value / 计算内在价值                | `method`, `params`                       |
| 10| `get_position_sizing`         | Position sizing and buy ladder / 仓位计算              | `intrinsic_value`, `current_price`       |
| 11| `get_do_not_invest_checklist` | Discipline checklist / 不为清单                        | (optional: `framework`)                  |
| 12| `export_report`               | Export to Markdown/PDF / 导出报告                      | `content`, `ticker`, `framework`, `report_id` |
| 13| `audit_report_citations`      | Audit source citations / 审计来源标注                   | `report_content`                         |
| 14| `validate_data_point`         | Cross-validate a data point / 交叉验证数据点           | `value`, `label`, `sources`              |

### handle_tool_call

```python
handle_tool_call(tool_name: str, inputs: dict) -> str
```

Dispatch a tool call by name and return a JSON string result.

The `export_report` tool performs a pre-export citation audit when
`block_export_on_high_risk` is enabled in config. If hallucination risk is
"high", the export is blocked and an error with the audit details is returned.

### get_tools

```python
get_tools() -> str
```

Return the full tool definition list as a formatted JSON string (for MCP registration).

---

## ReportNaming

Location / 位置: `src/export/naming.py`

Utility class for generating standardized, sanitized file names for reports.

### generate (staticmethod)

```python
@staticmethod
ReportNaming.generate(
    ticker: str,
    framework: str,
    report_id: str,
    pattern: Optional[str] = None,
    date: Optional[datetime] = None,
) -> str
```

Generate a sanitized base filename (no extension).

| Parameter  | Type             | Default                                 | Description                      |
|------------|------------------|-----------------------------------------|----------------------------------|
| `ticker`   | str              | --                                      | Stock ticker / token symbol      |
| `framework`| str              | --                                      | "mature", "growth", or "web3"    |
| `report_id`| str              | --                                      | UUID (truncated to 8 chars)      |
| `pattern`  | str or None      | `"{date}_{ticker}_{framework}_{report_id}"` | Custom naming pattern        |
| `date`     | datetime or None | today                                   | Report date                      |

**Returns / 返回**: `str` -- sanitized filename like `20260404_AAPL_growth_a1b2c3d4`.

### with_extension (staticmethod)

```python
@staticmethod
ReportNaming.with_extension(base_name: str, ext: str) -> str
```

Append a file extension, ensuring a single dot separator.

**Returns / 返回**: `str` -- e.g., `"20260404_AAPL_growth_a1b2c3d4.md"`.

---

## Usage Examples / 使用示例

### Example 1: Basic search / 基础搜索

```python
from src.search.exa_searcher import StockSearcher

searcher = StockSearcher()
result = searcher.search_stock_news("AAPL", num_results=5)
print(StockSearcher.format_results(result))
```

### Example 2: Intelligent routing / 智能路由

```python
from src.server.skill_router import UnifiedSkillRouter

router = UnifiedSkillRouter()
response = router.route("Generate research report for AAPL")
print(response["action"])        # "generate_report"
print(response["report"]["framework"])  # "growth"
```

### Example 3: Valuation cross-validation / 估值交叉验证

```python
from src.core.valuation import ValuationMethods as VM

results = [
    VM.dcf(fcf_current=100e9, growth_rate=0.08, shares_outstanding=15.7e9),
    VM.graham_formula(eps=6.42, growth_rate=0.08),
    VM.pe_relative(eps=6.42, industry_pe=28),
    VM.ev_ebitda(ebitda=130e9, industry_multiple=20, net_debt=50e9, shares_outstanding=15.7e9),
]
summary = VM.cross_validate(results)
print(f"Median: ${summary['median']}, Confidence: {summary['confidence']}")
```

### Example 4: Data freshness audit / 数据时效性审计

```python
from src.core.freshness import DataFreshnessChecker

checker = DataFreshnessChecker()
report = checker.check_report(open("report.md").read())
print(report["overall_label"])
```

### Example 5: Data validation / 数据验证

```python
from src.core.validator import DataValidator

validator = DataValidator()
result = validator.validate_data_point(
    value=38.3, label="Quarterly Revenue (B)",
    sources=[
        {"name": "SEC 10-Q", "url": "https://sec.gov/...", "date": "2026-03-15", "value": 38.3},
        {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/...", "date": "2026-03-15", "value": 38.2},
    ],
)
print(result["citation"])   # [来源: SEC 10-Q | 日期: 2026-03-15]
print(result["confidence"]) # high
```

### Example 6: Export report / 导出报告

```python
from src.export.exporter import ReportExporter

exporter = ReportExporter()
paths = exporter.export_both(
    content="# My Report\n...",
    ticker="AAPL",
    framework="growth",
    report_id="a1b2c3d4-5678-90ab-cdef",
)
print(paths["markdown"])  # research Output/markdown/20260404_AAPL_growth_a1b2c3d4.md
print(paths["pdf"])       # research Output/pdf/20260404_AAPL_growth_a1b2c3d4.pdf
```

---

## Related Docs / 相关文档

- [Quick Start / 快速开始](01-QUICKSTART.md)
- [Usage Guide / 使用指南](02-USAGE.md)
- [Integration / 集成指南](03-INTEGRATION.md)
- [Deployment / 部署指南](04-DEPLOYMENT.md)
- [Troubleshooting / 故障排查](06-TROUBLESHOOTING.md)
- [Project Structure / 项目结构](07-PROJECT-STRUCTURE.md)
