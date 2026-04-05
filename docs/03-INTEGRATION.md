# Claude Integration Guide / Claude 集成指南

**Crisis Investment Researcher v0.3.0**

Architecture, MCP tools, data flow, and best practices for Claude integration.

---

## Integration status / 集成状态

```
[OK] SKILL.md                     -- Claude auto-discovery / Claude 自动发现
[OK] .instructions.md             -- Usage instructions for Claude / Claude 使用说明
[OK] src/server/skill_router.py   -- UnifiedSkillRouter (intent dispatch)
[OK] src/server/mcp_server.py     -- ExaMCPServer (14 MCP tools)
[OK] src/claude_skill.py          -- CLI entry point / 命令行入口
[OK] config.yaml                  -- Centralized configuration / 集中配置
[OK] API key configured           -- Via config.yaml or .env
```

---

## Architecture / 架构

```
User (Claude Chat / CLI / Python)
 |
 v
src/claude_skill.py           -- Entry point: search_stock(), research(), search_stock_json()
 |
 v
src/server/skill_router.py    -- UnifiedSkillRouter: intent detection + dispatch
 |                                Detects: search / report / valuation / freshness /
 |                                         checklist / position / export
 |
 +---> src/search/exa_searcher.py      -- StockSearcher: Exa API with retry + source tier tagging
 |
 +---> src/core/researcher.py          -- InvestmentResearcher: 3 frameworks (mature/growth/web3)
 |        |                                Report skeletons, query planning, checklist, position sizing
 |        v
 |     src/core/valuation.py           -- ValuationMethods: 10+ methods (DCF, Graham, PE, PB, ...)
 |
 +---> src/core/freshness.py           -- DataFreshnessChecker: timeliness validation + citation audit
 |
 +---> src/core/validator.py           -- DataValidator: cross-validation, source scoring, confidence
 |
 +---> src/export/exporter.py          -- ReportExporter: Markdown + PDF dual output
 |        |
 |        v
 |     src/export/naming.py            -- ReportNaming: file naming with date/ticker/framework
 |
 v
src/config.py                          -- Centralized config loader (config.yaml > .env > defaults)
```

### MCP Server layer / MCP 服务器层

```
src/server/mcp_server.py      -- ExaMCPServer
 |
 +--- Wraps all modules above into 14 tool definitions
 +--- handle_tool_call(tool_name, inputs) -> JSON string
 +--- Pre-export audit enforcement (blocks high-risk exports)
```

---

## Data flow / 数据流

### Search flow / 搜索流程

```
User query
  |
  v
UnifiedSkillRouter.detect_search_type()    -- Pattern matching for intent
  |
  v
StockSearcher.search_*()                   -- Exa API call with retry + backoff
  |
  v
StockSearcher.classify_source_tier()       -- Tag each result: Tier 1-4
  |
  v
StockSearcher.format_results()             -- Formatted text with tier labels
  |
  v
Response with provenance warning           -- Includes search timestamp
```

### Research report flow / 研究报告流程

```
User: "Generate report for AAPL"
  |
  v
UnifiedSkillRouter._is_report_request()    -- Detect report intent
  |
  v
InvestmentResearcher.detect_framework()    -- Auto: mature / growth / web3
  |
  v
InvestmentResearcher.generate_report_skeleton()
  |  - Load template from research Output/templates/
  |  - Replace {{UUID}}, {{TARGET_NAME}}, {{TICKER}}, {{DATE}}, etc.
  |  - Return skeleton with {{PLACEHOLDER}} fields
  |
  v
InvestmentResearcher.get_research_queries()
  |  - Generate prioritized search queries (P1/P2/P3)
  |  - Each query specifies preferred sources and data type
  |
  v
[User/Claude fills placeholders using search results]
  |
  v
DataFreshnessChecker.check_report()        -- Validate data timeliness
DataFreshnessChecker.audit_source_citations() -- Detect uncited data
DataValidator.validate_data_point()         -- Cross-validate key figures
  |
  v
ReportExporter.export_both()               -- Markdown + PDF output
  |  (Pre-export audit blocks if hallucination_risk == "high")
  |
  v
research Output/markdown/*.md
research Output/pdf/*.pdf
```

---

## 14 MCP Tools / 14 个 MCP 工具

The `ExaMCPServer` in `src/server/mcp_server.py` exposes 14 tools:

### Search tools / 搜索工具 (4)

| #  | Tool name              | Description / 描述                        | Required params      |
|----|------------------------|-------------------------------------------|---------------------|
| 1  | `search_stock_news`    | Search latest news for a stock ticker     | `ticker`            |
| 2  | `search_market_analysis` | Search market analysis and trends       | `topic`             |
| 3  | `search_company_info`  | Search company information and earnings   | `company_name`      |
| 4  | `deep_research`        | Deep research with full text results      | `query`             |

All search tools accept an optional `num_results` parameter (default: 10).

### Research tools / 研究工具 (4)

