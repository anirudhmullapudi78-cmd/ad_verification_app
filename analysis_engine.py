"""
Enhanced Analysis Engine for Ad Verification
Provides detailed analysis including ad detection, classification, publisher info, and reliability scoring
"""
import re
from bs4 import BeautifulSoup
import tldextract

# Advertisement detection keywords and patterns
AD_KEYWORDS = [
    'buy now', 'shop now', 'limited time', 'special offer', 'discount', 'sale',
    'advertisement', 'ad', 'sponsored', 'promotion', 'deal', 'offer', 'save',
    'click here', 'learn more', 'sign up', 'subscribe', 'free trial', 'order now',
    'call now', 'visit us', 'act now', 'hurry', 'today only', 'while supplies last'
]

AD_TYPE_PATTERNS = {
    'product': ['product', 'buy', 'shop', 'purchase', 'order', 'price', 'cost', 'shipping'],
    'service': ['service', 'hire', 'book', 'appointment', 'consultation', 'call'],
    'real_estate': ['property', 'house', 'apartment', 'rent', 'lease', 'real estate', 'home'],
    'job': ['job', 'career', 'hiring', 'position', 'apply', 'employment', 'opportunity'],
    'education': ['course', 'learn', 'education', 'training', 'degree', 'certificate', 'class'],
    'healthcare': ['doctor', 'medical', 'health', 'treatment', 'clinic', 'hospital', 'therapy'],
    'financial': ['loan', 'credit', 'investment', 'insurance', 'mortgage', 'bank', 'finance'],
    'event': ['event', 'ticket', 'concert', 'show', 'festival', 'conference', 'meeting'],
    'food': ['restaurant', 'food', 'menu', 'dining', 'cafe', 'delivery', 'order food'],
    'travel': ['travel', 'hotel', 'flight', 'vacation', 'trip', 'booking', 'resort']
}

RELIABILITY_FACTORS = {
    'domain_age': 0.15,  # Older domains are more reliable
    'ssl_certificate': 0.10,  # HTTPS is more reliable
    'contact_info': 0.15,  # Having contact info increases reliability
    'social_media': 0.10,  # Social media presence
    'reviews_ratings': 0.10,  # Reviews and ratings
    'professional_design': 0.10,  # Professional appearance
    'clear_policies': 0.10,  # Privacy policy, terms of service
    'content_quality': 0.20  # Quality and accuracy of content
}

def detect_advertisement(text_content, html_content=None):
    """
    Detect if content is an advertisement
    
    Returns:
        dict with 'is_advertisement' (bool), 'confidence' (float), 'indicators' (list)
    """
    if not text_content:
        return {
            'is_advertisement': False,
            'confidence': 0.0,
            'indicators': []
        }
    
    text_lower = text_content.lower()
    indicators = []
    ad_score = 0
    
    # Check for ad keywords
    keyword_matches = [kw for kw in AD_KEYWORDS if kw in text_lower]
    if keyword_matches:
        indicators.append(f"Contains ad keywords: {', '.join(keyword_matches[:5])}")
        ad_score += len(keyword_matches) * 0.1
    
    # Check for promotional language patterns
    promotional_patterns = [
        r'\$\d+',  # Prices
        r'\d+% off',  # Discounts
        r'limited time',
        r'act now',
        r'call \d{3}',
        r'click here',
        r'buy now'
    ]
    
    pattern_matches = sum(1 for pattern in promotional_patterns if re.search(pattern, text_lower))
    if pattern_matches > 0:
        indicators.append(f"Contains {pattern_matches} promotional patterns")
        ad_score += pattern_matches * 0.15
    
    # Check HTML for ad-related meta tags or classes
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for sponsored/ad meta tags
        meta_tags = soup.find_all('meta', {'property': re.compile(r'og:|article:')})
        for meta in meta_tags:
            content = meta.get('content', '').lower()
            if any(kw in content for kw in ['sponsored', 'ad', 'promotion']):
                indicators.append("Contains ad-related meta tags")
                ad_score += 0.2
        
        # Check for common ad container classes
        ad_classes = soup.find_all(class_=re.compile(r'ad|advertisement|sponsored|promo', re.I))
        if ad_classes:
            indicators.append("Contains ad container elements")
            ad_score += 0.15
    
    # Normalize score to 0-1
    confidence = min(ad_score, 1.0)
    is_ad = confidence > 0.3
    
    return {
        'is_advertisement': is_ad,
        'confidence': round(confidence, 2),
        'indicators': indicators[:5]  # Limit to 5 indicators
    }

