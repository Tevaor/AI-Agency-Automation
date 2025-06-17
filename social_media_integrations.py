#!/usr/bin/env python3
"""
Enhanced Social Media Integrations
Uses dedicated API modules for each platform with proper error handling
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import time

# Import dedicated API modules
try:
    from twitter_api_integration import TwitterAPIv2
except ImportError:
    print("⚠️ Twitter API module not found, using fallback integration")

class SocialMediaIntegrations:
    def __init__(self):
        self.credentials = self.load_credentials()
        self.twitter = TwitterAPIv2() if 'TwitterAPIv2' in globals() else None
        
    def load_credentials(self) -> Dict[str, Any]:
        """Load all social media credentials"""
        try:
            with open("credentials.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def test_all_connections(self) -> Dict[str, Any]:
        """Test connections to all configured platforms"""
        results = {}
        
        # Test Twitter/X
        if self.twitter:
            print("🐦 Testing Twitter/X API v2...")
            twitter_result = self.twitter.test_connection()
            results["twitter"] = twitter_result
            
            if twitter_result["status"] == "success":
                print(f"✅ Twitter: {twitter_result['message']}")
                user_info = twitter_result["user_info"]
                print(f"   👤 @{user_info['username']} ({user_info['followers']:,} followers)")
            else:
                print(f"❌ Twitter: {twitter_result['message']}")
        else:
            results["twitter"] = {"status": "error", "message": "Twitter API module not available"}
            print("❌ Twitter: API module not available")
        
        # Test LinkedIn
        if "linkedin" in self.credentials:
            print("💼 Testing LinkedIn...")
            linkedin_result = self.test_linkedin_connection()
            results["linkedin"] = linkedin_result
            
            if linkedin_result["status"] == "success":
                print(f"✅ LinkedIn: {linkedin_result['message']}")
            else:
                print(f"❌ LinkedIn: {linkedin_result['message']}")
        else:
            results["linkedin"] = {"status": "error", "message": "LinkedIn credentials not configured"}
            print("❌ LinkedIn: Credentials not configured")
        
        # Test Facebook
        if "facebook" in self.credentials:
            print("📘 Testing Facebook...")
            facebook_result = self.test_facebook_connection()
            results["facebook"] = facebook_result
            
            if facebook_result["status"] == "success":
                print(f"✅ Facebook: {facebook_result['message']}")
            else:
                print(f"❌ Facebook: {facebook_result['message']}")
        else:
            results["facebook"] = {"status": "error", "message": "Facebook credentials not configured"}
            print("❌ Facebook: Credentials not configured")
        
        return results
    
    def test_linkedin_connection(self) -> Dict[str, Any]:
        """Test LinkedIn API connection"""
        try:
            creds = self.credentials.get("linkedin", {})
            access_token = creds.get("access_token")
            
            if not access_token:
                return {"status": "error", "message": "LinkedIn access token not found"}
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Test with profile endpoint
            response = requests.get(
                "https://api.linkedin.com/v2/me",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "LinkedIn connection successful",
                    "data": data,
                    "user_info": {
                        "id": data.get("id"),
                        "name": f"{data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}",
                        "email": data.get("email-address")
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"LinkedIn connection failed: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {"status": "error", "message": f"LinkedIn connection error: {str(e)}"}
    
    def test_facebook_connection(self) -> Dict[str, Any]:
        """Test Facebook API connection"""
        try:
            creds = self.credentials.get("facebook", {})
            access_token = creds.get("access_token")
            page_id = creds.get("page_id")
            
            if not access_token:
                return {"status": "error", "message": "Facebook access token not found"}
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Test with user endpoint
            response = requests.get(
                "https://graph.facebook.com/v18.0/me",
                headers=headers,
                params={"fields": "id,name,email"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Facebook connection successful",
                    "data": data,
                    "user_info": {
                        "id": data.get("id"),
                        "name": data.get("name"),
                        "email": data.get("email")
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Facebook connection failed: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {"status": "error", "message": f"Facebook connection error: {str(e)}"}
    
    def post_to_twitter(self, content: str, media_path: Optional[str] = None) -> Dict[str, Any]:
        """Post content to Twitter/X using API v2"""
        if not self.twitter:
            return {"status": "error", "message": "Twitter API module not available"}
        
        try:
            if media_path and os.path.exists(media_path):
                return self.twitter.post_tweet_with_media(content, media_path)
            else:
                return self.twitter.post_tweet(content)
        except Exception as e:
            return {"status": "error", "message": f"Twitter posting error: {str(e)}"}
    
    def post_to_linkedin(self, content: str, media_path: Optional[str] = None) -> Dict[str, Any]:
        """Post content to LinkedIn"""
        try:
            creds = self.credentials.get("linkedin", {})
            access_token = creds.get("access_token")
            
            if not access_token:
                return {"status": "error", "message": "LinkedIn access token not found"}
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # LinkedIn post data
            post_data = {
                "author": f"urn:li:person:{creds.get('user_id', '')}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "status": "success",
                    "message": "LinkedIn post published successfully",
                    "data": data,
                    "post_id": data.get("id")
                }
            else:
                return {
                    "status": "error",
                    "message": f"LinkedIn posting failed: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {"status": "error", "message": f"LinkedIn posting error: {str(e)}"}
    
    def post_to_facebook(self, content: str, media_path: Optional[str] = None) -> Dict[str, Any]:
        """Post content to Facebook"""
        try:
            creds = self.credentials.get("facebook", {})
            access_token = creds.get("access_token")
            page_id = creds.get("page_id")
            
            if not access_token:
                return {"status": "error", "message": "Facebook access token not found"}
            
            # Use page access token if page_id is provided
            if page_id:
                token = creds.get("page_access_token", access_token)
                endpoint = f"https://graph.facebook.com/v18.0/{page_id}/feed"
            else:
                token = access_token
                endpoint = "https://graph.facebook.com/v18.0/me/feed"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            post_data = {
                "message": content
            }
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Facebook post published successfully",
                    "data": data,
                    "post_id": data.get("id")
                }
            else:
                return {
                    "status": "error",
                    "message": f"Facebook posting failed: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {"status": "error", "message": f"Facebook posting error: {str(e)}"}
    
    def post_to_all_platforms(self, content: str, platforms: List[str] = None, media_path: Optional[str] = None) -> Dict[str, Any]:
        """Post content to multiple platforms"""
        if platforms is None:
            platforms = ["twitter", "linkedin", "facebook"]
        
        results = {}
        
        for platform in platforms:
            print(f"📤 Posting to {platform.title()}...")
            
            if platform == "twitter":
                results[platform] = self.post_to_twitter(content, media_path)
            elif platform == "linkedin":
                results[platform] = self.post_to_linkedin(content, media_path)
            elif platform == "facebook":
                results[platform] = self.post_to_facebook(content, media_path)
            else:
                results[platform] = {"status": "error", "message": f"Unknown platform: {platform}"}
            
            # Add delay between posts to avoid rate limiting
            time.sleep(2)
        
        return results
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics from all platforms"""
        analytics = {}
        
        # Twitter analytics
        if self.twitter:
            twitter_analytics = self.twitter.get_account_analytics()
            analytics["twitter"] = twitter_analytics
        
        # LinkedIn analytics (basic)
        if "linkedin" in self.credentials:
            analytics["linkedin"] = {
                "status": "info",
                "message": "LinkedIn analytics require additional API permissions"
            }
        
        # Facebook analytics (basic)
        if "facebook" in self.credentials:
            analytics["facebook"] = {
                "status": "info", 
                "message": "Facebook analytics require additional API permissions"
            }
        
        return analytics

