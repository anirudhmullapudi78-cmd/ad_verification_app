# Ad Verification App - API Documentation

## 1️⃣ Git Repository
**GitHub repo link:**  
[Your GitHub repository URL here]

**Branch name:** main  
**Latest code status:** Stable and working  
**Sonar API (Claude 3.5 Sonnet) integrated**  
**API keys moved to environment variables**  
**CORS enabled (via Flask)**  
**Tested with local frontend and API clients**

---

## 2️⃣ Project Structure
```
ad_verification_app/
├── app.py                           # Main Flask application
├── api_integrations.py              # External API integrations (WHOIS, VirusTotal, etc.)
├── analysis_engine.py               # Core ad detection and analysis logic
├── requirements.txt                 # Python dependencies
├── env_template.txt                 # Environment variables template
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── templates/                       # HTML templates
│   └── index.html
├── static/                          # CSS and JavaScript
│   ├── css/
│   └── js/
├── uploads/                         # User uploaded images (auto-created)
├── api_cache/                       # Cached API responses (auto-created)
├── html_cache/                      # Cached HTML content (auto-created)
├── publisher_cache/                 # Cached publisher data (auto-created)
├── verification_history/             # Verification history logs (auto-created)
└── logs/                            # Application logs (auto-created)
```

---

## 3️⃣ Entry File
**Entry file:** `app.py`

**How to run:**
```bash
python app.py
```

**Runs on:**
- `http://0.0.0.0:5000`
- `http://localhost:5000`

---

## 4️⃣ API Endpoints

### GET /
**Method:** GET  
**Purpose:** Serves HTML template (for local development)  
**Response:** HTML page

---

### POST /verify
**Method:** POST  
**Purpose:** Verify an advertisement by URL or uploaded image  
**Content-Type:** 
- `application/json` (for URL verification)
- `multipart/form-data` (for image upload)

**Input Options:**

**Option 1: URL Verification (JSON)**
```json
{
  "url": "https://example.com/advertisement"
}
```

**Option 2: Image Upload (Form Data)**
- Field name: `file`
- Accepted formats: PNG, JPG, JPEG, GIF, WEBP
- Max size: 16MB

**Response:** See section 6️⃣

---

### GET /uploads/<filename>
**Method:** GET  
**Purpose:** Serve uploaded image file  
**Response:** Image file (binary)

**Example:**
```
GET /uploads/screenshot.png
```

---

## 5️⃣ Input Format

### For URL Verification
**Content-Type:** `application/json`
```json
{
  "url": "string (required, must be valid URL)"
}
```

### For Image Verification
**Content-Type:** `multipart/form-data`
- **Field name:** `file`
- **Accepted formats:** PNG, JPG, JPEG, GIF, WEBP
- **Max size:** 16MB

---

## 6️⃣ Output Response

### URL Verification Response (Success)
```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "status": "success",
  "title": "Page Title",
  "text_length": 1234,
  "has_images": true,
  "has_links": true,
  
  "ad_detection": {
    "is_advertisement": true,
    "confidence": 0.85,
    "indicators": [
      "Contains ad keywords: buy now, shop now",
      "Contains 3 promotional patterns"
    ]
  },
  
  "ad_classification": {
    "ad_type": "product",
    "confidence": 0.80,
    "message": "This appears to be a product advertisement."
  },
  
  "publisher_info": {
    "name": "Company Name",
    "domain": "example.com",
    "email": "contact@example.com",
    "phone": "+1-234-567-8900"
  },
  
  "reliability": {
    "reliability_score": 0.75,
    "reliability_level": "High",
    "reliability_description": "This advertisement appears to be from a reliable source.",
    "factors": {
      "domain_age": 0.15,
      "ssl_certificate": 0.10,
      "contact_info": 0.15,
      "content_quality": 0.20
    },
    "warnings": [],
    "positive_indicators": [
      "Domain is over 2 years old",
      "HTTPS enabled",
      "Contact information available"
    ]
  },
  
  "api_verification": {
    "apis_used": ["whois", "virustotal", "safebrowsing"],
    "whois": {
      "available": true,
      "domain": "example.com",
      "registered": "2020-01-15",
      "domain_age_days": 1825,
      "registrar": "Example Registrar"
    },
    "virustotal": {
      "available": true,
      "detection_count": 0,
      "reputation_score": 95,
      "is_suspicious": false
    },
    "safebrowsing": {
      "available": true,
      "is_safe": true,
      "threats": [],
      "threat_count": 0
    }
  },
  
  "ai_analysis": {
    "available": true,
    "analysis_type": "ad_verification",
    "parsed_analysis": {
      "is_advertisement": true,
      "confidence": 90,
      "ad_type": "product",
      "indicators": ["Promotional language", "Call-to-action buttons"],
      "reliability_level": "High",
      "reliability_score": 85,
      "red_flags": [],
      "analysis_summary": "This is a legitimate product advertisement."
    },
    "model_used": "anthropic/claude-3.5-sonnet"
  },
  
  "nlp_analysis": {
    "entities": [
      {"text": "Company Name", "label": "ORG"},
      {"text": "New York", "label": "GPE"}
    ],
    "entity_count": 2
  },
  
  "verification": {
    "domain_valid": true,
    "accessible": true,
    "has_content": true,
    "is_advertisement": true
  }
}
```

