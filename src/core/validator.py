"""
Data Validator — cross-validation, source scoring, and confidence assessment.

Ensures all financial data in research reports meets credibility standards:
  - Multi-source cross-validation
  - Source tier scoring
  - Consistency checks between data points
  - Confidence level assessment
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional


class DataValidator:
    """
    Validates and scores data quality for investment research.

    Usage:
        validator = DataValidator()
        result = validator.validate_data_point(
            value=38.3, unit="B", label="Revenue",
            sources=[
                {"name": "SEC 10-Q", "url": "https://sec.gov/...", "date": "2026-03-15", "value": 38.3},
                {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/...", "date": "2026-03-15", "value": 38.2},
            ]
        )
    """

    # Tier labels
    TIER_LABELS = {
        1: "Tier 1 (官方/监管)",
        2: "Tier 2 (主流财经)",
        3: "Tier 3 (分析参考)",
        4: "Tier 4 (需交叉验证)",
    }

    def __init__(self, source_tiers: Optional[Dict[str, List[str]]] = None):
        """
        Args:
            source_tiers: Custom tier domain mapping. If None, loads from config.
        """
        if source_tiers is None:
            try:
                from src.config import get_source_tiers
                source_tiers = get_source_tiers()
            except Exception:
                source_tiers = {}
        self._tier_domains = source_tiers
        self.validation_log: List[Dict] = []

    def classify_source(self, url: str) -> int:
        """Classify a URL into a reliability tier (1=most reliable, 4=needs verification)."""
        url_lower = (url or "").lower()
        tier_keys = ["tier1", "tier2", "tier3"]
        for i, key in enumerate(tier_keys, 1):
            domains = self._tier_domains.get(key, [])
            for domain in domains:
                if domain.lower() in url_lower:
                    return i
        return 4

    def get_tier_label(self, tier: int) -> str:
        return self.TIER_LABELS.get(tier, self.TIER_LABELS[4])

    def validate_data_point(
        self,
        value: Any,
        label: str,
        sources: List[Dict],
        tolerance: float = 0.05,
    ) -> Dict:
        """
        Validate a single data point against multiple sources.

        Args:
            value: The reported value
            label: Description (e.g., "Revenue", "PE Ratio")
            sources: List of source dicts, each with keys:
                     name, url, date (str), value (numeric)
            tolerance: Acceptable relative difference between sources (default 5%)

        Returns:
            Dict with validation result: status, confidence, details
        """
        if not sources:
            result = {
                "label": label,
                "value": value,
                "status": "unverified",
                "confidence": "low",
                "source_count": 0,
                "message": f"No sources provided for '{label}'. Mark as unverified.",
                "citation": f"⚠️ 数据缺失 — {label} 未从可信来源获取到数据",
            }
            self.validation_log.append(result)
            return result

        # Score each source
        scored_sources = []
        for src in sources:
            tier = self.classify_source(src.get("url", ""))
            scored_sources.append({**src, "tier": tier, "tier_label": self.get_tier_label(tier)})

        # Sort by tier (lower = more credible)
        scored_sources.sort(key=lambda s: s["tier"])
        best_tier = scored_sources[0]["tier"]

        # Cross-validation: check numeric consistency
        numeric_values = [s.get("value") for s in scored_sources if _is_numeric(s.get("value"))]
        consistency = "consistent"
        max_deviation = 0.0

        if len(numeric_values) >= 2:
            ref = numeric_values[0]
            if ref != 0:
                deviations = [abs(v - ref) / abs(ref) for v in numeric_values[1:]]
                max_deviation = max(deviations) if deviations else 0
                if max_deviation > tolerance:
                    consistency = "inconsistent"

        # Determine confidence
        n_sources = len(scored_sources)
        if n_sources >= 2 and best_tier <= 2 and consistency == "consistent":
            confidence = "high"
            status = "verified"
        elif n_sources >= 2 and consistency == "consistent":
            confidence = "medium"
            status = "verified"
        elif n_sources == 1 and best_tier <= 2:
            confidence = "medium"
            status = "single_source"
        elif n_sources == 1:
            confidence = "low"
            status = "single_source"
        else:
            confidence = "low"
            status = "inconsistent"

        # Generate proper citation
        primary = scored_sources[0]
        date_str = primary.get("date", datetime.now().strftime("%Y-%m-%d"))
        citation = f"[来源: {primary['name']} | 日期: {date_str}]"
        if n_sources == 1:
            citation += " [单源未交叉验证]"

        result = {
            "label": label,
            "value": value,
            "status": status,
            "confidence": confidence,
            "source_count": n_sources,
            "best_tier": best_tier,
            "consistency": consistency,
            "max_deviation": f"{max_deviation:.1%}" if numeric_values else "N/A",
            "citation": citation,
            "sources": scored_sources,
        }

        if consistency == "inconsistent":
            result["warning"] = (
                f"Sources disagree on '{label}': "
                f"values = {numeric_values}, max deviation = {max_deviation:.1%}. "
                f"Manual verification required."
            )

        self.validation_log.append(result)
        return result

    def validate_search_results(self, results: List[Dict]) -> Dict:
        """
        Score and rank a batch of search results by source credibility.

        Args:
            results: List of search result dicts, each having 'url' and 'title' keys.

        Returns:
            Dict with scored results and overall quality assessment.
        """
        scored = []
        tier_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for r in results:
            url = r.get("url", "")
            tier = self.classify_source(url)
            tier_counts[tier] += 1
            scored.append({
                **r,
                "tier": tier,
                "tier_label": self.get_tier_label(tier),
            })

        # Sort by tier (most credible first)
        scored.sort(key=lambda s: s["tier"])

        total = len(scored)
        high_quality = tier_counts[1] + tier_counts[2]
        quality_ratio = high_quality / total if total > 0 else 0

        if quality_ratio >= 0.5:
            overall = "high"
        elif quality_ratio >= 0.2:
            overall = "medium"
        else:
            overall = "low"

        return {
            "total_results": total,
            "tier_distribution": tier_counts,
            "high_quality_ratio": f"{quality_ratio:.0%}",
            "overall_quality": overall,
            "scored_results": scored,
            "recommendation": _quality_recommendation(overall, tier_counts),
        }

    def assess_report_confidence(self, validation_results: List[Dict]) -> Dict:
        """
        Aggregate validation results into an overall report confidence score.

        Args:
            validation_results: List of validate_data_point() results.

        Returns:
            Overall confidence assessment.
        """
        if not validation_results:
            return {
                "overall_confidence": "unknown",
                "message": "No data points have been validated.",
            }

        verified = [r for r in validation_results if r.get("status") == "verified"]
        single_source = [r for r in validation_results if r.get("status") == "single_source"]
        unverified = [r for r in validation_results if r.get("status") == "unverified"]
        inconsistent = [r for r in validation_results if r.get("status") == "inconsistent"]

        total = len(validation_results)
        verified_ratio = len(verified) / total

        if verified_ratio >= 0.8 and not inconsistent:
            overall = "high"
        elif verified_ratio >= 0.5 and len(inconsistent) <= 1:
            overall = "medium"
        else:
            overall = "low"

        return {
            "overall_confidence": overall,
            "total_data_points": total,
            "verified_count": len(verified),
            "single_source_count": len(single_source),
            "unverified_count": len(unverified),
            "inconsistent_count": len(inconsistent),
            "verified_ratio": f"{verified_ratio:.0%}",
            "unverified_labels": [r["label"] for r in unverified],
            "inconsistent_labels": [r["label"] for r in inconsistent],
            "recommendation": _confidence_recommendation(overall, len(unverified), len(inconsistent)),
        }

    def get_validation_summary(self) -> str:
        """Generate a human-readable validation summary from the log."""
        if not self.validation_log:
            return "No validations performed."

        assessment = self.assess_report_confidence(self.validation_log)
        lines = [
            "═══ Data Validation Summary / 数据验证摘要 ═══",
            f"Total data points: {assessment['total_data_points']}",
            f"Verified (cross-validated): {assessment['verified_count']}",
            f"Single source: {assessment['single_source_count']}",
            f"Unverified: {assessment['unverified_count']}",
            f"Inconsistent: {assessment['inconsistent_count']}",
            f"Overall confidence: {assessment['overall_confidence'].upper()}",
        ]

        if assessment["unverified_labels"]:
            lines.append(f"Unverified fields: {', '.join(assessment['unverified_labels'])}")
        if assessment["inconsistent_labels"]:
            lines.append(f"Inconsistent fields: {', '.join(assessment['inconsistent_labels'])}")
        lines.append(f"Recommendation: {assessment['recommendation']}")

        return "\n".join(lines)


# ----------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------

def _is_numeric(value: Any) -> bool:
    """Check if a value is numeric."""
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value.replace(",", ""))
            return True
        except ValueError:
            return False
    return False


def _quality_recommendation(quality: str, tier_counts: Dict[int, int]) -> str:
    if quality == "high":
        return "Search results include strong Tier 1-2 sources. Suitable for report use."
    if quality == "medium":
        return (
            f"Limited high-quality sources (Tier 1: {tier_counts[1]}, Tier 2: {tier_counts[2]}). "
            "Consider additional targeted searches for Tier 1-2 data."
        )
    return (
        f"Most results are Tier 3-4 ({tier_counts[3] + tier_counts[4]} of {sum(tier_counts.values())}). "
        "Do NOT use for key financial figures without cross-validation from Tier 1-2 sources."
    )


def _confidence_recommendation(level: str, unverified: int, inconsistent: int) -> str:
    if level == "high":
        return "Data quality is strong. Report is suitable for export."
    if level == "medium":
        issues = []
        if unverified > 0:
            issues.append(f"{unverified} unverified data points need sources")
        if inconsistent > 0:
            issues.append(f"{inconsistent} inconsistent data points need manual review")
        return "Moderate confidence. " + "; ".join(issues) + "."
    return (
        f"LOW confidence — {unverified} unverified, {inconsistent} inconsistent data points. "
        "Do NOT export or use for investment decisions without fixing all issues."
    )