def main():
    """Test social media integrations"""
    print("🚀 Testing Enhanced Social Media Integrations")
    print("=" * 60)
    
    integrations = SocialMediaIntegrations()
    
    # Test all connections
    print("\n🔗 Testing Platform Connections...")
    connection_results = integrations.test_all_connections()
    
    # Summary
    print("\n📊 Connection Summary:")
    successful_platforms = []
    for platform, result in connection_results.items():
        if result["status"] == "success":
            successful_platforms.append(platform)
            print(f"✅ {platform.title()}: Connected")
        else:
            print(f"❌ {platform.title()}: {result['message']}")
    
    if successful_platforms:
        print(f"\n🎉 Successfully connected to {len(successful_platforms)} platform(s): {', '.join(successful_platforms)}")
        
        # Test posting
        test_content = f"🤖 Testing enhanced social media automation system! {datetime.now().strftime('%H:%M')}"
        
        print(f"\n📝 Testing Posting to {successful_platforms[0].title()}...")
        post_result = integrations.post_to_all_platforms(test_content, [successful_platforms[0]])
        
        for platform, result in post_result.items():
            if result["status"] == "success":
                print(f"✅ {platform.title()}: Post successful!")
                if "post_id" in result:
                    print(f"   📄 Post ID: {result['post_id']}")
            else:
                print(f"❌ {platform.title()}: {result['message']}")
    else:
        print("\n⚠️ No platforms connected successfully.")
        print("🔧 Please check your credentials.json file and API_SETUP_GUIDE.md")

if __name__ == "__main__":
    main() 