# Ad Verification App

A comprehensive web application for verifying and analyzing online advertisements, providing reliability assessments, publisher information, and security checks.

## Features

- 🔍 **URL Verification** - Analyze advertisements by URL
- 📸 **Image Analysis** - Upload and verify ad images with OCR
- 🤖 **AI-Powered Analysis** - Intelligent ad detection using Claude Sonnet
- 🛡️ **Security Checks** - Domain reputation and malware detection
- 📊 **Comprehensive Reports** - Detailed reliability assessments

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ad_verification_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys (Optional but recommended):**
   
   Create a `.env` file in the project root:
   ```env
   SONAR_API_KEY=your_sonar_api_key_here
   WHOIS_API_KEY=your_whois_api_key_here
   VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
   SAFEBROWSING_API_KEY=your_google_safebrowsing_api_key_here
   IPQUALITYSCORE_API_KEY=your_ipqualityscore_api_key_here
   ```
   
   **Note:** The `.env` file is already in `.gitignore` and will NOT be committed to GitHub.
   
   See `API_SETUP_GUIDE.md` for detailed API setup instructions.

4. **Run the application:**
   ```bash
   python app.py
   ```
   
   Or use the provided scripts:
   - Windows: `run_app.bat` or `run_app.ps1`
   
5. **Access the app:**
   Open your browser and navigate to `http://localhost:5000`

## Security

⚠️ **IMPORTANT:** Never commit API keys to GitHub!

- All API keys are stored in environment variables or `.env` files
- The `.env` file is automatically ignored by Git
- See `SECURITY.md` for detailed security guidelines

## API Configuration

The app supports multiple external APIs for enhanced verification:

- **Sonar API** (Recommended) - AI-powered content analysis
- **WHOIS API** - Domain registration information
- **VirusTotal API** - Domain reputation checking
- **Google Safe Browsing API** - Malware/phishing detection
- **IPQualityScore API** - Fraud detection

See `API_SETUP_GUIDE.md` for setup instructions and pricing information.

## Project Structure

```
ad_verification_app/
├── app.py                 # Main Flask application
├── api_integrations.py    # External API integrations
├── analysis_engine.py     # Core analysis logic
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules (protects API keys)
├── SECURITY.md           # Security guidelines
├── API_SETUP_GUIDE.md    # API setup instructions
├── templates/            # HTML templates
├── static/              # CSS and JavaScript
└── uploads/             # User uploaded files (gitignored)
```

## Usage

### Verify by URL

1. Enter a URL in the web interface
2. Click "Verify"
3. View comprehensive analysis results including:
   - Advertisement detection
   - Publisher information
   - Reliability assessment
   - Security checks
   - AI-powered insights

### Verify by Image

1. Upload an advertisement image
2. The app extracts text using OCR
3. Analyzes the content for ad verification
4. Provides detailed reliability assessment

## Development

### Running in Development Mode

The app runs in debug mode by default:
```bash
python app.py
```

### Environment Variables

The app automatically loads environment variables from:
1. System environment variables
2. `.env` file (if present)

## Troubleshooting

See `TROUBLESHOOTING.md` for common issues and solutions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure `.env` is not committed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on GitHub.

