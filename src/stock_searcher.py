"""Stock market information searcher using Exa API"""

import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
from exa_py import Exa


class StockSearcher:
    """Search for stock market information using Exa API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize StockSearcher.
        
        Args:
            api_key: Exa API key. If None, reads from EXA_API_KEY environment variable.
        """
        if api_key is None:
            # Load from .env file in the project root
            import pathlib
            env_path = pathlib.Path(__file__).parent.parent / ".env"
            load_dotenv(dotenv_path=env_path)
            api_key = os.environ.get("EXA_API_KEY")
            
        if not api_key:
            raise ValueError(
                "EXA_API_KEY not found. Please set it in .env file. "
                "Get your key from: https://dashboard.exa.ai/api-keys"
            )
        
        self.exa = Exa(api_key=api_key)
        self.search_type = "auto"  # Balanced relevance and speed
        self.num_results = 10
    
    def search_stock_news(
        self, 
        ticker: str, 
        num_results: int = 10,
        include_highlights: bool = True
    ) -> Dict:
        """
        Search for news about a stock ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
            num_results: Number of results to return
            include_highlights: Whether to include content highlights
            
        Returns:
            Dict containing search results
        """
        query = f"{ticker} stock news latest developments"
        
        kwargs = {
            "type": self.search_type,
            "num_results": num_results,
        }
        
        if include_highlights:
            kwargs["highlights"] = {"max_characters": 4000}
        
        results = self.exa.search_and_contents(query, **kwargs)
        
        return {
            "ticker": ticker,
            "query": query,
            "total_results": len(results.results),
            "results": results.results,
        }
    
    def search_market_analysis(
        self,
        topic: str,
        num_results: int = 10
    ) -> Dict:
        """
        Search for market analysis and insights.
        
        Args:
            topic: Market topic to search (e.g., 'tech stocks', 'AI companies')
            num_results: Number of results to return
            
        Returns:
            Dict containing search results
        """
        query = f"{topic} market analysis stock market trends"
        
        results = self.exa.search_and_contents(
            query,
            type=self.search_type,
            num_results=num_results,
            highlights={"max_characters": 4000}
        )
        
        return {
            "topic": topic,
            "query": query,
            "total_results": len(results.results),
            "results": results.results,
        }
    
    def search_company_info(
        self,
        company_name: str,
        num_results: int = 10
    ) -> Dict:
        """
        Search for company information.
        
        Args:
            company_name: Name of the company to search
            num_results: Number of results to return
            
        Returns:
            Dict containing search results
        """
        query = f"{company_name} company information earnings reports"
        
        results = self.exa.search_and_contents(
            query,
            type=self.search_type,
            num_results=num_results,
            highlights={"max_characters": 4000}
        )
        
        return {
            "company": company_name,
            "query": query,
            "total_results": len(results.results),
            "results": results.results,
        }
    
    def search_with_deep_research(
        self,
        query: str,
        num_results: int = 10
    ) -> Dict:
        """
        Perform deep research search for detailed results.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dict containing detailed search results
        """
        results = self.exa.search_and_contents(
            query,
            type="deep",  # Deep research for thorough results
            num_results=num_results,
            text={"max_characters": 20000}
        )
        
        return {
            "query": query,
            "search_type": "deep",
            "total_results": len(results.results),
            "results": results.results,
        }
    
    @staticmethod
    def format_results(results: Dict, max_items: int = 5) -> str:
        """
        Format search results for display.
        
        Args:
            results: Search results dictionary
            max_items: Maximum number of items to display
            
        Returns:
            Formatted string for display
        """
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
            output.append(f"{i}. {result.title}")
            output.append(f"   URL: {result.url}")
            
            if hasattr(result, 'highlights') and result.highlights:
                highlight = result.highlights[0][:200]
                output.append(f"   Highlight: {highlight}...")
            elif hasattr(result, 'text') and result.text:
                text_preview = result.text[:200]
                output.append(f"   Preview: {text_preview}...")
            
            output.append("")
        
        return "\n".join(output)
