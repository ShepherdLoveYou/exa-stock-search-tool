from setuptools import setup, find_packages

setup(
    name="exa-search-mcp",
    version="0.1.0",
    description="Exa Search MCP Server for Claude - Web search tool for stock market information",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "exa-py>=1.0.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "exa-mcp=src.mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
