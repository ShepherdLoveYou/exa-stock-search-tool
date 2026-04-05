# Troubleshooting Guide / 故障排查指南

Common issues and solutions for the Crisis Investment Researcher v0.3.0.

常见问题的解决方案，适用于 Crisis Investment Researcher v0.3.0。

---

## Table of Contents / 目录

1. [Error: UnicodeEncodeError / 编码错误](#error-1-unicodeencodeerror)
2. [Error: API Key Not Found / API Key 未找到](#error-2-api-key-not-found)
3. [Error: Module Not Found / 模块导入失败](#error-3-module-not-found)
4. [Error: Python Not in PATH / Python 不在 PATH 中](#error-4-python-not-in-path)
5. [Error: Virtual Environment Activation Failed / 虚拟环境激活失败](#error-5-virtual-environment-activation-failed)
6. [Error: Exa API Unauthorized / Exa API 授权失败](#error-6-exa-api-unauthorized)
7. [Error: config.yaml Parsing Error / config.yaml 解析错误](#error-7-configyaml-parsing-error)
8. [Error: PyYAML Not Installed / PyYAML 未安装](#error-8-pyyaml-not-installed)
9. [Error: Chromium/Playwright Not Installed for PDF / PDF 导出缺少 Chromium](#error-9-chromiumplaywright-not-installed)
10. [Error: Data Validation Warnings / 数据验证警告](#error-10-data-validation-warnings)
11. [FAQ / 常见问题](#faq)
12. [Debugging Tips / 调试技巧](#debugging-tips)
13. [Diagnostic Tools / 诊断工具](#diagnostic-tools)
14. [Full Troubleshooting Workflow / 完整故障排查流程](#full-troubleshooting-workflow)

---

## Error 1: UnicodeEncodeError

### Symptom / 现象

```
UnicodeEncodeError: 'gbk' codec can't encode character '\u274c'
```

### Cause / 原因

Windows PowerShell uses GBK encoding by default, which does not support all UTF-8 characters.

Windows PowerShell 默认编码为 GBK，不支持所有 UTF-8 字符。

### Solution / 解决方案

```powershell
# Set environment variable / 设置环境变量
$env:PYTHONIOENCODING="utf-8"

# Then run the command / 然后运行命令
.\venv\Scripts\python.exe src/claude_skill.py "query"
```

**Permanent fix / 持久化方案:**

Add the following line to your PowerShell profile:

在 PowerShell 配置文件中添加：

```powershell
$env:PYTHONIOENCODING="utf-8"
```

---

## Error 2: API Key Not Found

### Symptom / 现象

```
ValueError: EXA_API_KEY not found
```

### Cause / 原因

No API key is configured. The system checks in this order: environment variables / `.env` file, then `config.yaml`.

未配置 API Key。系统按以下优先级查找：环境变量 / `.env` 文件，然后 `config.yaml`。

### Solution / 解决方案

**Option A: Use config.yaml (recommended / 推荐)**

Edit `config.yaml` in the project root:

编辑项目根目录的 `config.yaml`：

```yaml
api_keys:
  exa: "your-actual-api-key-here"
```

**Option B: Use .env file**

1. Check if `.env` exists / 检查 `.env` 文件是否存在
```powershell
Test-Path .env
```

2. If it does not exist, copy from example / 如果不存在，复制模板
```powershell
cp .env.example .env
```

3. Edit `.env` and add your key / 编辑 `.env` 并添加 API Key
```
EXA_API_KEY=your-actual-api-key-here
```

4. Restart your terminal / 重启终端

**Configuration priority / 配置优先级:**
- Environment variables / `.env`  (highest / 最高)
- `config.yaml`  (middle / 中)
- Built-in defaults (lowest / 最低)

See `src/config.py` for the full loading logic.

---

## Error 3: Module Not Found

### Symptom / 现象

```
ModuleNotFoundError: No module named 'exa_py'
```

or / 或者

```
ModuleNotFoundError: No module named 'yaml'
```

### Cause / 原因

Dependencies are not installed, or the virtual environment is not activated.

依赖未安装，或虚拟环境未激活。

### Solution / 解决方案

1. Activate the virtual environment / 确认虚拟环境已激活
```powershell
# Check if prompt shows (venv). If not:
# 检查提示符是否显示 (venv)，如果没有：
.\venv\Scripts\Activate.ps1
```

2. Reinstall dependencies / 重新安装依赖
```powershell
pip install -r requirements.txt
```

3. Verify installation / 验证安装
```powershell
pip list | findstr exa_py
pip list | findstr PyYAML
```

---

## Error 4: Python Not in PATH

### Symptom / 现象

```
'python' is not recognized as an internal or external command
```

### Cause / 原因

Python is not added to the system PATH.

Python 未添加到系统 PATH。

### Solution / 解决方案

1. Use the full path directly / 使用完整路径
```powershell
C:\Users\YourUser\AppData\Local\Programs\Python\Python313\python.exe src/claude_skill.py "query"
```

2. Or reinstall Python / 或者重新安装 Python
   - Download from https://www.python.org/
   - Check "Add Python to PATH" during installation / 安装时勾选 "Add Python to PATH"
   - Restart VS Code and PowerShell / 重启 VS Code 和 PowerShell

---

## Error 5: Virtual Environment Activation Failed

### Symptom / 现象

```
PowerShell execution policies do not allow scripts to run
```

### Cause / 原因

PowerShell execution policy restricts script execution.

PowerShell 执行策略限制了脚本执行。

### Solution / 解决方案

```powershell
# Allow current user to run scripts / 允许当前用户运行脚本
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate virtual environment / 然后激活虚拟环境
.\venv\Scripts\Activate.ps1
```

---

## Error 6: Exa API Unauthorized

### Symptom / 现象

```
exa_py.APIError: Unauthorized
```

### Cause / 原因

The API key is invalid or expired.

API Key 无效或已过期。

### Solution / 解决方案

1. Verify the API key was copied correctly / 检查 API Key 是否正确复制
2. Visit https://dashboard.exa.ai/api-keys to generate a new key / 访问 https://dashboard.exa.ai/api-keys 生成新 Key
3. Update the key in `config.yaml` or `.env` / 更新 `config.yaml` 或 `.env` 中的 Key
4. Restart terminal / 重启终端

---

## Error 7: config.yaml Parsing Error

### Symptom / 现象

```
yaml.scanner.ScannerError: while scanning a simple key
```

or / 或者

```
yaml.parser.ParserError: expected <block end>, but found ...
```

### Cause / 原因

The `config.yaml` file contains syntax errors such as incorrect indentation, tabs instead of spaces, or malformed values.

`config.yaml` 文件存在语法错误，如缩进不正确、使用了 Tab 而非空格、或值格式错误。

### Solution / 解决方案

1. **Check indentation** -- YAML requires consistent spaces (not tabs).

   **检查缩进** -- YAML 要求统一使用空格（不能用 Tab）。

2. **Validate your YAML** -- Use an online YAML validator or run:

   **验证 YAML 格式** -- 使用在线 YAML 验证器或运行：
```python
import yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    yaml.safe_load(f)
```

3. **Common mistakes / 常见错误:**

```yaml
# WRONG: tab indentation / 错误：Tab 缩进
api_keys:
	exa: "key"

# CORRECT: 2-space indentation / 正确：2 空格缩进
api_keys:
  exa: "key"

# WRONG: unquoted special characters / 错误：未引用的特殊字符
api_keys:
  exa: key-with-#-symbol

# CORRECT: quoted string / 正确：引号包裹
api_keys:
  exa: "key-with-#-symbol"
```

4. **If the file is damaged**, delete it and recreate from the template structure shown in the project README. The system will fall back to built-in defaults when `config.yaml` is missing.

   **如果文件已损坏**，删除后参考项目 README 中的模板重新创建。当 `config.yaml` 缺失时，系统将使用内置默认值。

Note: `src/config.py` includes a minimal fallback YAML parser (`_parse_yaml_minimal`) that handles simple structures when PyYAML is not installed. However, for full nested config support, PyYAML is recommended.

注意：`src/config.py` 内置了一个极简 YAML 解析器 (`_parse_yaml_minimal`)，在 PyYAML 未安装时可处理简单结构。但为了完整支持嵌套配置，建议安装 PyYAML。

---

## Error 8: PyYAML Not Installed

### Symptom / 现象

```
ImportError: No module named 'yaml'
```

Or the config loader silently falls back to the minimal parser, causing nested config values (like `source_tiers` or `freshness_thresholds`) to be ignored.

或者配置加载器静默回退到极简解析器，导致嵌套配置项（如 `source_tiers` 或 `freshness_thresholds`）被忽略。

### Cause / 原因

`pyyaml` is listed in `requirements.txt` but was not installed.

`pyyaml` 在 `requirements.txt` 中列出但未被安装。

### Solution / 解决方案

```powershell
pip install pyyaml>=6.0
```

Or reinstall all dependencies / 或重新安装所有依赖：

```powershell
pip install -r requirements.txt
```

**Verify / 验证:**

```python
import yaml
print(yaml.__version__)
```

---

## Error 9: Chromium/Playwright Not Installed

### Symptom / 现象

When exporting a PDF report, you see:

导出 PDF 报告时，出现：

```
RuntimeError: PDF export failed: chromium not available
```

or / 或者

```
FileNotFoundError: playwright or chromium binary not found
```

### Cause / 原因

The PDF exporter (`src/export/exporter.py`) tries rendering engines in the order specified by `config.yaml` under `export.pdf_engines`. The default order is:

PDF 导出器 (`src/export/exporter.py`) 按 `config.yaml` 中 `export.pdf_engines` 指定的顺序尝试渲染引擎。默认顺序为：

1. `chromium` -- Best quality, requires Playwright / 最佳质量，需要 Playwright
2. `fitz` -- Good quality via PyMuPDF / 较好质量，通过 PyMuPDF
3. `text` -- Plain text fallback, always available / 纯文本备选，始终可用

If `chromium` is the first engine and Playwright is not installed, the error occurs.

如果 `chromium` 排在第一位而 Playwright 未安装，则会出错。

### Solution / 解决方案

**Option A: Install Playwright + Chromium (best quality / 最佳质量)**

```powershell
pip install playwright
playwright install chromium
```

**Option B: Use PyMuPDF instead / 使用 PyMuPDF 替代**

```powershell
pip install pymupdf>=1.23.0
```

Then edit `config.yaml` to change the engine priority:

然后编辑 `config.yaml` 将引擎优先级调整为：

```yaml
export:
  pdf_engines:
    - "fitz"
    - "text"
```

**Option C: Use text-only fallback / 仅使用纯文本备选**

```yaml
export:
  pdf_engines:
    - "text"
```

Note: Markdown reports are always exported successfully regardless of PDF engine availability. You can find exported Markdown files in `research Output/markdown/`.

注意：无论 PDF 引擎是否可用，Markdown 报告始终可以成功导出。导出的 Markdown 文件位于 `research Output/markdown/`。

---

## Error 10: Data Validation Warnings

### Symptom / 现象

The research output includes warnings such as:

研究输出中包含如下警告：

```
[WARNING] Data point "Revenue" has low confidence (1 source, Tier 3)
[WARNING] Stale data detected: "stock_price" is 5 days old (threshold: 1 day)
[WARNING] Cross-validation failed: values differ by >10% across sources
```

### Cause / 原因

The `DataValidator` (`src/core/validator.py`) and `DataFreshnessChecker` (`src/core/freshness.py`) enforce data quality standards configured in `config.yaml` under the `validation` section. Warnings are generated when:

`DataValidator` (`src/core/validator.py`) 和 `DataFreshnessChecker` (`src/core/freshness.py`) 根据 `config.yaml` 的 `validation` 配置段执行数据质量检查。出现警告的原因包括：

- A data point has fewer sources than `min_cross_validation_sources` (default: 2).
- The data source is low-tier (Tier 3 or Tier 4).
- Values from different sources diverge beyond the acceptable threshold.
- Data age exceeds the `freshness_thresholds` for its category.

- 数据点的来源数量低于 `min_cross_validation_sources`（默认：2）。
- 数据来源为低等级（Tier 3 或 Tier 4）。
- 不同来源的数值差异超过可接受范围。
- 数据年龄超过其类别的 `freshness_thresholds`。

### Solution / 解决方案

**These warnings are informational and designed to protect research quality.** They do not block execution unless `block_export_on_high_risk` is set to `true` in `config.yaml`.

**这些警告是信息性的，旨在保护研究质量。** 除非 `config.yaml` 中 `block_export_on_high_risk` 设为 `true`，否则不会阻止执行。

1. **To adjust thresholds / 调整阈值:**

Edit `config.yaml`:

```yaml
validation:
  min_cross_validation_sources: 1   # Relax to 1 source / 放宽到 1 个来源
  auto_flag_stale_data: false       # Disable stale warnings / 关闭过期警告
```

2. **To adjust freshness thresholds for specific categories / 调整特定类别的新鲜度阈值:**

```yaml
validation:
  freshness_thresholds:
    stock_price: 3       # Allow 3 days / 允许 3 天
    news_sentiment: 7    # Allow 7 days / 允许 7 天
```

3. **To customize source tiers / 自定义来源分级:**

Add trusted domains to higher tiers in `config.yaml`:

在 `config.yaml` 中将信任的域名添加到更高等级：

```yaml
source_tiers:
  tier2:
    - "your-trusted-source.com"
```

4. **To allow export despite warnings / 即使有警告也允许导出:**

```yaml
validation:
  block_export_on_high_risk: false
```

---

## FAQ

### Q1: Claude cannot retrieve search results / Claude 无法获得搜索结果

**Symptom / 症状:** Claude Chat returns no search results after a query.

**Checklist / 检查清单:**
- SKILL.md file exists and is valid / SKILL.md 文件存在且有效
- .instructions.md file exists / .instructions.md 文件存在
- Claude Chat is opened from the sidebar / Claude Chat 已从侧栏打开
- API key is configured (in `config.yaml` or `.env`) / API Key 已配置
- Dependencies are installed / 依赖已安装

**Steps / 解决步骤:**
```powershell
# 1. Verify integration / 验证集成
python check_integration.py

# 2. Test command line / 测试命令行
.\venv\Scripts\python.exe src/claude_skill.py "test query"

# 3. Restart Claude Chat
# Ctrl + Shift + L or close and reopen / 关闭并重新打开
```

---

### Q2: Search results are inaccurate / 搜索结果不准确

**Symptom / 症状:** Results are not relevant to the query.

**Cause / 原因:** The query is too vague or the `UnifiedSkillRouter` (`src/server/skill_router.py`) cannot determine the correct route.

查询表述不清，或 `UnifiedSkillRouter` (`src/server/skill_router.py`) 无法判断正确的路由。

**Improvements / 改进方案:**
```
BAD:    "Apple"
BETTER: "Apple stock news"

BAD:    "STOCK"
BETTER: "Tesla latest stock news"

BAD:    "market"
BETTER: "AI semiconductor market analysis"
```

---

### Q3: Slow response time / 响应速度很慢

**Symptom / 症状:** Search takes more than 5 seconds.

**Checks / 检查:**
1. Network connection is working / 网络连接是否正常
2. Exa API is responsive (typically <1 second) / Exa API 是否响应
3. `config.yaml` retry settings are reasonable / `config.yaml` 重试设置是否合理

**Optimization / 优化:**
```powershell
# Reduce number of results / 减少结果数量
.\venv\Scripts\python.exe src/claude_skill.py "query" --results 3
```

Check `config.yaml` network settings:

检查 `config.yaml` 网络设置：
```yaml
network:
  timeout: 30       # Reduce if needed / 按需降低
  max_retries: 3    # Reduce retries / 减少重试
  retry_delay: 1.0  # Reduce delay / 减少延迟
```

---

### Q4: Claude does not recognize the Skill / Claude 不识别 Skill

**Symptom / 症状:** Claude Chat does not show search suggestions.

**Diagnosis / 排查:**
```powershell
# Check SKILL.md
Test-Path SKILL.md

# Check .instructions.md
Test-Path .instructions.md

# View file contents
Get-Content SKILL.md | Select-Object -First 10
```

**Fix / 解决:**
```powershell
# Restart VS Code
# Ctrl + Shift + P -> Reload Window
```

---

### Q5: Certain queries cannot be routed / 某些查询无法路由

**Symptom / 症状:** The query is classified as "unknown" by the `UnifiedSkillRouter`.

查询被 `UnifiedSkillRouter` 识别为 "unknown" 类型。

**Example / 例子:**
```
Query:  "stock"
Result: search_type="unknown", confidence=0%
```

**Cause / 分析:**
- Query is too brief / 查询过于简洁
- Not enough context keywords / 缺少足够的上下文关键词

**Improvement / 改进:**
```
BAD:    "stock"
BETTER: "stock market news"

BAD:    "crypto"
BETTER: "cryptocurrency market analysis"

BAD:    "report"
BETTER: "Generate report for AAPL mature company"
```

---

## Debugging Tips / 调试技巧

### Enable verbose output / 启用详细输出

```python
from src.server.skill_router import UnifiedSkillRouter

router = UnifiedSkillRouter()

# Route a query and inspect the result
# 路由查询并检查结果
result = router.route("your query")
print(f"Action: {result.get('action')}")
print(f"Result: {result}")
```

---

### Test individual components / 测试单个组件

```python
# Test StockSearcher / 测试 StockSearcher
from src.search.exa_searcher import StockSearcher
searcher = StockSearcher()
result = searcher.search_stock_news("AAPL", num_results=3)
print(result)

# Test UnifiedSkillRouter / 测试 UnifiedSkillRouter
from src.server.skill_router import UnifiedSkillRouter
router = UnifiedSkillRouter()
result = router.search_and_format("Apple news")
print(result)

# Test InvestmentResearcher / 测试 InvestmentResearcher
from src.core.researcher import InvestmentResearcher
researcher = InvestmentResearcher(searcher)
framework = researcher.detect_framework("AAPL")
print(f"Framework: {framework}")

# Test DataValidator / 测试 DataValidator
from src.core.validator import DataValidator
validator = DataValidator()
print(f"Tier domains loaded: {bool(validator._tier_domains)}")

# Test DataFreshnessChecker / 测试 DataFreshnessChecker
from src.core.freshness import DataFreshnessChecker
checker = DataFreshnessChecker()
print(f"Reference date: {checker.reference_date}")

# Test ValuationMethods / 测试 ValuationMethods
from src.core.valuation import ValuationMethods
dcf_result = ValuationMethods.dcf(fcf_current=100, growth_rate=0.10)
print(f"DCF value: {dcf_result['total_enterprise_value']}")

# Test ReportExporter / 测试 ReportExporter
from src.export.exporter import ReportExporter
exporter = ReportExporter()
print(f"Markdown dir: {exporter.md_dir}")
print(f"PDF dir: {exporter.pdf_dir}")

# Test config loader / 测试配置加载
from src.config import get_search_config, get_validation_config
print(f"Search config: {get_search_config()}")
print(f"Validation config: {get_validation_config()}")
```

---

### Save debug logs / 查看日志

```powershell
# Run command and save output to file / 运行命令并保存输出到文件
.\venv\Scripts\python.exe src/claude_skill.py "query" 2>&1 | Tee-Object -FilePath debug.log

# View log / 查看日志
Get-Content debug.log
```

---

## Diagnostic Tools / 诊断工具

### Integration check script / 集成检查脚本

```powershell
python check_integration.py
```

**Expected output / 预期输出:**
```
SKILL.md exists
.instructions.md exists
Core modules import successfully
API Key configured
All dependencies installed
All checks passed!
```

---

### Run examples / 运行示例

```powershell
# Basic search / 基础搜索
python -m src.examples.basic_search

# Full demo / 完整演示
python -m src.examples.claude_skill_demo

# OpenAI demo
python -m src.examples.openai_function_calling

# Anthropic demo
python -m src.examples.anthropic_tool_use
```

---

## Full Troubleshooting Workflow / 完整故障排查流程

### Step 1: Verify environment / 验证环境

```powershell
# Check Python / 检查 Python
python --version

# Check virtual environment / 检查虚拟环境
.\venv\Scripts\python.exe --version

# Check integration / 检查集成
python check_integration.py
```

### Step 2: Verify configuration / 验证配置

```powershell
# Check config.yaml exists and is valid / 检查 config.yaml 是否存在且有效
.\venv\Scripts\python.exe -c "from src.config import get_search_config; print(get_search_config())"

# Check API key is loaded / 检查 API Key 是否加载
.\venv\Scripts\python.exe -c "from src.config import get_api_key; print('OK:', get_api_key('exa')[:8] + '...')"
```

### Step 3: Test command line / 测试命令行

```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Apple news" --results 3
```

### Step 4: Test Claude Chat / 测试 Claude Chat

```
Open VS Code / 打开 VS Code
Press Ctrl + L
Type: "Apple latest news"
Check if results are returned / 查看是否返回结果
```

### Step 5: Review logs / 查看日志

```powershell
$env:PYTHONIOENCODING="utf-8"
.\venv\Scripts\python.exe src/claude_skill.py "test" > output.log 2>&1
Get-Content output.log
```

---

## Getting Help / 获取帮助

If none of the solutions above resolve the issue:

如果以上解决方案都不能解决问题：

1. **Check all configuration files / 检查所有配置文件**
   - `config.yaml` -- Main configuration / 主配置
   - `.env` -- API keys (alternative) / API 密钥（备选）
   - `config/exa_config.json` -- Exa-specific config / Exa 专属配置
   - `config/mcp_config.json` -- MCP config / MCP 配置

2. **Run full diagnostics / 运行完整诊断**
   ```powershell
   python check_integration.py
   python -m src.examples.claude_skill_demo
   ```

3. **Inspect error stack trace / 查看错误堆栈**
   ```powershell
   .\venv\Scripts\python.exe -u src/claude_skill.py "query" 2>&1
   ```

4. **Consult documentation / 参考文档**
   - [Quick Start / 快速开始](01-QUICKSTART.md)
   - [Deployment / 部署指南](04-DEPLOYMENT.md)
   - [API Reference / API 参考](05-API-REFERENCE.md)

---

## Quick Solution Summary / 常见解决方案总结

| Problem / 问题 | Quick Fix / 快速解决 |
|---|---|
| Encoding error / 编码错误 | `$env:PYTHONIOENCODING="utf-8"` |
| API Key not found / API Key 未找到 | Edit `config.yaml` or `.env` |
| Module not found / 模块未找到 | `pip install -r requirements.txt` |
| Venv activation failed / 虚拟环境失败 | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Claude returns nothing / Claude 无结果 | `python check_integration.py` |
| config.yaml error / 配置解析错误 | Check indentation (spaces, not tabs) / 检查缩进 |
| PyYAML missing / PyYAML 缺失 | `pip install pyyaml>=6.0` |
| PDF export failed / PDF 导出失败 | `pip install playwright && playwright install chromium` |
| Data validation warnings / 数据验证警告 | Adjust thresholds in `config.yaml` / 在 config.yaml 中调整阈值 |

---

## Related Documentation / 相关文档

- [Quick Start / 快速开始](01-QUICKSTART.md)
- [Usage / 完整使用](02-USAGE.md)
- [Claude Integration / Claude 集成](03-INTEGRATION.md)
- [Deployment / 部署指南](04-DEPLOYMENT.md)
- [API Reference / API 参考](05-API-REFERENCE.md)
- [Project Structure / 项目结构](07-PROJECT-STRUCTURE.md)