def classify_ad_type(text_content):
    """
    Classify the type of advertisement
    
    Returns:
        dict with 'ad_type' (str), 'confidence' (float), 'subcategories' (list)
    """
    if not text_content:
        return {
            'ad_type': 'unknown',
            'confidence': 0.0,
            'subcategories': []
        }
    
    text_lower = text_content.lower()
    type_scores = {}
    
    for ad_type, keywords in AD_TYPE_PATTERNS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches > 0:
            type_scores[ad_type] = matches / len(keywords)
    
    if not type_scores:
        return {
            'ad_type': 'general',
            'confidence': 0.3,
            'subcategories': []
        }
    
    # Get the type with highest score
    best_type = max(type_scores.items(), key=lambda x: x[1])
    
    return {
        'ad_type': best_type[0],
        'confidence': round(best_type[1], 2),
        'subcategories': [k for k, v in type_scores.items() if v > 0.2 and k != best_type[0]][:3]
    }

def extract_publisher_info(soup, url):
    """
    Extract publisher/owner information from webpage
    
    Returns:
        dict with publisher information
    """
    publisher_info = {
        'name': None,
        'domain': None,
        'email': None,
        'phone': None,
        'address': None,
        'social_media': {},
        'meta_info': {}
    }
    
    # Extract domain
    extracted = tldextract.extract(url)
    publisher_info['domain'] = f"{extracted.domain}.{extracted.suffix}"
    
    # Extract from meta tags
    # Open Graph tags
    og_site_name = soup.find('meta', {'property': 'og:site_name'})
    if og_site_name:
        publisher_info['name'] = og_site_name.get('content')
        publisher_info['meta_info']['og_site_name'] = og_site_name.get('content')
    
    # Twitter card
    twitter_site = soup.find('meta', {'name': 'twitter:site'})
    if twitter_site:
        publisher_info['social_media']['twitter'] = twitter_site.get('content')
    
    # Author
    author = soup.find('meta', {'name': 'author'})
    if author:
        publisher_info['meta_info']['author'] = author.get('content')
    
    # Publisher
    publisher = soup.find('meta', {'property': 'article:publisher'})
    if publisher:
        publisher_info['meta_info']['publisher'] = publisher.get('content')
    
    # Try to find organization name in structured data (JSON-LD)
    json_ld = soup.find_all('script', {'type': 'application/ld+json'})
    for script in json_ld:
        try:
            import json
            data = json.loads(script.string)
            if isinstance(data, dict):
                if 'publisher' in data:
                    pub = data['publisher']
                    if isinstance(pub, dict) and 'name' in pub:
                        publisher_info['name'] = pub['name']
                if 'author' in data and not publisher_info['name']:
                    auth = data['author']
                    if isinstance(auth, dict) and 'name' in auth:
                        publisher_info['name'] = auth['name']
        except:
            pass
    
    # Extract contact information from text
    text_content = soup.get_text()
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text_content)
    if emails:
        publisher_info['email'] = emails[0]  # Take first email
    
    # Phone pattern (US format)
    phone_pattern = r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text_content)
    if phones:
        publisher_info['phone'] = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
    
    # If no name found, use domain as fallback
    if not publisher_info['name']:
        publisher_info['name'] = extracted.domain.title()
    
    return publisher_info

