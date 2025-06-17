# 🔗 Social Media API Setup Guide

This guide will help you connect your social media automation system to real platforms.

## 📋 Prerequisites

- Social media accounts (Twitter, LinkedIn, Facebook)
- Google account for Gmail integration
- Developer accounts for each platform

---

## 🐦 Twitter API Setup

### Step 1: Create Twitter Developer Account
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Sign in with your Twitter account
3. Apply for a developer account
4. Wait for approval (usually 24-48 hours)

### Step 2: Create App
1. Go to [developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)
2. Click "Create App"
3. Fill in app details:
   - App name: "Your Agency Social Media Automation"
   - Description: "Automated social media posting for agency"
   - Website: Your website URL
4. Click "Create"

### Step 3: Get API Keys
1. Go to "Keys and Tokens" tab
2. Generate "Consumer Keys" (API Key & Secret)
3. Generate "Authentication Tokens" (Access Token & Secret)
4. Generate "Bearer Token"

### Step 4: Configure App Permissions
1. Go to "App Permissions"
2. Select "Read and Write" permissions
3. Save changes

---

## 💼 LinkedIn API Setup

### Step 1: Create LinkedIn App
1. Go to [linkedin.com/developers](https://linkedin.com/developers)
2. Click "Create App"
3. Fill in app details:
   - App name: "Your Agency Social Media Automation"
   - LinkedIn Page: Your company page
   - App Logo: Upload your logo
4. Click "Create App"

### Step 2: Configure OAuth 2.0
1. Go to "Auth" tab
2. Add redirect URLs:
   - `http://localhost:5000/callback`
   - `https://yourdomain.com/callback`
3. Request these scopes:
   - `r_liteprofile`
   - `w_member_social`
   - `r_organization_social`
   - `w_organization_social`

### Step 3: Get Access Token
1. Use the OAuth 2.0 flow to get access token
2. Or use LinkedIn's token generator for testing

---

## 📘 Facebook API Setup

### Step 1: Create Facebook App
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click "Create App"
3. Select "Business" type
4. Fill in app details:
   - App name: "Your Agency Social Media Automation"
   - Contact email: Your email
5. Click "Create App"

### Step 2: Add Facebook Login
1. Go to "Add Products"
2. Add "Facebook Login"
3. Configure OAuth settings
4. Add redirect URIs

### Step 3: Get Page Access Token
1. Go to "Tools" → "Graph API Explorer"
2. Select your app
3. Select your Facebook page
4. Request these permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
5. Generate access token

### Step 4: Get Page ID
1. Go to your Facebook page
2. Click "About"
3. Copy the Page ID

---

## 🌐 Google API Setup

### Step 1: Create Google Cloud Project
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create new project
3. Enable APIs:
   - Gmail API
   - Google Sheets API
   - Google Drive API

### Step 2: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Configure consent screen:
   - User Type: External
   - App name: "Your Agency Social Media Automation"
   - User support email: Your email
   - Developer contact: Your email
4. Add scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/drive`

### Step 3: Get Refresh Token
1. Use OAuth 2.0 flow to get authorization code
2. Exchange code for refresh token
3. Save refresh token securely

---

## 🔧 Configuration

### Step 1: Install Required Packages
```bash
pip install requests google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 2: Create Credentials File
1. Copy `credentials_template.json` to `credentials.json`
2. Fill in your API keys:

```json
{
  "twitter": {
    "api_key": "your_twitter_api_key",
    "api_secret": "your_twitter_api_secret",
    "access_token": "your_twitter_access_token",
    "access_token_secret": "your_twitter_access_token_secret",
    "bearer_token": "your_twitter_bearer_token"
  },
  "linkedin": {
    "client_id": "your_linkedin_client_id",
    "client_secret": "your_linkedin_client_secret",
    "access_token": "your_linkedin_access_token"
  },
  "facebook": {
    "app_id": "your_facebook_app_id",
    "app_secret": "your_facebook_app_secret",
    "access_token": "your_facebook_access_token",
    "page_id": "your_facebook_page_id"
  },
  "google": {
    "client_id": "your_google_client_id",
    "client_secret": "your_google_client_secret",
    "refresh_token": "your_google_refresh_token"
  }
}
```

### Step 3: Test Connections
```bash
python social_media_integrations.py
```

---

## 🚀 Integration with Automation System

### Step 1: Update Web Interface
The web interface will automatically use real APIs when credentials are configured.

### Step 2: Test Real Posting
1. Go to your web dashboard
2. Add content to calendar
3. Process calendar to post to real platforms

### Step 3: Monitor Results
- Check your social media accounts
- Monitor engagement metrics
- Review email notifications

---

## 🔒 Security Best Practices

### 1. Secure Credentials
- Never commit credentials to version control
- Use environment variables in production
- Rotate API keys regularly

### 2. Rate Limiting
- Respect platform rate limits
- Implement delays between posts
- Monitor API usage

### 3. Error Handling
- Handle API errors gracefully
- Log failed attempts
- Implement retry logic

---

## 🆘 Troubleshooting

### Common Issues

#### Twitter API Errors
- **401 Unauthorized**: Check API keys and tokens
- **403 Forbidden**: Verify app permissions
- **429 Rate Limited**: Implement delays

#### LinkedIn API Errors
- **401 Unauthorized**: Refresh access token
- **403 Forbidden**: Check app permissions
- **400 Bad Request**: Verify post format

#### Facebook API Errors
- **401 Unauthorized**: Check access token
- **403 Forbidden**: Verify page permissions
- **400 Bad Request**: Check post content

#### Google API Errors
- **401 Unauthorized**: Refresh access token
- **403 Forbidden**: Check API scopes
- **429 Quota Exceeded**: Monitor usage limits

### Getting Help
1. Check platform developer documentation
2. Review API error messages
3. Test with platform tools first
4. Contact platform support if needed

---

## 🎯 Next Steps

1. **Set up all API credentials**
2. **Test individual platform connections**
3. **Configure your automation system**
4. **Start with small test posts**
5. **Monitor and optimize performance**

---

**🎉 Your social media automation system is now ready to connect to real platforms!** 