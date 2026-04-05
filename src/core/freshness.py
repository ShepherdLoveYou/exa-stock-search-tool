"""
src.core.freshness — Data Freshness Checker
Re-export from the original module for the new package layout
"""

# The freshness checker lives at src/data_freshness_checker.py
# We re-export it here for the core package interface
import re
from datetime import datetime
from typing import Dict, List, Optional


FRESHNESS_THRESHOLDS = {
    "stock_price": 1,
    "financial_statements": 120,
    "analyst_ratings": 30,
    "insider_trading": 14,
    "news_sentiment": 3,
    "market_data": 1,
    "industry_report": 180,
    "company_filing": 90,
    "earnings_call": 120,
    "management_guidance": 120,
    "tvl_data": 1,
    "protocol_revenue": 7,
    "token_unlock": 30,
    "governance_proposal": 14,
    "github_activity": 7,
    "community_metrics": 7,
    "treasury_balance": 7,
    "macro_economic": 30,
    "regulatory_filing": 90,
    "audit_report": 365,
}

STATUS_FRESH = "fresh"
STATUS_AGING = "aging"
STATUS_STALE = "stale"
STATUS_UNKNOWN = "unknown"


class DataFreshnessChecker:
    """Validates the timeliness of data used in investment research reports"""

    def __init__(self, reference_date: Optional[datetime] = None):
        self.reference_date = reference_date or datetime.now()
        self.findings: List[Dict] = []
        # Load custom thresholds from config if available
        try:
            from src.config import get_freshness_thresholds
            self._thresholds = get_freshness_thresholds()
        except Exception:
            self._thresholds = FRESHNESS_THRESHOLDS

    def check_data_point(
        self,
        category: str,
        source: str,
        data_date: Optional[datetime] = None,
        date_string: Optional[str] = None,
    ) -> Dict:
        if data_date is None and date_string:
            data_date = self._parse_date(date_string)

        if data_date is None:
            result = {
                "category": category,
                "source": source,
                "status": STATUS_UNKNOWN,
                "age_days": None,
                "threshold_days": FRESHNESS_THRESHOLDS.get(category, 30),
                "recommendation": "Unable to determine data date - manual verification required",
                "status_label": "unknown - 无法确定数据日期",
            }
            self.findings.append(result)
            return result

        age = (self.reference_date - data_date).days
        threshold = self._thresholds.get(category, 30)

        if age <= threshold:
            status = STATUS_FRESH
            label = f"fresh - 数据新鲜（{age}天前）"
            recommendation = "Data is current and reliable"
        elif age <= threshold * 2:
            status = STATUS_AGING
            label = f"aging - 数据老化（{age}天前，阈值{threshold}天）"
            recommendation = f"Data is aging - consider refreshing, threshold is {threshold} days"
        else:
            status = STATUS_STALE
            label = f"**stale** - 数据过期（{age}天前，阈值{threshold}天）"
            recommendation = "Data is STALE - must refresh before making investment decisions"

        result = {
            "category": category, "source": source,
            "data_date": data_date.isoformat(), "status": status,
            "age_days": age, "threshold_days": threshold,
            "recommendation": recommendation, "status_label": label,
        }
        self.findings.append(result)
        return result

    def check_report(self, report_content: str) -> Dict:
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(Q[1-4]\s*\d{4})',
            r'(FY\s*\d{4})',
            r'(\d{4}\s*Q[1-4])',
        ]

        found_dates = []
        for pattern in date_patterns:
            for match in re.finditer(pattern, report_content):
                parsed = self._parse_date(match.group(1))
                if parsed:
                    start = max(0, match.start() - 80)
                    end = min(len(report_content), match.end() + 80)
                    context = report_content[start:end].strip()
                    found_dates.append({
                        "date_string": match.group(1),
                        "parsed_date": parsed,
                        "context": context,
                    })

        section_findings = []
        for item in found_dates:
            category = self._infer_category(item["context"])
            check = self.check_data_point(
                category=category, source="report_scan",
                data_date=item["parsed_date"],
            )
            check["context"] = item["context"]
            check["date_string"] = item["date_string"]
            section_findings.append(check)

        stale_count = sum(1 for f in section_findings if f["status"] == STATUS_STALE)
        aging_count = sum(1 for f in section_findings if f["status"] == STATUS_AGING)
        fresh_count = sum(1 for f in section_findings if f["status"] == STATUS_FRESH)
        total = len(section_findings)

        if stale_count > 0:
            overall, overall_label = "NEEDS_UPDATE", f"**报告需要更新** - {stale_count}项数据已过期"
        elif aging_count > total * 0.3:
            overall, overall_label = "AGING", f"报告数据老化 - {aging_count}项数据接近过期"
        elif total == 0:
            overall, overall_label = "NO_DATES", "报告中未找到日期引用 - 无法自动验证时效性"
        else:
            overall, overall_label = "CURRENT", f"报告数据新鲜 - {fresh_count}/{total}项数据在有效期内"

        return {
            "overall_status": overall, "overall_label": overall_label,
            "total_data_points": total, "fresh_count": fresh_count,
            "aging_count": aging_count, "stale_count": stale_count,
            "findings": section_findings,
            "checked_at": self.reference_date.isoformat(),
        }

    def check_unfilled_fields(self, report_content: str) -> Dict:
        placeholders = re.findall(r'\{\{([A-Z_0-9]+)\}\}', report_content)
        unique_unfilled = list(set(placeholders))
        section_count = len(re.findall(r'^#{1,4}\s+', report_content, re.MULTILINE))
        total_estimated = section_count * 2
        filled_estimated = max(0, total_estimated - len(unique_unfilled))
        completeness = filled_estimated / total_estimated * 100 if total_estimated > 0 else 0

        critical_fields = [f for f in unique_unfilled if any(kw in f for kw in [
            "VAL_", "INTRINSIC", "PRICE", "SCORE", "TOTAL", "PASS", "DECISION", "POSITION"])]
        important_fields = [f for f in unique_unfilled if f not in critical_fields and any(kw in f for kw in [
            "ANALYSIS", "REVENUE", "MARGIN", "GROWTH", "MARKET", "FCF", "DEBT", "ROIC", "ROE", "TVL", "FEE"])]
        supplementary_fields = [f for f in unique_unfilled if f not in critical_fields and f not in important_fields]

        return {
            "total_unfilled": len(unique_unfilled),
            "completeness_estimate": f"{completeness:.0f}%",
            "critical_unfilled": sorted(critical_fields),
            "important_unfilled": sorted(important_fields),
            "supplementary_unfilled": sorted(supplementary_fields),
            "all_unfilled": sorted(unique_unfilled),
        }

    def generate_freshness_report(self) -> str:
        if not self.findings:
            return "No data freshness checks have been performed"
        lines = [
            "## Data Freshness Report / 数据时效性报告", "",
            f"**检查时间**: {self.reference_date.strftime('%Y-%m-%d %H:%M')}", "",
            "| 数据类别 | 来源 | 数据日期 | 状态 | 建议 |",
            "|----------|------|----------|------|------|",
        ]
        for f in self.findings:
            date_str = f.get("data_date", "N/A")
            if isinstance(date_str, str) and "T" in date_str:
                date_str = date_str[:10]
            lines.append(f"| {f['category']} | {f['source']} | {date_str} | {f['status_label']} | {f['recommendation']} |")
        stale = [f for f in self.findings if f["status"] == STATUS_STALE]
        if stale:
            lines.extend(["", "### Stale Data Alerts / 过期数据警告", ""])
            for s in stale:
                lines.append(f"- **{s['category']}** from {s['source']}: {s['age_days']} days old (threshold: {s['threshold_days']} days)")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Source citation audit — detect data points without proper sourcing
    # ------------------------------------------------------------------

    # Known reliable source domains (Tier 1-2)
    TIER1_DOMAINS = [
        "sec.gov", "edgar", "hkex", "csrc", "sse.com", "szse.cn",
        "federalreserve.gov", "fred.stlouisfed.org", "treasury.gov",
        "defillama", "etherscan", "dune.com",
    ]
    TIER2_DOMAINS = [
        "fmp", "finnhub", "tushare", "akshare", "coingecko",
        "stockanalysis.com", "marketbeat.com", "yahoo", "bloomberg",
        "reuters", "wsj.com", "cnbc.com",
    ]

    # Patterns that indicate properly cited data
    _CITATION_PATTERN = re.compile(
        r'\[(?:来源|来自|Source|source|数据来源)\s*[:：]\s*[^\]]{3,}(?:\|[^\]]+)?\]'
    )
    # Numerical data that SHOULD have a citation nearby
    _NUMERIC_DATA_PATTERN = re.compile(
        r'(?:[$￥¥€£][\d,.]+[BMKTbmkt万亿]*'  # currency amounts
        r'|[\d,.]+\s*(?:亿|万|billion|million|trillion|B|M|K|%)'  # numbers with units
        r'|(?:营收|收入|利润|净利|EPS|市值|Market\s*Cap|Revenue|Net\s*Income|FCF|EBITDA)'
        r'\s*[:：]?\s*[$￥]?[\d,.]+)'  # labeled financials
    )

    def audit_source_citations(self, report_content: str) -> Dict:
        """
        Scan a filled report for data points that lack proper source citations.

        Returns a dict with:
          - total_data_points: count of numeric/financial data references found
          - cited_count: how many have a nearby [来源: ...] tag
          - uncited_count: how many lack citation
          - uncited_items: list of uncited data snippets for manual review
          - hallucination_risk: "low" / "medium" / "high"
        """
        lines = report_content.split("\n")
        total_points = 0
        cited = 0
        uncited_items = []

        for i, line in enumerate(lines):
            # Find numeric/financial data in this line
            for match in self._NUMERIC_DATA_PATTERN.finditer(line):
                total_points += 1
                # Check if citation exists on this line or next 2 lines
                context_block = "\n".join(lines[max(0, i - 1):min(len(lines), i + 3)])
                if self._CITATION_PATTERN.search(context_block):
                    cited += 1
                else:
                    # Also accept markdown-style inline citations like (Source: ...)
                    alt_cite = re.search(
                        r'(?:\((?:来源|Source)\s*[:：][^)]+\)|【[^】]*来源[^】]*】)',
                        context_block
                    )
                    if alt_cite:
                        cited += 1
                    else:
                        snippet = line.strip()[:120]
                        if snippet not in [u["snippet"] for u in uncited_items]:
                            uncited_items.append({
                                "line": i + 1,
                                "snippet": snippet,
                                "data_match": match.group()[:60],
                            })

        uncited_count = total_points - cited

        if total_points == 0:
            risk = "unknown"
        elif uncited_count / total_points > 0.5:
            risk = "high"
        elif uncited_count / total_points > 0.2:
            risk = "medium"
        else:
            risk = "low"

        return {
            "total_data_points": total_points,
            "cited_count": cited,
            "uncited_count": uncited_count,
            "citation_rate": f"{cited / total_points:.0%}" if total_points > 0 else "N/A",
            "hallucination_risk": risk,
            "uncited_items": uncited_items[:30],  # cap at 30
            "recommendation": self._citation_recommendation(risk, uncited_count),
        }

    @staticmethod
    def _citation_recommendation(risk: str, uncited: int) -> str:
        if risk == "high":
            return (
                f"⚠️ 高幻觉风险: {uncited}个数据点缺少来源标注。"
                "请勿直接使用此报告做投资决策。必须为所有财务数据补充 [来源: XX | 日期: YYYY-MM-DD] 标注。"
            )
        if risk == "medium":
            return (
                f"⚠️ 中等风险: {uncited}个数据点缺少来源标注。"
                "建议对关键财务数据进行交叉验证并补充来源。"
            )
        if risk == "low":
            return "✅ 数据来源标注良好。建议定期复核关键数据的时效性。"
        return "无法评估 — 报告中未发现可识别的财务数据点。"

    def _parse_date(self, date_string: str) -> Optional[datetime]:
        formats = ["%Y-%m-%d", "%Y年%m月%d日", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%B %d, %Y", "%b %d, %Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_string.strip(), fmt)
            except ValueError:
                continue
        q_match = re.match(r'Q([1-4])\s*(\d{4})', date_string)
        if q_match:
            quarter, year = int(q_match.group(1)), int(q_match.group(2))
            return datetime(year, (quarter - 1) * 3 + 1, 1)
        q_match2 = re.match(r'(\d{4})\s*Q([1-4])', date_string)
        if q_match2:
            year, quarter = int(q_match2.group(1)), int(q_match2.group(2))
            return datetime(year, (quarter - 1) * 3 + 1, 1)
        fy_match = re.match(r'FY\s*(\d{4})', date_string)
        if fy_match:
            return datetime(int(fy_match.group(1)), 1, 1)
        return None

    def _infer_category(self, context: str) -> str:
        context_lower = context.lower()
        category_keywords = {
            "stock_price": ["stock price", "share price", "market price", "股价", "收盘价"],
            "financial_statements": ["revenue", "earnings", "income", "balance sheet", "营收", "利润", "财报", "资产负债"],
            "analyst_ratings": ["analyst", "rating", "target price", "分析师", "评级"],
            "insider_trading": ["insider", "director", "officer", "买入", "减持", "增持"],
            "news_sentiment": ["news", "article", "report", "新闻", "报道"],
            "tvl_data": ["tvl", "total value locked", "锁仓"],
            "protocol_revenue": ["protocol revenue", "fee", "协议收入", "手续费"],
            "token_unlock": ["unlock", "vesting", "解锁", "释放"],
            "governance_proposal": ["governance", "proposal", "vote", "治理", "提案"],
            "github_activity": ["github", "commit", "development", "开发"],
            "community_metrics": ["community", "discord", "telegram", "社区"],
            "treasury_balance": ["treasury", "dao", "金库"],
            "earnings_call": ["earnings call", "conference call", "电话会议"],
            "industry_report": ["industry", "sector", "market size", "行业", "市场规模"],
        }
        for category, keywords in category_keywords.items():
            if any(kw in context_lower for kw in keywords):
                return category
        return "news_sentiment"