def assess_reliability(url, soup, text_content, publisher_info, api_data=None):
    """
    Assess the reliability and accuracy of the advertisement
    Uses API data when available for more accurate assessment
    
    Args:
        url: The URL being verified
        soup: BeautifulSoup object of the webpage
        text_content: Extracted text content
        publisher_info: Publisher information dict
        api_data: Optional dict with API verification results
    
    Returns:
        dict with reliability score and factors
    """
    reliability_score = 0.0
    factors = {}
    warnings = []
    positive_indicators = []
    
    # Factor 1: Domain and SSL (0.15)
    extracted = tldextract.extract(url)
    domain_score = 0.0
    
    # Check if HTTPS
    if url.startswith('https://'):
        domain_score += 0.5
        positive_indicators.append("Uses HTTPS (secure connection)")
    else:
        warnings.append("Not using HTTPS - security concern")
    
    # Check domain extension (trusted TLDs)
    trusted_tlds = ['.com', '.org', '.edu', '.gov', '.net']
    if any(extracted.suffix == tld[1:] for tld in trusted_tlds):
        domain_score += 0.3
    else:
        warnings.append(f"Uncommon domain extension: .{extracted.suffix}")
    
    # Use API data for domain age and reputation if available
    domain_age_score = 0.0
    if api_data:
        # Use WHOIS data for domain age
        if api_data.get('whois') and api_data['whois'].get('available'):
            whois = api_data['whois']
            age_days = whois.get('domain_age_days')
            if age_days:
                if age_days > 365 * 2:  # More than 2 years old
                    domain_age_score = 0.3
                    positive_indicators.append(f"Domain is {age_days // 365} years old (established)")
                elif age_days > 365:  # More than 1 year old
                    domain_age_score = 0.2
                    positive_indicators.append(f"Domain is {age_days // 365} year old")
                elif age_days < 30:  # Very new domain
                    domain_age_score = -0.2
                    warnings.append(f"Domain is very new ({age_days} days old) - may be suspicious")
        
        # Use VirusTotal for reputation
        if api_data.get('virustotal') and api_data['virustotal'].get('available'):
            vt = api_data['virustotal']
            if vt.get('is_suspicious'):
                domain_age_score -= 0.3
                warnings.append(f"Domain flagged by security services ({vt.get('detection_count', 0)} detections)")
            elif vt.get('reputation_score', 0) > 80:
                domain_age_score += 0.2
                positive_indicators.append("Good reputation score from security services")
        
        # Use Safe Browsing API
        if api_data.get('safebrowsing') and api_data['safebrowsing'].get('available'):
            sb = api_data['safebrowsing']
            if not sb.get('is_safe'):
                domain_age_score -= 0.5
                threats = sb.get('threats', [])
                warnings.append(f"⚠️ SECURITY WARNING: URL flagged by Google Safe Browsing ({', '.join(threats)})")
        
        # Use IPQualityScore
        if api_data.get('ipqualityscore') and api_data['ipqualityscore'].get('available'):
            iqs = api_data['ipqualityscore']
            if iqs.get('phishing') or iqs.get('malware'):
                domain_age_score -= 0.5
                warnings.append("⚠️ SECURITY WARNING: URL flagged as phishing or malware")
            elif iqs.get('fraud_score', 0) > 75:
                domain_age_score -= 0.3
                warnings.append(f"High fraud risk score: {iqs.get('fraud_score')}/100")
            elif iqs.get('fraud_score', 0) < 25:
                domain_age_score += 0.2
                positive_indicators.append("Low fraud risk score from reputation service")
            
            # Use domain age from IPQualityScore if WHOIS not available
            if not api_data.get('whois') and iqs.get('domain_age_days'):
                age_info = iqs.get('domain_age_days')
                if isinstance(age_info, str) and 'year' in age_info.lower():
                    positive_indicators.append(f"Domain age: {age_info}")
    
    # Fallback to domain structure if no API data
    if domain_age_score == 0:
        if '.' not in extracted.subdomain or extracted.subdomain == '':
            domain_age_score = 0.2  # Main domain is more reliable
        else:
            warnings.append("Subdomain detected - may be less reliable")
    
    domain_score += domain_age_score
    factors['domain_security'] = round(domain_score, 2)
    reliability_score += domain_score * RELIABILITY_FACTORS['domain_age']
    
    # Factor 2: Contact Information (0.15)
    contact_score = 0.0
    if publisher_info.get('email'):
        contact_score += 0.4
        positive_indicators.append("Contact email available")
    if publisher_info.get('phone'):
        contact_score += 0.3
        positive_indicators.append("Contact phone available")
    if publisher_info.get('address'):
        contact_score += 0.3
        positive_indicators.append("Physical address available")
    
    if contact_score == 0:
        warnings.append("No contact information found")
    
    factors['contact_info'] = round(contact_score, 2)
    reliability_score += contact_score * RELIABILITY_FACTORS['contact_info']
    
    # Factor 3: Social Media Presence (0.10)
    social_score = 0.0
    if publisher_info.get('social_media'):
        social_count = len(publisher_info['social_media'])
        social_score = min(social_count * 0.3, 1.0)
        positive_indicators.append(f"Social media presence ({social_count} platforms)")
    else:
        warnings.append("No social media links found")
    
    factors['social_media'] = round(social_score, 2)
    reliability_score += social_score * RELIABILITY_FACTORS['social_media']
    
    # Factor 4: Professional Design & Policies (0.20)
    design_score = 0.0
    if soup:
        # Check for privacy policy
        privacy_links = soup.find_all('a', href=re.compile(r'privacy', re.I))
        if privacy_links:
            design_score += 0.3
            positive_indicators.append("Privacy policy available")
        
        # Check for terms of service
        terms_links = soup.find_all('a', href=re.compile(r'terms|tos', re.I))
        if terms_links:
            design_score += 0.2
            positive_indicators.append("Terms of service available")
        
        # Check for about page
        about_links = soup.find_all('a', href=re.compile(r'about', re.I))
        if about_links:
            design_score += 0.2
            positive_indicators.append("About page available")
        
        # Check for professional structure (navigation, footer)
        nav = soup.find('nav')
        footer = soup.find('footer')
        if nav and footer:
            design_score += 0.3
            positive_indicators.append("Professional website structure")
    
    factors['professional_design'] = round(design_score, 2)
    reliability_score += design_score * (RELIABILITY_FACTORS['professional_design'] + RELIABILITY_FACTORS['clear_policies'])
    
    # Factor 5: Content Quality (0.20)
    content_score = 0.0
    if text_content:
        # Check content length (more content = more reliable)
        if len(text_content) > 500:
            content_score += 0.3
            positive_indicators.append("Substantial content provided")
        elif len(text_content) < 100:
            warnings.append("Very little content - may be suspicious")
        
        # Check for excessive promotional language (reduces reliability)
        promotional_count = sum(1 for kw in AD_KEYWORDS if kw in text_content.lower())
        if promotional_count > 10:
            content_score -= 0.2
            warnings.append("Excessive promotional language detected")
        elif promotional_count < 5:
            content_score += 0.2
        
        # Check for specific claims (prices, guarantees, etc.)
        has_specific_info = bool(re.search(r'\$\d+|\d+%|\d+ years?', text_content))
        if has_specific_info:
            content_score += 0.3
            positive_indicators.append("Contains specific information")
        else:
            warnings.append("Lacks specific details")
        
        # Check for spelling/grammar (basic check)
        # This is simplified - in production, use a proper spell checker
        content_score += 0.2  # Assume reasonable quality
    
    factors['content_quality'] = round(max(content_score, 0), 2)
    reliability_score += max(content_score, 0) * RELIABILITY_FACTORS['content_quality']
    
    # Normalize final score
    reliability_score = max(0, min(1.0, reliability_score))
    
    # Determine reliability level
    if reliability_score >= 0.7:
        level = "High"
        level_desc = "This advertisement appears to be from a reliable source with good credibility indicators."
    elif reliability_score >= 0.5:
        level = "Medium"
        level_desc = "This advertisement has moderate reliability. Exercise caution and verify claims independently."
    elif reliability_score >= 0.3:
        level = "Low"
        level_desc = "This advertisement has low reliability indicators. Proceed with significant caution."
    else:
        level = "Very Low"
        level_desc = "This advertisement shows very few reliability indicators. Strongly recommend avoiding or extensive verification."
    
    return {
        'reliability_score': round(reliability_score, 2),
        'reliability_level': level,
        'reliability_description': level_desc,
        'factors': factors,
        'warnings': warnings[:5],  # Limit warnings
        'positive_indicators': positive_indicators[:5]  # Limit indicators
    }

