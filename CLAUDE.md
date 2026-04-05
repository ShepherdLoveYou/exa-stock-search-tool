# CLAUDE.md — 项目规则与记忆

> Claude 在每次任务前自动读取此文件。所有规则具有最高优先级。

---

## 语言规则

- **思考/推理**: 英文
- **输出文件、投研报告、用户可见内容**: 中文
- **代码/变量名/类名/函数名**: 英文（保持代码库一致性）
- **来源标注格式**: `[来源: XX | 日期: YYYY-MM-DD]`

---

## 投研助手行为规则

- 在报告第一行输出唯一 UUID
- 不使用表情符号
- 不使用"不过但是"等转折过渡词
- 不道歉、不免责声明、不奉承
- 基于互联网上的各种事实回答，先验证再回复
- 不编造内容
- 偏好批判性、深入的、结构化的回答
- 关键信息加粗，所有信息以 Markdown 格式处理和输出
- **职责**: 根据投研方法论分析并撰写投研报告，或对已有报告进行数据审查和信息时效性检查
- **工作方式**: 作为报告"填空"助手，针对不同标的使用不同投研方法
- **方法论参考**: `research Method/` 目录下的 PDF 和 MD 文档
  - 成熟公司危机投资投研方法
  - 成长性公司危机投资投研方法
  - Web3项目危机投资投研方法
  - 危机投资模型概念

---

## 项目概览

- **项目名**: Crisis Investment Researcher（危机投资研究器）
- **版本**: 0.3.0
- **用途**: 基于 Exa 搜索 API 的实时金融投研系统，与 Claude 深度集成
- **三大投研框架**: 成熟公司 / 成长性公司 / Web3项目
- **Python**: >= 3.9

---

## 项目结构

```
config.yaml              ← 唯一需要编辑的配置文件（中英文注释）
.env                     ← API 密钥备选方案

src/
  config.py              ← 统一配置加载器（优先级: 环境变量 > config.yaml > 默认值）
  claude_skill.py        ← CLI 入口

  search/
    exa_searcher.py      ← StockSearcher: Exa 搜索（含重试、来源分级）

  core/
    researcher.py        ← InvestmentResearcher: 三种投研框架、报告骨架、研究查询
    valuation.py         ← ValuationMethods: 10+ 估值方法（DCF/Graham/PE/PB/PS/EV-EBITDA/PEG/DDM等）
    freshness.py         ← DataFreshnessChecker: 20类数据时效性检查、来源审计
    validator.py         ← DataValidator: 交叉验证、来源评分、可信度评估

  server/
    mcp_server.py        ← ExaMCPServer: 14个MCP工具
    skill_router.py      ← UnifiedSkillRouter: 自然语言意图路由

  export/
    exporter.py          ← ReportExporter: Markdown + PDF 双格式导出（Chromium/fitz/文本）
    naming.py            ← ReportNaming: 文件命名规则

  utils/helpers.py       ← 工具函数
  examples/              ← 示例代码
  _deprecated/           ← 旧版本代码（仅供参考）

config/
  exa_config.json        ← Exa API 配置
  mcp_config.json        ← MCP 服务器配置

research Output/
  markdown/              ← 导出的 Markdown 报告
  pdf/                   ← 导出的 PDF 报告
  templates/             ← 报告模板（mature/growth/web3）

docs/                    ← 文档（01-07）
```

---

## 数据可信度铁律（最高优先级）

### 1. 数据必须真实
- **绝对禁止**编造任何财务数据（收入、利润、市值、PE、EPS、增长率等）
- 所有数字必须来自 Exa 搜索结果或 API 返回的原始数据
- 如果数据不可得，标注 `⚠️ 数据缺失 — 需人工补充`，绝不用推测值填充

### 2. 数据必须最新（Up to Date）
- **股价/币价**: 必须是当天或最近交易日的数据，超过1天标注 `⚠️ 非实时价格`
- **财务报表**: 必须使用最新季度/年度数据，超过120天标注 `⚠️ 数据可能已过时`
- **新闻/情绪**: 超过3天标注过期
- 生成报告前**必须先搜索最新数据**，不可直接使用上次搜索的缓存结果
- 所有数据标注获取时间: `[来源: XX | 日期: YYYY-MM-DD]`

### 3. 数据必须交叉验证
- 关键财务数据从 **≥2个独立来源** 获取并交叉验证
- 单一来源标注 `[单源未交叉验证]`
- 来源之间数值偏差 >5% 时必须标记不一致并人工确认

### 4. 来源可信度分级
| 等级 | 描述 | 示例 |
|------|------|------|
| Tier 1 | 官方/监管（最可信） | SEC EDGAR, FRED, DeFiLlama, Etherscan |
| Tier 2 | 主流财经 | Bloomberg, Reuters, Yahoo Finance, Seeking Alpha |
| Tier 3 | 分析参考 | Investopedia, Zacks, TipRanks |
| Tier 4 | 需验证 | 社交媒体、论坛、非核实来源 |
| 禁止 | Claude 自身记忆 | 训练数据有截止日期，可能过时或不准确 |

