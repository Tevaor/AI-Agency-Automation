#!/usr/bin/env python3
"""
Twitter API v2 Setup Diagnostic Tool
Helps identify and fix common setup issues
"""

import os
import json
import requests
from typing import Dict, Any

def check_credentials_file() -> Dict[str, Any]:
    """Check if credentials.json exists and has Twitter config"""
    result = {"status": "error", "message": "", "details": {}}
    
    if not os.path.exists("credentials.json"):
        result["message"] = "credentials.json file not found"
        result["details"]["file_exists"] = False
        return result
    
    try:
        with open("credentials.json", "r") as f:
            data = json.load(f)
        
        result["details"]["file_exists"] = True
        result["details"]["file_valid"] = True
        
        if "twitter" not in data:
            result["message"] = "Twitter credentials not found in credentials.json"
            result["details"]["twitter_section"] = False
            return result
        
        twitter_creds = data["twitter"]
        result["details"]["twitter_section"] = True
        
        # Check each required field
        required_fields = ["api_key", "api_secret", "access_token", "access_token_secret", "bearer_token"]
        missing_fields = []
        
        for field in required_fields:
            if field not in twitter_creds or not twitter_creds[field] or twitter_creds[field].startswith("YOUR_"):
                missing_fields.append(field)
        
        if missing_fields:
            result["message"] = f"Missing or placeholder Twitter credentials: {', '.join(missing_fields)}"
            result["details"]["missing_fields"] = missing_fields
            return result
        
        result["status"] = "success"
        result["message"] = "Twitter credentials found and appear valid"
        result["details"]["all_fields_present"] = True
        return result
        
    except json.JSONDecodeError:
        result["message"] = "credentials.json is not valid JSON"
        result["details"]["file_valid"] = False
        return result
    except Exception as e:
        result["message"] = f"Error reading credentials.json: {str(e)}"
        return result

def test_bearer_token(bearer_token: str) -> Dict[str, Any]:
    """Test if Bearer Token is valid"""
    result = {"status": "error", "message": "", "details": {}}
    
    if not bearer_token or bearer_token.startswith("YOUR_"):
        result["message"] = "Bearer token is missing or placeholder"
        return result
    
    try:
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://api.twitter.com/2/users/me",
            headers=headers,
            params={"user.fields": "id,name,username"}
        )
        
        result["details"]["status_code"] = response.status_code
        
        if response.status_code == 200:
            data = response.json()
            result["status"] = "success"
            result["message"] = "Bearer token is valid"
            result["details"]["user_info"] = {
                "id": data["data"]["id"],
                "name": data["data"]["name"],
                "username": data["data"]["username"]
            }
        elif response.status_code == 401:
            result["message"] = "Bearer token is invalid or expired"
        elif response.status_code == 403:
            result["message"] = "Bearer token lacks required permissions"
        elif response.status_code == 429:
            result["message"] = "Rate limit exceeded"
        else:
            result["message"] = f"Unexpected response: {response.status_code}"
            result["details"]["response_text"] = response.text[:200]
            
    except Exception as e:
        result["message"] = f"Error testing bearer token: {str(e)}"
    
    return result

def check_environment_variables() -> Dict[str, Any]:
    """Check if Twitter credentials are set as environment variables"""
    result = {"status": "info", "message": "", "details": {}}
    
    env_vars = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET", 
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
        "TWITTER_BEARER_TOKEN"
    ]
    
    found_vars = []
    for var in env_vars:
        if os.getenv(var):
            found_vars.append(var)
    
    if found_vars:
        result["message"] = f"Found {len(found_vars)} Twitter environment variables"
        result["details"]["found_vars"] = found_vars
    else:
        result["message"] = "No Twitter environment variables found"
        result["details"]["found_vars"] = []
    
    return result

def main():
    """Run comprehensive Twitter API setup diagnostics"""
    print("🔍 Twitter API v2 Setup Diagnostic Tool")
    print("=" * 50)
    
    # Check credentials file
    print("\n📁 Checking credentials.json...")
    creds_check = check_credentials_file()
    
    if creds_check["status"] == "success":
        print(f"✅ {creds_check['message']}")
        
        # Load credentials for testing
        with open("credentials.json", "r") as f:
            data = json.load(f)
            bearer_token = data["twitter"]["bearer_token"]
        
        # Test bearer token
        print("\n🔑 Testing Bearer Token...")
        token_test = test_bearer_token(bearer_token)
        
        if token_test["status"] == "success":
            print(f"✅ {token_test['message']}")
            user_info = token_test["details"]["user_info"]
            print(f"👤 Connected as: @{user_info['username']} ({user_info['name']})")
            
            print("\n🎉 Twitter API v2 setup is working correctly!")
            print("\nNext steps:")
            print("1. Run: python twitter_api_integration.py")
            print("2. Run: python enhanced_web_interface.py")
            print("3. Start posting content!")
            
        else:
            print(f"❌ {token_test['message']}")
            print(f"   Status Code: {token_test['details'].get('status_code', 'N/A')}")
            
            if token_test["details"].get("status_code") == 403:
                print("\n🔧 To fix 403 error:")
                print("1. Go to https://developer.twitter.com/")
                print("2. Check your app permissions (should be 'Read and Write')")
                print("3. Verify your developer account is approved")
                print("4. Regenerate your Bearer Token")
                
            elif token_test["details"].get("status_code") == 401:
                print("\n🔧 To fix 401 error:")
                print("1. Regenerate your Bearer Token")
                print("2. Check that your API keys are correct")
                print("3. Verify your app is properly configured")
                
    else:
        print(f"❌ {creds_check['message']}")
        
        if not creds_check["details"].get("file_exists"):
            print("\n🔧 To fix this:")
            print("1. Copy credentials_template.json to credentials.json")
            print("2. Fill in your Twitter API credentials")
            print("3. Follow the TWITTER_API_V2_SETUP.md guide")
            
        elif not creds_check["details"].get("twitter_section"):
            print("\n🔧 To fix this:")
            print("1. Add Twitter section to credentials.json")
            print("2. Fill in all required Twitter API credentials")
            
        elif creds_check["details"].get("missing_fields"):
            print("\n🔧 To fix this:")
            print("1. Get your Twitter API credentials from https://developer.twitter.com/")
            print("2. Replace placeholder values in credentials.json")
            print("3. Follow the TWITTER_API_V2_SETUP.md guide")
    
    # Check environment variables
    print("\n🌍 Checking environment variables...")
    env_check = check_environment_variables()
    print(f"ℹ️ {env_check['message']}")
    
    # Summary and recommendations
    print("\n📋 Summary:")
    if creds_check["status"] == "success" and "token_test" in locals() and token_test["status"] == "success":
        print("✅ Twitter API v2 is properly configured and working!")
    else:
        print("❌ Twitter API v2 needs configuration")
        print("\n📚 Resources:")
        print("- TWITTER_API_V2_SETUP.md - Detailed setup guide")
        print("- https://developer.twitter.com/ - Official documentation")
        print("- https://developer.twitter.com/en/docs/twitter-api - API reference")

if __name__ == "__main__":
    main() 