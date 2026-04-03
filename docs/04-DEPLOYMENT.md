# 🚀 部署和设置指南

完整的环境搭建、配置和验证流程。

---

## 📋 部署检查清单

### 前置条件 ✓
- [ ] Python 3.13+ 已安装
- [ ] VS Code 已安装 Copilot Chat
- [ ] Exa API Key 已获取

---

## ⚙️ 第1步：环境设置

### 方法A：自动设置脚本（推荐）

```powershell
# 运行完整设置脚本
.\scripts\setup_env.ps1
```

**脚本会自动**:
1. 创建虚拟环境 (venv)
2. 激活虚拟环境
3. 安装所有依赖
4. 验证安装

---

### 方法B：手动设置

#### 1. 创建虚拟环境
```powershell
python -m venv venv
```

#### 2. 激活虚拟环境
```powershell
.\venv\Scripts\Activate.ps1
```

#### 3. 安装依赖
```powershell
pip install -r requirements.txt
```

---

## 🔑 第2步：配置API密钥

### 获取Exa API Key

1. 访问 https://dashboard.exa.ai/api-keys
2. 登录或创建账户
3. 复制 API Key

### 设置.env文件

#### 1. 复制示例文件
```powershell
cp .env.example .env
```

#### 2. 编辑 .env
```env
EXA_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here（可选）
ANTHROPIC_API_KEY=your_anthropic_key_here（可选）
```

#### 3. 保存文件

---

## ✅ 第3步：验证安装

### 运行集成检查

```powershell
# 激活虚拟环境（如未激活）
.\venv\Scripts\Activate.ps1

# 运行检查
python check_integration.py
```

**期望输出**:
```
✅ SKILL.md exists
✅ .instructions.md exists
✅ Core modules import successfully
✅ API Key configured
✅ All dependencies installed
✅ All checks passed!
```

---

### 运行演示程序

```powershell
# 基本搜索示例
python -m src.examples.basic_search

# Claude Skill演示
python -m src.examples.claude_skill_demo

# OpenAI集成示例
python -m src.examples.openai_function_calling

# Anthropic集成示例
python -m src.examples.anthropic_tool_use
```

---

## 📦 依赖项说明

### 必需依赖

| 包 | 版本 | 用途 |
|-----|------|-----|
| exa-py | 2.10.2 | Exa API 客户端 |
| anthropic | 0.88.0 | Claude API |
| openai | 2.30.0 | OpenAI API |
| python-dotenv | 1.2.2 | 环境变量管理 |
| requests | 2.31.0 | HTTP 请求 |

### 验证依赖

```powershell
pip list
```

---

## 🔧 配置文件详解

### config/exa_config.json

```json
{
  "api_base": "https://api.exa.ai",
  "search_type": "auto",
  "num_results": 10,
  "highlights": true,
  "max_highlight_length": 4000,
  "timeout": 30
}
```

**说明**:
- `search_type: "auto"` - 平衡速度和相关性
- `num_results: 10` - 默认返回10条结果
- `highlights: true` - 包含内容摘要
- `max_highlight_length: 4000` - 摘要最大字符数

---

### config/mcp_config.json

```json
{
  "server_name": "exa-search-mcp",
  "version": "1.0.0",
  "capabilities": [
    "search_stock",
    "search_market_analysis",
    "search_company_info",
    "search_deep_research"
  ]
}
```

---

## 📁 项目结构验证

```
d:\MCP project\EXA search MCP\
├── src/
│   ├── stock_searcher.py          ✓
│   ├── skill_router.py             ✓
│   ├── claude_skill.py             ✓
│   ├── mcp_server.py               ✓
│   └── examples/
│       ├── basic_search.py         ✓
│       ├── stock_search.py         ✓
│       ├── claude_skill_demo.py    ✓
│       ├── openai_function_calling.py
│       └── anthropic_tool_use.py
├── config/
│   ├── exa_config.json             ✓
│   └── mcp_config.json             ✓
├── scripts/
│   ├── setup_env.ps1               ✓
│   └── install_dependencies.ps1    ✓
├── .env                            ✓ (API Key配置)
├── .env.example                    ✓
├── SKILL.md                        ✓
├── .instructions.md                ✓
├── requirements.txt                ✓
├── check_integration.py            ✓
└── README.md                       ✓
```

---

## 🧪 功能测试

### 测试1：基础搜索

```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Apple stock news"
```

**预期**: 返回5条Apple相关的新闻结果

---

### 测试2：JSON输出

```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Tesla analysis" --json
```

**预期**: 返回JSON格式的结果

---

### 测试3：Claude Chat集成

1. 在VS Code中按 `Ctrl + L`
2. 输入 "Apple latest news"
3. Claude自动调用搜索

**预期**: Claude返回搜索结果

---

## 🔄 更新和维护

### 更新依赖

```powershell
pip install --upgrade -r requirements.txt
```

### 检查过时包

```powershell
pip list --outdated
```

---

## 🆘 常见部署问题

### 问题1：Python不在PATH中
```
错误: 'python' is not recognized as an internal or external command
```

**解决方案**: 
1. 重新安装Python，勾选"Add Python to PATH"
2. 使用完整路径: `C:\Python313\python.exe`

---

### 问题2：虚拟环境激活失败
```
错误: PowerShell execution policy
```

**解决方案**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

### 问题3：依赖安装失败
```
错误: Could not find a version that satisfies the requirement
```

**解决方案**:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 问题4：API Key无效
```
错误: EXA_API_KEY not configured
```

**解决方案**:
1. 检查 `.env` 文件
2. 确认API Key正确复制
3. 重启终端

---

## 📊 部署验证报告

运行全面检查:

```powershell
# 生成验证报告
python check_integration.py > deployment_report.txt
```

---

## ✨ 部署完成

当所有检查都通过时 ✅

```
✅ 环境配置完成
✅ 依赖安装完成
✅ API配置完成
✅ 功能验证完成
✅ Claude集成完成

系统准备就绪！
```

---

## 🚀 开始使用

```powershell
# 1. 打开VS Code
code .

# 2. 按 Ctrl + L 打开Claude Chat

# 3. 输入查询
"Apple latest news"

# 4. 享受实时搜索！
```

---

## 📚 相关文档

- [快速开始](01-QUICKSTART.md)
- [完整使用](02-USAGE.md)
- [Claude集成](03-INTEGRATION.md)
- [故障排查](06-TROUBLESHOOTING.md)
- [项目结构](07-PROJECT-STRUCTURE.md)
