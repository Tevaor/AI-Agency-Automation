#!/usr/bin/env python3
"""
LinkedIn API v2 Integration
Uses the latest LinkedIn API for posting and management
Based on LinkedIn Developer Portal: https://www.linkedin.com/developers/
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import time

class LinkedInAPIv2:
    def __init__(self):
        self.base_url = "https://api.linkedin.com/v2"
        self.credentials = self.load_credentials()
        
    def load_credentials(self) -> Dict[str, str]:
        """Load LinkedIn API credentials"""
        try:
            with open("credentials.json", "r") as f:
                data = json.load(f)
                return data.get("linkedin", {})
        except FileNotFoundError:
            return {
                "client_id": os.getenv("LINKEDIN_CLIENT_ID"),
                "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
                "access_token": os.getenv("LINKEDIN_ACCESS_TOKEN"),
                "user_id": os.getenv("LINKEDIN_USER_ID")
            }
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.credentials['access_token']}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test LinkedIn API connection using /v2/me endpoint"""
        try:
            headers = self.get_headers()
            
            response = requests.get(
                f"{self.base_url}/me",
                headers=headers,
                params={
                    "projection": "(id,localizedFirstName,localizedLastName,profilePicture(displayImage~:playableStreams))"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "LinkedIn API v2 connection successful",
                    "data": data,
                    "user_info": {
                        "id": data["id"],
                        "name": f"{data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}",
                        "profile_id": data["id"]
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"LinkedIn API connection failed: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"LinkedIn connection error: {str(e)}",
                "data": None
            }
    
    def post_content(self, text: str, visibility: str = "PUBLIC") -> Dict[str, Any]:
        """
        Post content to LinkedIn using API v2
        Endpoint: POST /v2/ugcPosts
        """
        try:
            headers = self.get_headers()
            
            # LinkedIn UGC Post data structure
            post_data = {
                "author": f"urn:li:person:{self.credentials.get('user_id', '')}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "status": "success",
                    "message": "LinkedIn post published successfully",
                    "data": data,
                    "post_id": data.get("id"),
                    "text": text,
                    "created_at": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to post to LinkedIn: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"LinkedIn posting error: {str(e)}",
                "data": None
            }
    
    def post_with_media(self, text: str, media_url: str, media_title: str = "", media_description: str = "") -> Dict[str, Any]:
        """
        Post content with media to LinkedIn
        """
        try:
            headers = self.get_headers()
            
            post_data = {
                "author": f"urn:li:person:{self.credentials.get('user_id', '')}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "ARTICLE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": media_description
                                },
                                "media": media_url,
                                "title": {
                                    "text": media_title
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "status": "success",
                    "message": "LinkedIn post with media published successfully",
                    "data": data,
                    "post_id": data.get("id")
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to post with media: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"LinkedIn media posting error: {str(e)}",
                "data": None
            }
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get LinkedIn profile information
        Endpoint: GET /v2/me
        """
        try:
            headers = self.get_headers()
            
            response = requests.get(
                f"{self.base_url}/me",
                headers=headers,
                params={
                    "projection": "(id,localizedFirstName,localizedLastName,localizedHeadline,profilePicture(displayImage~:playableStreams),publicProfileUrl)"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Profile retrieved successfully",
                    "data": data,
                    "profile": {
                        "id": data["id"],
                        "name": f"{data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}",
                        "headline": data.get("localizedHeadline", ""),
                        "profile_url": data.get("publicProfileUrl", "")
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get profile: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Profile retrieval error: {str(e)}",
                "data": None
            }
    
    def get_network_updates(self, count: int = 10) -> Dict[str, Any]:
        """
        Get network updates (recent posts from connections)
        Note: This requires additional permissions
        """
        try:
            headers = self.get_headers()
            
            response = requests.get(
                f"{self.base_url}/networkSizes/urn:li:person:{self.credentials.get('user_id', '')}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Network information retrieved",
                    "data": data
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get network info: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Network retrieval error: {str(e)}",
                "data": None
            }
    
    def search_people(self, keywords: str, count: int = 10) -> Dict[str, Any]:
        """
        Search for people on LinkedIn
        Note: This requires additional permissions
        """
        try:
            headers = self.get_headers()
            
            response = requests.get(
                f"{self.base_url}/people",
                headers=headers,
                params={
                    "q": "people",
                    "keywords": keywords,
                    "count": count
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": f"Found {len(data.get('elements', []))} people",
                    "data": data
                }
            else:
                return {
                    "status": "error",
                    "message": f"Search failed: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Search error: {str(e)}",
                "data": None
            }
    
    def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """
        Get analytics for a specific post
        Note: This requires additional permissions
        """
        try:
            headers = self.get_headers()
            
            response = requests.get(
                f"{self.base_url}/socialMetrics/{post_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Post analytics retrieved",
                    "data": data
                }
            else:
                return {
                    "status": "error",
                    "message": f"Analytics retrieval failed: {response.status_code}",
                    "data": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Analytics error: {str(e)}",
                "data": None
            }
    
    def get_account_analytics(self) -> Dict[str, Any]:
        """Get comprehensive account analytics"""
        try:
            # Get profile info
            profile_result = self.get_profile()
            
            if profile_result["status"] != "success":
                return profile_result
            
            profile = profile_result["profile"]
            
            # Get network info
            network_result = self.get_network_updates()
            
            return {
                "status": "success",
                "message": "LinkedIn analytics retrieved successfully",
                "data": {
                    "profile": profile,
                    "network_info": network_result.get("data", {}),
                    "last_updated": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"LinkedIn analytics error: {str(e)}",
                "data": None
            }

def main():
    """Test LinkedIn API v2 integration"""
    print("💼 Testing LinkedIn API v2 Integration")
    print("=" * 50)
    
    linkedin = LinkedInAPIv2()
    
    # Test connection
    print("\n🔗 Testing API Connection...")
    connection = linkedin.test_connection()
    
    if connection["status"] == "success":
        print(f"✅ {connection['message']}")
        user_info = connection["user_info"]
        print(f"👤 User: {user_info['name']} (ID: {user_info['id']})")
        
        # Test posting
        print("\n📝 Testing Content Posting...")
        test_post = f"🤖 Testing LinkedIn API v2 integration from our automation system! {datetime.now().strftime('%H:%M')}"
        post_result = linkedin.post_content(test_post)
        
        if post_result["status"] == "success":
            print(f"✅ LinkedIn post published successfully!")
            print(f"📄 Post ID: {post_result['post_id']}")
            print(f"📝 Text: {post_result['text']}")
            
            # Get analytics
            print("\n📊 Getting Account Analytics...")
            analytics = linkedin.get_account_analytics()
            
            if analytics["status"] == "success":
                data = analytics["data"]
                profile = data["profile"]
                print(f"👤 Profile: {profile['name']}")
                print(f"💼 Headline: {profile['headline']}")
                print(f"🔗 Profile URL: {profile['profile_url']}")
        else:
            print(f"❌ LinkedIn posting failed: {post_result['message']}")
    else:
        print(f"❌ {connection['message']}")
        print("\n🔧 To fix this:")
        print("1. Check your credentials.json file")
        print("2. Verify your LinkedIn API credentials")
        print("3. Ensure your app has the correct permissions")
        print("4. Check the LINKEDIN_API_SETUP.md for detailed instructions")

if __name__ == "__main__":
    main() 