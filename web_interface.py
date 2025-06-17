#!/usr/bin/env python3
"""
Web Interface for Social Media Automation
A simple Flask web app to manage your social media automation
"""

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json
import datetime
from standalone_social_media_automation import SocialMediaAutomation

app = Flask(__name__)
automation = SocialMediaAutomation()

# Load existing data
automation.load_data()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Automation Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .content {
            padding: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .form-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        button:hover {
            opacity: 0.9;
        }
        .posts-section {
            margin-top: 30px;
        }
        .post-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .post-platform {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            color: white;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .platform-twitter { background: #1DA1F2; }
        .platform-linkedin { background: #0077B5; }
        .platform-facebook { background: #4267B2; }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Social Media Automation Dashboard</h1>
            <p>Manage your automated social media posts</p>
        </div>
        
        <div class="content">
            {% if message %}
            <div class="success-message">{{ message }}</div>
            {% endif %}
            
            {% if error %}
            <div class="error-message">{{ error }}</div>
            {% endif %}
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.total_posts }}</div>
                    <div>Total Posts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.pending_posts }}</div>
                    <div>Pending Posts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.avg_characters }}</div>
                    <div>Avg Characters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.avg_hashtags }}</div>
                    <div>Avg Hashtags</div>
                </div>
            </div>
            
            <div class="form-section">
                <h3>📝 Add New Content</h3>
                <form method="POST" action="/add_content">
                    <div class="form-group">
                        <label for="topic">Content Topic:</label>
                        <input type="text" id="topic" name="topic" required placeholder="e.g., AI automation benefits">
                    </div>
                    <div class="form-group">
                        <label for="platform">Platform:</label>
                        <select id="platform" name="platform" required>
                            <option value="twitter">Twitter</option>
                            <option value="linkedin">LinkedIn</option>
                            <option value="facebook">Facebook</option>
                        </select>
                    </div>
                    <button type="submit">Add to Calendar</button>
                </form>
            </div>
            
            <div class="form-section">
                <h3>🔄 Process Content Calendar</h3>
                <form method="POST" action="/process_calendar">
                    <button type="submit">Publish All Pending Posts</button>
                </form>
            </div>
            
            <div class="posts-section">
                <h3>📊 Recent Posts</h3>
                {% for post in recent_posts %}
                <div class="post-card">
                    <div class="post-platform platform-{{ post.platform }}">{{ post.platform.upper() }}</div>
                    <h4>{{ post.topic }}</h4>
                    <p><strong>Content:</strong> {{ post.content[:100] }}...</p>
                    <p><strong>Published:</strong> {{ post.published_at }}</p>
                    <p><strong>Characters:</strong> {{ post.character_count }}</p>
                    <p><strong>Hashtags:</strong> {{ post.hashtag_count }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Get analytics
    analytics = automation.get_analytics_summary()
    
    # Count pending posts
    pending_posts = len([e for e in automation.content_calendar if e["status"] == "pending"])
    
    # Get recent posts
    recent_posts = automation.published_posts[-5:]  # Last 5 posts
    
    stats = {
        "total_posts": analytics.get("total_posts", 0),
        "pending_posts": pending_posts,
        "avg_characters": round(analytics.get("average_characters", 0), 1),
        "avg_hashtags": round(analytics.get("average_hashtags", 0), 1)
    }
    
    return render_template_string(HTML_TEMPLATE, 
                                stats=stats, 
                                recent_posts=recent_posts,
                                message=request.args.get('message'),
                                error=request.args.get('error'))

@app.route('/add_content', methods=['POST'])
def add_content():
    """Add content to calendar"""
    try:
        topic = request.form['topic']
        platform = request.form['platform']
        
        automation.add_to_content_calendar(topic, platform)
        automation.save_data()
        
        return redirect(url_for('dashboard', message=f"Added '{topic}' for {platform} to calendar!"))
    except Exception as e:
        return redirect(url_for('dashboard', error=f"Error adding content: {str(e)}"))

@app.route('/process_calendar', methods=['POST'])
def process_calendar():
    """Process all pending content"""
    try:
        results = automation.process_content_calendar()
        automation.save_data()
        
        return redirect(url_for('dashboard', message=f"Published {len(results)} posts successfully!"))
    except Exception as e:
        return redirect(url_for('dashboard', error=f"Error processing calendar: {str(e)}"))

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    analytics = automation.get_analytics_summary()
    pending_posts = len([e for e in automation.content_calendar if e["status"] == "pending"])
    
    return jsonify({
        "total_posts": analytics.get("total_posts", 0),
        "pending_posts": pending_posts,
        "average_characters": round(analytics.get("average_characters", 0), 1),
        "average_hashtags": round(analytics.get("average_hashtags", 0), 1),
        "platforms": analytics.get("platforms", {})
    })

@app.route('/api/posts')
def api_posts():
    """API endpoint for posts"""
    return jsonify(automation.published_posts)

if __name__ == '__main__':
    print("🚀 Starting Social Media Automation Web Interface")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("=" * 50)
    
    # Add some sample data if none exists
    if not automation.content_calendar:
        print("📅 Adding sample content...")
        sample_topics = [
            "AI automation benefits for businesses",
            "Digital marketing trends 2024",
            "Customer engagement strategies"
        ]
        platforms = ["twitter", "linkedin", "facebook"]
        
        for topic in sample_topics:
            for platform in platforms:
                automation.add_to_content_calendar(topic, platform)
        
        automation.save_data()
        print("✅ Sample content added!")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 