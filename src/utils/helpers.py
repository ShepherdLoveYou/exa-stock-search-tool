"""Helper utilities for Exa Search MCP"""

import os
from typing import Optional
from dotenv import load_dotenv


def load_api_key(api_key: Optional[str] = None) -> str:
    """
    Load Exa API key from environment or parameter.
    
    Args:
        api_key: Optional API key to use directly
        
    Returns:
        str: The API key
        
    Raises:
        ValueError: If no API key is found
    """
    if api_key:
        return api_key
    
    # Try loading from .env file
    load_dotenv()
    
    exa_key = os.environ.get("EXA_API_KEY")
    if not exa_key:
        raise ValueError(
            "EXA_API_KEY not found. Please set it in .env file or "
            "pass it as a parameter. Get your key from: "
            "https://dashboard.exa.ai/api-keys"
        )
    
    return exa_key


def format_search_results(results, max_results: int = 5) -> str:
    """
    Format search results for display.
    
    Args:
        results: Search results from Exa
        max_results: Maximum number of results to display
        
    Returns:
        str: Formatted results
    """
    formatted = []
    
    for i, result in enumerate(results.results[:max_results], 1):
        item = f"{i}. {result.title}\n"
        item += f"   URL: {result.url}\n"
        
        if hasattr(result, 'highlights') and result.highlights:
            highlight = result.highlights[0] if result.highlights else ""
            item += f"   Highlight: {highlight[:150]}...\n"
        elif hasattr(result, 'text') and result.text:
            item += f"   Content: {result.text[:150]}...\n"
            
        formatted.append(item)
    
    return "\n".join(formatted)
