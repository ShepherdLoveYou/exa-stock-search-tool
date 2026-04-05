"""
Data Freshness Checker - Validates timeliness and reliability of research data
Ensures investment reports use current and accurate information
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


# Data freshness thresholds (in days)
FRESHNESS_THRESHOLDS = {
    "stock_price": 1,
    "financial_statements": 120,     # Quarterly reporting cycle
    "analyst_ratings": 30,
    "insider_trading": 14,
    "news_sentiment": 3,
    "market_data": 1,
    "industry_report": 180,
    "company_filing": 90,
    "earnings_call": 120,
    "management_guidance": 120,
    "tvl_data": 1,                   # Web3 on-chain data
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

# Freshness status labels
STATUS_FRESH = "fresh"         # Within threshold
STATUS_AGING = "aging"         # 1-2x threshold
STATUS_STALE = "stale"         # >2x threshold
STATUS_UNKNOWN = "unknown"     # No date available


class DataFreshnessChecker:
    """
    Validates the timeliness of data used in investment research reports
    Flags stale data that may lead to incorrect investment decisions
    """

    def __init__(self, reference_date: Optional[datetime] = None):
        """
        Args:
            reference_date: Date to check freshness against (defaults to now)
        """
        self.reference_date = reference_date or datetime.now()
        self.findings: List[Dict] = []

    def check_data_point(
        self,
        category: str,
        source: str,
        data_date: Optional[datetime] = None,
        date_string: Optional[str] = None,
    ) -> Dict:
        """
        Check freshness of a single data point

        Args:
            category: Data category key (must match FRESHNESS_THRESHOLDS)
            source: Name of the data source
            data_date: DateTime object of the data
            date_string: Alternative: parse date from string

        Returns:
            Dict with status, age_days, threshold, and recommendation
        """
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
        threshold = FRESHNESS_THRESHOLDS.get(category, 30)

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
            recommendation = f"Data is STALE - must refresh before making investment decisions"

        result = {
            "category": category,
            "source": source,
            "data_date": data_date.isoformat(),
            "status": status,
            "age_days": age,
            "threshold_days": threshold,
            "recommendation": recommendation,
            "status_label": label,
        }
        self.findings.append(result)
        return result

    def check_report(self, report_content: str) -> Dict:
        """
        Scan a report for date references and check data freshness

        Args:
            report_content: Markdown content of the research report

        Returns:
            Dict with overall assessment and per-section findings
        """
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
            matches = re.finditer(pattern, report_content)
            for match in matches:
                parsed = self._parse_date(match.group(1))
                if parsed:
                    # Find surrounding context
                    start = max(0, match.start() - 80)
                    end = min(len(report_content), match.end() + 80)
                    context = report_content[start:end].strip()
                    found_dates.append({
                        "date_string": match.group(1),
                        "parsed_date": parsed,
                        "context": context,
                    })

        # Check each found date
        section_findings = []
        for item in found_dates:
            category = self._infer_category(item["context"])
            check = self.check_data_point(
                category=category,
                source="report_scan",
                data_date=item["parsed_date"],
            )
            check["context"] = item["context"]
            check["date_string"] = item["date_string"]
            section_findings.append(check)

        # Overall assessment
        stale_count = sum(1 for f in section_findings if f["status"] == STATUS_STALE)
        aging_count = sum(1 for f in section_findings if f["status"] == STATUS_AGING)
        fresh_count = sum(1 for f in section_findings if f["status"] == STATUS_FRESH)
        total = len(section_findings)

        if stale_count > 0:
            overall = "NEEDS_UPDATE"
            overall_label = f"**报告需要更新** - {stale_count}项数据已过期"
        elif aging_count > total * 0.3:
            overall = "AGING"
            overall_label = f"报告数据老化 - {aging_count}项数据接近过期"
        elif total == 0:
            overall = "NO_DATES"
            overall_label = "报告中未找到日期引用 - 无法自动验证时效性"
        else:
            overall = "CURRENT"
            overall_label = f"报告数据新鲜 - {fresh_count}/{total}项数据在有效期内"

        return {
            "overall_status": overall,
            "overall_label": overall_label,
            "total_data_points": total,
            "fresh_count": fresh_count,
            "aging_count": aging_count,
            "stale_count": stale_count,
            "findings": section_findings,
            "checked_at": self.reference_date.isoformat(),
        }

    def check_unfilled_fields(self, report_content: str) -> Dict:
        """
        Check for unfilled template placeholders in a report

        Args:
            report_content: Markdown content of the research report

        Returns:
            Dict with unfilled fields and completeness percentage
        """
        placeholders = re.findall(r'\{\{([A-Z_0-9]+)\}\}', report_content)
        unique_unfilled = list(set(placeholders))

        # Estimate total fields by counting section headers
        section_count = len(re.findall(r'^#{1,4}\s+', report_content, re.MULTILINE))

        total_estimated = section_count * 2  # rough estimate
        filled_estimated = max(0, total_estimated - len(unique_unfilled))
        completeness = (
            filled_estimated / total_estimated * 100 if total_estimated > 0 else 0
        )

        # Categorize unfilled fields by priority
        critical_fields = [
            f for f in unique_unfilled
            if any(kw in f for kw in [
                "VAL_", "INTRINSIC", "PRICE", "SCORE", "TOTAL", "PASS",
                "DECISION", "POSITION",
            ])
        ]
        important_fields = [
            f for f in unique_unfilled
            if f not in critical_fields and any(kw in f for kw in [
                "ANALYSIS", "REVENUE", "MARGIN", "GROWTH", "MARKET",
                "FCF", "DEBT", "ROIC", "ROE", "TVL", "FEE",
            ])
        ]
        supplementary_fields = [
            f for f in unique_unfilled
            if f not in critical_fields and f not in important_fields
        ]

        return {
            "total_unfilled": len(unique_unfilled),
            "completeness_estimate": f"{completeness:.0f}%",
            "critical_unfilled": sorted(critical_fields),
            "important_unfilled": sorted(important_fields),
            "supplementary_unfilled": sorted(supplementary_fields),
            "all_unfilled": sorted(unique_unfilled),
        }

    def generate_freshness_report(self) -> str:
        """
        Generate a markdown summary of all freshness findings

        Returns:
            Markdown formatted freshness report
        """
        if not self.findings:
            return "No data freshness checks have been performed"

        lines = [
            "## Data Freshness Report / 数据时效性报告",
            "",
            f"**检查时间**: {self.reference_date.strftime('%Y-%m-%d %H:%M')}",
            "",
            "| 数据类别 | 来源 | 数据日期 | 状态 | 建议 |",
            "|----------|------|----------|------|------|",
        ]

        for f in self.findings:
            date_str = f.get("data_date", "N/A")
            if isinstance(date_str, str) and "T" in date_str:
                date_str = date_str[:10]
            lines.append(
                f"| {f['category']} | {f['source']} | {date_str} "
                f"| {f['status_label']} | {f['recommendation']} |"
            )

        stale = [f for f in self.findings if f["status"] == STATUS_STALE]
        if stale:
            lines.extend([
                "",
                "### Stale Data Alerts / 过期数据警告",
                "",
            ])
            for s in stale:
                lines.append(
                    f"- **{s['category']}** from {s['source']}: "
                    f"{s['age_days']} days old (threshold: {s['threshold_days']} days)"
                )

        return "\n".join(lines)

    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse various date formats"""
        formats = [
            "%Y-%m-%d",
            "%Y年%m月%d日",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%B %d, %Y",
            "%b %d, %Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_string.strip(), fmt)
            except ValueError:
                continue

        # Handle quarterly formats
        q_match = re.match(r'Q([1-4])\s*(\d{4})', date_string)
        if q_match:
            quarter, year = int(q_match.group(1)), int(q_match.group(2))
            month = (quarter - 1) * 3 + 1
            return datetime(year, month, 1)

        q_match2 = re.match(r'(\d{4})\s*Q([1-4])', date_string)
        if q_match2:
            year, quarter = int(q_match2.group(1)), int(q_match2.group(2))
            month = (quarter - 1) * 3 + 1
            return datetime(year, month, 1)

        fy_match = re.match(r'FY\s*(\d{4})', date_string)
        if fy_match:
            return datetime(int(fy_match.group(1)), 1, 1)

        return None

    def _infer_category(self, context: str) -> str:
        """Infer data category from surrounding context text"""
        context_lower = context.lower()

        category_keywords = {
            "stock_price": ["stock price", "share price", "market price", "股价", "收盘价"],
            "financial_statements": ["revenue", "earnings", "income", "balance sheet",
                                      "营收", "利润", "财报", "资产负债"],
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

        return "news_sentiment"  # default
