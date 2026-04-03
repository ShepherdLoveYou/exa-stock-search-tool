#!/usr/bin/env python3
"""
Claude Skill Integration Checker
Verify that all required files and dependencies are properly configured
"""

import os
import sys
from pathlib import Path


def check_file(path: str, description: str) -> bool:
    """Check if a file exists and print status"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description:<50} {path}")
    return exists


def check_imports() -> bool:
    """Check if Python modules can be imported"""
    try:
        from src.skill_router import ExaSkillRouter
        from src.claude_skill import search_stock
        print("✅ Python modules import successfully")
        return True
    except ImportError as e:
        print(f"❌ Python import error: {e}")
        return False


def check_api_key() -> bool:
    """Check if API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("EXA_API_KEY")
    
    if api_key and len(api_key) > 10:
        print(f"✅ API Key configured: {api_key[:10]}...")
        return True
    else:
        print("❌ API Key not configured in .env")
        return False


def main():
    """Run all checks"""
    print("\n" + "=" * 80)
    print("CLAUDE SKILL INTEGRATION CHECKER")
    print("=" * 80 + "\n")
    
    checks = {
        "Core Files": [
            ("SKILL.md", "SKILL.md - Claude Skill Definition"),
            (".instructions.md", ".instructions.md - Claude Instructions"),
        ],
        "Python Modules": [
            ("src/skill_router.py", "src/skill_router.py - Smart Router"),
            ("src/claude_skill.py", "src/claude_skill.py - Claude Interface"),
        ],
        "Configuration": [
            (".env", ".env - Environment Configuration"),
            ("requirements.txt", "requirements.txt - Dependencies"),
        ],
        "Examples": [
            ("src/examples/claude_skill_demo.py", "Demo Script"),
            ("src/examples/basic_search.py", "Basic Search Example"),
        ],
    }
    
    all_pass = True
    
    for category, files in checks.items():
        print(f"\n📋 {category}:")
        for filepath, description in files:
            if not check_file(filepath, description):
                all_pass = False
    
    # Check imports
    print(f"\n🐍 Python Imports:")
    if not check_imports():
        all_pass = False
    
    # Check API key
    print(f"\n🔑 API Configuration:")
    if not check_api_key():
        all_pass = False
    
    # Results
    print("\n" + "=" * 80)
    if all_pass:
        print("✅ ALL CHECKS PASSED - READY FOR CLAUDE!")
        print("=" * 80)
        print("\nYou can now:")
        print("  1. Use in Claude Chat (Ctrl+L)")
        print("  2. Run from command line: python src/claude_skill.py \"your query\"")
        print("  3. Import in Python: from src.skill_router import ExaSkillRouter")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - SEE ABOVE")
        print("=" * 80)
        print("\nTo fix:")
        print("  1. Make sure .env has EXA_API_KEY")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. Verify all files exist in project root")
        return 1


if __name__ == "__main__":
    sys.exit(main())
