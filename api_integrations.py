"""
API Integrations for Enhanced Verification Accuracy
Supports multiple APIs for domain verification, fact-checking, and reputation checking
"""
import requests
import os
from datetime import datetime
import tldextract

# API Configuration - Set these as environment variables or in a config file
API_CONFIG = {
    # WHOIS API - for domain information
    'whois_api_key': os.getenv('WHOIS_API_KEY', ''),
    'whois_api_url': 'https://www.whoisxmlapi.com/whoisserver/WhoisService',
    
    # VirusTotal API - for domain reputation
    'virustotal_api_key': os.getenv('VIRUSTOTAL_API_KEY', ''),
    'virustotal_api_url': 'https://www.virustotal.com/vtapi/v2/domain/report',
    
    # Google Safe Browsing API - for malware/phishing detection
    'safebrowsing_api_key': os.getenv('SAFEBROWSING_API_KEY', ''),
    'safebrowsing_api_url': 'https://safebrowsing.googleapis.com/v4/threatMatches:find',
    
    # IPQualityScore API - for domain reputation and fraud detection
    'ipqualityscore_api_key': os.getenv('IPQUALITYSCORE_API_KEY', ''),
    'ipqualityscore_api_url': 'https://www.ipqualityscore.com/api/json/url',
    
    # AbuseIPDB API - for IP reputation
    'abuseipdb_api_key': os.getenv('ABUSEIPDB_API_KEY', ''),
    'abuseipdb_api_url': 'https://api.abuseipdb.com/api/v2/check',
    
    # Sonar API - for AI-powered content analysis (via OpenRouter endpoint)
    'sonar_api_key': os.getenv('SONAR_API_KEY', ''),
    'sonar_api_url': 'https://openrouter.ai/api/v1/chat/completions',
    'sonar_model': 'anthropic/claude-3.5-sonnet',  # Can be changed to other models
}

def get_domain_whois(domain, api_key=None):
    """
    Get WHOIS information for a domain using WHOIS XML API
    
    Returns:
        dict with domain registration info, age, registrar, etc.
    """
    if not api_key:
        api_key = API_CONFIG.get('whois_api_key')
    
    if not api_key:
        return {
            'available': False,
            'error': 'WHOIS API key not configured'
        }
    
    try:
        url = API_CONFIG['whois_api_url']
        params = {
            'apiKey': api_key,
            'domainName': domain,
            'outputFormat': 'JSON'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant information
        whois_info = {
            'available': True,
            'domain': domain,
            'registered': data.get('WhoisRecord', {}).get('createdDate'),
            'registrar': data.get('WhoisRecord', {}).get('registrarName'),
            'expires': data.get('WhoisRecord', {}).get('expiresDate'),
            'name_servers': data.get('WhoisRecord', {}).get('nameServers', {}).get('hostNames', []),
            'contact_email': data.get('WhoisRecord', {}).get('contactEmail'),
            'domain_age_days': None
        }
        
        # Calculate domain age
        if whois_info['registered']:
            try:
                reg_date = datetime.fromisoformat(whois_info['registered'].replace('Z', '+00:00'))
                age_days = (datetime.now(reg_date.tzinfo) - reg_date).days
                whois_info['domain_age_days'] = age_days
            except:
                pass
        
        return whois_info
        
    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }

def check_virustotal_reputation(domain, api_key=None):
    """
    Check domain reputation using VirusTotal API
    
    Returns:
        dict with reputation scores, detection count, etc.
    """
    if not api_key:
        api_key = API_CONFIG.get('virustotal_api_key')
    
    if not api_key:
        return {
            'available': False,
            'error': 'VirusTotal API key not configured'
        }
    
    try:
        url = API_CONFIG['virustotal_api_url']
        params = {
            'apikey': api_key,
            'domain': domain
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('response_code') == 1:
            detections = data.get('detected_urls', [])
            detection_count = len([d for d in detections if d.get('positives', 0) > 0])
            
            return {
                'available': True,
                'domain': domain,
                'detection_count': detection_count,
                'total_scans': len(detections),
                'reputation_score': max(0, 100 - (detection_count * 10)),  # Simple scoring
                'categories': data.get('categories', {}),
                'subdomains': data.get('subdomains', []),
                'is_suspicious': detection_count > 0
            }
        else:
            return {
                'available': False,
                'error': 'Domain not found in VirusTotal database'
            }
            
    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }

