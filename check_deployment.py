#!/usr/bin/env python3
"""
Quick deployment helper - Validates setup before deployment
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Creating .env from template...")
        os.system("cp .env.example .env")
        print("✅ Created .env - Please edit it with your credentials")
        return False
    
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHANNEL_ID",
    ]
    
    optional_vars = [
        "OPENAI_API_KEY",
        "GROQ_API_KEY",
    ]
    
    with open(".env") as f:
        env_content = f.read()
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=your" in env_content:
            missing_required.append(var)
    
    for var in optional_vars:
        if f"{var}=" not in env_content or f"{var}=your" in env_content:
            missing_optional.append(var)
    
    if missing_required:
        print("❌ Missing required variables:")
        for var in missing_required:
            print(f"   - {var}")
        return False
    
    if missing_optional:
        print("⚠️  Missing optional variables (features may be limited):")
        for var in missing_optional:
            print(f"   - {var}")
        print("   You can add them later in .env\n")
    
    print("✅ All required variables are set\n")
    return True


def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import telegram
        import dotenv
        import PIL
        print("✅ All dependencies installed\n")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📥 Install with: pip install -r requirements.txt\n")
        return False


def main():
    print("🤖 AI-Driven Telegram Bot - Pre-deployment Check\n")
    print("=" * 50)
    
    checks = [
        ("Environment Variables", check_environment),
        ("Dependencies", check_dependencies),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✅ All checks passed! Ready to deploy.")
        print("\nNext steps:")
        print("1. Test locally: python main.py")
        print("2. Deploy to cloud: See DEPLOYMENT.md")
        return 0
    else:
        print("\n❌ Fix the issues above before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
