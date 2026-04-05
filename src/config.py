"""
Centralized configuration loader.

Priority order:
  1. Environment variables (.env file or system env)
  2. config.yaml
  3. Built-in defaults

All modules should import config from here instead of loading .env directly.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).parent.parent
_CONFIG_CACHE: Optional[Dict] = None


def _load_yaml() -> Dict:
    """Load config.yaml if available, otherwise return empty dict."""
    config_path = _PROJECT_ROOT / "config.yaml"
    if not config_path.exists():
        return {}
    try:
        # Use a minimal YAML parser to avoid heavy dependency.
        # Supports the flat structure of our config.yaml.
        import yaml  # PyYAML
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Fallback: parse simple key-value pairs only
        return _parse_yaml_minimal(config_path)


def _parse_yaml_minimal(path: Path) -> Dict:
    """Very simple YAML-like parser for our config format. Handles nested keys."""
    result: Dict = {}
    stack: list = [(result, -1)]

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        content = stripped.lstrip()

        # Pop stack to correct nesting level
        while len(stack) > 1 and stack[-1][1] >= indent:
            stack.pop()

        current_dict = stack[-1][0]

        if content.startswith("- "):
            # List item
            value = content[2:].strip().strip('"').strip("'")
            # Find the parent key that should be a list
            parent = stack[-1][0]
            # The last key added to parent should be the list
            if isinstance(parent, dict):
                for k in reversed(list(parent.keys())):
                    if isinstance(parent[k], list):
                        parent[k].append(value)
                        break
            continue

        if ":" not in content:
            continue

        key, _, val = content.partition(":")
        key = key.strip()
        val = val.strip()

        if not val:
            # Nested dict or list — peek next non-empty line to decide
            new_dict: Any = {}
            # Check if next content line starts with "-"
            # For simplicity, default to dict; convert to list if "-" items found
            current_dict[key] = new_dict
            stack.append((new_dict, indent))
        elif val.startswith("[") or val.startswith("{"):
            current_dict[key] = val
        else:
            # Scalar value
            val = val.strip('"').strip("'")
            if val.lower() == "true":
                current_dict[key] = True
            elif val.lower() == "false":
                current_dict[key] = False
            elif val.replace(".", "", 1).isdigit():
                current_dict[key] = float(val) if "." in val else int(val)
            else:
                current_dict[key] = val

    return result


def _deep_get(data: Dict, *keys: str, default: Any = None) -> Any:
    """Safely traverse nested dict."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def load_config(force_reload: bool = False) -> Dict:
    """Load and cache the merged configuration."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None and not force_reload:
        return _CONFIG_CACHE

    # Load .env first (lowest priority for API keys)
    env_path = _PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    yaml_cfg = _load_yaml()
    _CONFIG_CACHE = yaml_cfg
    return _CONFIG_CACHE


# ----------------------------------------------------------------
# Convenience accessors — all modules use these
# ----------------------------------------------------------------

def get_api_key(name: str = "exa") -> str:
    """Get API key. Env vars take precedence over config.yaml."""
    env_map = {
        "exa": "EXA_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    cfg = load_config()

    # 1. Check environment variable
    env_var = env_map.get(name, f"{name.upper()}_API_KEY")
    env_val = os.environ.get(env_var, "")
    if env_val:
        return env_val

    # 2. Check config.yaml
    yaml_val = _deep_get(cfg, "api_keys", name, default="")
    if yaml_val:
        return str(yaml_val)

    raise ValueError(
        f"API key '{name}' not found.\n"
        f"Please set it in one of these places:\n"
        f"  1. config.yaml -> api_keys -> {name}\n"
        f"  2. .env file -> {env_var}=your_key\n"
        f"  3. System environment variable: {env_var}\n"
        f"\nGet your Exa API key from: https://dashboard.exa.ai/api-keys"
    )


def get_search_config() -> Dict:
    """Return search-related settings."""
    cfg = load_config()
    search_cfg = _deep_get(cfg, "search", default={})
    return {
        "type": os.environ.get("SEARCH_TYPE", search_cfg.get("type", "auto")),
        "num_results": int(os.environ.get("NUM_RESULTS", search_cfg.get("num_results", 10))),
        "max_characters": int(os.environ.get("MAX_CHARACTERS", search_cfg.get("max_characters", 4000))),
        "content_mode": search_cfg.get("content_mode", "highlights"),
    }


def get_validation_config() -> Dict:
    """Return data validation settings."""
    cfg = load_config()
    return _deep_get(cfg, "validation", default={
        "require_source_citations": True,
        "min_cross_validation_sources": 2,
        "auto_flag_stale_data": True,
        "block_export_on_high_risk": True,
    })


_DEFAULT_FRESHNESS_THRESHOLDS = {
    "stock_price": 1, "financial_statements": 120, "analyst_ratings": 30,
    "insider_trading": 14, "news_sentiment": 3, "market_data": 1,
    "industry_report": 180, "company_filing": 90, "earnings_call": 120,
    "management_guidance": 120, "tvl_data": 1, "protocol_revenue": 7,
    "token_unlock": 30, "governance_proposal": 14, "github_activity": 7,
    "community_metrics": 7, "treasury_balance": 7, "macro_economic": 30,
    "regulatory_filing": 90, "audit_report": 365,
}


def get_freshness_thresholds() -> Dict[str, int]:
    """Return freshness thresholds from config or defaults."""
    cfg = load_config()
    custom = _deep_get(cfg, "validation", "freshness_thresholds", default={})
    merged = dict(_DEFAULT_FRESHNESS_THRESHOLDS)
    if isinstance(custom, dict):
        merged.update({k: int(v) for k, v in custom.items() if isinstance(v, (int, float))})
    return merged


def get_source_tiers() -> Dict[str, List[str]]:
    """Return source tier domain lists from config or defaults."""
    cfg = load_config()
    tiers = _deep_get(cfg, "source_tiers", default={})
    if tiers and isinstance(tiers, dict):
        return {k: v for k, v in tiers.items() if isinstance(v, list)}
    # Fallback to hardcoded defaults in exa_searcher
    return {}


def get_export_config() -> Dict:
    """Return export settings."""
    cfg = load_config()
    export_cfg = _deep_get(cfg, "export", default={})
    return {
        "markdown_dir": export_cfg.get("markdown_dir", "research Output/markdown"),
        "pdf_dir": export_cfg.get("pdf_dir", "research Output/pdf"),
        "naming_pattern": export_cfg.get("naming_pattern", "{date}_{ticker}_{framework}_{report_id}"),
        "pdf_engines": export_cfg.get("pdf_engines", ["chromium", "fitz", "text"]),
    }


def get_network_config() -> Dict:
    """Return network settings."""
    cfg = load_config()
    net = _deep_get(cfg, "network", default={})
    return {
        "timeout": int(net.get("timeout", 30)),
        "max_retries": int(net.get("max_retries", 3)),
        "retry_delay": float(net.get("retry_delay", 1.0)),
    }


def get_project_root() -> Path:
    """Return the project root directory."""
    return _PROJECT_ROOT
