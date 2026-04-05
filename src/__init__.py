"""
Crisis Investment Researcher — Exa-powered research + dual export
"""

__version__ = "0.3.0"
__author__ = "Exa Search MCP Contributors"

from .search.exa_searcher import StockSearcher
from .core.researcher import InvestmentResearcher
from .core.valuation import ValuationMethods
from .core.freshness import DataFreshnessChecker
from .core.validator import DataValidator
from .export.exporter import ReportExporter
from .server.mcp_server import ExaMCPServer

__all__ = [
    "StockSearcher",
    "InvestmentResearcher",
    "ValuationMethods",
    "DataFreshnessChecker",
    "DataValidator",
    "ReportExporter",
    "ExaMCPServer",
]
