# Project Structure / 项目结构说明

Crisis Investment Researcher v0.3.0 -- file organization and module reference.

Crisis Investment Researcher v0.3.0 -- 文件组织与模块参考。

---

## Table of Contents / 目录

1. [Full Project Tree / 完整项目树](#full-project-tree)
2. [Directory Reference / 目录说明](#directory-reference)
3. [Core Module Reference / 核心模块说明](#core-module-reference)
4. [Data Flow / 数据流](#data-flow)
5. [Configuration Hierarchy / 配置优先级](#configuration-hierarchy)
6. [File Purpose Matrix / 文件用途矩阵](#file-purpose-matrix)
7. [Module Dependency Graph / 模块依赖图](#module-dependency-graph)
8. [Usage Paths / 使用路径](#usage-paths)

---

## Full Project Tree / 完整项目树

```
d:\MCP project\EXA search MCP\
|
|-- config.yaml                          # Main configuration (bilingual comments)
|-- .env                                 # API keys alternative (not committed)
|-- .env.example                         # .env template
|-- requirements.txt                     # Python dependencies
|-- setup.py                             # Package configuration
|-- check_integration.py                 # Integration verification script
|-- README.md                            # Project overview
|-- SKILL.md                             # Claude auto-discovery file (required)
|-- .instructions.md                     # Claude usage instructions (required)
|-- .gitignore                           # Git ignore rules
|
|-- src/                                 # Main source code directory
|   |-- __init__.py
|   |-- config.py                        # Centralized config loader
|   |-- claude_skill.py                  # CLI entry point + Claude interface
|   |
|   |-- search/                          # Search layer
|   |   |-- __init__.py
|   |   |-- exa_searcher.py              # StockSearcher (retry, config-driven)
|   |
|   |-- core/                            # Research & analysis engine
|   |   |-- __init__.py
|   |   |-- researcher.py                # InvestmentResearcher (3 frameworks)
|   |   |-- valuation.py                 # ValuationMethods (10+ methods)
|   |   |-- freshness.py                 # DataFreshnessChecker
|   |   |-- validator.py                 # DataValidator (cross-validation)
|   |
|   |-- server/                          # Service layer
|   |   |-- __init__.py
|   |   |-- mcp_server.py                # ExaMCPServer (14 tools)
|   |   |-- skill_router.py              # UnifiedSkillRouter
|   |
|   |-- export/                          # Report output
|   |   |-- __init__.py
|   |   |-- exporter.py                  # ReportExporter (MD + PDF)
|   |   |-- naming.py                    # ReportNaming
|   |
|   |-- utils/                           # Shared utilities
|   |   |-- __init__.py
|   |   |-- helpers.py                   # API key loading, misc helpers
|   |
|   |-- examples/                        # Demo scripts
|   |   |-- __init__.py
|   |   |-- basic_search.py              # Basic search demo
|   |   |-- stock_search.py              # Stock search demo
|   |   |-- claude_skill_demo.py         # Claude Skill demo
|   |   |-- openai_function_calling.py   # OpenAI integration demo
|   |   |-- anthropic_tool_use.py        # Anthropic integration demo
|   |
|   |-- _deprecated/                     # Old module versions (reference only)
|
|-- config/                              # External configuration files
|   |-- exa_config.json                  # Exa API configuration
|   |-- mcp_config.json                  # MCP server configuration
|
|-- research Output/                     # Generated reports
|   |-- markdown/                        # Exported Markdown reports
|   |-- pdf/                             # Exported PDF reports
|   |-- templates/                       # Report templates
|       |-- mature_company_template.md   # Mature company framework template
|       |-- growth_company_template.md   # Growth company framework template
|       |-- web3_project_template.md     # Web3 project framework template
|
|-- docs/                                # Documentation
|   |-- 01-QUICKSTART.md
|   |-- 02-USAGE.md
|   |-- 03-INTEGRATION.md
|   |-- 04-DEPLOYMENT.md
|   |-- 05-API-REFERENCE.md
|   |-- 06-TROUBLESHOOTING.md
|   |-- 07-PROJECT-STRUCTURE.md          # This file / 本文件
|
|-- venv/                                # Python virtual environment (not committed)
|-- .vscode/                             # VS Code workspace settings
```

---

## Directory Reference / 目录说明

### `src/` -- Main Source Code / 主源代码

All application logic lives here. The directory is organized into layers by responsibility.

所有应用逻辑位于此处。目录按职责划分为多个层。

| Subdirectory / 子目录 | Purpose / 用途 | Key Classes / 关键类 |
|---|---|---|
| `src/` (root) | Entry points and config / 入口与配置 | `config.py`, `claude_skill.py` |
| `src/search/` | Data acquisition from Exa API / 从 Exa API 获取数据 | `StockSearcher` |
| `src/core/` | Research logic and analysis / 研究逻辑与分析 | `InvestmentResearcher`, `ValuationMethods`, `DataFreshnessChecker`, `DataValidator` |
| `src/server/` | Service interfaces (MCP, routing) / 服务接口 | `ExaMCPServer`, `UnifiedSkillRouter` |
| `src/export/` | Report generation and file output / 报告生成与导出 | `ReportExporter`, `ReportNaming` |
| `src/utils/` | Shared helpers / 通用工具 | `helpers.py` |
| `src/examples/` | Demo and integration examples / 示例与集成演示 | -- |
| `src/_deprecated/` | Archived old modules / 归档的旧模块 | -- |

### `config/` -- External Configuration / 外部配置

JSON configuration files for Exa API and MCP server settings. These supplement `config.yaml`.

Exa API 和 MCP 服务器的 JSON 配置文件。作为 `config.yaml` 的补充。

### `research Output/` -- Generated Reports / 生成的报告

Output directory for exported research reports. Organized into:

导出的研究报告输出目录。分为：

- `markdown/` -- Markdown format reports / Markdown 格式报告
- `pdf/` -- PDF format reports / PDF 格式报告
- `templates/` -- Report templates for the three research frameworks / 三种研究框架的报告模板

### `docs/` -- Documentation / 文档

Project documentation files numbered in reading order.

按阅读顺序编号的项目文档。

---

## Core Module Reference / 核心模块说明

### `src/config.py` -- Centralized Configuration Loader / 集中配置加载器

The single source of truth for all configuration. Every module imports its settings from here.

所有配置的唯一数据来源。每个模块都从此处导入配置。

**Key functions / 关键函数:**

| Function / 函数 | Returns / 返回值 | Description / 说明 |
|---|---|---|
| `get_api_key(service)` | `str` | API key for "exa", "openai", or "anthropic" / 对应服务的 API 密钥 |
| `get_search_config()` | `dict` | Search type, num_results, max_characters, content_mode / 搜索配置 |
| `get_network_config()` | `dict` | Timeout, max_retries, retry_delay / 网络配置 |
| `get_validation_config()` | `dict` | Citation requirements, cross-validation settings / 验证配置 |
| `get_freshness_thresholds()` | `dict` | Per-category freshness thresholds in days / 各类别新鲜度阈值 |
| `get_source_tiers()` | `dict` | Source credibility tier domain lists / 来源可信度分级域名列表 |

**Priority order / 优先级:**
1. Environment variables / `.env` (highest / 最高)
2. `config.yaml` (middle / 中)
3. Built-in defaults (lowest / 最低)

---

### `src/search/exa_searcher.py` -- StockSearcher / 搜索引擎

The data acquisition layer. Wraps the Exa API with retry logic, configurable parameters, and source tier awareness.

数据获取层。对 Exa API 进行封装，支持重试逻辑、可配置参数和来源分级。

**Class: `StockSearcher`**

| Method / 方法 | Description / 说明 |
|---|---|
| `__init__(api_key=None)` | Initialize with config-driven defaults / 使用配置驱动的默认值初始化 |
| `search_stock_news(ticker, num_results, include_highlights)` | Search latest news for a stock ticker / 搜索股票最新新闻 |
| `search_market_analysis(topic, num_results, include_highlights)` | Search market analysis and trends / 搜索市场分析与趋势 |
| `search_company_info(company_name, num_results, include_highlights)` | Search company information / 搜索公司信息 |
| `search_with_deep_research(query, num_results, include_highlights)` | Deep research with comprehensive results / 深度研究 |
| `format_results(results, max_items)` | Format raw results into readable text / 格式化原始结果 |

**Features / 特性:**
- Automatic retry with configurable delay (`network.max_retries`, `network.retry_delay`) / 自动重试
- Source tier domain lists loaded from `config.yaml` / 从配置加载来源分级
- All parameters driven by `config.yaml` / 所有参数由配置驱动

---

### `src/core/researcher.py` -- InvestmentResearcher / 投资研究引擎

The core research engine implementing the Crisis Investment methodology. Supports three research frameworks.

核心研究引擎，实现 Crisis Investment 方法论。支持三种研究框架。

**Class: `InvestmentResearcher`**

| Method / 方法 | Description / 说明 |
|---|---|
| `__init__(searcher=None)` | Initialize with optional StockSearcher / 可选传入 StockSearcher |
| `detect_framework(target, market)` | Auto-detect which framework to use / 自动检测应使用的框架 |
| `research(target, framework, ...)` | Execute full research pipeline / 执行完整研究流程 |

**Three frameworks / 三种框架:**

| Framework / 框架 | Constant / 常量 | Use Case / 适用场景 |
|---|---|---|
| Mature Company / 成熟公司 | `FRAMEWORK_MATURE` | Established companies with stable financials / 财务稳定的成熟企业 |
| Growth Company / 成长性公司 | `FRAMEWORK_GROWTH` | High-growth companies, pre-profit or rapid expansion / 高增长企业 |
| Web3 Project / Web3 项目 | `FRAMEWORK_WEB3` | Crypto, DeFi, DAO, NFT projects / 加密货币、DeFi、DAO、NFT 项目 |

**Templates** are stored in `research Output/templates/` as Markdown files.

报告模板以 Markdown 文件形式存储在 `research Output/templates/` 中。

---

### `src/core/valuation.py` -- ValuationMethods / 估值方法

A collection of 10+ static valuation calculation methods for cross-validation.

包含 10 余种静态估值计算方法，用于交叉验证。

**Class: `ValuationMethods`**

All methods are `@staticmethod` and return a `dict` with the method name, calculated values, and assumptions.

所有方法均为 `@staticmethod`，返回包含方法名、计算结果和假设条件的 `dict`。

| Method / 方法 | Description / 说明 |
|---|---|
| `dcf(...)` | Discounted Cash Flow / 自由现金流折现 |
| `pe_valuation(...)` | Price-to-Earnings / 市盈率估值 |
| `ps_valuation(...)` | Price-to-Sales / 市销率估值 |
| `pb_valuation(...)` | Price-to-Book / 市净率估值 |
| `ev_ebitda(...)` | Enterprise Value / EBITDA |
| `dividend_discount(...)` | Dividend Discount Model / 股息折现模型 |
| `sum_of_parts(...)` | Sum of the Parts / 分部估值 |
| ... and more | Additional methods per framework / 更多框架特定方法 |

---

### `src/core/freshness.py` -- DataFreshnessChecker / 数据新鲜度检查器

Validates the timeliness of data used in research reports. Each data category has a configurable age threshold.

验证研究报告中所用数据的时效性。每个数据类别都有可配置的年龄阈值。

**Class: `DataFreshnessChecker`**

| Method / 方法 | Description / 说明 |
|---|---|
| `__init__(reference_date=None)` | Set reference date for age calculations / 设置年龄计算的参考日期 |
| `check(data_type, data_date)` | Return freshness status for a data point / 返回数据点的新鲜度状态 |
| `check_report(data_items)` | Batch check all data in a report / 批量检查报告中所有数据 |

**Freshness statuses / 新鲜度状态:**
- `fresh` -- Within threshold / 在阈值内
- `aging` -- Approaching threshold / 接近阈值
- `stale` -- Exceeds threshold / 超过阈值
- `unknown` -- Cannot determine / 无法判断

Thresholds are loaded from `config.yaml` under `validation.freshness_thresholds`, with built-in defaults as fallback.

阈值从 `config.yaml` 的 `validation.freshness_thresholds` 加载，内置默认值作为备选。

---

### `src/core/validator.py` -- DataValidator / 数据验证器

Cross-validates financial data across multiple sources and assigns confidence scores based on source credibility tiers.

跨多个来源交叉验证财务数据，并根据来源可信度等级分配置信度评分。

**Class: `DataValidator`**

| Method / 方法 | Description / 说明 |
|---|---|
| `__init__(source_tiers=None)` | Load source tier domains from config / 从配置加载来源分级域名 |
| `validate_data_point(value, unit, label, sources)` | Validate a single data point / 验证单个数据点 |
| `get_source_tier(url)` | Determine credibility tier for a URL / 判断 URL 的可信度等级 |
| `cross_validate(sources)` | Check consistency across sources / 检查来源间的一致性 |

**Source tiers / 来源等级:**

| Tier / 等级 | Label / 标签 | Examples / 示例 |
|---|---|---|
| Tier 1 | Official / Regulatory (官方/监管) | sec.gov, hkex.com.hk, defillama.com |
| Tier 2 | Mainstream Financial (主流财经) | bloomberg.com, reuters.com, yahoo finance |
| Tier 3 | Analytical Reference (分析参考) | investopedia.com, tipranks.com |
| Tier 4 | Requires Cross-Validation (需交叉验证) | All other sources / 所有其他来源 |

Tier domain lists are configurable in `config.yaml` under `source_tiers`.

等级域名列表可在 `config.yaml` 的 `source_tiers` 中配置。

---

### `src/server/skill_router.py` -- UnifiedSkillRouter / 统一路由器

The central dispatch hub. Interprets natural language queries and routes them to the appropriate handler: search, research, valuation, freshness check, or report export.

核心分发中枢。解析自然语言查询，将其路由到相应的处理器：搜索、研究、估值、新鲜度检查或报告导出。

**Class: `UnifiedSkillRouter`**

| Method / 方法 | Description / 说明 |
|---|---|
| `__init__(api_key=None)` | Initialize all sub-components / 初始化所有子组件 |
| `route(user_input)` | Dispatch to the correct handler based on intent / 根据意图分发到正确的处理器 |
| `search_and_format(query, num_results, max_display)` | Search and return formatted text / 搜索并返回格式化文本 |
| `search_as_json(query, num_results)` | Search and return JSON / 搜索并返回 JSON |

**Internal routing logic / 内部路由逻辑:**

The `route()` method detects intent in this priority order:

`route()` 方法按以下优先级检测意图：

1. Report generation request / 报告生成请求
2. Freshness check request / 新鲜度检查请求
3. Valuation request / 估值请求
4. Checklist request / 检查清单请求
5. Position sizing request / 仓位计算请求
6. General search (fallback) / 通用搜索（兜底）

---

### `src/server/mcp_server.py` -- ExaMCPServer / MCP 服务器

Exposes 14 tools via the Model Context Protocol for external AI model integration.

通过 Model Context Protocol 暴露 14 个工具，用于外部 AI 模型集成。

**Class: `ExaMCPServer`**

| Tool / 工具 | Description / 说明 |
|---|---|
| `search_stock_news` | Search stock news by ticker / 按代码搜索股票新闻 |
| `search_market_analysis` | Search market trends / 搜索市场趋势 |
| `search_company_info` | Search company details / 搜索公司详情 |
| `search_deep_research` | Deep comprehensive search / 深度综合搜索 |
| `detect_framework` | Auto-detect research framework / 自动检测研究框架 |
| `run_research` | Execute full research pipeline / 执行完整研究流程 |
| `calculate_valuation` | Run valuation methods / 运行估值方法 |
| `check_freshness` | Check data freshness / 检查数据新鲜度 |
| `validate_data` | Cross-validate data points / 交叉验证数据点 |
| `export_markdown` | Export report as Markdown / 导出 Markdown 报告 |
| `export_pdf` | Export report as PDF / 导出 PDF 报告 |
| ... | Additional tools / 更多工具 |

---

### `src/export/exporter.py` -- ReportExporter / 报告导出器

Dual-format report export: Markdown and PDF. Output directories are configurable.

双格式报告导出：Markdown 和 PDF。输出目录可配置。

**Class: `ReportExporter`**

| Method / 方法 | Description / 说明 |
|---|---|
| `__init__(md_dir=None, pdf_dir=None)` | Set output directories (defaults from config) / 设置输出目录 |
| `export_markdown(content, ticker, framework, report_id, naming_pattern)` | Save as .md file / 保存为 .md 文件 |
| `export_pdf(content, ticker, framework, report_id, naming_pattern)` | Save as .pdf file / 保存为 .pdf 文件 |

**PDF engine priority** (configured in `config.yaml` under `export.pdf_engines`):

**PDF 引擎优先级**（在 `config.yaml` 的 `export.pdf_engines` 中配置）：

1. `chromium` -- Playwright-based, best quality / 基于 Playwright，最佳质量
2. `fitz` -- PyMuPDF-based, good quality / 基于 PyMuPDF，较好质量
3. `text` -- Plain text fallback, always available / 纯文本备选，始终可用

### `src/export/naming.py` -- ReportNaming / 报告命名

Generates standardized file names using a configurable pattern.

使用可配置的模式生成标准化文件名。

**Default pattern / 默认模式:** `{date}_{ticker}_{framework}_{report_id}`

**Example output / 示例输出:** `2026-04-04_AAPL_mature_a1b2c3d4.md`

---

### `src/claude_skill.py` -- CLI Entry Point / 命令行入口

The interface between Claude (or the command line) and the rest of the system. Provides three exported functions.

Claude（或命令行）与系统其余部分之间的接口。提供三个导出函数。

**Exported functions / 导出函数:**

| Function / 函数 | Returns / 返回 | Description / 说明 |
|---|---|---|
| `search_stock(query, num_results)` | `str` | Formatted text search results / 格式化文本搜索结果 |
| `research(query)` | `str` (JSON) | Full research pipeline result / 完整研究流程结果 |
| `search_stock_json(query, num_results)` | `str` (JSON) | Raw JSON search results / 原始 JSON 搜索结果 |

**CLI usage / 命令行用法:**
```powershell
python src/claude_skill.py "Generate report for AAPL"
python src/claude_skill.py "Analyze AI stocks"
python src/claude_skill.py "Valuation for Tesla"
```

---

## Data Flow / 数据流

### Research Pipeline / 研究流程

```
User Input (natural language query)
用户输入 (自然语言查询)
        |
        v
claude_skill.py
  (CLI entry point / 命令行入口)
        |
        v
UnifiedSkillRouter  [src/server/skill_router.py]
  (intent detection & dispatch / 意图检测与分发)
        |
        +--> StockSearcher  [src/search/exa_searcher.py]
        |      (Exa API calls with retry / Exa API 调用，带重试)
        |      |
        |      v
        |    Exa API  -->  Raw search results / 原始搜索结果
        |
        +--> InvestmentResearcher  [src/core/researcher.py]
        |      (3 framework pipelines / 三种框架流程)
        |      |
        |      +--> StockSearcher  (data acquisition / 数据获取)
        |      +--> ValuationMethods  [src/core/valuation.py]
        |      |      (10+ calculation methods / 10+ 计算方法)
        |      +--> DataFreshnessChecker  [src/core/freshness.py]
        |      |      (timeliness validation / 时效性验证)
        |      +--> DataValidator  [src/core/validator.py]
        |             (cross-validation & scoring / 交叉验证与评分)
        |
        +--> ReportExporter  [src/export/exporter.py]
               (Markdown + PDF output / Markdown + PDF 输出)
               |
               v
          research Output/
            markdown/   (*.md files)
            pdf/        (*.pdf files)
```

### Simple Search Flow / 简单搜索流程

```
User Input --> claude_skill.py --> UnifiedSkillRouter --> StockSearcher --> Exa API
                                                                              |
User Output <-- formatted text <-- UnifiedSkillRouter <-- raw results <-------+
```

### MCP Server Flow / MCP 服务器流程

```
External AI Model
        |
        v
ExaMCPServer  [src/server/mcp_server.py]
  (14 tool definitions / 14 个工具定义)
        |
        +--> StockSearcher
        +--> InvestmentResearcher
        +--> ValuationMethods
        +--> DataFreshnessChecker
        +--> DataValidator
        +--> ReportExporter
```

---

## Configuration Hierarchy / 配置优先级

The system uses a three-level configuration hierarchy managed by `src/config.py`.

系统使用由 `src/config.py` 管理的三级配置层次。

```
+---------------------------------------+
| Priority 1 (Highest / 最高优先级)     |
| Environment Variables / .env          |
|                                       |
|   EXA_API_KEY=xxx                     |
|   OPENAI_API_KEY=xxx                  |
|   ANTHROPIC_API_KEY=xxx               |
+---------------------------------------+
              |  (overrides / 覆盖)
              v
+---------------------------------------+
| Priority 2 (Middle / 中优先级)        |
| config.yaml                           |
|                                       |
|   api_keys:                           |
|     exa: "xxx"                        |
|   search:                             |
|     type: "auto"                      |
|     num_results: 10                   |
|   validation:                         |
|     min_cross_validation_sources: 2   |
|   source_tiers:                       |
|     tier1: [...]                      |
|   export:                             |
|     pdf_engines: [...]                |
|   network:                            |
|     timeout: 30                       |
+---------------------------------------+
              |  (overrides / 覆盖)
              v
+---------------------------------------+
| Priority 3 (Lowest / 最低优先级)      |
| Built-in Defaults                     |
|   (hardcoded in src/config.py and     |
|    individual modules)                |
|   (硬编码在 src/config.py 和各模块中) |
+---------------------------------------+
```

**Configuration sections in config.yaml:**

**config.yaml 中的配置段：**

| Section / 配置段 | Purpose / 用途 | Consumer Modules / 使用模块 |
|---|---|---|
| `api_keys` | API credentials / API 凭据 | All modules via `get_api_key()` |
| `search` | Search behavior / 搜索行为 | `StockSearcher` |
| `validation` | Data quality rules / 数据质量规则 | `DataValidator`, `DataFreshnessChecker`, `ExaMCPServer` |
| `source_tiers` | Source credibility domains / 来源可信度域名 | `DataValidator`, `StockSearcher` |
| `export` | Report output settings / 报告输出设置 | `ReportExporter`, `ReportNaming` |
| `network` | Timeout and retry / 超时与重试 | `StockSearcher` |

---

## File Purpose Matrix / 文件用途矩阵

### Source Files / 源代码文件

| File / 文件 | Purpose / 用途 | Required / 必需 | Git Tracked / 提交 Git |
|---|---|---|---|
| `src/config.py` | Centralized config loader / 集中配置加载 | Yes | Yes |
| `src/claude_skill.py` | CLI entry point + Claude interface / 入口与 Claude 接口 | Yes | Yes |
| `src/search/exa_searcher.py` | Exa API search engine / Exa API 搜索引擎 | Yes | Yes |
| `src/core/researcher.py` | Investment research engine / 投资研究引擎 | Yes | Yes |
| `src/core/valuation.py` | Valuation calculations / 估值计算 | Yes | Yes |
| `src/core/freshness.py` | Data freshness checker / 数据新鲜度检查 | Yes | Yes |
| `src/core/validator.py` | Data cross-validation / 数据交叉验证 | Yes | Yes |
| `src/server/mcp_server.py` | MCP server (14 tools) / MCP 服务器 | Optional | Yes |
| `src/server/skill_router.py` | Unified query router / 统一查询路由 | Yes | Yes |
| `src/export/exporter.py` | Markdown + PDF export / 报告导出 | Yes | Yes |
| `src/export/naming.py` | Report file naming / 报告文件命名 | Yes | Yes |
| `src/utils/helpers.py` | Shared utilities / 共享工具 | Yes | Yes |

### Configuration Files / 配置文件

| File / 文件 | Purpose / 用途 | Required / 必需 | Git Tracked / 提交 Git |
|---|---|---|---|
| `config.yaml` | Main configuration / 主配置文件 | Recommended | Yes (without secrets) |
| `.env` | API keys (alternative) / API 密钥 | Optional | No |
| `.env.example` | `.env` template / 模板 | Yes | Yes |
| `config/exa_config.json` | Exa-specific settings / Exa 专属设置 | Optional | Yes |
| `config/mcp_config.json` | MCP server settings / MCP 服务器设置 | Optional | Yes |

### Claude Integration Files / Claude 集成文件

| File / 文件 | Purpose / 用途 | Required / 必需 | Git Tracked / 提交 Git |
|---|---|---|---|
| `SKILL.md` | Claude auto-discovery / Claude 自动发现 | Yes | Yes |
| `.instructions.md` | Claude usage instructions / Claude 使用说明 | Yes | Yes |

### Project Files / 项目文件

| File / 文件 | Purpose / 用途 | Required / 必需 | Git Tracked / 提交 Git |
|---|---|---|---|
| `requirements.txt` | Python dependencies / Python 依赖 | Yes | Yes |
| `setup.py` | Package configuration / 包配置 | Yes | Yes |
| `check_integration.py` | Integration verification / 集成验证 | Recommended | Yes |
| `README.md` | Project overview / 项目说明 | Recommended | Yes |

### Output Directories / 输出目录

| Directory / 目录 | Purpose / 用途 | Git Tracked / 提交 Git |
|---|---|---|
| `research Output/markdown/` | Generated Markdown reports / 生成的 Markdown 报告 | No (gitignored) |
| `research Output/pdf/` | Generated PDF reports / 生成的 PDF 报告 | No (gitignored) |
| `research Output/templates/` | Report templates / 报告模板 | Yes |
| `venv/` | Virtual environment / 虚拟环境 | No |

---

## Module Dependency Graph / 模块依赖图

This diagram shows which modules import from which. Arrows point from the importer to the dependency.

此图展示模块间的导入关系。箭头从导入方指向被依赖方。

```
                       src/config.py
                      /    |    |    \
                     v     v    v     v
         exa_searcher   freshness  validator   exporter
              |             |         |
              v             v         v
     +--------+--------+--------+--------+
     |                                    |
     v                                    v
  researcher  <--- (uses searcher,    valuation
     |               valuation,
     |               freshness)
     v
  +--+--+
  |     |
  v     v
skill_router    mcp_server
  |     |         |
  v     v         v
  (imports: searcher, researcher, valuation,
   freshness, validator, exporter)
         |
         v
   claude_skill.py
     (imports: skill_router)
```

**Detailed import map / 详细导入关系:**

| Module / 模块 | Imports From / 导入自 |
|---|---|
| `src/config.py` | `dotenv`, `yaml` (external) |
| `src/search/exa_searcher.py` | `src/config`, `exa_py` (external) |
| `src/core/researcher.py` | (receives `StockSearcher` via constructor) |
| `src/core/valuation.py` | (no internal imports -- standalone / 无内部导入) |
| `src/core/freshness.py` | `src/config` |
| `src/core/validator.py` | `src/config` |
| `src/export/exporter.py` | `src/export/naming` |
| `src/export/naming.py` | (no internal imports -- standalone / 无内部导入) |
| `src/server/skill_router.py` | `src/config`, `src/search/exa_searcher`, `src/core/researcher`, `src/core/valuation`, `src/core/freshness`, `src/core/validator`, `src/export/exporter` |
| `src/server/mcp_server.py` | `src/config`, `src/search/exa_searcher`, `src/core/researcher`, `src/core/valuation`, `src/core/freshness`, `src/core/validator`, `src/export/exporter` |
| `src/claude_skill.py` | `src/server/skill_router` |

**External dependencies / 外部依赖:**

| Package / 包 | Used By / 使用者 | Purpose / 用途 |
|---|---|---|
| `exa-py` | `StockSearcher` | Exa API client / Exa API 客户端 |
| `python-dotenv` | `src/config`, `src/utils/helpers` | .env file loading / .env 文件加载 |
| `pyyaml` | `src/config` | YAML config parsing / YAML 配置解析 |
| `markdown` | `ReportExporter` | Markdown to HTML conversion / Markdown 转 HTML |
| `pymupdf` | `ReportExporter` | PDF generation (fitz engine) / PDF 生成 |
| `playwright` | `ReportExporter` | PDF generation (chromium engine) / PDF 生成 |
| `openai` | Examples only / 仅示例 | OpenAI function calling demo |
| `anthropic` | Examples only / 仅示例 | Anthropic tool use demo |
| `requests` | Various / 多处 | HTTP requests / HTTP 请求 |

---

## Usage Paths / 使用路径

### Path 1: Claude Chat Integration / Claude Chat 集成

```
Claude Chat --> SKILL.md --> .instructions.md --> claude_skill.py --> UnifiedSkillRouter --> ...
```

### Path 2: Command Line / 命令行

```
Terminal --> claude_skill.py --> UnifiedSkillRouter --> StockSearcher / InvestmentResearcher --> ...
```

### Path 3: MCP Server / MCP 服务器

```
External AI Model --> ExaMCPServer --> StockSearcher / InvestmentResearcher / ... --> results
```

### Path 4: Direct Python Import / 直接 Python 导入

```python
from src.search.exa_searcher import StockSearcher
from src.core.researcher import InvestmentResearcher
from src.core.valuation import ValuationMethods
from src.server.skill_router import UnifiedSkillRouter
from src.export.exporter import ReportExporter
```

---

## Modification Guide / 修改指南

### Safe to modify / 安全修改

- Search parameters in `config.yaml` / 修改 `config.yaml` 中的搜索参数
- Source tier domain lists in `config.yaml` / 修改 `config.yaml` 中的来源分级域名
- Freshness thresholds in `config.yaml` / 修改 `config.yaml` 中的新鲜度阈值
- Report templates in `research Output/templates/` / 修改报告模板
- Add new valuation methods to `src/core/valuation.py` / 添加新估值方法
- Add new search methods to `src/search/exa_searcher.py` / 添加新搜索方法
- Update documentation / 更新文档

### Modify with caution / 谨慎修改

- `src/claude_skill.py` exported function signatures (breaks Claude integration) / 导出函数签名
- `SKILL.md` name field (breaks Claude discovery) / name 字段
- `src/config.py` priority logic (affects all modules) / 优先级逻辑
- `src/server/skill_router.py` routing logic (affects all query dispatch) / 路由逻辑

---

## Related Documentation / 相关文档

- [Quick Start / 快速开始](01-QUICKSTART.md)
- [Usage / 完整使用](02-USAGE.md)
- [Claude Integration / Claude 集成](03-INTEGRATION.md)
- [Deployment / 部署指南](04-DEPLOYMENT.md)
- [API Reference / API 参考](05-API-REFERENCE.md)
- [Troubleshooting / 故障排查](06-TROUBLESHOOTING.md)
