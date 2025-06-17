# Quick Setup Guide - Social Media Automation

## Current Status
Based on your test results:
- ❌ **Twitter**: 403 error (permissions/credentials issue)
- ❌ **LinkedIn**: Credentials not configured
- ❌ **Facebook**: Credentials not configured

## Immediate Action Plan

### 1. Fix Twitter API (403 Error)

The 403 error indicates your Twitter app lacks proper permissions. Here's how to fix it:

#### Step 1: Update Twitter App Permissions
1. Go to [https://developer.twitter.com/](https://developer.twitter.com/)
2. Navigate to your app settings
3. Go to "App permissions" → Set to **"Read and Write"**
4. Save changes

#### Step 2: Regenerate Tokens
1. Go to "Keys and tokens" tab
2. **Regenerate** your Access Token and Secret
3. Copy the new Bearer Token
4. Update your `credentials.json`

#### Step 3: Verify Credentials
```json
{
  "twitter": {
    "api_key": "YOUR_ACTUAL_API_KEY",
    "api_secret": "YOUR_ACTUAL_API_SECRET",
    "access_token": "YOUR_NEW_ACCESS_TOKEN",
    "access_token_secret": "YOUR_NEW_ACCESS_TOKEN_SECRET",
    "bearer_token": "YOUR_NEW_BEARER_TOKEN"
  }
}
```

### 2. Configure LinkedIn API

Based on your LinkedIn developer URLs, you have apps set up. Here's how to configure them:

#### Step 1: Get LinkedIn Credentials
1. Go to [https://www.linkedin.com/developers/apps/223819743/products](https://www.linkedin.com/developers/apps/223819743/products)
2. Copy your **Client ID** and **Client Secret**

#### Step 2: Generate Access Token
1. Go to [https://www.linkedin.com/developers/tools/oauth/playground](https://www.linkedin.com/developers/tools/oauth/playground)
2. Enter your Client ID and Client Secret
3. Set redirect URI to: `https://www.linkedin.com/developers/tools/oauth/playground`
4. Select scopes: `r_liteprofile w_member_social`
5. Click "Request Token" and authorize
6. Copy the generated access token

#### Step 3: Get Your LinkedIn User ID
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     "https://api.linkedin.com/v2/me"
```

#### Step 4: Update Credentials
```json
{
  "linkedin": {
    "client_id": "YOUR_LINKEDIN_CLIENT_ID",
    "client_secret": "YOUR_LINKEDIN_CLIENT_SECRET",
    "access_token": "YOUR_LINKEDIN_ACCESS_TOKEN",
    "user_id": "YOUR_LINKEDIN_USER_ID"
  }
}
```

### 3. Test Your Setup

#### Quick Test Commands
```bash
# Test Twitter only
python twitter_api_integration.py

# Test LinkedIn only
python linkedin_api_integration.py

# Test all platforms
python social_media_integrations.py

# Run web interface
python enhanced_web_interface.py
```

## Expected Results

### Successful Twitter Setup
```
🐦 Testing Twitter/X API v2 Integration
==================================================
🔗 Testing API Connection...
✅ Twitter API v2 connection successful
👤 User: @yourusername (Your Name)
📊 Followers: 1,234
📈 Following: 567
🐦 Tweets: 890
```

### Successful LinkedIn Setup
```
💼 Testing LinkedIn API v2 Integration
==================================================
🔗 Testing API Connection...
✅ LinkedIn API v2 connection successful
👤 User: John Doe (ID: abc123)
📝 Testing Content Posting...
✅ LinkedIn post published successfully!
📄 Post ID: urn:li:activity:123456789
```

## Common Issues & Quick Fixes

### Twitter 403 Error
- **Cause**: App permissions not set to "Read and Write"
- **Fix**: Update app permissions in Twitter Developer Portal

### Twitter 401 Error
- **Cause**: Invalid or expired tokens
- **Fix**: Regenerate all tokens in Twitter Developer Portal

### LinkedIn "Credentials not configured"
- **Cause**: Missing LinkedIn section in credentials.json
- **Fix**: Add LinkedIn credentials as shown above

### LinkedIn 403 Error
- **Cause**: App not verified or missing permissions
- **Fix**: Complete app verification process

## File Structure Check

Ensure you have these files:
```
📁 Your Project Directory
├── 📄 credentials.json (your actual credentials)
├── 📄 credentials_template.json (template)
├── 📄 twitter_api_integration.py
├── 📄 linkedin_api_integration.py
├── 📄 social_media_integrations.py
├── 📄 enhanced_web_interface.py
├── 📄 TWITTER_API_V2_SETUP.md
├── 📄 LINKEDIN_API_SETUP.md
└── 📄 QUICK_SETUP_GUIDE.md
```

## Security Notes

⚠️ **Important Security Practices**:
1. Never commit `credentials.json` to version control
2. Add `credentials.json` to your `.gitignore` file
3. Use environment variables in production
4. Regularly rotate your access tokens

## Next Steps After Setup

1. **Test Individual Platforms**
   ```bash
   python twitter_api_integration.py
   python linkedin_api_integration.py
   ```

2. **Test Combined Integration**
   ```bash
   python social_media_integrations.py
   ```

3. **Launch Web Interface**
   ```bash
   python enhanced_web_interface.py
   ```

4. **Start Automating**
   - Add content to your calendar
   - Schedule posts
   - Monitor analytics

## Support Resources

- **Twitter**: [https://developer.twitter.com/](https://developer.twitter.com/)
- **LinkedIn**: [https://www.linkedin.com/developers/](https://www.linkedin.com/developers/)
- **Detailed Guides**: 
  - `TWITTER_API_V2_SETUP.md`
  - `LINKEDIN_API_SETUP.md`

## Quick Diagnostic

Run this to check your current setup:
```bash
python test_twitter_setup.py
```

This will tell you exactly what's missing or incorrect in your configuration.

---

**Need Help?** If you're still having issues after following this guide, check the detailed setup guides or run the diagnostic tools for specific error messages. 