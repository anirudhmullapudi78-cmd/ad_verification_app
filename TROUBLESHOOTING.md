# Troubleshooting EasyOCR Errors

## Quick Fix Checklist

### ✅ EasyOCR is Installed and Working
The diagnostic test confirms EasyOCR is properly installed in your virtual environment (`C:\venv_easyocr`).

### Common Issues and Solutions

#### 1. **Warnings vs Errors**
If you see messages like:
- `UserWarning: 'pin_memory' argument is set as true...`
- `UnicodeEncodeError` or `charmap` errors

**These are WARNINGS, not errors.** The app will still work. These are harmless and can be ignored.

#### 2. **Error When Uploading Images**
If you get an error when uploading an image:

**Check:**
- Is the image format supported? (PNG, JPG, JPEG, GIF, WEBP)
- Is the file size under 16MB?
- Check the browser console (F12) for JavaScript errors
- Check the terminal/console where the app is running for the exact error message

#### 3. **Error at App Startup**
If the app won't start:

**Run this to check:**
```powershell
C:\venv_easyocr\Scripts\python.exe diagnose_easyocr.py
```

**If it fails:**
- Reinstall EasyOCR: `C:\venv_easyocr\Scripts\pip.exe install --upgrade easyocr`
- Check internet connection (models need to download on first use)

#### 4. **"EasyOCR not installed" Error**
If you see this message:

**Solution:**
```powershell
C:\venv_easyocr\Scripts\pip.exe install easyocr
```

#### 5. **Encoding Errors (Windows)**
If you see `UnicodeEncodeError` or `charmap` errors:

**These are usually harmless** - they're just display issues with the progress bar. The app code handles these automatically.

**To suppress them:**
- The app already sets UTF-8 encoding in `run_app.bat`
- If still seeing errors, they're likely just warnings

## Getting Help

To get specific help, please provide:

1. **The exact error message** (copy/paste from terminal)
2. **When it occurs:**
   - At startup?
   - When uploading an image?
   - When processing an image?
3. **What you were trying to do** when the error occurred

## Test EasyOCR Manually

Run this to test EasyOCR:
```powershell
C:\venv_easyocr\Scripts\python.exe diagnose_easyocr.py
```

If this passes, EasyOCR is working correctly and the issue is likely:
- A warning (not an error)
- An issue with a specific image
- A different part of the app

## Verify App is Running

1. Check if the app started successfully
2. Open browser to: `http://localhost:5000`
3. Try uploading a simple test image
4. Check the terminal for any error messages

