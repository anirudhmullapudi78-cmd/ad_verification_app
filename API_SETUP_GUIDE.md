# API Setup Guide for Enhanced Verification

## Overview

The app now supports external APIs to provide **more accurate and reliable** verification data. These APIs can significantly improve the accuracy of:

- Domain age and registration information
- Security and reputation scores
- Malware/phishing detection
- Fraud risk assessment

## Available APIs

### 1. Sonar API (AI-Powered Analysis) ⭐ RECOMMENDED
**Purpose:** AI-powered content analysis using Claude Sonnet (or other models) for intelligent ad verification

**Provider:** Sonar API (via OpenRouter endpoint)

**Pricing:**
- Pay-per-use based on model selected
- Claude 3.5 Sonnet: ~$0.003 per 1K tokens (very affordable)
- Free models also available

**Setup:**
1. Get your Sonar API key
2. Set environment variable: `SONAR_API_KEY=your_key_here`
   - Or use: `$env:SONAR_API_KEY="your_key"` in PowerShell
   - Or set permanently: `[System.Environment]::SetEnvironmentVariable("SONAR_API_KEY", "your_key", "User")`

**Benefits:**
- AI-powered ad detection and classification
- Intelligent reliability assessment
- Red flag detection
- Publisher information extraction
- Natural language understanding
- Works with multiple AI models (Claude, GPT, etc.)

**Model Used:** `anthropic/claude-3.5-sonnet` (can be changed in `api_integrations.py`)

**Status:** ✅ Already configured with your API key!

---

### 2. WHOIS API (Recommended)
**Purpose:** Get accurate domain registration information, age, and registrar details

**Provider:** WHOIS XML API (https://www.whoisxmlapi.com/)

**Pricing:** 
- Free tier: 500 queries/month
- Paid: Starting at $10/month for 5,000 queries

**Setup:**
1. Sign up at https://www.whoisxmlapi.com/
2. Get your API key from the dashboard
3. Set environment variable: `WHOIS_API_KEY=your_key_here`

**Benefits:**
- Accurate domain age (instead of estimates)
- Registrar information
- Registration and expiration dates

---

### 2. VirusTotal API (Recommended)
**Purpose:** Check domain reputation and security threats

**Provider:** VirusTotal (https://www.virustotal.com/)

**Pricing:**
- Free tier: 4 requests/minute, 500 requests/day
- Paid: Starting at $15/month for higher limits

**Setup:**
1. Sign up at https://www.virustotal.com/
2. Get your API key from your account settings
3. Set environment variable: `VIRUSTOTAL_API_KEY=your_key_here`

**Benefits:**
- Real-time threat detection
- Reputation scores from multiple security vendors
- Malware and phishing detection

---

### 3. Google Safe Browsing API (Recommended)
**Purpose:** Check URLs against Google's malware and phishing database

**Provider:** Google Cloud Platform

**Pricing:**
- Free tier: 10,000 requests/day
- Paid: $0.50 per 1,000 requests after free tier

**Setup:**
1. Go to https://console.cloud.google.com/
2. Create a project and enable "Safe Browsing API"
3. Create credentials (API key)
4. Set environment variable: `SAFEBROWSING_API_KEY=your_key_here`

**Benefits:**
- Google's comprehensive threat database
- Real-time phishing and malware detection
- Free tier is generous

---

### 4. IPQualityScore API (Optional)
**Purpose:** Advanced fraud detection and URL reputation

**Provider:** IPQualityScore (https://www.ipqualityscore.com/)

**Pricing:**
- Free tier: 5,000 requests/month
- Paid: Starting at $20/month for 25,000 requests

**Setup:**
1. Sign up at https://www.ipqualityscore.com/
2. Get your API key from the dashboard
3. Set environment variable: `IPQUALITYSCORE_API_KEY=your_key_here`

**Benefits:**
- Advanced fraud scoring
- Domain reputation metrics
- Phishing and malware detection

---

## Setup Instructions

### Option 1: Environment Variables (Recommended)

Create a `.env` file in your project root (or set system environment variables):

```env
SONAR_API_KEY=your_sonar_key_here
WHOIS_API_KEY=your_whois_api_key_here
VIRUSTOTAL_API_KEY=your_virustotal_key_here
SAFEBROWSING_API_KEY=your_google_key_here
IPQUALITYSCORE_API_KEY=your_ipqs_key_here
```

**For Windows (PowerShell):**
```powershell
$env:SONAR_API_KEY="your_key_here"
$env:WHOIS_API_KEY="your_key_here"
$env:VIRUSTOTAL_API_KEY="your_key_here"
$env:SAFEBROWSING_API_KEY="your_key_here"
```

**For Windows (Command Prompt):**
```cmd
set WHOIS_API_KEY=your_key_here
set VIRUSTOTAL_API_KEY=your_key_here
set SAFEBROWSING_API_KEY=your_key_here
```

### Option 2: Modify api_integrations.py

You can directly edit `api_integrations.py` and set the API keys in the `API_CONFIG` dictionary (not recommended for production).

### Option 3: Create config.py (Alternative)

Create a `config.py` file:

```python
API_KEYS = {
    'whois_api_key': 'your_key_here',
    'virustotal_api_key': 'your_key_here',
    'safebrowsing_api_key': 'your_key_here',
    'ipqualityscore_api_key': 'your_key_here'
}
```

Then modify `api_integrations.py` to import from `config.py`.

## Testing API Setup

After setting up your API keys, test them:

```python
# Test script
from api_integrations import get_enhanced_domain_info
import os

# Set your keys
os.environ['WHOIS_API_KEY'] = 'your_key'
os.environ['VIRUSTOTAL_API_KEY'] = 'your_key'

# Test
result = get_enhanced_domain_info('example.com', 'https://example.com')
print(result)
```

## Recommended Setup (Minimum)

For best results with minimal cost:

1. **Sonar API** (Pay-per-use, ~$0.003 per analysis) - AI-powered intelligent analysis ⭐ ✅ CONFIGURED
2. **Google Safe Browsing API** (FREE) - Essential for security
3. **VirusTotal API** (FREE tier) - Good reputation checking
4. **WHOIS API** (FREE tier) - Accurate domain age

**Cost:** ~$0.003 per verification (very affordable) + FREE security checks

## How It Works

- **Without APIs:** The app uses heuristics and pattern matching (less accurate)
- **With APIs:** The app uses real data from security services and domain registries (much more accurate)

The app will automatically:
- Use API data when available
- Fall back to heuristics if APIs are not configured
- Show which APIs were used in the verification report

## Cost Considerations

**Free Setup (Recommended):**
- Google Safe Browsing: FREE (10K requests/day)
- VirusTotal: FREE (500 requests/day)
- WHOIS XML API: FREE (500 requests/month)

**Total Cost: $0/month** for moderate usage

**Paid Setup (High Volume):**
- All APIs with higher limits: ~$50-100/month
- Suitable for commercial/production use

## Security Note

**Never commit API keys to version control!**

- Use environment variables
- Add `.env` to `.gitignore`
- Don't share your API keys

## Troubleshooting

**APIs not working?**
1. Check API keys are set correctly
2. Verify API keys are valid (test in browser/Postman)
3. Check API rate limits haven't been exceeded
4. Check internet connection
5. Look at app console for error messages

**API errors?**
- The app will gracefully fall back to heuristics
- Check the API provider's status page
- Verify your API key permissions

## Next Steps

1. Choose which APIs you want to use
2. Sign up and get API keys
3. Set environment variables
4. Restart the app
5. Test with a URL to see API data in the verification report

The app will automatically use the APIs when available and show the results in the "API Verification Data" section!