| #  | Tool name                   | Description / 描述                                    | Required params              |
|----|-----------------------------|-------------------------------------------------------|------------------------------|
| 5  | `generate_research_report`  | Generate report skeleton (auto-detects framework)     | `target_name`, `ticker`      |
| 6  | `get_research_queries`      | Get prioritized queries to fill a report              | `target_name`, `ticker`, `framework` |
| 7  | `check_report_freshness`    | Check data freshness of a report                      | `report_content`             |
| 8  | `check_unfilled_fields`     | Find unfilled fields (critical/important/supplementary)| `report_content`            |

### Valuation tools / 估值工具 (3)

| #  | Tool name                     | Description / 描述                                          | Required params                      |
|----|-------------------------------|-------------------------------------------------------------|--------------------------------------|
| 9  | `calculate_valuation`         | Calculate intrinsic value (DCF, Graham, PE, PB, PS, EV/EBITDA, PEG, DDM, owner_earnings, replacement_cost, cross_validate) | `method`, `params` |
| 10 | `get_position_sizing`         | Calculate position sizing and buy ladder                    | `intrinsic_value`, `current_price`   |
| 11 | `get_do_not_invest_checklist` | Return the do-not-invest discipline checklist               | (optional: `framework`)             |

### Export and audit tools / 导出与审计工具 (3)

| #  | Tool name                 | Description / 描述                                              | Required params                                |
|----|---------------------------|-----------------------------------------------------------------|-----------------------------------------------|
| 12 | `export_report`           | Export report to Markdown/PDF/both                              | `content`, `ticker`, `framework`, `report_id` |
| 13 | `audit_report_citations`  | Audit report for uncited data, detect hallucination risk        | `report_content`                              |
| 14 | `validate_data_point`     | Cross-validate a data point with confidence scoring             | `value`, `label`, `sources`                   |

### Valuation method options for `calculate_valuation`

The `method` parameter accepts one of:

```
dcf, graham, pe, pb, ps, ev_ebitda, peg, ddm,
owner_earnings, replacement_cost, cross_validate
```

Each method requires different `params`. See `src/core/valuation.py` for parameter details.

---

## UnifiedSkillRouter intent detection / 统一路由意图检测

The router in `src/server/skill_router.py` classifies natural language input into actions:

| Intent / 意图            | Keywords / 关键词                                          | Action             |
|--------------------------|------------------------------------------------------------|--------------------|
| Report generation        | report, research, framework, 投研, 报告, 研报, 分析        | `generate_report`  |
| Freshness check          | freshness, stale, outdated, 时效, 过期, 新鲜               | `freshness_check`  |
| Valuation                | valuation, dcf, graham, intrinsic value, 估值, 折现         | `valuation`        |
| Checklist                | checklist, discipline, do not invest, 不为清单, 纪律        | `checklist`        |
| Position sizing          | position, sizing, buy ladder, 仓位, 建仓, 资金管理         | `position_sizing`  |
| Search (default)         | Everything else                                            | `search`           |

---

## Using in Claude Chat / 在 Claude Chat 中使用

### Step 1: Open project in VS Code

Claude automatically discovers the project via `SKILL.md` and `.instructions.md`.

### Step 2: Open Claude Chat (Ctrl + L)

### Step 3: Use natural language queries

**Search examples / 搜索示例:**

```
"What's the latest with Apple stock?"
"Analyze AI tech stocks"
"Research Amazon company information"
"Deep research on quantum computing"
```

**Report examples / 报告示例:**

```
"Generate a research report for Tesla (TSLA)"
"Create investment report for Uniswap (UNI) in crypto"
"Write report for HSBC (0005.HK)"
```

**Valuation examples / 估值示例:**

```
"Calculate DCF valuation for AAPL: FCF=100B, growth=15%, discount=10%"
"Graham formula: EPS=6.5, growth=15%"
"Cross-validate these valuations"
```

**Validation examples / 验证示例:**

```
"Check if this report data is still current"
"Audit citations in this report"
"Validate this revenue figure against these sources"
```

**Export examples / 导出示例:**

```
"Export this report to PDF"
"Save report as both markdown and PDF"
```

### Conversation chaining / 对话链式调用

Claude maintains context across turns, enabling multi-step workflows:

```
User: "Generate a research report for Apple (AAPL)"
Claude: [Generates skeleton, lists unfilled fields, suggests search queries]

User: "Search for the data to fill the critical fields"
Claude: [Runs multiple searches, fills in placeholders with cited data]

User: "Run valuation with the financial data we found"
Claude: [Calculates DCF, PE, Graham, cross-validates]

User: "Check data freshness and audit citations"
Claude: [Flags stale data, identifies uncited data points]

User: "Export the final report"
Claude: [Runs pre-export audit, exports to Markdown + PDF]
```

---

## SKILL.md configuration / SKILL.md 配置

The `SKILL.md` file in the project root is the auto-discovery entry point for Claude:

```yaml
---
description: Crisis Investment Research Assistant - Generate structured investment
  reports using three research frameworks ...
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
---
```

This file also contains:

- Core philosophy and methodology
- Data integrity and anti-hallucination rules (7 rules)
- Source priority tiers
- All 14 tool descriptions
- Report output requirements (Data Audit Summary)

---

## .instructions.md configuration / .instructions.md 配置

