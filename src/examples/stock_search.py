"""Stock market focused search example"""

import os
from dotenv import load_dotenv
from src.stock_searcher import StockSearcher


def main():
    """Run stock market focused search examples"""
    
    load_dotenv()
    searcher = StockSearcher()
    
    print("=" * 80)
    print("STOCK MARKET SEARCH EXAMPLES")
    print("=" * 80)
    
    # Search for specific company information
    print("\n1. Searching for Microsoft company information...")
    ms_results = searcher.search_company_info("Microsoft", num_results=5)
    print(StockSearcher.format_results(ms_results, max_items=3))
    
    # Deep research on market trends
    print("\n2. Performing deep research on semiconductor industry...")
    semi_results = searcher.search_with_deep_research(
        "semiconductor industry trends and market leaders",
        num_results=5
    )
    print(StockSearcher.format_results(semi_results, max_items=3))
    
    # Market analysis on growth stocks
    print("\n3. Searching for growth stocks market analysis...")
    growth_results = searcher.search_market_analysis("growth stocks 2024", num_results=5)
    print(StockSearcher.format_results(growth_results, max_items=3))


if __name__ == "__main__":
    main()
