#!/usr/bin/env python3
"""
Claude Skill Integration Checker
Verify that all required files and dependencies are properly configured.
"""

import os
import sys
from pathlib import Path


def check_file(path: str, description: str) -> bool:
    exists = os.path.exists(path)
    status = "OK" if exists else "MISSING"
    print(f"  [{status}] {description:<55} {path}")
    return exists


def check_imports() -> bool:
    try:
        from src.config import load_config, get_api_key
        from src.server.skill_router import UnifiedSkillRouter
        from src.server.mcp_server import ExaMCPServer
        from src.core.researcher import InvestmentResearcher
        from src.core.valuation import ValuationMethods
        from src.core.freshness import DataFreshnessChecker
        from src.core.validator import DataValidator
        from src.search.exa_searcher import StockSearcher
        from src.export.exporter import ReportExporter
        from src.claude_skill import search_stock
        print("  [OK] All Python modules import successfully")
        return True
    except ImportError as e:
        print(f"  [FAIL] Import error: {e}")
        return False


def check_api_key() -> bool:
    try:
        from src.config import get_api_key
        key = get_api_key("exa")
        if key and len(key) > 10:
            print(f"  [OK] API Key configured: {key[:10]}...")
            return True
    except Exception:
        pass
    print("  [FAIL] API Key not configured. Set it in config.yaml or .env")
    return False


def check_config() -> bool:
    config_yaml = os.path.exists("config.yaml")
    env_file = os.path.exists(".env")
    if config_yaml:
        print("  [OK] config.yaml found")
        return True
    if env_file:
        print("  [OK] .env found (consider using config.yaml for easier setup)")
        return True
    print("  [FAIL] No config.yaml or .env found")
    return False


def main():
    print()
    print("=" * 70)
    print("  Crisis Investment Researcher - Integration Checker")
    print("=" * 70)

    all_pass = True

    print("\n[1/5] Core Files:")
    for path, desc in [
        ("SKILL.md", "Claude Skill Definition"),
        (".instructions.md", "Claude Instructions"),
        ("config.yaml", "Main Configuration"),
        ("requirements.txt", "Dependencies"),
    ]:
        if not check_file(path, desc):
            all_pass = False

    print("\n[2/5] Source Modules:")
    for path, desc in [
        ("src/config.py", "Centralized Config Loader"),
        ("src/claude_skill.py", "Claude Skill Entry Point"),
        ("src/search/exa_searcher.py", "Exa Search Engine"),
        ("src/core/researcher.py", "Investment Researcher"),
        ("src/core/valuation.py", "Valuation Methods (10+)"),
        ("src/core/freshness.py", "Data Freshness Checker"),
        ("src/core/validator.py", "Data Validator & Cross-Validation"),
        ("src/server/mcp_server.py", "MCP Server (14 tools)"),
        ("src/server/skill_router.py", "Unified Skill Router"),
        ("src/export/exporter.py", "Report Exporter (MD + PDF)"),
    ]:
        if not check_file(path, desc):
            all_pass = False

    print("\n[3/5] Configuration:")
    if not check_config():
        all_pass = False

    print("\n[4/5] Python Imports:")
    if not check_imports():
        all_pass = False

    print("\n[5/5] API Key:")
    if not check_api_key():
        all_pass = False

    print()
    print("=" * 70)
    if all_pass:
        print("  ALL CHECKS PASSED - Ready to use!")
        print("=" * 70)
        print()
        print("  Usage:")
        print('    Claude Chat: Ctrl+L -> type your query')
        print('    CLI: python src/claude_skill.py "Apple stock news"')
        print('    Research: python src/claude_skill.py "Report for AAPL" --research')
        return 0
    else:
        print("  SOME CHECKS FAILED - See above for details")
        print("=" * 70)
        print()
        print("  To fix:")
        print("    1. Set your API key in config.yaml or .env")
        print("    2. Run: pip install -r requirements.txt")
        print("    3. Ensure all source files are present")
        return 1


if __name__ == "__main__":
    sys.exit(main())
