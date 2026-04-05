"""
Investment Research Assistant - Crisis Investment Research Framework
Supports three methodologies: Mature Company, Growth Company, Web3 Project
"""

import uuid
import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path


# Framework type constants
FRAMEWORK_MATURE = "mature"
FRAMEWORK_GROWTH = "growth"
FRAMEWORK_WEB3 = "web3"

TEMPLATE_DIR = Path(__file__).parent.parent / "research Output" / "templates"
OUTPUT_DIR = Path(__file__).parent.parent / "research Output"


class InvestmentResearcher:
    """
    Core investment research engine implementing the Crisis Investment methodology
    Three frameworks:
    - Mature Company: 7 major steps with scoring (人/事/果 each 10-point scale)
    - Growth Company: 14 sections covering business/financials/valuation
    - Web3 Project: 15 sections including tokenomics/on-chain/ecosystem
    """

    def __init__(self, searcher=None):
        """
        Args:
            searcher: Optional StockSearcher instance for data retrieval
        """
        self.searcher = searcher
        self._templates = {}

    def detect_framework(self, target: str, market: str = "") -> str:
        """
        Auto-detect which research framework to use based on target and market

        Args:
            target: Company name, ticker, or token symbol
            market: Market hint - 'us', 'hk', 'a-share', 'crypto', etc

        Returns:
            Framework type string
        """
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

        # Default to growth for tech/general stocks
        return FRAMEWORK_GROWTH

    def load_template(self, framework: str) -> str:
        """Load the markdown template for a given framework"""
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
        """
        Generate a report skeleton with metadata filled in

        Args:
            target_name: Company/project name
            ticker: Stock ticker or token symbol
            market: Market identifier
            framework: Framework type (auto-detected if empty)

        Returns:
            Dict with report_id, framework, template content, and metadata
        """
        if not framework:
            framework = self.detect_framework(target_name, market)

        report_id = str(uuid.uuid4())
        now = datetime.now()
        template = self.load_template(framework)

        # Fill in metadata placeholders
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
        """
        Generate search queries needed to fill the report template

        Args:
            target_name: Company/project name
            ticker: Ticker/token symbol
            framework: Framework type

        Returns:
            List of dicts with query, field, and priority
        """
        queries = []

        # Common queries for all frameworks
        common = [
            {"query": f"{target_name} {ticker} company overview strategic positioning",
             "field": "STRATEGIC_POSITIONING", "priority": 1},
            {"query": f"{target_name} {ticker} target users pain points solutions",
             "field": "TARGET_USER/PAIN_POINT/SOLUTION", "priority": 1},
            {"query": f"{target_name} {ticker} TAM SAM SOM market size 2024 2025",
             "field": "MARKET_SIZE", "priority": 2},
            {"query": f"{target_name} founder CEO background leadership",
             "field": "FOUNDER_ANALYSIS", "priority": 2},
            {"query": f"{target_name} {ticker} competitors comparison market share",
             "field": "COMPETITOR_MOAT", "priority": 3},
        ]
        queries.extend(common)

        if framework == FRAMEWORK_MATURE:
            queries.extend(self._mature_queries(target_name, ticker))
        elif framework == FRAMEWORK_GROWTH:
            queries.extend(self._growth_queries(target_name, ticker))
        elif framework == FRAMEWORK_WEB3:
            queries.extend(self._web3_queries(target_name, ticker))

        # Valuation queries - common to all
        queries.extend([
            {"query": f"{target_name} {ticker} DCF valuation intrinsic value",
             "field": "VAL_1", "priority": 1},
            {"query": f"{target_name} {ticker} PE PB PS ratio valuation peers",
             "field": "VAL_3/VAL_4/VAL_5", "priority": 1},
            {"query": f"{target_name} {ticker} EV EBITDA enterprise value",
             "field": "VAL_6", "priority": 2},
            {"query": f"{target_name} {ticker} analyst price target consensus",
             "field": "CATALYST_SIGNALS", "priority": 2},
            {"query": f"{target_name} {ticker} short selling report bear case risks",
             "field": "RISK_REWARD_ANALYSIS", "priority": 3},
        ])

        queries.sort(key=lambda x: x["priority"])
        return queries

    def _mature_queries(self, name: str, ticker: str) -> List[Dict]:
        """Queries specific to mature company framework"""
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
        """Queries specific to growth company framework"""
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
        """Queries specific to Web3 project framework"""
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
        """
        Return the do-not-invest checklist (不为清单) items

        Returns:
            List of checklist items with id, rule, and check_field
        """
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
        """
        Calculate position sizing based on the capital management rules

        Args:
            intrinsic_value: Calculated intrinsic value per share
            current_price: Current market price

        Returns:
            Dict with buy prices, position sizes, and zone classification
        """
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

    def save_report(self, report_data: Dict) -> str:
        """
        Save the report to the research Output directory

        Args:
            report_data: Dict from generate_report_skeleton or filled report

        Returns:
            Path to saved file
        """
        framework_labels = {
            FRAMEWORK_MATURE: "成熟公司",
            FRAMEWORK_GROWTH: "成长性公司",
            FRAMEWORK_WEB3: "Web3项目",
        }

        label = framework_labels.get(report_data["framework"], "投研")
        filename = (
            f"{report_data['created_at'][:10]}_"
            f"{report_data['ticker']}_"
            f"{label}_"
            f"{report_data['report_id'][:8]}.md"
        )

        output_path = OUTPUT_DIR / filename
        output_path.write_text(report_data["content"], encoding="utf-8")
        return str(output_path)

    def _extract_unfilled(self, content: str) -> List[str]:
        """Extract remaining {{PLACEHOLDER}} fields from template"""
        return list(set(re.findall(r'\{\{([A-Z_0-9]+)\}\}', content)))

    def _infer_market(self, ticker: str) -> str:
        """Infer market from ticker format"""
        ticker = ticker.upper()
        if re.match(r'^\d{4,6}\.(?:HK|hk)$', ticker):
            return "港股"
        if re.match(r'^\d{6}\.(?:SH|SZ|sh|sz)$', ticker):
            return "A股"
        if re.match(r'^[A-Z]{1,5}$', ticker):
            return "美股"
        return "未知"


