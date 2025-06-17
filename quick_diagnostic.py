#!/usr/bin/env python3
"""
Quick Diagnostic Tool for Social Media Integrations
Checks the status of all platforms and provides specific guidance
"""

import os
import json
from datetime import datetime

def check_credentials_file():
    """Check if credentials.json exists and has content"""
    if not os.path.exists("credentials.json"):
        return {
            "exists": False,
            "message": "❌ credentials.json file not found",
            "action": "Copy credentials_template.json to credentials.json and fill in your API keys"
        }
    
    try:
        with open("credentials.json", "r") as f:
            data = json.load(f)
        
        platforms = []
        issues = []
        
        # Check Twitter
        if "twitter" in data:
            twitter = data["twitter"]
            if all(key in twitter and twitter[key] and not twitter[key].startswith("YOUR_") 
                   for key in ["api_key", "api_secret", "access_token", "access_token_secret", "bearer_token"]):
                platforms.append("✅ Twitter")
            else:
                platforms.append("❌ Twitter")
                issues.append("Twitter credentials need to be filled in")
        else:
            platforms.append("❌ Twitter")
            issues.append("Twitter section missing from credentials.json")
        
        # Check LinkedIn
        if "linkedin" in data:
            linkedin = data["linkedin"]
            if all(key in linkedin and linkedin[key] and not linkedin[key].startswith("YOUR_") 
                   for key in ["client_id", "client_secret", "access_token", "user_id"]):
                platforms.append("✅ LinkedIn")
            else:
                platforms.append("❌ LinkedIn")
                issues.append("LinkedIn credentials need to be filled in")
        else:
            platforms.append("❌ LinkedIn")
            issues.append("LinkedIn section missing from credentials.json")
        
        # Check Facebook
        if "facebook" in data:
            facebook = data["facebook"]
            if all(key in facebook and facebook[key] and not facebook[key].startswith("YOUR_") 
                   for key in ["app_id", "app_secret", "access_token"]):
                platforms.append("✅ Facebook")
            else:
                platforms.append("❌ Facebook")
                issues.append("Facebook credentials need to be filled in")
        else:
            platforms.append("❌ Facebook")
            issues.append("Facebook section missing from credentials.json")
        
        return {
            "exists": True,
            "message": f"📄 credentials.json found",
            "platforms": platforms,
            "issues": issues,
            "action": "Fill in missing credentials and fix issues above"
        }
        
    except json.JSONDecodeError:
        return {
            "exists": True,
            "message": "❌ credentials.json is not valid JSON",
            "action": "Fix the JSON format in credentials.json"
        }
    except Exception as e:
        return {
            "exists": True,
            "message": f"❌ Error reading credentials.json: {str(e)}",
            "action": "Check the file format and permissions"
        }

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "twitter_api_integration.py",
        "linkedin_api_integration.py", 
        "social_media_integrations.py",
        "enhanced_web_interface.py",
        "credentials_template.json"
    ]
    
    missing_files = []
    existing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(f"✅ {file}")
        else:
            missing_files.append(f"❌ {file}")
    
    return {
        "missing": missing_files,
        "existing": existing_files,
        "all_present": len(missing_files) == 0
    }

def main():
    """Run quick diagnostic"""
    print("🔍 Quick Social Media Integration Diagnostic")
    print("=" * 50)
    print(f"📅 Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check credentials
    print("\n📁 Checking credentials.json...")
    creds_status = check_credentials_file()
    print(f"   {creds_status['message']}")
    
    if creds_status.get("platforms"):
        print("\n📊 Platform Status:")
        for platform in creds_status["platforms"]:
            print(f"   {platform}")
    
    if creds_status.get("issues"):
        print("\n⚠️ Issues Found:")
        for issue in creds_status["issues"]:
            print(f"   • {issue}")
    
    # Check required files
    print("\n📄 Checking required files...")
    files_status = check_required_files()
    
    if files_status["existing"]:
        print("   ✅ Found files:")
        for file in files_status["existing"]:
            print(f"      {file}")
    
    if files_status["missing"]:
        print("   ❌ Missing files:")
        for file in files_status["missing"]:
            print(f"      {file}")
    
    # Summary and recommendations
    print("\n📋 Summary:")
    
    if not creds_status["exists"]:
        print("❌ No credentials file found")
        print("\n🔧 Immediate Action Required:")
        print("1. Copy credentials_template.json to credentials.json")
        print("2. Fill in your API credentials")
        print("3. Follow the setup guides:")
        print("   - TWITTER_API_V2_SETUP.md")
        print("   - LINKEDIN_API_SETUP.md")
    
    elif creds_status.get("issues"):
        print("⚠️ Credentials need configuration")
        print("\n🔧 Action Required:")
        print(creds_status["action"])
        print("\n📚 Setup Guides:")
        print("- QUICK_SETUP_GUIDE.md (start here)")
        print("- TWITTER_API_V2_SETUP.md")
        print("- LINKEDIN_API_SETUP.md")
    
    elif files_status["all_present"]:
        print("✅ All files present and credentials configured")
        print("\n🚀 Ready to test!")
        print("\nNext steps:")
        print("1. Test individual platforms:")
        print("   python twitter_api_integration.py")
        print("   python linkedin_api_integration.py")
        print("2. Test combined integration:")
        print("   python social_media_integrations.py")
        print("3. Launch web interface:")
        print("   python enhanced_web_interface.py")
    
    else:
        print("⚠️ Some files are missing")
        print("\n🔧 Action Required:")
        print("Download or recreate missing files")
    
    # Quick test recommendation
    print("\n🧪 Quick Test:")
    if creds_status["exists"] and files_status["all_present"]:
        print("Run: python social_media_integrations.py")
    else:
        print("Fix the issues above first, then run the test")

if __name__ == "__main__":
    main() 