"""
Claude Skill Integration - Smart routing for Exa Stock Search
"""

import json
import re
from typing import Dict, List, Optional
from src.stock_searcher import StockSearcher


class ExaSkillRouter:
    """
    Intelligent router that interprets natural language queries
    and routes them to the appropriate search function.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the skill router with StockSearcher"""
        self.searcher = StockSearcher(api_key)
    
    def detect_search_type(self, query: str) -> Dict[str, any]:
        """
        Detect the search type from natural language query.
        
        Returns: {
            'type': 'stock_news' | 'market_analysis' | 'company_info' | 'deep_research',
            'query': str,
            'confidence': float (0-1)
        }
        """
        query_lower = query.lower()
        
        # Pattern matching for different search types
        patterns = {
            'stock_news': [
                r'(?:what\'s|what is|latest|news|recent)\s+(?:with|about|on|for)\s+([A-Z]{1,5})',
                r'([A-Z]{1,5})\s+(?:stock|ticker)\s+(?:news|price|movement)',
                r'(?:stock|ticker)\s+([A-Z]{1,5})',
                r'(?:search|find)\s+news\s+(?:about|on|for)\s+([A-Z]{1,5})',
            ],
            'market_analysis': [
                r'(?:analyze|analysis|trend|trends)\s+(?:in|for)\s+([a-z\s]+)\s+(?:stocks|market|sector)',
                r'(?:market|sector)\s+(?:analysis|trends|outlook)\s+(?:for|on|in)\s+([a-z\s]+)',
                r'(?:what\'s|what is)\s+(?:happening|going on)\s+(?:in|with)\s+(?:the\s+)?([a-z\s]+)\s+(?:stocks|market)',
            ],
            'company_info': [
                r'(?:research|find|info|information)\s+(?:about|on)\s+([a-z\s]+)\s+(?:company|corp)',
                r'company\s+(?:info|information|research)\s+(?:about|on|for)\s+([a-z\s]+)',
                r'(?:tell|give|show)\s+me\s+(?:about|on)\s+([a-z\s]+)\s+company',
            ],
            'deep_research': [
                r'(?:deep|thorough|comprehensive)\s+(?:research|analysis)\s+(?:on|about|into)\s+(.+)',
                r'(?:research|analyze)\s+(?:deeply|thoroughly)\s+(.+)',
                r'(?:investigate|explore)\s+(.+)\s+in\s+detail',
            ]
        }
        
        # Try to match patterns
        for search_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, query_lower, re.IGNORECASE)
                if match:
                    search_query = match.group(1) if match.groups() else query
                    return {
                        'type': search_type,
                        'query': search_query.strip(),
                        'confidence': 0.9
                    }
        
        # Default: treat as market analysis
        return {
            'type': 'market_analysis',
            'query': query,
            'confidence': 0.5
        }
    
    def search(self, query: str, num_results: int = 10) -> Dict:
        """
        Main entry point - search based on natural language query.
        
        Args:
            query: Natural language search query
            num_results: Number of results to return
            
        Returns:
            Formatted search results
        """
        # Detect search type
        detection = self.detect_search_type(query)
        search_type = detection['type']
        search_query = detection['query']
        
        print(f"🔍 Detected: {search_type} (confidence: {detection['confidence']:.1%})")
        print(f"📝 Query: {search_query}\n")
        
        # Route to appropriate search function
        if search_type == 'stock_news':
            # Extract ticker
            ticker = search_query.upper()
            # Clean up ticker to 1-5 characters
            ticker = re.sub(r'[^A-Z]', '', ticker)[:5]
            if not ticker:
                ticker = search_query.upper()
            return self.searcher.search_stock_news(ticker, num_results)
        
        elif search_type == 'company_info':
            return self.searcher.search_company_info(search_query, num_results)
        
        elif search_type == 'deep_research':
            return self.searcher.search_with_deep_research(search_query, num_results)
        
        else:  # market_analysis
            return self.searcher.search_market_analysis(search_query, num_results)
    
    def search_and_format(self, query: str, num_results: int = 10, max_display: int = 5) -> str:
        """
        Search and return formatted results as string (for Claude output).
        
        Args:
            query: Natural language search query
            num_results: Number of results to fetch
            max_display: Maximum results to display
            
        Returns:
            Formatted string results
        """
        results = self.search(query, num_results)
        return StockSearcher.format_results(results, max_display)
    
    def search_as_json(self, query: str, num_results: int = 10) -> str:
        """
        Search and return results as JSON (for API/integration).
        
        Args:
            query: Natural language search query
            num_results: Number of results to fetch
            
        Returns:
            JSON string with results
        """
        results = self.search(query, num_results)
        
        # Convert to JSON-serializable format
        json_results = {
            "query": query,
            "search_type": results.get("search_type", "unknown"),
            "total_results": results.get("total_results", 0),
            "results": []
        }
        
        for result in results.get("results", [])[:10]:
            json_results["results"].append({
                "title": result.title,
                "url": result.url,
                "highlight": result.highlights[0][:200] if hasattr(result, 'highlights') and result.highlights else "",
            })
        
        return json.dumps(json_results, ensure_ascii=False, indent=2)


def main():
    """Example usage"""
    router = ExaSkillRouter()
    
    # Test queries
    test_queries = [
        "What's the latest with Apple stock?",
        "Analyze AI tech stocks",
        "Research Microsoft company information",
        "Deep research on quantum computing",
    ]
    
    print("=" * 70)
    print("EXA SKILL ROUTER - DEMO")
    print("=" * 70)
    
    for query in test_queries:
        print(f"\n📌 User: {query}")
        print("-" * 70)
        try:
            results = router.search_and_format(query, num_results=3, max_display=2)
            print(results)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print()


if __name__ == "__main__":
    main()
