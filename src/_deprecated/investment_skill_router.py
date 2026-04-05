"""
Investment Research Skill Router
Routes natural language research requests to the correct framework and tools
"""

import re
import json
from typing import Dict, Optional
from src.investment_researcher import InvestmentResearcher, ValuationMethods, FRAMEWORK_MATURE, FRAMEWORK_GROWTH, FRAMEWORK_WEB3
from src.data_freshness_checker import DataFreshnessChecker
from src.stock_searcher import StockSearcher


class InvestmentSkillRouter:
    """
    Routes investment research requests to appropriate handlers
    Supports: report generation, data review, freshness check, valuation, discipline check
    """

    def __init__(self, api_key: Optional[str] = None):
        self.searcher = StockSearcher(api_key)
        self.researcher = InvestmentResearcher(self.searcher)

    def route(self, user_input: str) -> Dict:
        """
        Parse user intent and route to the correct handler

        Args:
            user_input: Natural language request

        Returns:
            Dict with action taken and results
        """
        input_lower = user_input.lower()

        # Detect intent
        if self._is_report_request(input_lower):
            return self._handle_report_request(user_input)
        elif self._is_freshness_check(input_lower):
            return self._handle_freshness_check(user_input)
        elif self._is_valuation_request(input_lower):
            return self._handle_valuation_request(user_input)
        elif self._is_checklist_request(input_lower):
            return self._handle_checklist_request(user_input)
        elif self._is_position_request(input_lower):
            return self._handle_position_request(user_input)
        else:
            return self._handle_search_request(user_input)

    def _is_report_request(self, text: str) -> bool:
        keywords = [
            "report", "research", "投研", "报告", "研报",
            "generate", "create report", "write report",
            "分析", "framework", "框架",
        ]
        return any(kw in text for kw in keywords)

    def _is_freshness_check(self, text: str) -> bool:
        keywords = [
            "freshness", "timeliness", "stale", "outdated", "current",
            "时效", "过期", "新鲜", "更新", "check data",
        ]
        return any(kw in text for kw in keywords)

    def _is_valuation_request(self, text: str) -> bool:
        keywords = [
            "valuation", "dcf", "graham", "intrinsic value", "估值",
            "pe ratio", "pb ratio", "ev/ebitda", "peg",
            "内在价值", "折现",
        ]
        return any(kw in text for kw in keywords)

    def _is_checklist_request(self, text: str) -> bool:
        keywords = [
            "checklist", "discipline", "不为清单", "rules",
            "do not invest", "纪律",
        ]
        return any(kw in text for kw in keywords)

    def _is_position_request(self, text: str) -> bool:
        keywords = [
            "position", "sizing", "仓位", "建仓", "buy ladder",
            "allocation", "资金管理",
        ]
        return any(kw in text for kw in keywords)

    def _handle_report_request(self, user_input: str) -> Dict:
        """Extract target info and generate report skeleton"""
        # Try to extract ticker
        ticker_match = re.search(r'\b([A-Z]{1,5})\b', user_input)
        ticker = ticker_match.group(1) if ticker_match else ""

        # Try to extract company name (text before/around ticker)
        name = user_input
        for remove in ["generate", "create", "write", "report", "research", "for", "about", "on"]:
            name = re.sub(rf'\b{remove}\b', '', name, flags=re.IGNORECASE)
        name = name.strip().strip("()（）")
        if not name:
            name = ticker

        # Detect market hints
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
        """Check data freshness of provided content"""
        checker = DataFreshnessChecker()
        # The actual report content would be passed separately
        return {
            "action": "freshness_check",
            "message": "Provide the report content to check freshness",
            "checker_ready": True,
        }

    def _handle_valuation_request(self, user_input: str) -> Dict:
        """Parse valuation parameters and calculate"""
        return {
            "action": "valuation",
            "available_methods": [
                "DCF自由现金流折现",
                "DDM股利折现模型",
                "PE市盈率对标",
                "PB市净率对标",
                "PS市销率对标",
                "EV/EBITDA企业价值倍数",
                "格雷厄姆公式",
                "PEG估值法",
                "股东盈余估值法",
                "重置成本法",
            ],
            "message": "Provide financial parameters for the valuation method",
        }

    def _handle_checklist_request(self, user_input: str) -> Dict:
        """Return the do-not-invest checklist"""
        framework = FRAMEWORK_GROWTH  # default
        if "mature" in user_input.lower() or "成熟" in user_input:
            framework = FRAMEWORK_MATURE
        elif "web3" in user_input.lower() or "crypto" in user_input.lower():
            framework = FRAMEWORK_WEB3

        checklist = self.researcher.get_checklist(framework)
        return {
            "action": "checklist",
            "framework": framework,
            "checklist": checklist,
        }

    def _handle_position_request(self, user_input: str) -> Dict:
        """Parse values and calculate position sizing"""
        numbers = re.findall(r'[\d.]+', user_input)
        if len(numbers) >= 2:
            intrinsic = float(numbers[0])
            current = float(numbers[1])
            result = self.researcher.get_position_sizing(intrinsic, current)
            return {"action": "position_sizing", "result": result}

        return {
            "action": "position_sizing",
            "message": "Provide intrinsic value and current price",
        }

    def _handle_search_request(self, user_input: str) -> Dict:
        """Fallback to general search"""
        return {
            "action": "search",
            "message": "Routing to general search",
            "query": user_input,
        }


def main():
    """Demo usage"""
    router = InvestmentSkillRouter()

    test_inputs = [
        "Generate a research report for Apple (AAPL)",
        "投研分析 Uniswap (UNI) crypto",
        "Run the do-not-invest checklist for mature company",
        "Calculate position sizing: intrinsic value 200, current price 95",
    ]

    for query in test_inputs:
        print(f"\n{'='*60}")
        print(f"Input: {query}")
        print(f"{'='*60}")
        result = router.route(query)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str)[:500])


if __name__ == "__main__":
    main()