### 5. 估值输入参数溯源
- 每种估值方法的每个输入参数必须标注数据来源
- 无法溯源的方法标注 `N/A — 输入数据不可得`
- 交叉验证只基于有可信数据支撑的方法

### 6. 导出前强制审计
- 导出 PDF/Markdown 前必须运行 `audit_report_citations`
- `hallucination_risk = "high"` 时**禁止导出**
- `hallucination_risk = "medium"` 时必须向用户提示风险

---

## 投研报告输出规范

### 报告语言
- 报告正文: **中文**
- 公司名/专有名词: 保留英文原名（如 Tempus AI, SEC EDGAR）
- 财务术语: 中文为主，括号内附英文（如 "营收（Revenue）"）

### 数据标注格式
```
财务数据:  数值 [来源: API名称/文件类型 | 日期: YYYY-MM-DD]
搜索数据:  内容 [来源: Exa搜索→原始出处 | 日期: YYYY-MM-DD]
计算数据:  结果 [计算公式 | 输入来源: XX]
缺失数据:  ⚠️ 数据缺失 — 原因说明，需人工补充
过期数据:  数值 [来源: XX | 日期: YYYY-MM-DD] ⚠️ 数据可能已过时(超过N天)
未验证:   数值 [来源: XX | 单源未交叉验证]
```

### 报告尾部必须附加
```
═══ 数据审计摘要 ═══
数据来源统计: Exa搜索 X条 | API数据 X条 | 用户提供 X条
交叉验证: X项已验证 | X项单源 | X项缺失
数据新鲜度: 最新数据日期 YYYY-MM-DD | 最旧数据日期 YYYY-MM-DD
幻觉风险提示: [列出任何可能不准确的数据点及原因]
数据可信度评级: 高/中/低（附理由）
```

---

## 关键类与导入路径

| 类名 | 路径 | 用途 |
|------|------|------|
| `StockSearcher` | `src.search.exa_searcher` | Exa 搜索（含重试） |
| `UnifiedSkillRouter` | `src.server.skill_router` | 自然语言路由 |
| `InvestmentResearcher` | `src.core.researcher` | 投研框架、报告生成 |
| `ValuationMethods` | `src.core.valuation` | 10+ 估值方法 |
| `DataFreshnessChecker` | `src.core.freshness` | 数据时效性检查 |
| `DataValidator` | `src.core.validator` | 交叉验证、可信度评分 |
| `ReportExporter` | `src.export.exporter` | MD + PDF 导出 |
| `ExaMCPServer` | `src.server.mcp_server` | MCP 服务器（14工具） |

**已废弃路径（不要使用）**:
- ~~`src.stock_searcher`~~ → 用 `src.search.exa_searcher`
- ~~`src.skill_router`~~ / ~~`ExaSkillRouter`~~ → 用 `src.server.skill_router` / `UnifiedSkillRouter`
- ~~`src.mcp_server`~~ → 用 `src.server.mcp_server`

---

## 配置优先级

```
环境变量 (.env / 系统环境) > config.yaml > 代码内默认值
```

所有模块通过 `src.config` 统一读取配置，不直接加载 `.env`。

---

## MCP 工具列表（14个）

1. `search_stock_news` — 按代码搜索股票新闻
2. `search_market_analysis` — 市场趋势分析
3. `search_company_info` — 公司研究
4. `deep_research` — 深度研究搜索
5. `generate_research_report` — 生成报告骨架（自动选框架）
6. `get_research_queries` — 优先搜索查询列表
7. `check_report_freshness` — 检查数据时效性
8. `check_unfilled_fields` — 查找未填字段
9. `calculate_valuation` — 运行估值方法
10. `get_position_sizing` — 建仓阶梯与区域
11. `get_do_not_invest_checklist` — 投资纪律清单
12. `audit_report_citations` — 来源审计（检测幻觉风险）
13. `export_report` — 导出 MD/PDF（含导出前审计）
14. `validate_data_point` — 交叉验证数据点

---

## 投研工作流

```
1. 搜索最新数据（Exa 实时搜索，确保数据 up to date）
2. 自动选择框架（成熟公司 / 成长性公司 / Web3）
3. 生成报告骨架（含所有待填字段）
4. 获取优先搜索查询列表
5. 逐字段搜索并填充（标注来源和日期）
6. 运行估值交叉验证（≥10种方法，每个输入溯源）
7. 检查数据时效性（标记过期数据）
8. 来源审计（检测幻觉风险）
9. 导出报告（仅在审计通过后）
```

---

## Git 规范

- 远程仓库: `https://github.com/ShepherdLoveYou/exa-stock-search-tool.git`
- 主分支: `main`
- `.env` 已在 `.gitignore` 中，不提交
- `config.yaml` 中的 API key 留空提交
