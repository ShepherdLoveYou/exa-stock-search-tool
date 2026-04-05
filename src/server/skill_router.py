"""
Unified Skill Router — merges search routing + investment research routing
Single entry point for natural language request dispatch
"""

import re
import json
from typing import Dict, Optional

from src.config import get_api_key
from src.search.exa_searcher import StockSearcher
from src.core.researcher import InvestmentResearcher
from src.core.freshness import DataFreshnessChecker
from src.core.valuation import ValuationMethods
from src.core.validator import DataValidator
from src.core import FRAMEWORK_MATURE, FRAMEWORK_GROWTH, FRAMEWORK_WEB3
from src.export.exporter import ReportExporter


class UnifiedSkillRouter:
    """
    Intelligent router that interprets natural language queries
    and dispatches to search, research, valuation, freshness, or export handlers.
    """

    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or get_api_key("exa")
        self.searcher = StockSearcher(api_key)
        self.researcher = InvestmentResearcher(self.searcher)
        self.validator = DataValidator()
        self.exporter = ReportExporter()

    # ------------------------------------------------------------------
    # Top-level dispatch
    # ------------------------------------------------------------------

    def route(self, user_input: str) -> Dict:
        input_lower = user_input.lower()

        if self._is_report_request(input_lower):
            return self._handle_report_request(user_input)
        if self._is_freshness_check(input_lower):
            return self._handle_freshness_check(user_input)
        if self._is_valuation_request(input_lower):
            return self._handle_valuation_request(user_input)
        if self._is_checklist_request(input_lower):
            return self._handle_checklist_request(user_input)
        if self._is_position_request(input_lower):
            return self._handle_position_request(user_input)
        return self._handle_search_request(user_input)

    # ------------------------------------------------------------------
    # Search-oriented convenience methods (from old ExaSkillRouter)
    # ------------------------------------------------------------------

    def detect_search_type(self, query: str) -> Dict:
        query_lower = query.lower()
        patterns = {
            'stock_news': [
                r'(?:what\'s|what is|latest|news|recent)\s+(?:with|about|on|for)\s+([A-Z]{1,5})',
                r'([A-Z]{1,5})\s+(?:stock|ticker)\s+(?:news|price|movement)',
            ],
            'market_analysis': [
                r'(?:analyze|analysis|trend)\s+(?:in|for)\s+([a-z\s]+)\s+(?:stocks|market|sector)',
            ],
            'company_info': [
                r'(?:research|info|information)\s+(?:about|on)\s+([a-z\s]+)\s+(?:company|corp)',
            ],
            'deep_research': [
                r'(?:deep|thorough|comprehensive)\s+(?:research|analysis)\s+(?:on|about|into)\s+(.+)',
            ],
        }
        for search_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, query_lower, re.IGNORECASE)
                if match:
                    return {'type': search_type, 'query': match.group(1).strip(), 'confidence': 0.9}
        return {'type': 'market_analysis', 'query': query, 'confidence': 0.5}

    def search(self, query: str, num_results: int = 10) -> Dict:
        detection = self.detect_search_type(query)
        search_type = detection['type']
        search_query = detection['query']
        if search_type == 'stock_news':
            ticker = re.sub(r'[^A-Z]', '', search_query.upper())[:5] or search_query.upper()
            return self.searcher.search_stock_news(ticker, num_results)
        elif search_type == 'company_info':
            return self.searcher.search_company_info(search_query, num_results)
        elif search_type == 'deep_research':
            return self.searcher.search_with_deep_research(search_query, num_results)
        else:
            return self.searcher.search_market_analysis(search_query, num_results)

    def search_and_format(self, query: str, num_results: int = 10, max_display: int = 5) -> str:
        results = self.search(query, num_results)
        return StockSearcher.format_results(results, max_display)

    def search_as_json(self, query: str, num_results: int = 10) -> str:
        results = self.search(query, num_results)
        json_results = {
            "query": query,
            "total_results": results.get("total_results", 0),
            "results": [],
        }
        for result in results.get("results", [])[:10]:
            json_results["results"].append({
                "title": result.title,
                "url": result.url,
                "highlight": result.highlights[0][:200] if hasattr(result, 'highlights') and result.highlights else "",
            })
        return json.dumps(json_results, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Intent detection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_report_request(text: str) -> bool:
        return any(kw in text for kw in [
            "report", "research", "投研", "报告", "研报",
            "generate", "create report", "write report", "分析", "framework", "框架"])

    @staticmethod
    def _is_freshness_check(text: str) -> bool:
        return any(kw in text for kw in [
            "freshness", "timeliness", "stale", "outdated",
            "时效", "过期", "新鲜", "更新", "check data"])

    @staticmethod
    def _is_valuation_request(text: str) -> bool:
        return any(kw in text for kw in [
            "valuation", "dcf", "graham", "intrinsic value", "估值",
            "pe ratio", "pb ratio", "ev/ebitda", "peg", "内在价值", "折现"])

    @staticmethod
    def _is_checklist_request(text: str) -> bool:
        return any(kw in text for kw in [
            "checklist", "discipline", "不为清单", "rules", "do not invest", "纪律"])

    @staticmethod
    def _is_position_request(text: str) -> bool:
        return any(kw in text for kw in [
            "position", "sizing", "仓位", "建仓", "buy ladder", "allocation", "资金管理"])

    # ------------------------------------------------------------------
    # Request handlers
    # ------------------------------------------------------------------

    def _handle_report_request(self, user_input: str) -> Dict:
        ticker_match = re.search(r'\b([A-Z]{1,5})\b', user_input)
        ticker = ticker_match.group(1) if ticker_match else ""
        name = user_input
        for remove in ["generate", "create", "write", "report", "research", "for", "about", "on"]:
            name = re.sub(rf'\b{remove}\b', '', name, flags=re.IGNORECASE)
        name = name.strip().strip("()（）") or ticker

        market = ""
        if any(kw in user_input.lower() for kw in ["crypto", "web3", "defi", "token", "代币"]):
            market = "crypto"
        elif any(kw in user_input.lower() for kw in ["港股", "hk", "hong kong"]):
            market = "hk"
        elif any(kw in user_input.lower() for kw in ["a股", "a-share", "沪", "深"]):
            market = "a-share"

        report = self.researcher.generate_report_skeleton(name, ticker, market)
        queries = self.researcher.get_research_queries(name, ticker, report["framework"])

        return {
            "action": "generate_report",
            "report": report,
            "research_queries": queries,
            "next_steps": [
                f"Report skeleton generated with framework: {report['framework']}",
                f"There are {len(report['unfilled_fields'])} fields to fill",
                f"Use {len(queries)} prioritized search queries to gather data",
                "Fill in each {{PLACEHOLDER}} with verified data",
                "Run freshness check after filling to validate timeliness",
            ],
        }

    def _handle_freshness_check(self, user_input: str) -> Dict:
        return {
            "action": "freshness_check",
            "message": "Provide the report content to check freshness",
            "checker_ready": True,
        }

    def _handle_valuation_request(self, user_input: str) -> Dict:
        return {
            "action": "valuation",
            "available_methods": [
                "DCF", "Graham", "PE", "PB", "PS",
                "EV/EBITDA", "PEG", "DDM", "Owner Earnings", "Replacement Cost",
            ],
            "message": "Provide financial parameters for the valuation method",
        }

    def _handle_checklist_request(self, user_input: str) -> Dict:
        framework = FRAMEWORK_GROWTH
        if "mature" in user_input.lower() or "成熟" in user_input:
            framework = FRAMEWORK_MATURE
        elif "web3" in user_input.lower() or "crypto" in user_input.lower():
            framework = FRAMEWORK_WEB3
        return {
            "action": "checklist",
            "framework": framework,
            "checklist": self.researcher.get_checklist(framework),
        }

    def _handle_position_request(self, user_input: str) -> Dict:
        numbers = re.findall(r'[\d.]+', user_input)
        if len(numbers) >= 2:
            result = self.researcher.get_position_sizing(float(numbers[0]), float(numbers[1]))
            return {"action": "position_sizing", "result": result}
        return {"action": "position_sizing", "message": "Provide intrinsic value and current price"}

    def _handle_search_request(self, user_input: str) -> Dict:
        return {"action": "search", "message": "Routing to general search", "query": user_input}
