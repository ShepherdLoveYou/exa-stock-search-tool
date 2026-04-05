"""
Investment Research Engine - Crisis Investment Research Framework
Supports three methodologies: Mature Company, Growth Company, Web3 Project
"""

import uuid
import re
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


FRAMEWORK_MATURE = "mature"
FRAMEWORK_GROWTH = "growth"
FRAMEWORK_WEB3 = "web3"

FRAMEWORK_LABELS = {
    FRAMEWORK_MATURE: "成熟公司",
    FRAMEWORK_GROWTH: "成长性公司",
    FRAMEWORK_WEB3: "Web3项目",
}

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "research Output" / "templates"


class InvestmentResearcher:
    """
    Core investment research engine implementing the Crisis Investment methodology
    """

    def __init__(self, searcher=None):
        self.searcher = searcher
        self._templates = {}

    def detect_framework(self, target: str, market: str = "") -> str:
        market_lower = market.lower() if market else ""
        target_lower = target.lower() if target else ""

        crypto_keywords = [
            "crypto", "web3", "defi", "dex", "dao", "nft", "token",
            "chain", "protocol", "layer", "bridge", "swap", "vault",
            "eth", "btc", "sol", "avax", "matic", "arb",
        ]

        if market_lower in ("crypto", "web3", "defi"):
            return FRAMEWORK_WEB3
        for kw in crypto_keywords:
            if kw in target_lower or kw in market_lower:
                return FRAMEWORK_WEB3

        mature_indicators = [
            "bank", "insurance", "energy", "oil", "utility",
            "telecom", "tobacco", "pharma", "consumer staple",
        ]
        for indicator in mature_indicators:
            if indicator in target_lower or indicator in market_lower:
                return FRAMEWORK_MATURE

        return FRAMEWORK_GROWTH

    def load_template(self, framework: str) -> str:
        if framework in self._templates:
            return self._templates[framework]

        template_map = {
            FRAMEWORK_MATURE: "mature_company_template.md",
            FRAMEWORK_GROWTH: "growth_company_template.md",
            FRAMEWORK_WEB3: "web3_project_template.md",
        }

        filename = template_map.get(framework)
        if not filename:
            raise ValueError(f"Unknown framework: {framework}")

        template_path = TEMPLATE_DIR / filename
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")
        self._templates[framework] = content
        return content

    def generate_report_skeleton(
        self,
        target_name: str,
        ticker: str,
        market: str = "",
        framework: str = "",
    ) -> Dict:
        if not framework:
            framework = self.detect_framework(target_name, market)

        report_id = str(uuid.uuid4())
        now = datetime.now()
        template = self.load_template(framework)

        replacements = {
            "{{UUID}}": report_id,
            "{{TARGET_NAME}}": target_name,
            "{{TICKER}}": ticker.upper(),
            "{{MARKET}}": market or self._infer_market(ticker),
            "{{DATE}}": now.strftime("%Y-%m-%d"),
            "{{DATA_DATE}}": now.strftime("%Y-%m-%d"),
        }

        if framework == FRAMEWORK_WEB3:
            replacements["{{SECTOR}}"] = market or "DeFi"

        content = template
        for key, value in replacements.items():
            content = content.replace(key, value)

        return {
            "report_id": report_id,
            "framework": framework,
            "target_name": target_name,
            "ticker": ticker,
            "market": market,
            "created_at": now.isoformat(),
            "content": content,
            "unfilled_fields": self._extract_unfilled(content),
        }

    def get_research_queries(self, target_name: str, ticker: str, framework: str) -> List[Dict]:
        queries = []

        common = [
            {"query": f"{target_name} {ticker} company overview strategic positioning",
             "field": "STRATEGIC_POSITIONING", "priority": 1,
             "preferred_sources": ["official website", "SEC filings", "exchange announcements"],
             "data_type": "qualitative"},
            {"query": f"{target_name} {ticker} target users pain points solutions",
             "field": "TARGET_USER/PAIN_POINT/SOLUTION", "priority": 1,
             "preferred_sources": ["product documentation", "official blog", "earnings call transcript"],
             "data_type": "qualitative"},
            {"query": f"{target_name} {ticker} TAM SAM SOM market size 2024 2025",
             "field": "MARKET_SIZE", "priority": 2,
             "preferred_sources": ["industry reports (McKinsey/BCG/Gartner)", "analyst reports"],
             "data_type": "quantitative", "requires_source_citation": True},
            {"query": f"{target_name} founder CEO background leadership",
             "field": "FOUNDER_ANALYSIS", "priority": 2,
             "preferred_sources": ["LinkedIn", "official bio", "interviews"],
             "data_type": "qualitative"},
            {"query": f"{target_name} {ticker} competitors comparison market share",
             "field": "COMPETITOR_MOAT", "priority": 3,
             "preferred_sources": ["industry reports", "SEC filings", "financial data APIs"],
             "data_type": "quantitative", "requires_source_citation": True},
        ]
        queries.extend(common)

        if framework == FRAMEWORK_MATURE:
            queries.extend(self._mature_queries(target_name, ticker))
        elif framework == FRAMEWORK_GROWTH:
            queries.extend(self._growth_queries(target_name, ticker))
        elif framework == FRAMEWORK_WEB3:
            queries.extend(self._web3_queries(target_name, ticker))

        queries.extend([
            {"query": f"{target_name} {ticker} DCF valuation intrinsic value",
             "field": "VAL_1", "priority": 1,
             "preferred_sources": ["financial data API (FMP/Finnhub)", "SEC filings", "analyst reports"],
             "data_type": "quantitative", "requires_source_citation": True,
             "cross_validation": "Must use API-sourced FCF/growth data, not memorized values"},
            {"query": f"{target_name} {ticker} PE PB PS ratio valuation peers",
             "field": "VAL_3/VAL_4/VAL_5", "priority": 1,
             "preferred_sources": ["FMP API", "Finnhub API", "financial databases"],
             "data_type": "quantitative", "requires_source_citation": True,
             "cross_validation": "Compare ratios from ≥2 sources"},
            {"query": f"{target_name} {ticker} EV EBITDA enterprise value",
             "field": "VAL_6", "priority": 2,
             "preferred_sources": ["FMP API", "SEC filings (10-K/10-Q)"],
             "data_type": "quantitative", "requires_source_citation": True},
            {"query": f"{target_name} {ticker} analyst price target consensus",
             "field": "CATALYST_SIGNALS", "priority": 2,
             "preferred_sources": ["Finnhub API", "analyst reports"],
             "data_type": "quantitative", "requires_source_citation": True},
            {"query": f"{target_name} {ticker} short selling report bear case risks",
             "field": "RISK_REWARD_ANALYSIS", "priority": 3,
             "preferred_sources": ["short seller reports (Hindenburg/Muddy Waters)", "SEC filings"],
             "data_type": "qualitative"},
        ])

        queries.sort(key=lambda x: x["priority"])
        return queries

    def _mature_queries(self, name: str, ticker: str) -> List[Dict]:
        return [
            {"query": f"{name} {ticker} crisis restructuring cost cutting layoffs",
             "field": "SELF_RESCUE_ANALYSIS", "priority": 1},
            {"query": f"{name} {ticker} divestiture non-core business spin-off",
             "field": "RESTRUCTURE_ANALYSIS", "priority": 2},
            {"query": f"{name} {ticker} fundraising capital raise debt financing",
             "field": "EXTERNAL_RESCUE_ANALYSIS", "priority": 2},
            {"query": f"{name} mission vision corporate culture values",
             "field": "PEOPLE_1", "priority": 3},
            {"query": f"{name} {ticker} insider trading management buy sell shares",
             "field": "PEOPLE_7", "priority": 2},
            {"query": f"{name} {ticker} M&A acquisitions buyback history value creation",
             "field": "PEOPLE_5", "priority": 3},
            {"query": f"{name} {ticker} ROIC ROE net margin historical financial",
             "field": "FIN_1_HIST", "priority": 1},
            {"query": f"{name} {ticker} revenue growth rate historical trend",
             "field": "FIN_2_HIST", "priority": 1},
            {"query": f"{name} {ticker} cash flow net income ratio operating",
             "field": "FIN_3_HIST", "priority": 2},
            {"query": f"{name} {ticker} debt equity ratio interest coverage",
             "field": "FIN_5_HIST", "priority": 2},
            {"query": f"{name} {ticker} patent monopoly exclusive rights moat",
             "field": "BIZ_1", "priority": 3},
            {"query": f"{name} {ticker} market share industry leader ranking",
             "field": "BIZ_2", "priority": 2},
            {"query": f"{name} {ticker} pricing power industry position",
             "field": "BIZ_3", "priority": 3},
        ]

    def _growth_queries(self, name: str, ticker: str) -> List[Dict]:
        return [
            {"query": f"{name} {ticker} revenue growth rate YoY quarterly",
             "field": "GROWTH_SPEED", "priority": 1},
            {"query": f"{name} {ticker} gross margin operating margin trend",
             "field": "GROSS_MARGIN", "priority": 1},
            {"query": f"{name} {ticker} ROIC return on invested capital peers",
             "field": "ROIC_VALUE", "priority": 2},
            {"query": f"{name} {ticker} free cash flow FCF trend",
             "field": "FCF_ANALYSIS", "priority": 2},
            {"query": f"{name} {ticker} debt ratio leverage balance sheet",
             "field": "DEBT_ANALYSIS", "priority": 2},
            {"query": f"{name} {ticker} product positioning niche market segment",
             "field": "PRODUCT_POSITIONING", "priority": 3},
            {"query": f"{name} {ticker} business model revenue streams",
             "field": "PROFIT_MODEL", "priority": 2},
            {"query": f"{name} {ticker} network effect ecosystem advantage moat",
             "field": "ECOSYSTEM_ADVANTAGE", "priority": 3},
            {"query": f"{name} {ticker} brand recognition category leader mind share",
             "field": "BRAND_MINDSHARE", "priority": 3},
            {"query": f"{name} retained earnings value creation market cap",
             "field": "RETAINED_EARNINGS_VALUE", "priority": 3},
            {"query": f"{name} {ticker} owner earnings shareholder yield",
             "field": "OWNER_EARNINGS", "priority": 3},
        ]

    def _web3_queries(self, name: str, ticker: str) -> List[Dict]:
        return [
            {"query": f"{name} {ticker} TVL total value locked trend",
             "field": "TVL_CURRENT", "priority": 1},
            {"query": f"{name} {ticker} protocol revenue fees income",
             "field": "FEE_REVENUE_30D", "priority": 1},
            {"query": f"{name} {ticker} tokenomics token economics model",
             "field": "TOKEN_INCENTIVE_FLYWHEEL", "priority": 1},
            {"query": f"{name} {ticker} token unlock vesting schedule",
             "field": "UNLOCK_SCHEDULE", "priority": 2},
            {"query": f"{name} {ticker} token buyback burn mechanism",
             "field": "BUYBACK_MECHANISM", "priority": 2},
            {"query": f"{name} {ticker} DAO treasury holdings stablecoin",
             "field": "TREASURY_TOTAL", "priority": 2},
            {"query": f"{name} {ticker} active addresses users growth",
             "field": "ACTIVE_ADDRESSES", "priority": 2},
            {"query": f"{name} {ticker} github commits development activity",
             "field": "GITHUB_COMMITS", "priority": 3},
            {"query": f"{name} {ticker} governance proposals voting participation",
             "field": "GOVERNANCE_PARTICIPATION", "priority": 3},
            {"query": f"{name} {ticker} technical architecture innovation",
             "field": "TECH_INNOVATION", "priority": 3},
            {"query": f"{name} {ticker} consensus mechanism design",
             "field": "CONSENSUS_INNOVATION", "priority": 3},
            {"query": f"{name} {ticker} roadmap milestones progress 2024 2025",
             "field": "CATALYST_SIGNALS", "priority": 2},
            {"query": f"{name} {ticker} community discord telegram activity",
             "field": "COMMUNITY_ACTIVE_USERS", "priority": 3},
            {"query": f"{name} {ticker} FDV fully diluted valuation TVL ratio",
             "field": "VAL_2", "priority": 1},
        ]

    def get_checklist(self, framework: str) -> List[Dict]:
        return [
            {"id": 1, "rule": "终生投资不超30支股票和30支代币", "check_field": "portfolio_count"},
            {"id": 2, "rule": "没有买完后踏实睡觉的坚定信心不投", "check_field": "SLEEP_WELL"},
            {"id": 3, "rule": "业务看不到5年10倍增长空间不投" if framework != FRAMEWORK_MATURE
                  else "业务看不到3年5倍增长空间不投", "check_field": "TEN_X_POTENTIAL"},
            {"id": 4, "rule": "不符合'与优秀的人做伟大的事'不投", "check_field": "CHECK_3"},
            {"id": 5, "rule": "价格不是便宜到令人惊悚不投（5折）", "check_field": "BELOW_50_PCT"},
            {"id": 6, "rule": "未来没有可持续的确定盈利能力不投", "check_field": "CHECK_1"},
            {"id": 7, "rule": "看不懂/说不清/犹豫不决/非常识判断等一律不投", "check_field": "manual_check"},
            {"id": 8, "rule": "单比投资总额不超总资产的20%且现金极值不低于20%", "check_field": "POSITION_SIZE"},
            {"id": 9, "rule": "从产生交易念头到实际下单必须间隔24小时", "check_field": "manual_check"},
            {"id": 10, "rule": "同时持仓数量永远不能超过7个", "check_field": "portfolio_count"},
        ]

    def get_position_sizing(self, intrinsic_value: float, current_price: float) -> Dict:
        discount = current_price / intrinsic_value if intrinsic_value > 0 else 1.0

        price_90 = intrinsic_value * 0.9
        price_70 = intrinsic_value * 0.7
        price_50 = intrinsic_value * 0.5

        if discount <= 0.5:
            zone = "deep_water"
            zone_label = "深水区（长期持有复利增长）"
            max_single = 0.20
        elif discount <= 0.7:
            zone = "shallow_water"
            zone_label = "浅水区→深水区过渡"
            max_single = 0.10
        elif discount <= 0.9:
            zone = "shallow_water"
            zone_label = "浅水区（均值回归套利）"
            max_single = 0.05
        else:
            zone = "waiting"
            zone_label = "等待区（保持流动性）"
            max_single = 0

        return {
            "intrinsic_value": intrinsic_value,
            "current_price": current_price,
            "discount_rate": f"{discount:.1%}",
            "zone": zone,
            "zone_label": zone_label,
            "max_single_position": f"{max_single:.0%}",
            "buy_ladder": {
                "9折": {"price": round(price_90, 2), "allocation": "30%"},
                "7折": {"price": round(price_70, 2), "allocation": "30%"},
                "5折": {"price": round(price_50, 2), "allocation": "40%"},
            },
        }

    def _extract_unfilled(self, content: str) -> List[str]:
        return list(set(re.findall(r'\{\{([A-Z_0-9]+)\}\}', content)))

    def _infer_market(self, ticker: str) -> str:
        ticker = ticker.upper()
        if re.match(r'^\d{4,6}\.(?:HK|hk)$', ticker):
            return "港股"
        if re.match(r'^\d{6}\.(?:SH|SZ|sh|sz)$', ticker):
            return "A股"
        if re.match(r'^[A-Z]{1,5}$', ticker):
            return "美股"
        return "未知"
