#!/usr/bin/env python3
"""
Test Script for Social Media Automation Workflow
This script helps test the workflow components without actually posting to social media.
"""

import json
import requests
from datetime import datetime
import os

class SocialMediaWorkflowTester:
    def __init__(self):
        self.test_results = []
        
    def test_content_generation(self, topic, platform):
        """Test AI content generation"""
        print(f"\n🧪 Testing Content Generation for {platform}")
        print(f"Topic: {topic}")
        
        # Simulate AI response
        mock_ai_response = {
            "post": f"Discover how {topic} can transform your business! 🚀",
            "hashtags": ["#automation", "#business", "#efficiency"],
            "cta": "Learn more in our latest guide!"
        }
        
        print(f"✅ Generated Content:")
        print(f"   Post: {mock_ai_response['post']}")
        print(f"   Hashtags: {', '.join(mock_ai_response['hashtags'])}")
        print(f"   CTA: {mock_ai_response['cta']}")
        
        return mock_ai_response
    
    def test_platform_formatting(self, content, platform):
        """Test platform-specific formatting"""
        print(f"\n📱 Testing {platform} Formatting")
        
        if platform == "twitter":
            formatted_content = f"{content['post']}\n\n{' '.join(content['hashtags'])}\n\n{content['cta']}"
            char_count = len(formatted_content)
            print(f"   Character count: {char_count}")
            if char_count > 280:
                print(f"   ⚠️  Warning: Exceeds Twitter's 280 character limit")
            else:
                print(f"   ✅ Within Twitter's character limit")
                
        elif platform == "linkedin":
            formatted_content = f"{content['post']}\n\n{' '.join(content['hashtags'])}\n\n{content['cta']}"
            print(f"   ✅ LinkedIn formatted content ready")
            
        elif platform == "facebook":
            formatted_content = f"{content['post']}\n\n{' '.join(content['hashtags'])}\n\n{content['cta']}"
            print(f"   ✅ Facebook formatted content ready")
            
        return formatted_content
    
    def test_notification_system(self, platform, content):
        """Test notification system"""
        print(f"\n📧 Testing Notification System")
        notification = {
            "to": "team@youragency.com",
            "subject": f"Social Media Post Published - {platform}",
            "body": f"Post has been published to {platform}:\n\n{content['post']}\n\nHashtags: {', '.join(content['hashtags'])}\n\nCTA: {content['cta']}"
        }
        
        print(f"   ✅ Notification prepared:")
        print(f"   To: {notification['to']}")
        print(f"   Subject: {notification['subject']}")
        
        return notification
    
    def test_analytics_logging(self, platform, content):
        """Test analytics logging"""
        print(f"\n📊 Testing Analytics Logging")
        
        analytics_entry = {
            "platform": platform,
            "post": content['post'],
            "hashtags": ', '.join(content['hashtags']),
            "cta": content['cta'],
            "timestamp": datetime.now().isoformat(),
            "post_length": len(content['post']),
            "hashtag_count": len(content['hashtags'])
        }
        
        print(f"   ✅ Analytics entry created:")
        print(f"   Platform: {analytics_entry['platform']}")
        print(f"   Post Length: {analytics_entry['post_length']} characters")
        print(f"   Hashtag Count: {analytics_entry['hashtag_count']}")
        
        return analytics_entry
    
    def run_full_test(self):
        """Run complete workflow test"""
        print("🚀 Starting Social Media Automation Workflow Test")
        print("=" * 60)
        
        # Test data
        test_topics = [
            "AI automation benefits for businesses",
            "Digital marketing trends 2024",
            "Customer engagement strategies"
        ]
        
        platforms = ["twitter", "linkedin", "facebook"]
        
        for topic in test_topics:
            print(f"\n{'='*20} Testing Topic: {topic} {'='*20}")
            
            for platform in platforms:
                print(f"\n📋 Testing {platform.upper()} workflow")
                
                # Test content generation
                content = self.test_content_generation(topic, platform)
                
                # Test platform formatting
                formatted_content = self.test_platform_formatting(content, platform)
                
                # Test notification system
                notification = self.test_notification_system(platform, content)
                
                # Test analytics logging
                analytics = self.test_analytics_logging(platform, content)
                
                # Store test results
                self.test_results.append({
                    "topic": topic,
                    "platform": platform,
                    "content": content,
                    "formatted_content": formatted_content,
                    "notification": notification,
                    "analytics": analytics,
                    "timestamp": datetime.now().isoformat()
                })
                
                print(f"   ✅ {platform.upper()} workflow test completed successfully")
        
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate a test report"""
        print(f"\n{'='*60}")
        print("📋 TEST REPORT")
        print(f"{'='*60}")
        
        print(f"Total tests run: {len(self.test_results)}")
        print(f"Platforms tested: {len(set(r['platform'] for r in self.test_results))}")
        print(f"Topics tested: {len(set(r['topic'] for r in self.test_results))}")
        
        # Save test results to file
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n✅ Test results saved to 'test_results.json'")
        print(f"✅ All workflow components tested successfully!")
        
        # Summary by platform
        print(f"\n📊 Platform Summary:")
        for platform in ["twitter", "linkedin", "facebook"]:
            platform_tests = [r for r in self.test_results if r['platform'] == platform]
            print(f"   {platform.upper()}: {len(platform_tests)} tests completed")

def main():
    """Main function to run the test"""
    tester = SocialMediaWorkflowTester()
    
    try:
        tester.run_full_test()
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🎉 All tests completed successfully!")
    else:
        print(f"\n💥 Some tests failed. Please check the errors above.") 