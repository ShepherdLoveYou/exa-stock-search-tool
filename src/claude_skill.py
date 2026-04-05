"""
Claude Skill — Crisis Investment Researcher
Direct interface for Claude to call search + research functions
"""

import sys
import json
import os

# Ensure project root is on path for direct execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server.skill_router import UnifiedSkillRouter


def search_stock(query: str, num_results: int = 10) -> str:
    try:
        router = UnifiedSkillRouter()
        return router.search_and_format(query, num_results, max_display=5)
    except Exception as e:
        return f"Search error: {str(e)}"


def research(query: str) -> str:
    """Route a research request and return JSON result"""
    try:
        router = UnifiedSkillRouter()
        result = router.route(query)
        return json.dumps(result, ensure_ascii=False, default=str, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def search_stock_json(query: str, num_results: int = 10) -> str:
    try:
        router = UnifiedSkillRouter()
        return router.search_as_json(query, num_results)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print("Crisis Investment Researcher Skill")
        print("-" * 50)
        print("Usage: python src/claude_skill.py \"Your query\"")
        print("\nExamples:")
        print('  python src/claude_skill.py "Generate report for AAPL"')
        print('  python src/claude_skill.py "Analyze AI stocks"')
        print('  python src/claude_skill.py "Valuation for Tesla"')
        print("\nFlags: --json, --research, --results N")
        return

    query = sys.argv[1]
    output_format = "text"
    mode = "search"
    num_results = 10

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--json":
            output_format = "json"
        elif arg == "--research":
            mode = "research"
        elif arg == "--results" and i + 1 < len(sys.argv):
            try:
                num_results = int(sys.argv[i + 1])
            except ValueError:
                pass

    if mode == "research":
        print(research(query))
    elif output_format == "json":
        print(search_stock_json(query, num_results))
    else:
        print(search_stock(query, num_results))


__all__ = ['search_stock', 'search_stock_json', 'research']


if __name__ == "__main__":
    main()