def analyze_image_type(image_path, ocr_text):
    """
    Analyze the type of image
    
    Returns:
        dict with image type information
    """
    import cv2
    from PIL import Image
    
    try:
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        aspect_ratio = width / height if height > 0 else 0
        
        image_type = {
            'format': 'unknown',
            'dimensions': f"{width}x{height}",
            'aspect_ratio': round(aspect_ratio, 2),
            'likely_purpose': 'unknown'
        }
        
        # Determine likely purpose based on dimensions
        if 0.9 <= aspect_ratio <= 1.1:
            image_type['format'] = 'square'
            image_type['likely_purpose'] = 'social_media_post'
        elif aspect_ratio > 1.5:
            image_type['format'] = 'wide'
            image_type['likely_purpose'] = 'banner_ad'
        elif aspect_ratio < 0.7:
            image_type['format'] = 'tall'
            image_type['likely_purpose'] = 'vertical_ad'
        else:
            image_type['format'] = 'standard'
            image_type['likely_purpose'] = 'general_ad'
        
        # Refine based on OCR text
        if ocr_text:
            text_lower = ocr_text.lower()
            if any(kw in text_lower for kw in ['qr', 'code', 'scan']):
                image_type['likely_purpose'] = 'qr_code_promotion'
            elif any(kw in text_lower for kw in ['coupon', 'discount', 'code']):
                image_type['likely_purpose'] = 'coupon'
            elif any(kw in text_lower for kw in ['flyer', 'poster']):
                image_type['likely_purpose'] = 'flyer_poster'
        
        return image_type
    except Exception as e:
        return {
            'format': 'unknown',
            'error': str(e)
        }

