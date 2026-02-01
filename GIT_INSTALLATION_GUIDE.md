# Git Installation and Setup Guide

## Problem: Git is Not Installed

If you're getting `git: command not found`, you need to install Git first.

---

## 🚀 Option 1: Install Git (Recommended)

### Step 1: Download Git for Windows

1. **Go to:** https://git-scm.com/download/win
2. **Click the download button** (it will download the latest version)
3. **Wait for download to complete**

### Step 2: Install Git

1. **Run the installer** (Git-x.x.x-64-bit.exe)
2. **Click "Next"** through the installation wizard
3. **Use default settings** (recommended for beginners)
4. **Important settings:**
   - ✅ Use Git from the command line and also from 3rd-party software
   - ✅ Use bundled OpenSSH
   - ✅ Use the OpenSSL library
   - ✅ Checkout Windows-style, commit Unix-style line endings
   - ✅ Use MinTTY (default terminal)
   - ✅ Default (fast-forward or merge)
   - ✅ Git Credential Manager
   - ✅ Enable file system caching

5. **Click "Install"**
6. **Wait for installation to complete**
7. **Click "Finish"**

### Step 3: Restart PowerShell

**IMPORTANT:** Close and reopen PowerShell after installation!

1. Close your current PowerShell window
2. Open a new PowerShell window
3. Navigate back to your project:
   ```powershell
   cd C:\Users\Anirudh\ad_verification_app
   ```

### Step 4: Verify Installation

```powershell
git --version
```

You should see something like: `git version 2.42.0.windows.2`

---

## 🚀 Option 2: Use GitHub Desktop (Easier - No Command Line!)

If you don't want to use command line, use GitHub Desktop instead:

### Step 1: Download GitHub Desktop

1. **Go to:** https://desktop.github.com/
2. **Click "Download for Windows"**
3. **Run the installer**
4. **Sign in with your GitHub account**

### Step 2: Add Your Repository

1. **Open GitHub Desktop**
2. **Click "File" → "Add Local Repository"**
3. **Browse to:** `C:\Users\Anirudh\ad_verification_app`
4. **Click "Add Repository"**

### Step 3: Publish to GitHub

1. **Click "Publish repository"** button (top right)
2. **Name your repository:** `ad_verification_app`
3. **Choose:** Public or Private
4. **IMPORTANT:** Make sure "Keep this code private" is unchecked if you want it public
5. **Click "Publish Repository"**

**Done!** Your code is now on GitHub! 🎉

---

## 🚀 Option 3: Use GitHub Web Interface (No Installation!)

You can upload files directly through GitHub's website:

### Step 1: Create Repository on GitHub

1. **Go to:** https://github.com
2. **Sign in** (or create account)
3. **Click "+" → "New repository"**
4. **Name it:** `ad_verification_app`
5. **Choose:** Public or Private
6. **DO NOT check any boxes** (README, .gitignore, license)
7. **Click "Create repository"**

### Step 2: Upload Files

1. **On the repository page, click "uploading an existing file"**
2. **Drag and drop your project folder** OR click "choose your files"
3. **Select all files EXCEPT:**
   - ❌ `.env` (if it exists - contains API keys!)
   - ❌ `__pycache__/` folders
   - ❌ `api_cache/`, `html_cache/`, etc.
   - ❌ `uploads/` folder
   - ❌ `logs/` folder

4. **Scroll down, add commit message:** "Initial commit"
5. **Click "Commit changes"**

**Done!** Your code is on GitHub! 🎉

---

## ✅ Which Method Should You Use?

### Use GitHub Desktop if:
- ✅ You prefer a visual interface
- ✅ You don't want to use command line
- ✅ You want the easiest option

### Use Git Command Line if:
- ✅ You want to learn Git properly
- ✅ You plan to do more development
- ✅ You want full control

### Use GitHub Web Interface if:
- ✅ You just want to upload once
- ✅ You don't want to install anything
- ✅ It's a one-time upload

---

## 🔧 Troubleshooting

### "Git is not recognized" after installation

**Solution:**
1. **Close ALL PowerShell/Command Prompt windows**
2. **Restart your computer** (sometimes needed)
3. **Open new PowerShell**
4. **Try again:** `git --version`

### "Permission denied" errors

**Solution:**
- Make sure you're signed in to GitHub
- Use Personal Access Token instead of password

### Can't find the repository folder

**Solution:**
```powershell
cd C:\Users\Anirudh\ad_verification_app
```

---

## 📝 Quick Command Reference (After Git Installation)

Once Git is installed, use these commands:

```powershell
# Initialize repository
git init

# Add all files
git add .

# Check status (verify .env is NOT included)
git status

# Commit
git commit -m "Initial commit: Ad Verification App"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ad_verification_app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🆘 Still Having Issues?

1. **Check if Git is installed:**
   ```powershell
   git --version
   ```

2. **If not installed:** Use Option 1 (Install Git) or Option 2 (GitHub Desktop)

3. **If installed but not working:** Restart PowerShell/Computer

4. **For web upload:** Use Option 3 (GitHub Web Interface)

---

## 🎯 Recommended: Start with GitHub Desktop

**For beginners, I recommend GitHub Desktop** - it's the easiest way to get started!

1. Download: https://desktop.github.com/
2. Install and sign in
3. Add your repository
4. Click "Publish"
5. Done! ✅

---

**Need more help?** Let me know which step you're stuck on!

