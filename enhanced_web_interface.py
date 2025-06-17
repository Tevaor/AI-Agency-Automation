#!/usr/bin/env python3
"""
Enhanced Web Interface with Real Social Media Integrations
Connects to actual social media platforms and Google services
"""

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json
import datetime
import os
from social_media_integrations import SocialMediaIntegrations

app = Flask(__name__)
integrations = SocialMediaIntegrations()

# Enhanced HTML Template with Real Platform Integration
ENHANCED_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Social Media Automation Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
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
        .connection-status {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .connection-card {
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }
        .connection-success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #28a745;
        }
        .connection-error {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #dc3545;
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
        .warning-message {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }
        .tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
            font-weight: bold;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .credentials-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .platform-credentials {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Professional Social Media Automation</h1>
            <p>Connect to real platforms and automate your social media presence</p>
        </div>
        
        <div class="content">
            {% if message %}
            <div class="success-message">{{ message }}</div>
            {% endif %}
            
            {% if error %}
            <div class="error-message">{{ error }}</div>
            {% endif %}
            
            {% if warning %}
            <div class="warning-message">{{ warning }}</div>
            {% endif %}
            
            <div class="tabs">
                <div class="tab active" onclick="showTab('dashboard')">📊 Dashboard</div>
                <div class="tab" onclick="showTab('content')">📝 Content</div>
                <div class="tab" onclick="showTab('connections')">🔗 Connections</div>
                <div class="tab" onclick="showTab('analytics')">📈 Analytics</div>
            </div>
            
            <!-- Dashboard Tab -->
            <div id="dashboard" class="tab-content active">
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
                
                <div class="connection-status">
                    {% for platform, status in connection_status.items() %}
                    <div class="connection-card {{ 'connection-success' if status.status == 'success' else 'connection-error' }}">
                        {{ platform.upper() }}: {{ status.message }}
                    </div>
                    {% endfor %}
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
            
            <!-- Content Tab -->
            <div id="content" class="tab-content">
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
                        <div class="form-group">
                            <label for="image_path">Image (optional):</label>
                            <input type="file" id="image_path" name="image_path" accept="image/*">
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
            </div>
            
            <!-- Connections Tab -->
            <div id="connections" class="tab-content">
                <div class="credentials-section">
                    <h3>🔗 Platform Connections</h3>
                    
                    <div class="platform-credentials">
                        <h4>🐦 Twitter</h4>
                        <p>Status: {{ connection_status.twitter.message }}</p>
                        <button onclick="testConnection('twitter')">Test Connection</button>
                    </div>
                    
                    <div class="platform-credentials">
                        <h4>💼 LinkedIn</h4>
                        <p>Status: {{ connection_status.linkedin.message }}</p>
                        <button onclick="testConnection('linkedin')">Test Connection</button>
                    </div>
                    
                    <div class="platform-credentials">
                        <h4>📘 Facebook</h4>
                        <p>Status: {{ connection_status.facebook.message }}</p>
                        <button onclick="testConnection('facebook')">Test Connection</button>
                    </div>
                    
                    <div class="platform-credentials">
                        <h4>🌐 Google</h4>
                        <p>Status: {{ connection_status.google.message }}</p>
                        <button onclick="testConnection('google')">Test Connection</button>
                    </div>
                </div>
                
                <div class="form-section">
                    <h3>⚙️ Configure Credentials</h3>
                    <p>Update your credentials.json file with your API keys to enable real platform posting.</p>
                    <a href="/download_credentials_template" class="button">Download Credentials Template</a>
                </div>
            </div>
            
            <!-- Analytics Tab -->
            <div id="analytics" class="tab-content">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{{ analytics.twitter.total_posts if analytics.twitter else 0 }}</div>
                        <div>Twitter Posts</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ analytics.linkedin.total_posts if analytics.linkedin else 0 }}</div>
                        <div>LinkedIn Posts</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ analytics.facebook.total_posts if analytics.facebook else 0 }}</div>
                        <div>Facebook Posts</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ analytics.total_posts }}</div>
                        <div>Total Posts</div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h3>📊 Platform Performance</h3>
                    {% for platform, stats in analytics.platforms.items() %}
                    <div class="platform-credentials">
                        <h4>{{ platform.upper() }}</h4>
                        <p>Total Posts: {{ stats.total_posts }}</p>
                        <p>Average Characters: {{ stats.total_characters // stats.total_posts if stats.total_posts > 0 else 0 }}</p>
                        <p>Total Hashtags: {{ stats.total_hashtags }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tab contents
            var tabContents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove('active');
            }
            
            // Remove active class from all tabs
            var tabs = document.getElementsByClassName('tab');
            for (var i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove('active');
            }
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        function testConnection(platform) {
            fetch('/test_connection/' + platform)
                .then(response => response.json())
                .then(data => {
                    alert(platform.toUpperCase() + ': ' + data.message);
                    location.reload();
                })
                .catch(error => {
                    alert('Error testing connection: ' + error);
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard with real platform integration"""
    # Test all connections
    connection_results = integrations.test_all_connections()
    
    # Get analytics
    analytics = integrations.get_analytics_summary() if hasattr(integrations, 'get_analytics_summary') else {
        "total_posts": 0,
        "platforms": {}
    }
    
    # Count pending posts (simulated for now)
    pending_posts = 5  # This would come from your content calendar
    
    # Get recent posts (simulated for now)
    recent_posts = [
        {
            "platform": "twitter",
            "topic": "AI automation benefits",
            "content": "Discover how AI automation can transform your business! 🚀",
            "published_at": datetime.datetime.now().isoformat(),
            "character_count": 76,
            "hashtag_count": 4
        }
    ]
    
    stats = {
        "total_posts": analytics.get("total_posts", 0),
        "pending_posts": pending_posts,
        "avg_characters": round(analytics.get("average_characters", 0), 1),
        "avg_hashtags": round(analytics.get("average_hashtags", 0), 1)
    }
    
    return render_template_string(ENHANCED_HTML_TEMPLATE, 
                                stats=stats, 
                                recent_posts=recent_posts,
                                connection_status=connection_results,
                                analytics=analytics,
                                message=request.args.get('message'),
                                error=request.args.get('error'),
                                warning=request.args.get('warning'))

@app.route('/add_content', methods=['POST'])
def add_content():
    """Add content to calendar with real platform posting"""
    try:
        topic = request.form['topic']
        platform = request.form['platform']
        
        # Generate content using AI
        content = integrations.generate_content(topic, platform)
        
        # Post to real platform if credentials are configured
        if platform == "twitter":
            result = integrations.post_to_twitter(content["formatted_content"])
        elif platform == "linkedin":
            result = integrations.post_to_linkedin(content["formatted_content"])
        elif platform == "facebook":
            result = integrations.post_to_facebook(content["formatted_content"])
        
        if result["status"] == "success":
            return redirect(url_for('dashboard', message=f"Posted to {platform}: {result['message']}"))
        else:
            return redirect(url_for('dashboard', error=f"Failed to post to {platform}: {result['message']}"))
            
    except Exception as e:
        return redirect(url_for('dashboard', error=f"Error adding content: {str(e)}"))

@app.route('/process_calendar', methods=['POST'])
def process_calendar():
    """Process all pending content with real platform posting"""
    try:
        # This would process your content calendar and post to real platforms
        results = []
        
        # Simulate posting to multiple platforms
        platforms = ["twitter", "linkedin", "facebook"]
        for platform in platforms:
            content = f"Automated post to {platform} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            if platform == "twitter":
                result = integrations.post_to_twitter(content)
            elif platform == "linkedin":
                result = integrations.post_to_linkedin(content)
            elif platform == "facebook":
                result = integrations.post_to_facebook(content)
            
            results.append(result)
        
        success_count = len([r for r in results if r["status"] == "success"])
        
        return redirect(url_for('dashboard', message=f"Posted {success_count} posts to real platforms!"))
    except Exception as e:
        return redirect(url_for('dashboard', error=f"Error processing calendar: {str(e)}"))

@app.route('/test_connection/<platform>')
def test_connection(platform):
    """Test connection to specific platform"""
    try:
        if platform == "twitter":
            result = integrations.test_twitter_connection()
        elif platform == "linkedin":
            result = integrations.test_linkedin_connection()
        elif platform == "facebook":
            result = integrations.test_facebook_connection()
        elif platform == "google":
            result = integrations.test_google_connection()
        else:
            result = {"status": "error", "message": "Unknown platform"}
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download_credentials_template')
def download_credentials_template():
    """Download credentials template"""
    return send_file('credentials_template.json', as_attachment=True)

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    analytics = integrations.get_analytics_summary() if hasattr(integrations, 'get_analytics_summary') else {
        "total_posts": 0,
        "platforms": {}
    }
    
    return jsonify({
        "total_posts": analytics.get("total_posts", 0),
        "platforms": analytics.get("platforms", {})
    })

@app.route('/api/posts')
def api_posts():
    """API endpoint for posts"""
    # This would return real posts from your platforms
    return jsonify([])

if __name__ == '__main__':
    print("🚀 Starting Enhanced Social Media Automation Web Interface")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔗 Real platform integration enabled!")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 