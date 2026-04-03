"""Basic stock search example"""

import os
from dotenv import load_dotenv
from src.stock_searcher import StockSearcher


def main():
    """Run basic stock search examples"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize the searcher
    searcher = StockSearcher()
    
    print("=" * 80)
    print("BASIC EXA STOCK SEARCH EXAMPLES")
    print("=" * 80)
    
    # Example 1: Search for stock news
    print("\n1. Searching for APPLE (AAPL) stock news...")
    apple_results = searcher.search_stock_news("AAPL", num_results=5)
    print(StockSearcher.format_results(apple_results, max_items=3))
    
    # Example 2: Search for Tesla news
    print("\n2. Searching for TESLA (TSLA) stock news...")
    tesla_results = searcher.search_stock_news("TSLA", num_results=5)
    print(StockSearcher.format_results(tesla_results, max_items=3))
    
    # Example 3: Market analysis
    print("\n3. Searching for AI tech stocks market analysis...")
    market_results = searcher.search_market_analysis("AI tech stocks", num_results=5)
    print(StockSearcher.format_results(market_results, max_items=3))


if __name__ == "__main__":
    main()
