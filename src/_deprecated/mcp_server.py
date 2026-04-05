"""MCP Server implementation for Exa Search + Investment Research"""

import json
import os
from typing import Optional
from dotenv import load_dotenv
from .stock_searcher import StockSearcher
from .investment_researcher import InvestmentResearcher, ValuationMethods
from .data_freshness_checker import DataFreshnessChecker


class ExaMCPServer:
    """MCP Server for Exa Search + Investment Research integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the MCP server.
        
        Args:
            api_key: Exa API key (optional, reads from env if not provided)
        """
        self.searcher = StockSearcher(api_key)
        self.researcher = InvestmentResearcher(self.searcher)
        self.freshness_checker = DataFreshnessChecker()
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
            },
            {
                "name": "generate_research_report",
                "description": "Generate a crisis investment research report skeleton using the appropriate framework (mature/growth/web3). Auto-detects framework from target and market. Returns markdown template with metadata filled in and a list of unfilled fields that need data.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target_name": {
                            "type": "string",
                            "description": "Company or project name (e.g., 'Apple', 'Uniswap')"
                        },
                        "ticker": {
                            "type": "string",
                            "description": "Stock ticker or token symbol (e.g., 'AAPL', 'UNI')"
                        },
                        "market": {
                            "type": "string",
                            "description": "Market: 'us', 'hk', 'a-share', 'crypto'. Auto-detected if empty.",
                            "default": ""
                        },
                        "framework": {
                            "type": "string",
                            "description": "Force framework: 'mature', 'growth', 'web3'. Auto-detected if empty.",
                            "enum": ["", "mature", "growth", "web3"],
                            "default": ""
                        }
                    },
                    "required": ["target_name", "ticker"]
                }
            },
            {
                "name": "get_research_queries",
                "description": "Get the list of search queries needed to fill a research report for a given target. Returns prioritized queries mapped to report fields.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target_name": {
                            "type": "string",
                            "description": "Company or project name"
                        },
                        "ticker": {
                            "type": "string",
                            "description": "Stock ticker or token symbol"
                        },
                        "framework": {
                            "type": "string",
                            "description": "Framework: 'mature', 'growth', 'web3'",
                            "enum": ["mature", "growth", "web3"]
                        }
                    },
                    "required": ["target_name", "ticker", "framework"]
                }
            },
            {
                "name": "check_report_freshness",
                "description": "Check data freshness/timeliness of a research report. Scans for date references and flags stale data that needs updating.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_content": {
                            "type": "string",
                            "description": "Full markdown content of the research report to check"
                        }
                    },
                    "required": ["report_content"]
                }
            },
            {
                "name": "check_unfilled_fields",
                "description": "Check which fields in a research report still need to be filled in. Categorizes unfilled fields by priority (critical/important/supplementary).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_content": {
                            "type": "string",
                            "description": "Full markdown content of the research report to check"
                        }
                    },
                    "required": ["report_content"]
                }
            },
            {
                "name": "calculate_valuation",
                "description": "Calculate intrinsic value using multiple valuation methods and cross-validate. Supports DCF, Graham, PE/PB/PS relative, EV/EBITDA, PEG, DDM, owner earnings, replacement cost.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "method": {
                            "type": "string",
                            "description": "Valuation method to use",
                            "enum": ["dcf", "graham", "pe", "pb", "ps", "ev_ebitda", "peg", "ddm", "owner_earnings", "replacement_cost", "cross_validate"]
                        },
                        "params": {
                            "type": "object",
                            "description": "Parameters specific to the valuation method. See method documentation for required fields."
                        }
                    },
                    "required": ["method", "params"]
                }
            },
            {
                "name": "get_position_sizing",
                "description": "Calculate position sizing and buy ladder based on intrinsic value vs current price. Classifies into shallow water (套利) / deep water (长期持有) / waiting zones per capital management rules.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "intrinsic_value": {
                            "type": "number",
                            "description": "Calculated intrinsic value per share"
                        },
                        "current_price": {
                            "type": "number",
                            "description": "Current market price per share"
                        }
                    },
                    "required": ["intrinsic_value", "current_price"]
                }
            },
            {
                "name": "get_do_not_invest_checklist",
                "description": "Return the '不为清单' (do-not-invest checklist) for pre-investment discipline check. 12 rules that must all pass before any position is opened.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "framework": {
                            "type": "string",
                            "description": "Framework type for threshold variations",
                            "enum": ["mature", "growth", "web3"],
                            "default": "growth"
                        }
                    }
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
            elif tool_name == "generate_research_report":
                result = self.researcher.generate_report_skeleton(
                    target_name=inputs["target_name"],
                    ticker=inputs["ticker"],
                    market=inputs.get("market", ""),
                    framework=inputs.get("framework", ""),
                )
                return json.dumps(result, ensure_ascii=False, default=str)
            elif tool_name == "get_research_queries":
                result = self.researcher.get_research_queries(
                    target_name=inputs["target_name"],
                    ticker=inputs["ticker"],
                    framework=inputs["framework"],
                )
                return json.dumps(result, ensure_ascii=False)
            elif tool_name == "check_report_freshness":
                checker = DataFreshnessChecker()
                result = checker.check_report(inputs["report_content"])
                return json.dumps(result, ensure_ascii=False)
            elif tool_name == "check_unfilled_fields":
                checker = DataFreshnessChecker()
                result = checker.check_unfilled_fields(inputs["report_content"])
                return json.dumps(result, ensure_ascii=False)
            elif tool_name == "calculate_valuation":
                result = self._handle_valuation(inputs["method"], inputs["params"])
                return json.dumps(result, ensure_ascii=False)
            elif tool_name == "get_position_sizing":
                result = self.researcher.get_position_sizing(
                    intrinsic_value=inputs["intrinsic_value"],
                    current_price=inputs["current_price"],
                )
                return json.dumps(result, ensure_ascii=False)
            elif tool_name == "get_do_not_invest_checklist":
                result = self.researcher.get_checklist(
                    framework=inputs.get("framework", "growth")
                )
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
            
            # Format results for display (search-based tools)
            return self.searcher.format_results(result)
        
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _handle_valuation(self, method: str, params: dict) -> dict:
        """Route valuation calculations to the appropriate method"""
        vm = ValuationMethods
        method_map = {
            "dcf": vm.dcf,
            "graham": vm.graham_formula,
            "pe": vm.pe_relative,
            "pb": vm.pb_relative,
            "ps": vm.ps_relative,
            "ev_ebitda": vm.ev_ebitda,
            "peg": vm.peg,
            "ddm": vm.ddm,
            "owner_earnings": vm.owner_earnings_valuation,
            "replacement_cost": vm.replacement_cost,
            "cross_validate": vm.cross_validate,
        }
        func = method_map.get(method)
        if not func:
            return {"error": f"Unknown valuation method: {method}"}
        return func(**params)
    
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