### Image Verification Response (Success)
```json
{
  "filename": "screenshot.png",
  "status": "success",
  "image_info": {
    "width": 1920,
    "height": 1080,
    "aspect_ratio": 1.78
  },
  "image_type": {
    "type": "advertisement",
    "confidence": 0.85
  },
  "ocr_text": "Buy now! Limited time offer. Call 1-800-123-4567",
  
  "ad_detection": {
    "is_advertisement": true,
    "confidence": 0.90,
    "indicators": [
      "Contains ad keywords: buy now, limited time",
      "Contains promotional patterns"
    ]
  },
  
  "ad_classification": {
    "ad_type": "product",
    "confidence": 0.85,
    "message": "This appears to be a product advertisement."
  },
  
  "publisher_info": {
    "name": null,
    "domain": "example.com",
    "email": "contact@example.com",
    "phone": "1-800-123-4567",
    "extracted_from_image": true
  },
  
  "reliability": {
    "reliability_score": 0.60,
    "reliability_level": "Medium",
    "reliability_description": "Image-based advertisements require additional verification.",
    "factors": {
      "has_contact_info": 0.3,
      "has_text_content": 0.4,
      "image_quality": 0.3
    },
    "warnings": [],
    "positive_indicators": [
      "Contact information found in image",
      "Text content extracted from image"
    ]
  },
  
  "verification": {
    "has_text": true,
    "text_length": 45,
    "is_advertisement": true
  },
  
  "ai_analysis": {
    "available": true,
    "parsed_analysis": {
      "is_advertisement": true,
      "confidence": 92,
      "ad_type": "product",
      "reliability_level": "Medium",
      "reliability_score": 65
    }
  },
  
  "nlp_analysis": {
    "entities": [
      {"text": "1-800-123-4567", "label": "CARDINAL"}
    ],
    "entity_count": 1
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": "Error message here",
  "url": "https://example.com"  // (if URL verification)
}
```

or

```json
{
  "filename": "image.png",
  "status": "error",
  "error": "Could not load image file"
}
```

---

## 7️⃣ Model / Logic Info

### Advertisement Detection
**Method:** Local pattern matching + AI enhancement  
**Location:** 
- Primary: Local (analysis_engine.py)
- Enhancement: Sonar API (cloud-based, optional)

**Logic:**
- Keyword matching (buy now, shop now, limited time, etc.)
- Promotional pattern detection (prices, discounts, call-to-action)
- HTML meta tag analysis (for URL verification)
- AI-powered analysis via Sonar API (if configured)

**Dependencies:** 
- Local: `beautifulsoup4`, `re` (built-in)
- Cloud: `requests` (for Sonar API)

---

### Ad Classification
**Method:** Local pattern matching + AI enhancement  
**Location:** Local (analysis_engine.py)

**Ad Types Detected:**
- `product` - Product advertisements
- `service` - Service advertisements
- `real_estate` - Real estate listings
- `job` - Job postings
- `education` - Educational courses/training
- `healthcare` - Medical/healthcare services
- `financial` - Financial services, loans, insurance
- `event` - Events, concerts, conferences
- `food` - Restaurants, food delivery
- `travel` - Travel, hotels, flights
- `general` - General advertisements

**Dependencies:** `re` (built-in), `beautifulsoup4`

---

### Publisher Information Extraction
**Method:** HTML parsing + regex + AI enhancement  
**Location:** Local (analysis_engine.py)

**Extracted Information:**
- Publisher name
- Domain/website
- Email addresses
- Phone numbers
- Contact information

**Dependencies:** `beautifulsoup4`, `re` (built-in), `tldextract`

---

### Reliability Assessment
**Method:** Multi-factor scoring algorithm + API data + AI enhancement  
**Location:** Local (analysis_engine.py) + External APIs

**Factors Considered:**
- Domain age (from WHOIS API)
- SSL certificate (HTTPS)
- Contact information availability
- Social media presence
- Reviews and ratings
- Professional design indicators
- Privacy policy / Terms of service
- Content quality
- Security reputation (VirusTotal, Safe Browsing)
- Fraud score (IPQualityScore)

**Scoring:**
- 0.7+ = High reliability
- 0.5-0.7 = Medium reliability
- 0.3-0.5 = Low reliability
- <0.3 = Very Low reliability

**Dependencies:** 
- Local: `analysis_engine.py`
- External: Multiple APIs (WHOIS, VirusTotal, Safe Browsing, IPQualityScore)

---

### OCR (Text Extraction from Images)
**Method:** EasyOCR (local)  
**Location:** Local

**Model:** EasyOCR with English language support  
**Features:**
- Text extraction from images
- Confidence scores for each text detection
- Bounding box coordinates

**Dependencies:** `easyocr`, `opencv-python`, `pillow`

**Note:** EasyOCR models are downloaded on first use (~500MB)

---

### AI-Powered Analysis (Sonar API)
**Method:** Cloud API (OpenRouter endpoint)  
**Location:** Cloud-based

