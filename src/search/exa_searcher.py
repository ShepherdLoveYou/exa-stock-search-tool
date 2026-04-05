"""Stock market information searcher using Exa API"""

import time
import logging
from typing import Dict, List, Optional

from exa_py import Exa

from src.config import get_api_key, get_search_config, get_network_config, get_source_tiers

logger = logging.getLogger(__name__)


class StockSearcher:
    """Search for stock market information using Exa API with retry and validation."""

    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or get_api_key("exa")
        self.exa = Exa(api_key=api_key)

        search_cfg = get_search_config()
        self.search_type = search_cfg["type"]
        self.num_results = search_cfg["num_results"]
        self.max_characters = search_cfg["max_characters"]
        self.content_mode = search_cfg["content_mode"]

        net_cfg = get_network_config()
        self.max_retries = net_cfg["max_retries"]
        self.retry_delay = net_cfg["retry_delay"]
        self.timeout = net_cfg["timeout"]

        # Load source tiers from config
        tiers = get_source_tiers()
        self._tier1 = tiers.get("tier1", self.TIER1_DOMAINS)
        self._tier2 = tiers.get("tier2", self.TIER2_DOMAINS)
        self._tier3 = tiers.get("tier3", self.TIER3_DOMAINS)

    # ------------------------------------------------------------------
    # Search methods
    # ------------------------------------------------------------------

    def search_stock_news(self, ticker: str, num_results: int = 0, include_highlights: bool = True) -> Dict:
        num_results = num_results or self.num_results
        query = f"{ticker} stock news latest developments"
        kwargs = {"type": self.search_type, "num_results": num_results}
        if include_highlights and self.content_mode == "highlights":
            kwargs["highlights"] = {"max_characters": self.max_characters}
        results = self._search_with_retry(query, **kwargs)
        return {"ticker": ticker, "query": query, "total_results": len(results.results), "results": results.results}

    def search_market_analysis(self, topic: str, num_results: int = 0) -> Dict:
        num_results = num_results or self.num_results
        query = f"{topic} market analysis stock market trends"
        results = self._search_with_retry(
            query, type=self.search_type, num_results=num_results,
            highlights={"max_characters": self.max_characters},
        )
        return {"topic": topic, "query": query, "total_results": len(results.results), "results": results.results}

    def search_company_info(self, company_name: str, num_results: int = 0) -> Dict:
        num_results = num_results or self.num_results
        query = f"{company_name} company information earnings reports"
        results = self._search_with_retry(
            query, type=self.search_type, num_results=num_results,
            highlights={"max_characters": self.max_characters},
        )
        return {"company": company_name, "query": query, "total_results": len(results.results), "results": results.results}

    def search_with_deep_research(self, query: str, num_results: int = 0) -> Dict:
        num_results = num_results or self.num_results
        results = self._search_with_retry(
            query, type="deep", num_results=num_results,
            text={"max_characters": 20000},
        )
        return {"query": query, "search_type": "deep", "total_results": len(results.results), "results": results.results}

    # ------------------------------------------------------------------
    # Retry logic
    # ------------------------------------------------------------------

    def _search_with_retry(self, query: str, **kwargs):
        """Execute Exa search with automatic retry on transient failures."""
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.exa.search_and_contents(query, **kwargs)
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                # Don't retry on auth errors or invalid params
                if any(kw in error_str for kw in ["unauthorized", "invalid", "api key", "403", "401"]):
                    raise
                if attempt < self.max_retries:
                    wait = self.retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                    logger.warning(f"Search attempt {attempt} failed: {e}. Retrying in {wait:.1f}s...")
                    time.sleep(wait)
        raise last_error  # type: ignore[misc]

    # ------------------------------------------------------------------
    # Source reliability classification
    # ------------------------------------------------------------------

    # Fallback domain lists (used when config is empty)
    TIER1_DOMAINS = [
        "sec.gov", "hkex.com.hk", "csrc.gov.cn", "sse.com.cn", "szse.cn",
        "federalreserve.gov", "fred.stlouisfed.org", "treasury.gov",
        "bls.gov", "worldbank.org", "imf.org",
        "defillama.com", "etherscan.io", "dune.com", "bscscan.com", "solscan.io",
    ]
    TIER2_DOMAINS = [
        "stockanalysis.com", "marketbeat.com", "finance.yahoo.com",
        "bloomberg.com", "reuters.com", "wsj.com", "cnbc.com", "ft.com",
        "seekingalpha.com", "fool.com", "barrons.com",
        "coingecko.com", "coinmarketcap.com", "tradingview.com", "morningstar.com",
    ]
    TIER3_DOMAINS = [
        "investopedia.com", "thestreet.com", "benzinga.com",
        "zacks.com", "tipranks.com", "simplywall.st",
        "macrotrends.net", "gurufocus.com", "finviz.com",
    ]

    def classify_source_tier(self, url: str) -> str:
        """Classify a URL into reliability tiers."""
        url_lower = (url or "").lower()
        for domain in self._tier1:
            if domain.lower() in url_lower:
                return "Tier 1 (官方/监管)"
        for domain in self._tier2:
            if domain.lower() in url_lower:
                return "Tier 2 (主流财经)"
        for domain in self._tier3:
            if domain.lower() in url_lower:
                return "Tier 3 (分析参考)"
        return "Tier 4 (需交叉验证)"

    # Keep classmethod for backward compatibility
    @classmethod
    def _classify_source_tier(cls, url: str) -> str:
        url_lower = (url or "").lower()
        for domain in cls.TIER1_DOMAINS:
            if domain in url_lower:
                return "Tier 1 (官方/监管)"
        for domain in cls.TIER2_DOMAINS:
            if domain in url_lower:
                return "Tier 2 (主流财经)"
        for domain in cls.TIER3_DOMAINS:
            if domain in url_lower:
                return "Tier 3 (分析参考)"
        return "Tier 4 (需交叉验证)"

    # ------------------------------------------------------------------
    # Result formatting
    # ------------------------------------------------------------------

    @classmethod
    def format_results(cls, results: Dict, max_items: int = 5) -> str:
        output = []
        output.append(f"\n{'='*60}")
        if "ticker" in results:
            output.append(f"Stock Ticker: {results['ticker']}")
        elif "company" in results:
            output.append(f"Company: {results['company']}")
        elif "topic" in results:
            output.append(f"Topic: {results['topic']}")
        output.append(f"Found {results['total_results']} results")
        output.append(f"{'='*60}\n")

        for i, result in enumerate(results["results"][:max_items], 1):
            tier = cls._classify_source_tier(result.url)
            output.append(f"{i}. [{tier}] {result.title}")
            output.append(f"   URL: {result.url}")
            if hasattr(result, 'highlights') and result.highlights:
                output.append(f"   Highlight: {result.highlights[0][:200]}...")
            elif hasattr(result, 'text') and result.text:
                output.append(f"   Preview: {result.text[:200]}...")
            output.append("")

        return "\n".join(output)