The `.instructions.md` file provides Claude with operating instructions, including:

- How to route different query types
- Anti-hallucination enforcement rules
- Source citation format: `[Source: XX | Date: YYYY-MM-DD]`
- When to use each tool
- Export audit requirements

---

## Anti-hallucination safeguards / 反幻觉保障

The system enforces data integrity at multiple layers:

1. **Source tier tagging** -- Every search result is classified Tier 1-4
2. **Citation audit** -- `audit_report_citations` scans for uncited financial data
3. **Cross-validation** -- `validate_data_point` checks consistency across sources
4. **Freshness check** -- `check_report_freshness` flags stale data
5. **Pre-export block** -- Export is blocked when hallucination risk is "high"
6. **Valuation source warning** -- Valuation results without `_source` fields are flagged
7. **Cross-validate confidence downgrade** -- If >50% of valuation methods lack sources, confidence is downgraded

---

## Python integration examples / Python 集成示例

### Full workflow example / 完整工作流示例

```python
from src.server.skill_router import UnifiedSkillRouter
from src.core.researcher import InvestmentResearcher
from src.core.valuation import ValuationMethods
from src.core.freshness import DataFreshnessChecker
from src.core.validator import DataValidator
from src.search.exa_searcher import StockSearcher
from src.export.exporter import ReportExporter

# Initialize / 初始化
searcher = StockSearcher()
researcher = InvestmentResearcher(searcher)
validator = DataValidator()
exporter = ReportExporter()

# 1. Generate report skeleton / 生成报告骨架
report = researcher.generate_report_skeleton("Apple", "AAPL")

# 2. Get research queries / 获取研究查询
queries = researcher.get_research_queries("Apple", "AAPL", report["framework"])

# 3. Search and fill data / 搜索填充数据
for q in queries[:5]:
    results = searcher.search_stock_news(q["query"], num_results=3)
    # ... fill report placeholders with results

# 4. Validate key data points / 验证关键数据
result = validator.validate_data_point(
    value=124.0, label="Q1 Revenue (B)",
    sources=[
        {"name": "SEC 10-Q", "url": "https://sec.gov/...", "date": "2026-03-15", "value": 124.0},
        {"name": "Yahoo Finance", "url": "https://yahoo.com/...", "date": "2026-03-15", "value": 123.9},
    ],
)

# 5. Calculate valuations / 计算估值
dcf = ValuationMethods.dcf(fcf_current=100e9, growth_rate=0.12, shares_outstanding=15e9)
graham = ValuationMethods.graham_formula(eps=6.5, growth_rate=0.15)
cross = ValuationMethods.cross_validate([dcf, graham])

# 6. Check freshness / 检查时效性
checker = DataFreshnessChecker()
freshness = checker.check_report(report["content"])

# 7. Audit citations / 审计来源标注
audit = checker.audit_source_citations(report["content"])

# 8. Export / 导出
if audit["hallucination_risk"] != "high":
    paths = exporter.export_both(
        content=report["content"],
        ticker="AAPL",
        framework=report["framework"],
        report_id=report["report_id"],
    )
```

### Using the MCP server directly / 直接使用 MCP 服务器

```python
from src.server.mcp_server import ExaMCPServer
import json

server = ExaMCPServer()

# List all 14 tools / 列出所有 14 个工具
print(server.get_tools())

# Call a tool / 调用工具
result = server.handle_tool_call("search_stock_news", {"ticker": "AAPL", "num_results": 5})
print(result)

# Generate report via MCP / 通过 MCP 生成报告
result = server.handle_tool_call("generate_research_report", {
    "target_name": "Apple",
    "ticker": "AAPL",
    "market": "us",
})
report = json.loads(result)
print(report["framework"])
```

---

## Troubleshooting / 故障排查

### Claude does not call search tools / Claude 不调用搜索工具

1. Verify `SKILL.md` exists in the project root and is valid YAML frontmatter.
2. Verify `.instructions.md` exists and is complete.
3. Restart Claude Chat (Ctrl+Shift+L) to reload the skill.

### Search results are inaccurate / 搜索结果不准确

1. Use more specific queries with clear intent.
2. Check that the API key is valid at https://dashboard.exa.ai
3. Try `deep` search type for more thorough results.

### Export blocked / 导出被阻止

The export is blocked when `hallucination_risk` is "high". To fix:

1. Run `audit_report_citations` to see which data points lack citations.
2. Add `[来源: XX | 日期: YYYY-MM-DD]` tags to all financial data.
3. Re-run the audit until risk drops to "medium" or "low".
4. Alternatively, set `validation.block_export_on_high_risk: false` in `config.yaml` to disable the block (not recommended).

### PDF generation fails / PDF 生成失败

The system falls back through three engines:

1. Install Playwright + Chromium for best results:
   ```powershell
   pip install playwright
   playwright install chromium
   ```
2. Or install PyMuPDF: `pip install pymupdf`
3. Last resort: plain text PDF (always available).

---

## Related docs / 相关文档

- [Quick start / 快速开始](01-QUICKSTART.md)
- [Complete usage guide / 完整使用指南](02-USAGE.md)