**Model:** `anthropic/claude-3.5-sonnet` (configurable)  
**Endpoint:** `https://openrouter.ai/api/v1/chat/completions`

**Capabilities:**
- Intelligent ad detection
- Ad type classification
- Reliability assessment
- Red flag detection
- Publisher information extraction
- Natural language understanding

**Authentication:** API key (Bearer token)  
**Dependencies:** `requests`, `openai` (used as OpenRouter client)

**Alternative Models Available:**
- `perplexity/sonar-reasoning`
- `perplexity/sonar`
- Other OpenRouter models

---

### Domain Verification APIs

#### WHOIS API
**Method:** Cloud API (WHOIS XML API)  
**Location:** Cloud-based  
**Endpoint:** `https://www.whoisxmlapi.com/whoisserver/WhoisService`  
**Purpose:** Domain registration information, age, registrar  
**Authentication:** API key  
**Dependencies:** `requests`

#### VirusTotal API
**Method:** Cloud API  
**Location:** Cloud-based  
**Endpoint:** `https://www.virustotal.com/vtapi/v2/domain/report`  
**Purpose:** Domain reputation, malware detection  
**Authentication:** API key  
**Dependencies:** `requests`

#### Google Safe Browsing API
**Method:** Cloud API  
**Location:** Cloud-based  
**Endpoint:** `https://safebrowsing.googleapis.com/v4/threatMatches:find`  
**Purpose:** Malware and phishing detection  
**Authentication:** API key  
**Dependencies:** `requests`

#### IPQualityScore API
**Method:** Cloud API  
**Location:** Cloud-based  
**Endpoint:** `https://www.ipqualityscore.com/api/json/url`  
**Purpose:** Fraud detection, URL reputation  
**Authentication:** API key  
**Dependencies:** `requests`

#### AbuseIPDB API
**Method:** Cloud API  
**Location:** Cloud-based  
**Endpoint:** `https://api.abuseipdb.com/api/v2/check`  
**Purpose:** IP reputation checking  
**Authentication:** API key  
**Dependencies:** `requests`

---

### NLP Analysis
**Method:** spaCy (local)  
**Location:** Local

**Model:** `en_core_web_sm` (English small model)  
**Purpose:** Named entity recognition, text analysis  
**Features:**
- Entity extraction (ORG, PERSON, GPE, etc.)
- Entity counting
- Text analysis

**Dependencies:** `spacy`  
**Note:** Model must be downloaded separately: `python -m spacy download en_core_web_sm`

---

## 8️⃣ Requirements.txt
```
flask
requests
beautifulsoup4
tldextract
spacy
easyocr
pillow
opencv-python
python-dotenv
```

**Additional Notes:**
- **spacy**: Requires model download (`python -m spacy download en_core_web_sm`)
- **easyocr**: Downloads models on first use (~500MB)
- **opencv-python**: Image processing library
- **python-dotenv**: Loads environment variables from `.env` file

---

## 9️⃣ Additional Notes for Integration

### Environment Variables
All API keys are stored in `.env` file (use `env_template.txt` as template):

**Required (for full functionality):**
- `SONAR_API_KEY` - Sonar API key (OpenRouter)
- `WHOIS_API_KEY` - WHOIS XML API key (optional)
- `VIRUSTOTAL_API_KEY` - VirusTotal API key (optional)
- `SAFEBROWSING_API_KEY` - Google Safe Browsing API key (optional)
- `IPQUALITYSCORE_API_KEY` - IPQualityScore API key (optional)
- `ABUSEIPDB_API_KEY` - AbuseIPDB API key (optional)

**Note:** The app works without API keys but with limited functionality. Sonar API is recommended for best results.

### CORS
**Status:** Enabled via Flask (allows cross-origin requests)  
**Configuration:** Default Flask CORS settings

### File Storage
- **Uploads:** Saved to `uploads/` directory (created automatically)
- **Cache:** API responses cached in `api_cache/`, `html_cache/`, `publisher_cache/`
- **Logs:** Application logs saved to `logs/` directory
- **History:** Verification history saved to `verification_history/`

### Port
**Default:** Flask port 5000  
**Configurable:** Change in `app.py` (line 498)

### Error Handling
All endpoints return JSON with:
- `status`: "success" or "error"
- `error`: Error message (if status is "error")
- Additional fields based on endpoint

### API Caching
The app implements caching for:
- API responses (WHOIS, VirusTotal, etc.)
- HTML content
- Publisher information

This reduces API calls and improves performance.

### Graceful Degradation
- If APIs are not configured, the app falls back to local analysis
- If EasyOCR is not installed, image verification returns an error
- If spaCy model is not available, NLP analysis is skipped
- All features work independently

### Rate Limiting
**Note:** External APIs have rate limits:
- Sonar API: Pay-per-use (check OpenRouter pricing)
- WHOIS API: 500 queries/month (free tier)
- VirusTotal: 4 requests/minute, 500/day (free tier)
- Google Safe Browsing: 10,000 requests/day (free tier)
- IPQualityScore: 5,000 requests/month (free tier)

The app includes caching to minimize API calls.

---

**Best regards,**

