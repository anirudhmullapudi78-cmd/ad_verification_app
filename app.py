from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import tldextract
from PIL import Image
import cv2
import spacy
from dotenv import load_dotenv
from analysis_engine import (
    detect_advertisement, classify_ad_type, extract_publisher_info,
    assess_reliability, analyze_image_type
)
from api_integrations import get_enhanced_domain_info, analyze_with_sonar

# Load environment variables from .env file
load_dotenv()

# Try to import EasyOCR (optional)
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    easyocr = None
    print("Warning: EasyOCR not installed. Image OCR will not be available.")
    print("Install with: pip install easyocr")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load spaCy model (if available)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None
    print("Warning: spaCy model not found. Run: python -m spacy download en_core_web_sm")

# Initialize EasyOCR reader lazily (only when needed)
# This avoids startup errors and allows models to download on first use
reader = None
reader_initialized = False

def get_easyocr_reader():
    """Initialize EasyOCR reader on first use (lazy loading)"""
    global reader, reader_initialized
    
    if not EASYOCR_AVAILABLE:
        return None
    
    if not reader_initialized:
        try:
            print("Initializing EasyOCR... This may take a moment on first run.")
            print("Downloading models if needed (this may take several minutes)...")
            print("(You may see encoding warnings - these can be ignored)")
            
            # Initialize EasyOCR - encoding errors in progress bar are harmless
            reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            print("✓ EasyOCR initialized successfully!")
            reader_initialized = True
        except Exception as e:
            # Check if it's just an encoding error (which is harmless)
            error_str = str(e)
            if 'charmap' in error_str or 'UnicodeEncodeError' in error_str:
                # Encoding error is just in the progress bar display
                # Try to use the reader anyway if it was partially initialized
                try:
                    # Test if reader actually works despite the error
                    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
                    print("✓ EasyOCR initialized (encoding warning can be ignored)")
                    reader_initialized = True
                except:
                    reader = None
                    reader_initialized = True
                    print(f"Warning: EasyOCR initialization had issues: {e}")
            else:
                reader = None
                reader_initialized = True
                print(f"Warning: EasyOCR initialization failed: {e}")
                print("Image OCR will not be available.")
    
    return reader

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    """Verify an ad by URL or uploaded image"""
    data = request.get_json() if request.is_json else request.form
    
    if 'url' in data:
        # Verify by URL
        url = data['url']
        result = verify_url(url)
        return jsonify(result)
    
    elif 'file' in request.files:
        # Verify by uploaded image
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            result = verify_image(filepath)
            return jsonify(result)
    
    return jsonify({'error': 'Invalid request'}), 400

def verify_url(url):
    """Verify an ad URL with comprehensive analysis"""
    try:
        # Extract domain information
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"
        
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = str(soup)
        
        # Extract text content
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Enhanced Analysis
        # 1. Detect if it's an advertisement
        ad_detection = detect_advertisement(text_content, html_content)
        
        # 2. Classify ad type (if it's an ad)
        ad_classification = {}
        if ad_detection['is_advertisement']:
            ad_classification = classify_ad_type(text_content)
        
        # 3. Extract publisher/owner information
        publisher_info = extract_publisher_info(soup, url)
        
        # 3.5. Get enhanced domain info from APIs (if configured)
        api_data = get_enhanced_domain_info(domain, url)
        
        # 3.6. AI-powered analysis using Sonar API (if configured)
        ai_analysis = None
        if text_content:
            # Use Sonar API for AI analysis of the content
            ai_analysis = analyze_with_sonar(text_content[:4000], 'ad_verification')
            if ai_analysis.get('available') and ai_analysis.get('parsed_analysis'):
                # Enhance ad detection with AI results
                ai_result = ai_analysis['parsed_analysis']
                if ai_result.get('is_advertisement') is not None:
                    # Update ad detection with AI confidence
                    ad_detection['is_advertisement'] = ai_result.get('is_advertisement', ad_detection['is_advertisement'])
                    ad_detection['ai_confidence'] = ai_result.get('confidence', ad_detection['confidence'])
                    ad_detection['ai_indicators'] = ai_result.get('indicators', [])
                
                # Enhance ad classification with AI results
                if ai_result.get('ad_type'):
                    ad_classification['ad_type'] = ai_result.get('ad_type')
                    ad_classification['ai_enhanced'] = True
        
        # 4. Assess reliability (with API data if available)
        reliability_assessment = assess_reliability(url, soup, text_content, publisher_info, api_data)
        
        # Enhance reliability with AI analysis if available
        if ai_analysis and ai_analysis.get('parsed_analysis'):
            ai_result = ai_analysis['parsed_analysis']
            if ai_result.get('reliability_level'):
                # Use AI reliability assessment if available
                reliability_assessment['ai_enhanced'] = True
                reliability_assessment['ai_reliability_level'] = ai_result.get('reliability_level')
                reliability_assessment['ai_reliability_score'] = ai_result.get('reliability_score', 0) / 100.0
                if ai_result.get('red_flags'):
                    reliability_assessment['ai_red_flags'] = ai_result.get('red_flags', [])
                    reliability_assessment['warnings'].extend(ai_result.get('red_flags', []))
                if ai_result.get('analysis_summary'):
                    reliability_assessment['ai_summary'] = ai_result.get('analysis_summary')
        
        # Build comprehensive verification result
        verification_result = {
            'url': url,
            'domain': domain,
            'status': 'success',
            'title': soup.title.string if soup.title else 'No title',
            'text_length': len(text_content),
            'has_images': len(soup.find_all('img')) > 0,
            'has_links': len(soup.find_all('a')) > 0,
            
            # Advertisement Detection
            'ad_detection': {
                'is_advertisement': ad_detection['is_advertisement'],
                'confidence': ad_detection['confidence'],
                'indicators': ad_detection['indicators']
            },
            
            # Ad Classification (if applicable)
            'ad_classification': ad_classification if ad_detection['is_advertisement'] else {
                'ad_type': 'not_an_advertisement',
                'confidence': 1.0 - ad_detection['confidence'],
                'message': 'This content does not appear to be an advertisement.'
            },
            
            # Publisher/Owner Information
            'publisher_info': publisher_info,
            
            # Reliability Assessment
            'reliability': reliability_assessment,
            
            # API Verification Data (if available)
            'api_verification': api_data if api_data.get('apis_used') else None,
            
            # AI Analysis (Sonar API) - if available
            'ai_analysis': ai_analysis if ai_analysis and ai_analysis.get('available') else None,
            
            # Basic verification
            'verification': {
                'domain_valid': bool(extracted.domain),
                'accessible': True,
                'has_content': len(text_content) > 0,
                'is_advertisement': ad_detection['is_advertisement']
            }
        }
        
        # NLP analysis if spaCy is available
        if nlp and text_content:
            doc = nlp(text_content[:2000])  # Increased limit for better analysis
            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents[:15]]
            verification_result['nlp_analysis'] = {
                'entities': entities,
                'entity_count': len(entities)
            }
        
        return verification_result
        
    except requests.RequestException as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e),
            'verification': {
                'accessible': False
            }
        }
    except Exception as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }

