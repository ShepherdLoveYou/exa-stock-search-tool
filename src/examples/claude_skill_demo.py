"""
Example: Using Exa Stock Search with Claude Skill Router
Demonstrates natural language query routing and smart search
"""

from src.skill_router import ExaSkillRouter


def main():
    """Run skill router examples"""
    
    router = ExaSkillRouter()
    
    print("=" * 80)
    print("EXA STOCK SEARCH SKILL ROUTER - EXAMPLES")
    print("=" * 80)
    print("\nThis demonstrates how natural language queries are intelligently routed")
    print("to the appropriate search function.\n")
    
    # Example 1: Stock News
    print("\n" + "=" * 80)
    print("EXAMPLE 1: STOCK NEWS SEARCH")
    print("=" * 80)
    query1 = "What's the latest with Apple stock?"
    print(f"\n📝 Query: {query1}")
    print("-" * 80)
    result1 = router.search_and_format(query1, num_results=3, max_display=2)
    print(result1)
    
    # Example 2: Market Analysis
    print("\n" + "=" * 80)
    print("EXAMPLE 2: MARKET ANALYSIS")
    print("=" * 80)
    query2 = "Analyze AI tech stocks market trends"
    print(f"\n📝 Query: {query2}")
    print("-" * 80)
    result2 = router.search_and_format(query2, num_results=3, max_display=2)
    print(result2)
    
    # Example 3: Company Research
    print("\n" + "=" * 80)
    print("EXAMPLE 3: COMPANY RESEARCH")
    print("=" * 80)
    query3 = "Research Microsoft company information"
    print(f"\n📝 Query: {query3}")
    print("-" * 80)
    result3 = router.search_and_format(query3, num_results=3, max_display=2)
    print(result3)
    
    # Example 4: Deep Research
    print("\n" + "=" * 80)
    print("EXAMPLE 4: DEEP RESEARCH")
    print("=" * 80)
    query4 = "Deep research on semiconductor industry trends"
    print(f"\n📝 Query: {query4}")
    print("-" * 80)
    result4 = router.search_and_format(query4, num_results=3, max_display=2)
    print(result4)
    
    print("\n" + "=" * 80)
    print("✅ All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
