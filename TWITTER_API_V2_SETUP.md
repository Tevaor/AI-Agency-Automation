# Twitter/X API v2 Setup Guide

## Overview
This guide will help you set up Twitter API v2 access for your social media automation system. The Twitter API v2 is the latest version and provides enhanced features for posting tweets, retrieving analytics, and managing your account.

## Prerequisites
- A Twitter/X account
- A Twitter Developer account (free)
- Basic understanding of API authentication

## Step 1: Create a Twitter Developer Account

1. **Visit the Twitter Developer Portal**
   - Go to [https://developer.twitter.com/](https://developer.twitter.com/)
   - Sign in with your Twitter account

2. **Apply for Developer Access**
   - Click "Apply for a developer account"
   - Fill out the application form
   - Explain your use case (e.g., "Social media automation for business")
   - Wait for approval (usually 24-48 hours)

## Step 2: Create a Twitter App

1. **Create a New App**
   - In the developer portal, click "Create App"
   - Give your app a name (e.g., "My Social Media Automation")
   - Add a description

2. **Configure App Settings**
   - Go to "App Settings" → "User authentication settings"
   - Enable "OAuth 1.0a"
   - Set App permissions to "Read and Write"
   - Add callback URLs if needed
   - Save changes

## Step 3: Generate API Keys and Tokens

1. **Get API Keys**
   - Go to "Keys and tokens" tab
   - Copy your "API Key" and "API Key Secret"

2. **Generate Access Tokens**
   - Scroll down to "Authentication Tokens"
   - Click "Generate" for "Access Token and Secret"
   - Copy both the "Access Token" and "Access Token Secret"

3. **Get Bearer Token**
   - In the same section, copy your "Bearer Token"

## Step 4: Configure Your Credentials

1. **Copy the Template**
   ```bash
   cp credentials_template.json credentials.json
   ```

2. **Fill in Your Twitter Credentials**
   ```json
   {
     "twitter": {
       "api_key": "YOUR_ACTUAL_API_KEY",
       "api_secret": "YOUR_ACTUAL_API_SECRET", 
       "access_token": "YOUR_ACTUAL_ACCESS_TOKEN",
       "access_token_secret": "YOUR_ACTUAL_ACCESS_TOKEN_SECRET",
       "bearer_token": "YOUR_ACTUAL_BEARER_TOKEN"
     }
   }
   ```

## Step 5: Test Your Setup

1. **Run the Twitter API Test**
   ```bash
   python twitter_api_integration.py
   ```

2. **Expected Output**
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

## Common Issues and Solutions

### 403 Forbidden Error
**Cause**: Insufficient permissions or incorrect authentication
**Solutions**:
1. Ensure your app has "Read and Write" permissions
2. Verify all API keys and tokens are correct
3. Check that your developer account is approved
4. Make sure you're using the correct Bearer Token

### 401 Unauthorized Error
**Cause**: Invalid or expired tokens
**Solutions**:
1. Regenerate your access tokens
2. Check that your Bearer Token is current
3. Verify API key and secret are correct

### Rate Limiting (429 Error)
**Cause**: Exceeding API rate limits
**Solutions**:
1. Implement delays between requests
2. Check your current rate limit status
3. Consider upgrading to a paid plan for higher limits

## API v2 Endpoints Used

### Core Endpoints
- `GET /2/users/me` - Get current user info
- `POST /2/tweets` - Create a new tweet
- `GET /2/users/{id}/tweets` - Get user's tweets
- `GET /2/tweets/{id}` - Get specific tweet
- `GET /2/tweets/search/recent` - Search recent tweets

### Media Upload
- `POST /1.1/media/upload.json` - Upload media files

## Rate Limits

### Free Tier Limits
- **Tweets**: 300 per 15-minute window
- **User lookup**: 300 per 15-minute window
- **Tweet lookup**: 300 per 15-minute window
- **Search**: 180 per 15-minute window

### Paid Tier Limits
- Higher limits available with paid plans
- Check [Twitter API Pricing](https://developer.twitter.com/en/pricing) for details

## Security Best Practices

1. **Never commit credentials to version control**
   - Add `credentials.json` to your `.gitignore`
   - Use environment variables in production

2. **Rotate tokens regularly**
   - Regenerate access tokens periodically
   - Monitor for suspicious activity

3. **Use least privilege principle**
   - Only request necessary permissions
   - Review app permissions regularly

## Environment Variables (Alternative)

Instead of using `credentials.json`, you can set environment variables:

```bash
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
export TWITTER_BEARER_TOKEN="your_bearer_token"
```

## Testing Your Integration

1. **Test Connection**
   ```python
   from twitter_api_integration import TwitterAPIv2
   
   twitter = TwitterAPIv2()
   result = twitter.test_connection()
   print(result)
   ```

2. **Test Posting**
   ```python
   result = twitter.post_tweet("Hello from my automation system!")
   print(result)
   ```

3. **Test Analytics**
   ```python
   analytics = twitter.get_account_analytics()
   print(analytics)
   ```

## Next Steps

Once your Twitter API v2 integration is working:

1. **Test with the web interface**
   ```bash
   python enhanced_web_interface.py
   ```

2. **Set up other platforms** (LinkedIn, Facebook)
3. **Configure automated posting schedules**
4. **Monitor analytics and engagement**

## Support Resources

- [Twitter API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [API Reference](https://developer.twitter.com/en/docs/api-reference-index)
- [Rate Limiting Guide](https://developer.twitter.com/en/docs/twitter-api/rate-limits)
- [Error Codes](https://developer.twitter.com/en/docs/twitter-api/error-codes)

## Troubleshooting Checklist

- [ ] Developer account approved
- [ ] App created with correct permissions
- [ ] All API keys and tokens generated
- [ ] Credentials file properly configured
- [ ] App has "Read and Write" permissions
- [ ] Bearer Token is current
- [ ] No typos in credentials
- [ ] Rate limits not exceeded
- [ ] Network connectivity working

If you're still having issues after checking all items, please refer to the [Twitter Developer Forum](https://twittercommunity.com/) for additional support. 