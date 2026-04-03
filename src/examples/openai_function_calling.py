"""Example: Function calling with OpenAI API"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.stock_searcher import StockSearcher


def main():
    """Demonstrate function calling with OpenAI"""
    
    load_dotenv()
    
    # Initialize clients
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    searcher = StockSearcher()
    
    # Define tools for OpenAI
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_stock_news",
                "description": "Search for latest news about a stock ticker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock ticker symbol (e.g., 'AAPL', 'GOOGL')"
                        }
                    },
                    "required": ["ticker"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_market_analysis",
                "description": "Search for market analysis and trends",
                "parameters": {
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
        }
    ]
    
    # Initial message
    messages = [
        {"role": "user", "content": "What are the latest developments in AI stocks? Give me information about NVIDIA and market trends."}
    ]
    
    print("=" * 80)
    print("OPENAI FUNCTION CALLING EXAMPLE")
    print("=" * 80)
    print(f"\nUser: {messages[0]['content']}\n")
    
    # First API call
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    print(f"Assistant: {response.choices[0].message.content}\n")
    
    # Check if the model wants to call a function
    while response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        
        print(f"📞 Calling tool: {tool_name}")
        print(f"   Arguments: {tool_args}\n")
        
        # Execute the appropriate function
        if tool_name == "search_stock_news":
            result = searcher.search_stock_news(tool_args["ticker"], num_results=5)
            search_results = StockSearcher.format_results(result)
        elif tool_name == "search_market_analysis":
            result = searcher.search_market_analysis(tool_args["topic"], num_results=5)
            search_results = StockSearcher.format_results(result)
        else:
            search_results = "Function not found"
        
        # Add the assistant response and tool result to messages
        messages.append(response.choices[0].message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": search_results
        })
        
        # Call the API again with the tool results
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        print(f"Final Answer: {response.choices[0].message.content}\n")


if __name__ == "__main__":
    main()
