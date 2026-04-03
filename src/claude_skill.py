"""
Claude Skill - Exa Stock Search
Direct interface for Claude to call stock search functions
"""

import sys
import json
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.skill_router import ExaSkillRouter


def search_stock(query: str, num_results: int = 10) -> str:
    """
    Main function that Claude will call.
    
    Args:
        query: User's natural language search query
        num_results: Number of results to return
        
    Returns:
        Formatted search results as string
    """
    try:
        router = ExaSkillRouter()
        results = router.search_and_format(query, num_results, max_display=5)
        return results
    except Exception as e:
        return f"❌ Search error: {str(e)}"


def search_stock_json(query: str, num_results: int = 10) -> str:
    """
    Return results as JSON for programmatic access.
    
    Args:
        query: User's natural language search query
        num_results: Number of results to return
        
    Returns:
        JSON formatted results
    """
    try:
        router = ExaSkillRouter()
        return router.search_as_json(query, num_results)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False), "error"


def main():
    """
    CLI entry point - allows running from command line.
    Usage: python src/claude_skill.py "Your search query"
    """
    if len(sys.argv) < 2:
        print("📖 Exa Stock Search Skill")
        print("-" * 50)
        print("Usage: python src/claude_skill.py \"Your search query\"")
        print("\nExamples:")
        print("  python src/claude_skill.py \"What's the latest with Apple?\"")
        print("  python src/claude_skill.py \"Analyze AI stocks\"")
        print("  python src/claude_skill.py \"Research Tesla\"")
        print("\nOptional:")
        print("  --json: Return results as JSON")
        print("  --results N: Return N results (default: 10)")
        return
    
    query = sys.argv[1]
    output_format = "text"
    num_results = 10
    
    # Parse optional arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--json":
            output_format = "json"
        elif arg == "--results" and i+1 < len(sys.argv):
            try:
                num_results = int(sys.argv[i+1])
            except ValueError:
                pass
    
    # Execute search
    if output_format == "json":
        result = search_stock_json(query, num_results)
        print(result)
    else:
        result = search_stock(query, num_results)
        print(result)


# Export functions for Claude to call
__all__ = [
    'search_stock',
    'search_stock_json',
]


if __name__ == "__main__":
    main()
