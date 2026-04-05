"""
src.core — Business logic for Crisis Investment Research

Modules:
  researcher  — InvestmentResearcher: report generation, query planning, checklists
  valuation   — ValuationMethods: 10+ cross-validation methods
  freshness   — DataFreshnessChecker: data timeliness validation
  validator   — DataValidator: cross-validation, source scoring, confidence
"""

from .researcher import InvestmentResearcher, FRAMEWORK_MATURE, FRAMEWORK_GROWTH, FRAMEWORK_WEB3
from .valuation import ValuationMethods
from .freshness import DataFreshnessChecker
from .validator import DataValidator

__all__ = [
    "InvestmentResearcher",
    "ValuationMethods",
    "DataFreshnessChecker",
    "DataValidator",
    "FRAMEWORK_MATURE",
    "FRAMEWORK_GROWTH",
    "FRAMEWORK_WEB3",
]
