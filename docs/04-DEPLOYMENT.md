# Deployment and Setup Guide / 部署和设置指南

v0.3.0 -- Crisis Investment Researcher

Complete environment setup, configuration, and verification workflow.
完整的环境搭建、配置和验证流程。

---

## Prerequisites / 前置条件

- Python 3.10+
- Exa API key (get it from https://dashboard.exa.ai/api-keys)
- (Optional) OpenAI or Anthropic API key for LLM integration examples

---

## Step 1: Configure API Keys / 第1步: 配置 API 密钥

The system reads configuration from **two sources** with the following priority:

1. Environment variables (`.env` file or system env) -- highest priority
2. `config.yaml` -- recommended for non-developers

### Option A: config.yaml (recommended / 推荐)

Open `config.yaml` in the project root. This is the **only** file most users need to edit.

```yaml
# ── API Keys ──
api_keys:
  exa: "your-exa-api-key-here"       # Required / 必填
  openai: ""                          # Optional / 选填
  anthropic: ""                       # Optional / 选填
```

The file also contains search, validation, source-tier, export, and network settings.
Each section is commented in both English and Chinese. Key sections:

| Section / 区块         | Purpose / 用途                                             |
|------------------------|------------------------------------------------------------|
| `api_keys`             | API credentials / API 密钥                                 |
| `search`               | Search type, result count, content mode / 搜索类型与数量    |
| `validation`           | Source-citation rules, freshness thresholds / 数据验证规则  |
| `source_tiers`         | Domain-based credibility ranking / 来源可信度分级           |
| `export`               | Output directories, naming pattern, PDF engines / 导出设置  |
| `network`              | Timeout, retry count, retry delay / 网络设置               |

#### search section details / 搜索设置详解

```yaml
search:
  type: "auto"            # "auto" | "fast" | "deep" | "deep-reasoning"
  num_results: 10         # Results per search / 每次搜索返回数量
  max_characters: 4000    # Max chars per result / 每条结果最大字符数
  content_mode: "highlights"  # "highlights" (saves tokens) | "text" (full article)
```

#### validation section details / 数据验证详解

```yaml
validation:
  require_source_citations: true       # Require [来源: XX] tags / 要求来源标注
  min_cross_validation_sources: 2      # Min sources for cross-validation / 最少交叉验证来源数
  auto_flag_stale_data: true           # Auto-flag stale data / 自动标记过期数据
  block_export_on_high_risk: true      # Block PDF export if hallucination risk is high
  freshness_thresholds:                # Freshness thresholds in days (20 categories)
    stock_price: 1
    financial_statements: 120
    analyst_ratings: 30
    # ... (see config.yaml for all 20 categories)
```

#### export section details / 导出设置详解

```yaml
export:
  markdown_dir: "research Output/markdown"
  pdf_dir: "research Output/pdf"
  naming_pattern: "{date}_{ticker}_{framework}_{report_id}"
  pdf_engines:
    - "chromium"     # Best quality (needs playwright)
    - "fitz"         # Good quality (needs pymupdf, included in requirements.txt)
    - "text"         # Plain text fallback, always available
```

#### network section details / 网络设置详解

```yaml
network:
  timeout: 30          # Request timeout in seconds / 请求超时 (秒)
  max_retries: 3       # Retry count on transient failure / 失败重试次数
  retry_delay: 1.0     # Base delay between retries (exponential backoff) / 重试间隔 (秒)
```

### Option B: .env file (alternative / 备选)

Create a `.env` file in the project root:

```env
EXA_API_KEY=your-exa-api-key-here
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

Environment variables always override values in `config.yaml`.
环境变量的优先级始终高于 `config.yaml`。

---

## Step 2: Install Dependencies / 第2步: 安装依赖

```bash
pip install -r requirements.txt
```

### Required dependencies / 必需依赖

| Package / 包     | Min Version | Purpose / 用途                           |
|-------------------|-------------|------------------------------------------|
| exa-py            | 1.0.0       | Exa search API client / Exa 搜索客户端   |
| python-dotenv     | 1.0.0       | Load .env files / 读取 .env 文件         |
| openai            | 1.0.0       | OpenAI API (optional integration)        |
| anthropic         | 0.7.0       | Anthropic API (optional integration)     |
| requests          | 2.31.0      | HTTP requests / HTTP 请求                |
| markdown          | 3.4.0       | Markdown-to-HTML conversion / MD 转 HTML |
| pymupdf           | 1.23.0      | PDF rendering via fitz / PDF 渲染        |
| pyyaml            | 6.0         | YAML config parsing / YAML 配置解析      |

### Optional: Chromium PDF engine / 可选: Chromium PDF 引擎

For the highest-quality PDF output (the system tries engines in the order defined
in `config.yaml` and falls back automatically):

```bash
pip install playwright
playwright install chromium
```

If Playwright/Chromium is not installed, the system falls back to pymupdf (fitz),
then to a plain-text PDF fallback. No manual action is needed.

---

## Step 3: Verify Installation / 第3步: 验证安装

```bash
python check_integration.py
```

The checker runs five groups of tests:

1. **Core files** -- SKILL.md, .instructions.md, config.yaml, requirements.txt
2. **Source modules** -- all 10 Python modules under `src/`
3. **Configuration** -- config.yaml or .env detected
4. **Python imports** -- all classes import without errors
5. **API key** -- Exa API key is present and non-empty

Expected output when everything is correct:

```
======================================================================
  Crisis Investment Researcher - Integration Checker
======================================================================

[1/5] Core Files:
  [OK] Claude Skill Definition                                SKILL.md
  [OK] Claude Instructions                                    .instructions.md
  [OK] Main Configuration                                     config.yaml
  [OK] Dependencies                                           requirements.txt

[2/5] Source Modules:
  [OK] Centralized Config Loader                              src/config.py
  [OK] Claude Skill Entry Point                               src/claude_skill.py
  [OK] Exa Search Engine                                      src/search/exa_searcher.py
  [OK] Investment Researcher                                  src/core/researcher.py
  [OK] Valuation Methods (10+)                                src/core/valuation.py
  [OK] Data Freshness Checker                                 src/core/freshness.py
  [OK] Data Validator & Cross-Validation                      src/core/validator.py
  [OK] MCP Server (14 tools)                                  src/server/mcp_server.py
  [OK] Unified Skill Router                                   src/server/skill_router.py
  [OK] Report Exporter (MD + PDF)                             src/export/exporter.py

[3/5] Configuration:
  [OK] config.yaml found

[4/5] Python Imports:
  [OK] All Python modules import successfully

[5/5] API Key:
  [OK] API Key configured: abc1234567...

======================================================================
  ALL CHECKS PASSED - Ready to use!
======================================================================
```

---

## Project Structure / 项目结构 (v0.3.0)

```
d:\MCP project\EXA search MCP\
|-- config.yaml                   # Main config (THE file non-coders edit)
|-- .env                          # API keys (alternative to config.yaml)
|-- requirements.txt              # Python dependencies
|-- check_integration.py          # Integration checker
|-- SKILL.md                      # Claude Skill definition
|-- .instructions.md              # Claude custom instructions
|-- setup.py                      # Package metadata
|
|-- src/
|   |-- __init__.py
|   |-- config.py                 # Centralized config loader
|   |-- claude_skill.py           # CLI entry point
|   |
|   |-- search/
|   |   |-- __init__.py
|   |   +-- exa_searcher.py       # StockSearcher (retry, source tiers)
|   |
|   |-- core/
|   |   |-- __init__.py
|   |   |-- researcher.py         # InvestmentResearcher (mature/growth/web3)
|   |   |-- valuation.py          # ValuationMethods (10+ methods)
|   |   |-- freshness.py          # DataFreshnessChecker (20 categories)
|   |   +-- validator.py          # DataValidator (cross-validation, scoring)
|   |
|   |-- server/
|   |   |-- __init__.py
|   |   |-- mcp_server.py         # ExaMCPServer (14 MCP tools)
|   |   +-- skill_router.py       # UnifiedSkillRouter
|   |
|   |-- export/
|   |   |-- __init__.py
|   |   |-- exporter.py           # ReportExporter (Markdown + PDF)
|   |   +-- naming.py             # ReportNaming (templated filenames)
|   |
|   +-- examples/                 # Example scripts
|
|-- research Output/
|   |-- markdown/                 # Exported .md reports
|   |-- pdf/                      # Exported .pdf reports
|   +-- templates/                # Report skeleton templates
|
+-- docs/                         # Documentation
```

---

## Quick Functional Test / 快速功能测试

### Test 1: CLI search / 命令行搜索

```bash
python src/claude_skill.py "Apple stock news"
```

Expected: formatted search results with source tier labels.

### Test 2: JSON output / JSON 输出

```bash
python src/claude_skill.py "Tesla analysis" --json
```

Expected: JSON-formatted search results.

### Test 3: Research report skeleton / 投研报告骨架

```bash
python src/claude_skill.py "Report for AAPL" --research
```

Expected: a report skeleton with `{{PLACEHOLDER}}` fields and prioritized search queries.

---

## Update Dependencies / 更新依赖

```bash
pip install --upgrade -r requirements.txt
```

Check for outdated packages:

```bash
pip list --outdated
```

---

## Common Deployment Issues / 常见部署问题

### Issue: API key not found

```
ValueError: API key 'exa' not found.
```

Solution: set the key in `config.yaml` under `api_keys.exa`, or in `.env` as `EXA_API_KEY=...`.
解决: 在 `config.yaml` 的 `api_keys.exa` 或 `.env` 的 `EXA_API_KEY` 中填入密钥。

### Issue: Dependency install failure

```
ERROR: Could not find a version that satisfies the requirement
```

Solution:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: PDF export produces plain text

This means neither Chromium nor fitz rendered successfully. Install the optional
Chromium engine:

```bash
pip install playwright
playwright install chromium
```

Or verify pymupdf is installed: `pip install pymupdf`.

### Issue: PowerShell execution policy (Windows)

```
.\venv\Scripts\Activate.ps1 : cannot be loaded because running scripts is disabled
```

Solution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Related Docs / 相关文档

- [Quick Start / 快速开始](01-QUICKSTART.md)
- [Usage Guide / 使用指南](02-USAGE.md)
- [Integration / 集成指南](03-INTEGRATION.md)
- [API Reference / API 参考](05-API-REFERENCE.md)
- [Troubleshooting / 故障排查](06-TROUBLESHOOTING.md)
- [Project Structure / 项目结构](07-PROJECT-STRUCTURE.md)