def verify_image(image_path):
    """Verify an ad image using OCR and comprehensive image analysis"""
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return {
                'filename': os.path.basename(image_path),
                'status': 'error',
                'error': 'Could not load image file'
            }
        
        height, width = img.shape[:2]
        
        # OCR text extraction using EasyOCR (lazy initialization)
        ocr_text = ""
        ocr_reader = get_easyocr_reader()
        
        if ocr_reader:
            try:
                # EasyOCR returns a list of tuples: (bbox, text, confidence)
                results = ocr_reader.readtext(image_path)
                # Extract text from results
                ocr_text = " ".join([result[1] for result in results])
            except Exception as e:
                print(f"EasyOCR error: {e}")
                ocr_text = ""
        elif not EASYOCR_AVAILABLE:
            return {
                'filename': os.path.basename(image_path),
                'status': 'error',
                'error': 'EasyOCR is not installed. Please install it with: pip install easyocr',
                'image_info': {
                    'width': width,
                    'height': height,
                    'aspect_ratio': round(width / height, 2) if height > 0 else 0
                }
            }
        else:
            return {
                'filename': os.path.basename(image_path),
                'status': 'error',
                'error': 'EasyOCR not initialized. Please check EasyOCR installation.',
                'image_info': {
                    'width': width,
                    'height': height,
                    'aspect_ratio': round(width / height, 2) if height > 0 else 0
                }
            }
        
        # Enhanced Analysis
        # 1. Analyze image type
        image_type_analysis = analyze_image_type(image_path, ocr_text)
        
        # 2. Detect if it's an advertisement
        ad_detection = detect_advertisement(ocr_text, None)
        
        # 3. Classify ad type (if it's an ad)
        ad_classification = {}
        if ad_detection['is_advertisement']:
            ad_classification = classify_ad_type(ocr_text)
        
        # 3.5. AI-powered analysis using Sonar API (if configured and OCR text available)
        ai_analysis = None
        if ocr_text and ocr_text.strip():
            # Use Sonar API for AI analysis of the OCR text
            ai_analysis = analyze_with_sonar(ocr_text[:4000], 'ad_verification')
            if ai_analysis.get('available') and ai_analysis.get('parsed_analysis'):
                # Enhance ad detection with AI results
                ai_result = ai_analysis['parsed_analysis']
                if ai_result.get('is_advertisement') is not None:
                    # Update ad detection with AI confidence
                    ad_detection['is_advertisement'] = ai_result.get('is_advertisement', ad_detection['is_advertisement'])
                    ad_detection['ai_confidence'] = ai_result.get('confidence', ad_detection['confidence'])
                    ad_detection['ai_indicators'] = ai_result.get('indicators', [])
                
                # Enhance ad classification with AI results
                if ai_result.get('ad_type'):
                    ad_classification['ad_type'] = ai_result.get('ad_type')
                    ad_classification['ai_enhanced'] = True
        
        # 4. Extract publisher info from text (limited for images)
        publisher_info = {
            'name': None,
            'domain': None,
            'email': None,
            'phone': None,
            'extracted_from_image': True
        }
        
        # Try to extract contact info from OCR text
        import re
        if ocr_text:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, ocr_text)
            if emails:
                publisher_info['email'] = emails[0]
            
            phone_pattern = r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_pattern, ocr_text)
            if phones:
                publisher_info['phone'] = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
            
            # Try to find website/domain
            url_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
            urls = re.findall(url_pattern, ocr_text)
            if urls:
                publisher_info['domain'] = urls[0]
        
        # 4.5. Enhance reliability with AI analysis if available
        if ai_analysis and ai_analysis.get('parsed_analysis'):
            ai_result = ai_analysis['parsed_analysis']
            if ai_result.get('publisher_info'):
                # Update publisher info with AI findings
                publisher_info.update(ai_result.get('publisher_info', {}))
        
        # 5. Assess reliability (simplified for images)
        reliability_assessment = {
            'reliability_score': 0.5,  # Default medium score for images
            'reliability_level': 'Medium',
            'reliability_description': 'Image-based advertisements require additional verification. Check the source and verify claims independently.',
            'factors': {
                'has_contact_info': 0.3 if (publisher_info.get('email') or publisher_info.get('phone')) else 0.0,
                'has_text_content': 0.4 if ocr_text.strip() else 0.0,
                'image_quality': 0.3
            },
            'warnings': [],
            'positive_indicators': []
        }
        
        # Refine reliability based on available information
        if publisher_info.get('email') or publisher_info.get('phone'):
            reliability_assessment['reliability_score'] += 0.1
            reliability_assessment['positive_indicators'].append("Contact information found in image")
        else:
            reliability_assessment['warnings'].append("No contact information found in image")
        
        if ocr_text.strip():
            reliability_assessment['reliability_score'] += 0.1
            reliability_assessment['positive_indicators'].append("Text content extracted from image")
        else:
            reliability_assessment['warnings'].append("No text content found in image")
        
        reliability_assessment['reliability_score'] = min(1.0, reliability_assessment['reliability_score'])
        
        # Enhance reliability with AI analysis if available
        if ai_analysis and ai_analysis.get('parsed_analysis'):
            ai_result = ai_analysis['parsed_analysis']
            if ai_result.get('reliability_level'):
                reliability_assessment['ai_enhanced'] = True
                reliability_assessment['ai_reliability_level'] = ai_result.get('reliability_level')
                reliability_assessment['ai_reliability_score'] = ai_result.get('reliability_score', 0) / 100.0
                if ai_result.get('red_flags'):
                    reliability_assessment['ai_red_flags'] = ai_result.get('red_flags', [])
                    reliability_assessment['warnings'].extend(ai_result.get('red_flags', []))
                if ai_result.get('analysis_summary'):
                    reliability_assessment['ai_summary'] = ai_result.get('analysis_summary')
        
        if reliability_assessment['reliability_score'] >= 0.7:
            reliability_assessment['reliability_level'] = 'High'
        elif reliability_assessment['reliability_score'] >= 0.5:
            reliability_assessment['reliability_level'] = 'Medium'
        elif reliability_assessment['reliability_score'] >= 0.3:
            reliability_assessment['reliability_level'] = 'Low'
        else:
            reliability_assessment['reliability_level'] = 'Very Low'
        
        # Build comprehensive verification result
        verification_result = {
            'filename': os.path.basename(image_path),
            'status': 'success',
            'image_info': {
                'width': width,
                'height': height,
                'aspect_ratio': round(width / height, 2) if height > 0 else 0
            },
            'image_type': image_type_analysis,
            'ocr_text': ocr_text.strip(),
            
            # Advertisement Detection
            'ad_detection': {
                'is_advertisement': ad_detection['is_advertisement'],
                'confidence': ad_detection['confidence'],
                'indicators': ad_detection['indicators']
            },
            
            # Ad Classification (if applicable)
            'ad_classification': ad_classification if ad_detection['is_advertisement'] else {
                'ad_type': 'not_an_advertisement',
                'confidence': 1.0 - ad_detection['confidence'],
                'message': 'This image does not appear to be an advertisement.'
            },
            
            # Publisher/Owner Information
            'publisher_info': publisher_info,
            
            # Reliability Assessment
            'reliability': reliability_assessment,
            
            'verification': {
                'has_text': len(ocr_text.strip()) > 0,
                'text_length': len(ocr_text.strip()),
                'is_advertisement': ad_detection['is_advertisement']
            },
            
            # AI Analysis (Sonar API) - if available
            'ai_analysis': ai_analysis if ai_analysis and ai_analysis.get('available') else None
        }
        
        # NLP analysis on OCR text if available
        if nlp and ocr_text.strip():
            doc = nlp(ocr_text[:1000])  # Increased limit
            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents[:15]]
            verification_result['nlp_analysis'] = {
                'entities': entities,
                'entity_count': len(entities)
            }
        
        return verification_result
        
    except Exception as e:
        return {
            'filename': os.path.basename(image_path),
            'status': 'error',
            'error': str(e)
        }

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

