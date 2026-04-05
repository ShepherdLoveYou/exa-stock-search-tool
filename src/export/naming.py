"""
Templated report file naming
Pattern: {date}_{ticker}_{framework}_{id}.{ext}
"""

import re
from datetime import datetime
from typing import Optional


# Framework labels for file names
FRAMEWORK_LABELS = {
    "mature": "mature",
    "growth": "growth",
    "web3": "web3",
}


class ReportNaming:
    """Generate standardized file names for research reports"""

    DEFAULT_PATTERN = "{date}_{ticker}_{framework}_{report_id}"

    @staticmethod
    def generate(
        ticker: str,
        framework: str,
        report_id: str,
        pattern: Optional[str] = None,
        date: Optional[datetime] = None,
    ) -> str:
        """
        Generate a sanitized base filename (no extension).

        Args:
            ticker: Stock ticker / token symbol
            framework: Framework type (mature/growth/web3)
            report_id: UUID or short ID for uniqueness
            pattern: Custom naming pattern with {date}, {ticker}, {framework}, {report_id} placeholders
            date: Report date (defaults to today)

        Returns:
            Sanitized filename string without extension
        """
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y%m%d")
        fw_label = FRAMEWORK_LABELS.get(framework, framework)
        short_id = report_id[:8] if len(report_id) > 8 else report_id

        template = pattern or ReportNaming.DEFAULT_PATTERN
        name = template.format(
            date=date_str,
            ticker=ticker.upper(),
            framework=fw_label,
            report_id=short_id,
        )

        # Sanitize: only keep alphanumeric, hyphens, underscores
        name = re.sub(r'[^\w\-]', '_', name)
        return name

    @staticmethod
    def with_extension(base_name: str, ext: str) -> str:
        """Append extension, ensuring single dot"""
        ext = ext.lstrip(".")
        return f"{base_name}.{ext}"
