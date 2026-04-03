"""MCP Server implementation for Exa Search"""

import json
import os
from typing import Optional
from dotenv import load_dotenv
from .stock_searcher import StockSearcher


class ExaMCPServer:
    """MCP Server for Exa Search integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the MCP server.
        
        Args:
            api_key: Exa API key (optional, reads from env if not provided)
        """
        self.searcher = StockSearcher(api_key)
        self.tools = self._setup_tools()
    
    def _setup_tools(self) -> list:
        """Define available tools for the MCP server"""
        return [
            {
                "name": "search_stock_news",
                "description": "Search for latest news and developments about a specific stock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock ticker symbol (e.g., 'AAPL', 'GOOGL')"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "search_market_analysis",
                "description": "Search for market analysis and trends",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Market topic to analyze (e.g., 'tech stocks', 'AI companies')"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "search_company_info",
                "description": "Search for company information including earnings reports",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "company_name": {
                            "type": "string",
                            "description": "Name of the company"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["company_name"]
                }
            },
            {
                "name": "deep_research",
                "description": "Perform deep research search for thorough analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Research query"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    def handle_tool_call(self, tool_name: str, inputs: dict) -> str:
        """
        Handle a tool call from Claude.
        
        Args:
            tool_name: Name of the tool to call
            inputs: Input parameters for the tool
            
        Returns:
            JSON string with results
        """
        try:
            if tool_name == "search_stock_news":
                result = self.searcher.search_stock_news(
                    ticker=inputs["ticker"],
                    num_results=inputs.get("num_results", 10)
                )
            elif tool_name == "search_market_analysis":
                result = self.searcher.search_market_analysis(
                    topic=inputs["topic"],
                    num_results=inputs.get("num_results", 10)
                )
            elif tool_name == "search_company_info":
                result = self.searcher.search_company_info(
                    company_name=inputs["company_name"],
                    num_results=inputs.get("num_results", 10)
                )
            elif tool_name == "deep_research":
                result = self.searcher.search_with_deep_research(
                    query=inputs["query"],
                    num_results=inputs.get("num_results", 10)
                )
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
            
            # Format results for display
            return self.searcher.format_results(result)
        
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_tools(self) -> str:
        """Get available tools definition"""
        return json.dumps(self.tools, indent=2)


def main():
    """Main entry point for the MCP server"""
    load_dotenv()
    
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        print("Error: EXA_API_KEY not set. Please configure your API key.")
        return
    
    server = ExaMCPServer(api_key)
    print("Exa MCP Server initialized successfully!")
    print(f"\nAvailable tools:\n{server.get_tools()}")


if __name__ == "__main__":
    main()