def check_safebrowsing(url, api_key=None):
    """
    Check URL against Google Safe Browsing API
    
    Returns:
        dict with threat information
    """
    if not api_key:
        api_key = API_CONFIG.get('safebrowsing_api_key')
    
    if not api_key:
        return {
            'available': False,
            'error': 'Safe Browsing API key not configured'
        }
    
    try:
        api_url = API_CONFIG['safebrowsing_api_url'] + f'?key={api_key}'
        
        payload = {
            'client': {
                'clientId': 'ad-verification-app',
                'clientVersion': '1.0'
            },
            'threatInfo': {
                'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
                'platformTypes': ['ANY_PLATFORM'],
                'threatEntryTypes': ['URL'],
                'threatEntries': [{'url': url}]
            }
        }
        
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'matches' in data and len(data['matches']) > 0:
            threats = [match.get('threatType') for match in data['matches']]
            return {
                'available': True,
                'is_safe': False,
                'threats': threats,
                'threat_count': len(threats)
            }
        else:
            return {
                'available': True,
                'is_safe': True,
                'threats': [],
                'threat_count': 0
            }
            
    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }

def check_ipqualityscore(url, api_key=None):
    """
    Check URL reputation using IPQualityScore API
    
    Returns:
        dict with fraud score, reputation, and safety indicators
    """
    if not api_key:
        api_key = API_CONFIG.get('ipqualityscore_api_key')
    
    if not api_key:
        return {
            'available': False,
            'error': 'IPQualityScore API key not configured'
        }
    
    try:
        api_url = API_CONFIG['ipqualityscore_api_url']
        params = {
            'key': api_key,
            'url': url,
            'strictness': 1
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success', False):
            return {
                'available': True,
                'fraud_score': data.get('fraud_score', 0),
                'is_safe': data.get('unsafe', False) == False,
                'suspicious': data.get('suspicious', False),
                'phishing': data.get('phishing', False),
                'malware': data.get('malware', False),
                'spam': data.get('spam', False),
                'reputation_score': data.get('reputation', 0),
                'domain_age_days': data.get('domain_age', {}).get('human', 'Unknown'),
                'domain_rank': data.get('domain_rank', 0)
            }
        else:
            return {
                'available': False,
                'error': data.get('message', 'API request failed')
            }
            
    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }

