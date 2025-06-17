#!/usr/bin/env python3
"""
Twitter/X API v2 Integration
Uses the latest Twitter API v2 endpoints for posting and management
Based on: https://developer.x.com/apitools/api?endpoint=%2F2%2Ftweets&method=get
"""

import os
import json
import requests
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime
import time

class TwitterAPIv2:
    def __init__(self):
        self.base_url = "https://api.twitter.com/2"
        self.credentials = self.load_credentials()
        
    def load_credentials(self) -> Dict[str, str]:
        """Load Twitter API credentials"""
        try:
            with open("credentials.json", "r") as f:
                data = json.load(f)
                return data.get("twitter", {})
        except FileNotFoundError:
            return {
                "api_key": os.getenv("TWITTER_API_KEY"),
                "api_secret": os.getenv("TWITTER_API_SECRET"),
                "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
                "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                "bearer_token": os.getenv("TWITTER_BEARER_TOKEN")
            }
    
    def get_headers(self, auth_type: str = "bearer") -> Dict[str, str]:
        """Get headers for API requests"""
        if auth_type == "bearer":
            return {
                "Authorization": f"Bearer {self.credentials['bearer_token']}",
                "Content-Type": "application/json"
            }
        elif auth_type == "oauth":
            # For OAuth 1.0a requests
            return {
                "Content-Type": "application/json"
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Twitter API connection using /2/users/me endpoint"""
        try:
            headers = self.get_headers("bearer")
            
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=headers,
                params={
                    "user.fields": "id,name,username,created_at,description,public_metrics"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Twitter API v2 connection successful",
                    "data": data,
                    "user_info": {
                        "id": data["data"]["id"],
                        "name": data["data"]["name"],
                        "username": data["data"]["username"],
                        "followers": data["data"]["public_metrics"]["followers_count"],
                        "following": data["data"]["public_metrics"]["following_count"],
                        "tweets": data["data"]["public_metrics"]["tweet_count"]
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Twitter API connection failed: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Twitter connection error: {str(e)}",
                "data": None
            }
    
    def post_tweet(self, text: str, media_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Post a tweet using Twitter API v2
        Endpoint: POST /2/tweets
        """
        try:
            headers = self.get_headers("bearer")
            
            # Prepare tweet data
            tweet_data = {
                "text": text
            }
            
            # Add media if provided
            if media_ids:
                tweet_data["media"] = {
                    "media_ids": media_ids
                }
            
            response = requests.post(
                f"{self.base_url}/tweets",
                headers=headers,
                json=tweet_data
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Tweet posted successfully",
                    "data": data,
                    "tweet_id": data["data"]["id"],
                    "text": data["data"]["text"],
                    "created_at": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to post tweet: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tweet posting error: {str(e)}",
                "data": None
            }
    
    def upload_media(self, file_path: str) -> Dict[str, Any]:
        """
        Upload media using Twitter API v1.1 (required for media upload)
        Endpoint: POST /1.1/media/upload.json
        """
        try:
            headers = self.get_headers("bearer")
            
            with open(file_path, "rb") as f:
                files = {"media": f}
                response = requests.post(
                    "https://upload.twitter.com/1.1/media/upload.json",
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "Media uploaded successfully",
                    "data": data,
                    "media_id": data["media_id_string"]
                }
            else:
                return {
                    "status": "error",
                    "message": f"Media upload failed: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Media upload error: {str(e)}",
                "data": None
            }
    
    def get_user_tweets(self, user_id: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Get user tweets using Twitter API v2
        Endpoint: GET /2/users/{id}/tweets
        """
        try:
            headers = self.get_headers("bearer")
            
            response = requests.get(
                f"{self.base_url}/users/{user_id}/tweets",
                headers=headers,
                params={
                    "max_results": max_results,
                    "tweet.fields": "created_at,public_metrics,entities",
                    "exclude": "retweets,replies"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": f"Retrieved {len(data.get('data', []))} tweets",
                    "data": data,
                    "tweets": data.get("data", [])
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get tweets: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Get tweets error: {str(e)}",
                "data": None
            }
    
    def get_tweet_metrics(self, tweet_id: str) -> Dict[str, Any]:
        """
        Get tweet metrics using Twitter API v2
        Endpoint: GET /2/tweets/{id}
        """
        try:
            headers = self.get_headers("bearer")
            
            response = requests.get(
                f"{self.base_url}/tweets/{tweet_id}",
                headers=headers,
                params={
                    "tweet.fields": "public_metrics,created_at,entities"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                metrics = data["data"]["public_metrics"]
                return {
                    "status": "success",
                    "message": "Tweet metrics retrieved successfully",
                    "data": data,
                    "metrics": {
                        "retweets": metrics["retweet_count"],
                        "likes": metrics["like_count"],
                        "replies": metrics["reply_count"],
                        "quotes": metrics["quote_count"],
                        "impressions": metrics.get("impression_count", 0)
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get tweet metrics: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Get metrics error: {str(e)}",
                "data": None
            }
    
    def search_tweets(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Search tweets using Twitter API v2
        Endpoint: GET /2/tweets/search/recent
        """
        try:
            headers = self.get_headers("bearer")
            
            response = requests.get(
                f"{self.base_url}/tweets/search/recent",
                headers=headers,
                params={
                    "query": query,
                    "max_results": max_results,
                    "tweet.fields": "created_at,public_metrics,author_id",
                    "user.fields": "name,username"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": f"Found {len(data.get('data', []))} tweets",
                    "data": data,
                    "tweets": data.get("data", [])
                }
            else:
                return {
                    "status": "error",
                    "message": f"Search failed: {response.status_code}",
                    "data": response.text,
                    "error_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Search error: {str(e)}",
                "data": None
            }
    
    def post_tweet_with_media(self, text: str, media_path: str) -> Dict[str, Any]:
        """Post tweet with media attachment"""
        try:
            # First upload the media
            media_result = self.upload_media(media_path)
            
            if media_result["status"] != "success":
                return media_result
            
            # Then post the tweet with media
            media_id = media_result["media_id"]
            return self.post_tweet(text, [media_id])
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Post with media error: {str(e)}",
                "data": None
            }
    
    def get_account_analytics(self) -> Dict[str, Any]:
        """Get comprehensive account analytics"""
        try:
            # Get user info
            user_result = self.test_connection()
            
            if user_result["status"] != "success":
                return user_result
            
            user_info = user_result["user_info"]
            
            # Get recent tweets
            tweets_result = self.get_user_tweets(user_info["id"], 20)
            
            if tweets_result["status"] != "success":
                return tweets_result
            
            # Calculate analytics
            tweets = tweets_result["tweets"]
            total_likes = sum(tweet["public_metrics"]["like_count"] for tweet in tweets)
            total_retweets = sum(tweet["public_metrics"]["retweet_count"] for tweet in tweets)
            total_replies = sum(tweet["public_metrics"]["reply_count"] for tweet in tweets)
            
            return {
                "status": "success",
                "message": "Analytics retrieved successfully",
                "data": {
                    "account": user_info,
                    "recent_tweets": len(tweets),
                    "total_likes": total_likes,
                    "total_retweets": total_retweets,
                    "total_replies": total_replies,
                    "avg_engagement": (total_likes + total_retweets + total_replies) / len(tweets) if tweets else 0
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Analytics error: {str(e)}",
                "data": None
            }

def main():
    """Test Twitter API v2 integration"""
    print("🐦 Testing Twitter/X API v2 Integration")
    print("=" * 50)
    
    twitter = TwitterAPIv2()
    
    # Test connection
    print("\n🔗 Testing API Connection...")
    connection = twitter.test_connection()
    
    if connection["status"] == "success":
        print(f"✅ {connection['message']}")
        user_info = connection["user_info"]
        print(f"👤 User: @{user_info['username']} ({user_info['name']})")
        print(f"📊 Followers: {user_info['followers']:,}")
        print(f"📈 Following: {user_info['following']:,}")
        print(f"🐦 Tweets: {user_info['tweets']:,}")
        
        # Test posting a tweet
        print("\n📝 Testing Tweet Posting...")
        test_tweet = f"🤖 Testing Twitter API v2 integration from our automation system! {datetime.now().strftime('%H:%M')}"
        post_result = twitter.post_tweet(test_tweet)
        
        if post_result["status"] == "success":
            print(f"✅ Tweet posted successfully!")
            print(f"🐦 Tweet ID: {post_result['tweet_id']}")
            print(f"📝 Text: {post_result['text']}")
            
            # Get analytics
            print("\n📊 Getting Account Analytics...")
            analytics = twitter.get_account_analytics()
            
            if analytics["status"] == "success":
                data = analytics["data"]
                print(f"📈 Recent Tweets: {data['recent_tweets']}")
                print(f"❤️ Total Likes: {data['total_likes']:,}")
                print(f"🔄 Total Retweets: {data['total_retweets']:,}")
                print(f"💬 Total Replies: {data['total_replies']:,}")
                print(f"📊 Avg Engagement: {data['avg_engagement']:.1f}")
        else:
            print(f"❌ Tweet posting failed: {post_result['message']}")
    else:
        print(f"❌ {connection['message']}")
        print("\n🔧 To fix this:")
        print("1. Check your credentials.json file")
        print("2. Verify your Twitter API keys and tokens")
        print("3. Ensure your app has the correct permissions")
        print("4. Check the API_SETUP_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main() 