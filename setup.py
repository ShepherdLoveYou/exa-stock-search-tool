from setuptools import setup, find_packages

setup(
    name="crisis-investment-researcher",
    version="0.3.0",
    description="Crisis Investment Researcher — Exa-powered research with dual MD+PDF export",
    author="Crisis Investment Research System",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "exa-py>=1.0.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "requests>=2.31.0",
        "markdown>=3.4.0",
        "pymupdf>=1.23.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "exa-mcp=src.server.mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
