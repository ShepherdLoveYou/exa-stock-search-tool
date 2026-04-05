"""MCP Server — Exa Search + Investment Research + Dual Export"""

import json
from datetime import datetime
from typing import Dict, Optional

from src.config import get_api_key, get_validation_config
from src.search.exa_searcher import StockSearcher
from src.core.researcher import InvestmentResearcher
from src.core.valuation import ValuationMethods
from src.core.freshness import DataFreshnessChecker
from src.core.validator import DataValidator
from src.export.exporter import ReportExporter


class ExaMCPServer:
    """MCP Server for Exa Search + Investment Research + Report Export"""

    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or get_api_key("exa")
        self.searcher = StockSearcher(api_key)
        self.researcher = InvestmentResearcher(self.searcher)
        self.freshness_checker = DataFreshnessChecker()
        self.validator = DataValidator()
        self.exporter = ReportExporter()
        self._validation_config = get_validation_config()
        self.tools = self._setup_tools()

    def _setup_tools(self) -> list:
        return [
            {
                "name": "search_stock_news",
                "description": "Search for latest news about a specific stock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Stock ticker symbol"},
                        "num_results": {"type": "integer", "default": 10},
                    },
                    "required": ["ticker"],
                },
            },
            {
                "name": "search_market_analysis",
                "description": "Search for market analysis and trends",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Market topic"},
                        "num_results": {"type": "integer", "default": 10},
                    },
                    "required": ["topic"],
                },
            },
            {
                "name": "search_company_info",
                "description": "Search for company information and earnings",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "company_name": {"type": "string"},
                        "num_results": {"type": "integer", "default": 10},
                    },
                    "required": ["company_name"],
                },
            },
            {
                "name": "deep_research",
                "description": "Deep research search for thorough analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "num_results": {"type": "integer", "default": 10},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "generate_research_report",
                "description": "Generate a crisis investment research report skeleton (mature/growth/web3). Auto-detects framework.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target_name": {"type": "string", "description": "Company or project name"},
                        "ticker": {"type": "string", "description": "Stock ticker or token symbol"},
                        "market": {"type": "string", "default": ""},
                        "framework": {"type": "string", "enum": ["", "mature", "growth", "web3"], "default": ""},
                    },
                    "required": ["target_name", "ticker"],
                },
            },
            {
                "name": "get_research_queries",
                "description": "Get prioritized search queries to fill a research report",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target_name": {"type": "string"},
                        "ticker": {"type": "string"},
                        "framework": {"type": "string", "enum": ["mature", "growth", "web3"]},
                    },
                    "required": ["target_name", "ticker", "framework"],
                },
            },
            {
                "name": "check_report_freshness",
                "description": "Check data freshness of a research report — flags stale data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_content": {"type": "string"},
                    },
                    "required": ["report_content"],
                },
            },
            {
                "name": "check_unfilled_fields",
                "description": "Check which fields in a report still need data (critical/important/supplementary)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_content": {"type": "string"},
                    },
                    "required": ["report_content"],
                },
            },
            {
                "name": "calculate_valuation",
                "description": "Calculate intrinsic value using DCF, Graham, PE/PB/PS, EV/EBITDA, PEG, DDM, etc.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "method": {
                            "type": "string",
                            "enum": ["dcf", "graham", "pe", "pb", "ps", "ev_ebitda", "peg", "ddm",
                                     "owner_earnings", "replacement_cost", "cross_validate"],
                        },
                        "params": {"type": "object"},
                    },
                    "required": ["method", "params"],
                },
            },
            {
                "name": "get_position_sizing",
                "description": "Calculate position sizing and buy ladder based on intrinsic vs current price",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "intrinsic_value": {"type": "number"},
                        "current_price": {"type": "number"},
                    },
                    "required": ["intrinsic_value", "current_price"],
                },
            },
            {
                "name": "get_do_not_invest_checklist",
                "description": "Return the do-not-invest checklist for pre-investment discipline check",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "framework": {"type": "string", "enum": ["mature", "growth", "web3"], "default": "growth"},
                    },
                },
            },
            {
                "name": "export_report",
                "description": "Export a completed research report to Markdown and/or PDF. Dual output to separate folders with templated filenames.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Full markdown content of the report"},
                        "ticker": {"type": "string"},
                        "framework": {"type": "string", "enum": ["mature", "growth", "web3"]},
                        "report_id": {"type": "string", "description": "UUID for the report"},
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "pdf", "both"],
                            "default": "both",
                        },
                    },
                    "required": ["content", "ticker", "framework", "report_id"],
                },
            },
            {
                "name": "audit_report_citations",
                "description": "Audit a research report for data points lacking source citations. Detects hallucination risk.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_content": {"type": "string", "description": "Full markdown content to audit"},
                    },
                    "required": ["report_content"],
                },
            },
            {
                "name": "validate_data_point",
                "description": "Validate a data point against multiple sources for cross-validation and confidence scoring.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "value": {"description": "The data value to validate"},
                        "label": {"type": "string", "description": "Data label (e.g. 'Revenue', 'PE Ratio')"},
                        "sources": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "url": {"type": "string"},
                                    "date": {"type": "string"},
                                    "value": {"type": "number"},
                                },
                            },
                            "description": "List of sources with name, url, date, and value",
                        },
                    },
                    "required": ["value", "label", "sources"],
                },
            },
        ]

    # ------------------------------------------------------------------
    # Tool call handler
    # ------------------------------------------------------------------

    def handle_tool_call(self, tool_name: str, inputs: dict) -> str:
        try:
            # --- Search tools ---
            if tool_name == "search_stock_news":
                result = self.searcher.search_stock_news(inputs["ticker"], inputs.get("num_results", 0))
                return self._format_search_response(result)
            if tool_name == "search_market_analysis":
                result = self.searcher.search_market_analysis(inputs["topic"], inputs.get("num_results", 0))
                return self._format_search_response(result)
            if tool_name == "search_company_info":
                result = self.searcher.search_company_info(inputs["company_name"], inputs.get("num_results", 0))
                return self._format_search_response(result)
            if tool_name == "deep_research":
                result = self.searcher.search_with_deep_research(inputs["query"], inputs.get("num_results", 0))
                return self._format_search_response(result, deep=True)

            # --- Research tools ---
            if tool_name == "generate_research_report":
                result = self.researcher.generate_report_skeleton(
                    inputs["target_name"], inputs["ticker"],
                    inputs.get("market", ""), inputs.get("framework", ""))
                return json.dumps(result, ensure_ascii=False, default=str)
            if tool_name == "get_research_queries":
                result = self.researcher.get_research_queries(inputs["target_name"], inputs["ticker"], inputs["framework"])
                return json.dumps(result, ensure_ascii=False)
            if tool_name == "check_report_freshness":
                checker = DataFreshnessChecker()
                return json.dumps(checker.check_report(inputs["report_content"]), ensure_ascii=False)
            if tool_name == "check_unfilled_fields":
                checker = DataFreshnessChecker()
                return json.dumps(checker.check_unfilled_fields(inputs["report_content"]), ensure_ascii=False)
            if tool_name == "calculate_valuation":
                result = self._handle_valuation(inputs["method"], inputs["params"])
                if inputs["method"] != "cross_validate":
                    params = inputs.get("params", {})
                    has_sources = any(k.endswith("_source") for k in params)
                    if not has_sources:
                        result["source_warning"] = (
                            "此估值计算的输入参数未包含 _source 字段。"
                            "为防止幻觉，请确保每个关键输入均来自可验证的数据源。"
                        )
                return json.dumps(result, ensure_ascii=False)
            if tool_name == "get_position_sizing":
                result = self.researcher.get_position_sizing(inputs["intrinsic_value"], inputs["current_price"])
                return json.dumps(result, ensure_ascii=False)
            if tool_name == "get_do_not_invest_checklist":
                result = self.researcher.get_checklist(inputs.get("framework", "growth"))
                return json.dumps(result, ensure_ascii=False)

            # --- Export tool (with pre-export audit) ---
            if tool_name == "export_report":
                return self._handle_export(inputs)

            # --- Audit tool ---
            if tool_name == "audit_report_citations":
                checker = DataFreshnessChecker()
                audit = checker.audit_source_citations(inputs["report_content"])
                return json.dumps(audit, ensure_ascii=False)

            # --- Validation tool ---
            if tool_name == "validate_data_point":
                result = self.validator.validate_data_point(
                    value=inputs["value"],
                    label=inputs["label"],
                    sources=inputs.get("sources", []),
                )
                return json.dumps(result, ensure_ascii=False, default=str)

            return json.dumps({"error": f"Unknown tool: {tool_name}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _format_search_response(self, result: Dict, deep: bool = False) -> str:
        """Format search results with provenance warning (DRY)."""
        formatted = self.searcher.format_results(result)
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        search_label = "Exa深度搜索" if deep else "Exa搜索引擎实时抓取"
        return (
            f"{formatted}\n\n"
            f"⚠️ 数据溯源提示: 以上数据来自{search_label}，"
            f"搜索时间: {now}。请交叉验证关键财务数据。"
        )

    def _handle_valuation(self, method: str, params: dict) -> dict:
        vm = ValuationMethods
        method_map = {
            "dcf": vm.dcf, "graham": vm.graham_formula,
            "pe": vm.pe_relative, "pb": vm.pb_relative,
            "ps": vm.ps_relative, "ev_ebitda": vm.ev_ebitda,
            "peg": vm.peg, "ddm": vm.ddm,
            "owner_earnings": vm.owner_earnings_valuation,
            "replacement_cost": vm.replacement_cost,
            "cross_validate": vm.cross_validate,
        }
        func = method_map.get(method)
        if not func:
            return {"error": f"Unknown valuation method: {method}"}
        return func(**params)

    def _handle_export(self, inputs: dict) -> str:
        """Export with pre-export audit enforcement."""
        content = inputs["content"]
        ticker = inputs["ticker"]
        framework = inputs["framework"]
        report_id = inputs["report_id"]
        fmt = inputs.get("format", "both")

        # Pre-export audit (enforced by config)
        if self._validation_config.get("block_export_on_high_risk", True):
            checker = DataFreshnessChecker()
            audit = checker.audit_source_citations(content)
            if audit.get("hallucination_risk") == "high":
                return json.dumps({
                    "error": "EXPORT_BLOCKED",
                    "reason": "Hallucination risk is HIGH. Fix uncited data points before exporting.",
                    "audit": audit,
                }, ensure_ascii=False)

        if fmt == "markdown":
            path = self.exporter.export_markdown(content, ticker, framework, report_id)
            return json.dumps({"exported": "markdown", "path": str(path)}, ensure_ascii=False)
        elif fmt == "pdf":
            path = self.exporter.export_pdf(content, ticker, framework, report_id)
            return json.dumps({"exported": "pdf", "path": str(path)}, ensure_ascii=False)
        else:
            paths = self.exporter.export_both(content, ticker, framework, report_id)
            return json.dumps({
                "exported": "both",
                "markdown_path": str(paths["markdown"]),
                "pdf_path": str(paths["pdf"]),
            }, ensure_ascii=False)

    def get_tools(self) -> str:
        return json.dumps(self.tools, indent=2)


def main():
    api_key = get_api_key("exa")
    server = ExaMCPServer(api_key)
    print("Exa MCP Server initialized successfully!")
    print(f"\nAvailable tools ({len(server.tools)}):\n{server.get_tools()}")


if __name__ == "__main__":
    main()
