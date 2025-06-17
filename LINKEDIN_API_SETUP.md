# LinkedIn API v2 Setup Guide

## Overview
This guide will help you set up LinkedIn API v2 access for your social media automation system. Based on your LinkedIn developer apps, this guide will walk you through the complete setup process.

## Prerequisites
- A LinkedIn account
- A LinkedIn Developer account
- Your LinkedIn app (ID: 223819743) from the developer portal

## Step 1: Access Your LinkedIn Developer Portal

1. **Visit Your LinkedIn Developer Portal**
   - Go to [https://www.linkedin.com/developers/apps/223819743/products](https://www.linkedin.com/developers/apps/223819743/products)
   - Sign in with your LinkedIn account

2. **App Verification Status**
   - Check your app verification status at: [https://www.linkedin.com/developers/apps/verification/2c6443fc-5082-4fca-bc87-faed10d40403](https://www.linkedin.com/developers/apps/verification/2c6443fc-5082-4fca-bc87-faed10d40403)
   - Ensure your app is properly verified for production use

## Step 2: Configure Your LinkedIn App

1. **App Settings**
   - In your developer portal, go to "App Settings"
   - Configure the following settings:

2. **OAuth 2.0 Settings**
   - **Authorized redirect URLs**: Add your callback URLs
   - **Authorized JavaScript origins**: Add your domain
   - **Application permissions**: Request necessary scopes

3. **Required Permissions**
   - `r_liteprofile` - Read basic profile information
   - `w_member_social` - Post content to LinkedIn
   - `r_organization_social` - Read organization posts (if posting as company)
   - `w_organization_social` - Post as organization (if needed)

## Step 3: Generate Access Tokens

1. **Get Client ID and Secret**
   - In your app dashboard, copy your "Client ID" and "Client Secret"
   - These are your app's credentials

2. **Generate Access Token**
   - Use the OAuth 2.0 flow to get user access tokens
   - Or use the LinkedIn OAuth playground for testing

3. **Get User ID**
   - Use the `/v2/me` endpoint to get your LinkedIn user ID
   - This is required for posting content

## Step 4: OAuth 2.0 Authorization Flow

### Option 1: Manual Token Generation (for testing)

1. **Visit LinkedIn OAuth Playground**
   - Go to [https://www.linkedin.com/developers/tools/oauth/playground](https://www.linkedin.com/developers/tools/oauth/playground)

2. **Configure OAuth Settings**
   - Enter your Client ID and Client Secret
   - Set redirect URI to: `https://www.linkedin.com/developers/tools/oauth/playground`
   - Select required scopes: `r_liteprofile w_member_social`

3. **Generate Token**
   - Click "Request Token"
   - Authorize your app
   - Copy the generated access token

### Option 2: Programmatic Token Generation

```python
import requests

def get_linkedin_token(client_id, client_secret, redirect_uri, auth_code):
    """Exchange authorization code for access token"""
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(token_url, data=data)
    return response.json()
```

## Step 5: Configure Your Credentials

1. **Update credentials.json**
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

2. **Get Your User ID**
   ```bash
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
        "https://api.linkedin.com/v2/me"
   ```

## Step 6: Test Your Setup

1. **Run the LinkedIn API Test**
   ```bash
   python linkedin_api_integration.py
   ```

2. **Expected Output**
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

## Common Issues and Solutions

### 403 Forbidden Error
**Cause**: Insufficient permissions or app not verified
**Solutions**:
1. Ensure your app has the required permissions
2. Check that your app is verified for production use
3. Verify your access token has the correct scopes
4. Make sure you're using the correct user ID

### 401 Unauthorized Error
**Cause**: Invalid or expired access token
**Solutions**:
1. Regenerate your access token
2. Check that your client ID and secret are correct
3. Verify the token hasn't expired

### 400 Bad Request Error
**Cause**: Invalid request format or missing parameters
**Solutions**:
1. Check your post data structure
2. Verify all required fields are present
3. Ensure your user ID is correct

## API v2 Endpoints Used

### Core Endpoints
- `GET /v2/me` - Get current user profile
- `POST /v2/ugcPosts` - Create a new post
- `GET /v2/networkSizes/{personId}` - Get network information
- `GET /v2/socialMetrics/{postId}` - Get post analytics

### Post Types Supported
- **Text Posts**: Simple text content
- **Article Posts**: Posts with media/links
- **Company Posts**: Posts on behalf of organizations

## Rate Limits

### LinkedIn API Limits
- **Posts**: 25 per day (free tier)
- **Profile reads**: 100 per day
- **Network reads**: 100 per day

### Paid Tier Limits
- Higher limits available with LinkedIn Marketing Solutions
- Check [LinkedIn API Pricing](https://business.linkedin.com/marketing-solutions/success/linkedin-ads-api) for details

## Security Best Practices

1. **Secure Token Storage**
   - Never commit access tokens to version control
   - Use environment variables in production
   - Implement token refresh mechanisms

2. **App Permissions**
   - Request only necessary permissions
   - Regularly review app permissions
   - Use least privilege principle

3. **Error Handling**
   - Implement proper error handling for API calls
   - Log errors for debugging
   - Handle rate limiting gracefully

## Environment Variables (Alternative)

Instead of using `credentials.json`, you can set environment variables:

```bash
export LINKEDIN_CLIENT_ID="your_client_id"
export LINKEDIN_CLIENT_SECRET="your_client_secret"
export LINKEDIN_ACCESS_TOKEN="your_access_token"
export LINKEDIN_USER_ID="your_user_id"
```

## Testing Your Integration

1. **Test Connection**
   ```python
   from linkedin_api_integration import LinkedInAPIv2
   
   linkedin = LinkedInAPIv2()
   result = linkedin.test_connection()
   print(result)
   ```

2. **Test Posting**
   ```python
   result = linkedin.post_content("Hello from my automation system!")
   print(result)
   ```

3. **Test Profile Retrieval**
   ```python
   profile = linkedin.get_profile()
   print(profile)
   ```

## Next Steps

Once your LinkedIn API v2 integration is working:

1. **Test with the web interface**
   ```bash
   python enhanced_web_interface.py
   ```

2. **Set up automated posting schedules**
3. **Monitor post performance**
4. **Integrate with other platforms**

## Support Resources

- [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
- [LinkedIn API v2 Documentation](https://docs.microsoft.com/en-us/linkedin/shared/api-guide/concepts/versioning)
- [LinkedIn Marketing API](https://docs.microsoft.com/en-us/linkedin/marketing/)
- [LinkedIn Developer Community](https://www.linkedin.com/help/linkedin/answer/a522)

## Troubleshooting Checklist

- [ ] App is verified for production use
- [ ] All required permissions are granted
- [ ] Access token is valid and not expired
- [ ] User ID is correctly configured
- [ ] Post data structure is correct
- [ ] Rate limits not exceeded
- [ ] Network connectivity working

## App Verification Process

If your app needs verification:

1. **Complete App Information**
   - Fill out all required app details
   - Provide clear use case description
   - Add privacy policy and terms of service

2. **Submit for Review**
   - Go to the verification page
   - Submit your app for review
   - Wait for LinkedIn's response

3. **Address Feedback**
   - Respond to any questions from LinkedIn
   - Make requested changes
   - Resubmit if needed

For additional support, visit the [LinkedIn Developer Support](https://www.linkedin.com/help/linkedin/answer/a522) page. 