class ValuationMethods:
    """
    Collection of valuation calculation utilities
    Supports 10+ methods for cross-validation as required by the framework
    """

    @staticmethod
    def dcf(
        fcf_current: float,
        growth_rate: float,
        terminal_growth: float = 0.03,
        discount_rate: float = 0.10,
        years: int = 10,
        shares_outstanding: float = 1.0,
    ) -> Dict:
        """Discounted Cash Flow valuation"""
        projected_fcf = []
        fcf = fcf_current
        for yr in range(1, years + 1):
            fcf = fcf * (1 + growth_rate)
            pv = fcf / ((1 + discount_rate) ** yr)
            projected_fcf.append({"year": yr, "fcf": round(fcf, 2), "pv": round(pv, 2)})

        terminal_value = (
            fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
        )
        terminal_pv = terminal_value / ((1 + discount_rate) ** years)

        total_pv = sum(item["pv"] for item in projected_fcf) + terminal_pv
        per_share = total_pv / shares_outstanding if shares_outstanding > 0 else 0

        return {
            "method": "DCF自由现金流折现",
            "total_enterprise_value": round(total_pv, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "fcf_current": fcf_current,
                "growth_rate": f"{growth_rate:.1%}",
                "terminal_growth": f"{terminal_growth:.1%}",
                "discount_rate": f"{discount_rate:.1%}",
                "projection_years": years,
            },
        }

    @staticmethod
    def graham_formula(eps: float, growth_rate: float, aaa_yield: float = 0.045) -> Dict:
        """Benjamin Graham intrinsic value formula: V = EPS * (8.5 + 2g) * 4.4 / Y"""
        g = growth_rate * 100  # Convert to percentage
        value = eps * (8.5 + 2 * g) * 4.4 / (aaa_yield * 100)
        return {
            "method": "格雷厄姆公式",
            "per_share_value": round(value, 2),
            "assumptions": {
                "eps": eps,
                "growth_rate": f"{growth_rate:.1%}",
                "aaa_bond_yield": f"{aaa_yield:.1%}",
            },
        }

    @staticmethod
    def pe_relative(eps: float, industry_pe: float, premium: float = 1.0) -> Dict:
        """PE ratio relative valuation"""
        value = eps * industry_pe * premium
        return {
            "method": "PE市盈率对标",
            "per_share_value": round(value, 2),
            "assumptions": {
                "eps": eps,
                "industry_pe": industry_pe,
                "premium_factor": premium,
            },
        }

    @staticmethod
    def pb_relative(bvps: float, industry_pb: float) -> Dict:
        """PB ratio relative valuation"""
        value = bvps * industry_pb
        return {
            "method": "PB市净率对标",
            "per_share_value": round(value, 2),
            "assumptions": {"book_value_per_share": bvps, "industry_pb": industry_pb},
        }

    @staticmethod
    def ps_relative(revenue_per_share: float, industry_ps: float) -> Dict:
        """PS ratio relative valuation"""
        value = revenue_per_share * industry_ps
        return {
            "method": "PS市销率对标",
            "per_share_value": round(value, 2),
            "assumptions": {
                "revenue_per_share": revenue_per_share,
                "industry_ps": industry_ps,
            },
        }

    @staticmethod
    def ev_ebitda(
        ebitda: float,
        industry_multiple: float,
        net_debt: float,
        shares_outstanding: float,
    ) -> Dict:
        """EV/EBITDA enterprise value valuation"""
        ev = ebitda * industry_multiple
        equity_value = ev - net_debt
        per_share = equity_value / shares_outstanding if shares_outstanding > 0 else 0
        return {
            "method": "EV/EBITDA企业价值倍数",
            "enterprise_value": round(ev, 2),
            "equity_value": round(equity_value, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "ebitda": ebitda,
                "industry_multiple": industry_multiple,
                "net_debt": net_debt,
            },
        }

    @staticmethod
    def peg(eps: float, growth_rate: float, target_peg: float = 1.0) -> Dict:
        """PEG ratio valuation"""
        g = growth_rate * 100
        fair_pe = target_peg * g
        value = eps * fair_pe
        return {
            "method": "PEG估值法",
            "per_share_value": round(value, 2),
            "fair_pe": round(fair_pe, 1),
            "assumptions": {
                "eps": eps,
                "growth_rate": f"{growth_rate:.1%}",
                "target_peg": target_peg,
            },
        }

    @staticmethod
    def owner_earnings_valuation(
        owner_earnings: float,
        growth_rate: float,
        discount_rate: float = 0.10,
        shares_outstanding: float = 1.0,
    ) -> Dict:
        """Warren Buffett owner earnings valuation"""
        if discount_rate <= growth_rate:
            cap_rate = discount_rate + 0.02
        else:
            cap_rate = discount_rate - growth_rate

        value = owner_earnings / cap_rate
        per_share = value / shares_outstanding if shares_outstanding > 0 else 0
        return {
            "method": "股东盈余估值法",
            "total_value": round(value, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "owner_earnings": owner_earnings,
                "growth_rate": f"{growth_rate:.1%}",
                "discount_rate": f"{discount_rate:.1%}",
            },
        }

    @staticmethod
    def ddm(
        dividend_per_share: float,
        growth_rate: float,
        required_return: float = 0.10,
    ) -> Dict:
        """Dividend Discount Model (Gordon Growth)"""
        if required_return <= growth_rate:
            return {
                "method": "DDM股利折现模型",
                "per_share_value": None,
                "note": "Required return must exceed growth rate",
            }

        value = dividend_per_share * (1 + growth_rate) / (required_return - growth_rate)
        return {
            "method": "DDM股利折现模型",
            "per_share_value": round(value, 2),
            "assumptions": {
                "dividend_per_share": dividend_per_share,
                "growth_rate": f"{growth_rate:.1%}",
                "required_return": f"{required_return:.1%}",
            },
        }

    @staticmethod
    def replacement_cost(total_assets: float, intangibles: float, liabilities: float, shares: float) -> Dict:
        """Replacement/liquidation cost valuation"""
        nav = total_assets - intangibles - liabilities
        per_share = nav / shares if shares > 0 else 0
        return {
            "method": "重置成本法",
            "net_asset_value": round(nav, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "total_assets": total_assets,
                "intangibles_excluded": intangibles,
                "total_liabilities": liabilities,
            },
        }

    @staticmethod
    def cross_validate(valuations: List[Dict]) -> Dict:
        """
        Cross-validate multiple valuation results
        Returns median, mean, range, and confidence assessment
        """
        values = [
            v["per_share_value"]
            for v in valuations
            if v.get("per_share_value") is not None and v["per_share_value"] > 0
        ]

        if not values:
            return {"error": "No valid valuations to cross-validate"}

        values_sorted = sorted(values)
        n = len(values_sorted)
        median = (
            values_sorted[n // 2]
            if n % 2 == 1
            else (values_sorted[n // 2 - 1] + values_sorted[n // 2]) / 2
        )

        mean = sum(values) / n
        spread = (max(values) - min(values)) / median if median > 0 else 0

        confidence = "high" if spread < 0.3 else "medium" if spread < 0.6 else "low"

        return {
            "method_count": n,
            "median": round(median, 2),
            "mean": round(mean, 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "spread": f"{spread:.1%}",
            "confidence": confidence,
            "all_values": [round(v, 2) for v in values_sorted],
        }