def analyze_with_sonar(content, analysis_type='ad_verification', api_key=None):
    """
    Use Sonar API (via OpenRouter endpoint) for AI-powered content analysis
    
    Args:
        content: Text content to analyze
        analysis_type: Type of analysis ('ad_verification', 'reliability', 'fact_check')
        api_key: Sonar API key
    
    Returns:
        dict with AI analysis results
    """
    if not api_key:
        api_key = API_CONFIG.get('sonar_api_key')
    
    if not api_key:
        return {
            'available': False,
            'error': 'Sonar API key not configured'
        }
    
    try:
        # Prepare analysis prompt based on type
        if analysis_type == 'ad_verification':
            system_prompt = """You are an expert advertisement verification analyst. Analyze the provided content and determine:
1. Is this an advertisement? (Yes/No with confidence 0-100%)
2. If yes, what type of advertisement? (product, service, real estate, job, education, healthcare, financial, event, food, travel, or general)
3. What are the key indicators that led to your conclusion?
4. Assess the reliability and credibility of this advertisement (High/Medium/Low/Very Low)
5. Identify any red flags or suspicious elements
6. Extract publisher/owner information if available

Respond in a structured JSON format."""
            
            user_prompt = f"""Analyze this content for advertisement verification:

{content[:4000]}

Provide a detailed analysis in JSON format with the following structure:
{{
    "is_advertisement": true/false,
    "confidence": 0-100,
    "ad_type": "type or null",
    "indicators": ["indicator1", "indicator2"],
    "reliability_level": "High/Medium/Low/Very Low",
    "reliability_score": 0-100,
    "red_flags": ["flag1", "flag2"],
    "publisher_info": {{"name": "...", "contact": "..."}},
    "analysis_summary": "brief summary"
}}"""
        
        elif analysis_type == 'reliability':
            system_prompt = """You are an expert in assessing the reliability and credibility of online content, especially advertisements."""
            user_prompt = f"""Assess the reliability and accuracy of this content:

{content[:4000]}

Provide a reliability assessment in JSON format."""
        
        else:  # fact_check
            system_prompt = """You are a fact-checking expert. Verify claims and assess accuracy."""
            user_prompt = f"""Fact-check this content:

{content[:4000]}

Provide fact-checking results in JSON format."""
        
        # Make API request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://ad-verification-app.local',  # Optional: for tracking
            'X-Title': 'Ad Verification App'  # Optional: for tracking
        }
        
        payload = {
            'model': API_CONFIG.get('sonar_model', 'anthropic/claude-3.5-sonnet'),
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': 0.3,  # Lower temperature for more consistent analysis
            'max_tokens': 2000
        }
        
        response = requests.post(
            API_CONFIG['sonar_api_url'],
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract response
        if 'choices' in data and len(data['choices']) > 0:
            content_response = data['choices'][0]['message']['content']
            
            # Try to parse JSON from response
            import json
            try:
                # Extract JSON from markdown code blocks if present
                if '```json' in content_response:
                    json_start = content_response.find('```json') + 7
                    json_end = content_response.find('```', json_start)
                    content_response = content_response[json_start:json_end].strip()
                elif '```' in content_response:
                    json_start = content_response.find('```') + 3
                    json_end = content_response.find('```', json_start)
                    content_response = content_response[json_start:json_end].strip()
                
                parsed_response = json.loads(content_response)
                
                return {
                    'available': True,
                    'analysis_type': analysis_type,
                    'raw_response': content_response,
                    'parsed_analysis': parsed_response,
                    'model_used': data.get('model', API_CONFIG.get('sonar_model'))
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw response
                return {
                    'available': True,
                    'analysis_type': analysis_type,
                    'raw_response': content_response,
                    'parsed_analysis': None,
                    'model_used': data.get('model', API_CONFIG.get('sonar_model')),
                    'note': 'Response could not be parsed as JSON, returning raw text'
                }
        else:
            return {
                'available': False,
                'error': 'Unexpected API response format'
            }
            
    except requests.RequestException as e:
        return {
            'available': False,
            'error': f'API request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }

def get_enhanced_domain_info(domain, url):
    """
    Get comprehensive domain information using available APIs
    
    Returns:
        dict with all available domain information
    """
    enhanced_info = {
        'whois': None,
        'virustotal': None,
        'safebrowsing': None,
        'ipqualityscore': None,
        'openrouter': None,
        'apis_used': [],
        'apis_available': []
    }
    
    # Try WHOIS
    whois_result = get_domain_whois(domain)
    if whois_result.get('available'):
        enhanced_info['whois'] = whois_result
        enhanced_info['apis_used'].append('whois')
    elif 'error' in whois_result and 'not configured' not in whois_result['error']:
        enhanced_info['apis_available'].append('whois')
    
    # Try VirusTotal
    vt_result = check_virustotal_reputation(domain)
    if vt_result.get('available'):
        enhanced_info['virustotal'] = vt_result
        enhanced_info['apis_used'].append('virustotal')
    elif 'error' in vt_result and 'not configured' not in vt_result['error']:
        enhanced_info['apis_available'].append('virustotal')
    
    # Try Safe Browsing
    sb_result = check_safebrowsing(url)
    if sb_result.get('available'):
        enhanced_info['safebrowsing'] = sb_result
        enhanced_info['apis_used'].append('safebrowsing')
    elif 'error' in sb_result and 'not configured' not in sb_result['error']:
        enhanced_info['apis_available'].append('safebrowsing')
    
    # Try IPQualityScore
    iqs_result = check_ipqualityscore(url)
    if iqs_result.get('available'):
        enhanced_info['ipqualityscore'] = iqs_result
        enhanced_info['apis_used'].append('ipqualityscore')
    elif 'error' in iqs_result and 'not configured' not in iqs_result['error']:
        enhanced_info['apis_available'].append('ipqualityscore')
    
    # Note: OpenRouter analysis is called separately with content, not here
    
    return enhanced_info

