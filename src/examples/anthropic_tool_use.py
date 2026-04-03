"""Example: Tool use with Anthropic (Claude) API"""

import os
from dotenv import load_dotenv
import anthropic
from src.stock_searcher import StockSearcher


def main():
    """Demonstrate tool use with Claude API"""
    
    load_dotenv()
    
    # Initialize clients
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    searcher = StockSearcher()
    
    # Define tools for Claude
    tools = [
        {
            "name": "search_stock_news",
            "description": "Search for latest news and developments about a specific stock",
            "input_schema": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., 'AAPL', 'GOOGL')"
                    }
                },
                "required": ["ticker"]
            }
        },
        {
            "name": "search_market_analysis",
            "description": "Search for market analysis and trends",
            "input_schema": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Market topic to analyze"
                    }
                },
                "required": ["topic"]
            }
        }
    ]
    
    # Initial message
    messages = [
        {"role": "user", "content": "Tell me about the latest developments in quantum computing stocks and which companies are leading this space."}
    ]
    
    print("=" * 80)
    print("ANTHROPIC (CLAUDE) TOOL USE EXAMPLE")
    print("=" * 80)
    print(f"\nUser: {messages[0]['content']}\n")
    
    # Make the API call with tools enabled
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        tools=tools,
        messages=messages
    )
    
    # Process the response in an agentic loop
    while response.stop_reason == "tool_use":
        # Find the tool use block
        tool_use = next((block for block in response.content if block.type == "tool_use"), None)
        
        if not tool_use:
            break
        
        tool_name = tool_use.name
        tool_input = tool_use.input
        
        print(f"🛠️  Using tool: {tool_name}")
        print(f"   Input: {tool_input}\n")
        
        # Execute the appropriate tool
        if tool_name == "search_stock_news":
            result = searcher.search_stock_news(tool_input["ticker"], num_results=5)
            tool_result = StockSearcher.format_results(result)
        elif tool_name == "search_market_analysis":
            result = searcher.search_market_analysis(tool_input["topic"], num_results=5)
            tool_result = StockSearcher.format_results(result)
        else:
            tool_result = "Tool not found"
        
        # Build the messages for the next call
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": tool_result
                }
            ]
        })
        
        # Make another API call
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
    
    # Extract final text response
    final_response = next(
        (block.text for block in response.content if hasattr(block, "text")),
        "No response"
    )
    
    print(f"Assistant Final Answer:\n{final_response}\n")


if __name__ == "__main__":
    main()
