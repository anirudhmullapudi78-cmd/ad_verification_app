# Quick Start: Upload to GitHub

## 🚀 Complete Step-by-Step Guide

### Step 0: Install Git (If Not Already Installed)

**Check if Git is installed:**
```powershell
git --version
```

**If Git is NOT installed:**

1. **Download Git for Windows:**
   - Go to: https://git-scm.com/download/win
   - Download the installer
   - Run the installer (use default settings)

2. **Restart PowerShell** after installation

3. **Verify installation:**
   ```powershell
   git --version
   ```
   Should show something like: `git version 2.x.x`

---

## Step 1: Verify Your App is Secure

```powershell
python check_security.py
```

✅ **All checks should pass** before proceeding.

---

## Step 2: Initialize Git Repository

Open PowerShell in your project folder (`C:\Users\Anirudh\ad_verification_app`) and run:

```powershell
git init
```

You should see: `Initialized empty Git repository in ...`

---

## Step 3: Add All Files

```powershell
git add .
```

---

## Step 4: Check What Will Be Committed

**VERY IMPORTANT:** Verify `.env` is NOT being committed:

```powershell
git status
```

**Look for:**
- ✅ `.env` should NOT be in "Changes to be committed"
- ✅ If you see `.env` listed, it should be under "Untracked files" (that's OK)

**If `.env` appears in "Changes to be committed":**
```powershell
git reset HEAD .env
```

---

## Step 5: Create Your First Commit

```powershell
git commit -m "Initial commit: Ad Verification App"
```

---

## Step 6: Create GitHub Account (If Needed)

1. Go to **https://github.com**
2. Click **"Sign up"**
3. Follow the registration process
4. Verify your email

---

## Step 7: Create New Repository on GitHub

1. **Sign in to GitHub.com**

2. **Click the green "New" button** (or the "+" icon → "New repository")

3. **Fill in the form:**
   - **Repository name:** `ad_verification_app`
   - **Description:** `Web application for verifying online advertisements`
   - **Visibility:** Choose **Public** or **Private**
   - **IMPORTANT:** Leave all checkboxes UNCHECKED:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license

4. **Click "Create repository"**

5. **Copy the repository URL** that GitHub shows you
   - It looks like: `https://github.com/YOUR_USERNAME/ad_verification_app.git`
   - You'll need this in the next step

---

## Step 8: Connect and Push to GitHub

Run these commands (replace `YOUR_USERNAME` with your actual GitHub username):

```powershell
# Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/ad_verification_app.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

**You'll be prompted for:**
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (see below)

---

## Step 9: Create Personal Access Token

GitHub requires a token instead of password:

1. **Go to GitHub.com** → Click your profile picture → **Settings**

2. **Scroll down** → Click **"Developer settings"** (left sidebar)

3. **Click "Personal access tokens"** → **"Tokens (classic)"**

4. **Click "Generate new token"** → **"Generate new token (classic)"**

5. **Fill in:**
   - **Note:** `ad_verification_app`
   - **Expiration:** Choose duration (90 days recommended)
   - **Select scopes:** Check **`repo`** (full control of private repositories)

6. **Click "Generate token"**

7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`

8. **Use this token as your password** when Git asks for credentials

---

## Step 10: Verify Upload

1. **Go to your GitHub repository page**
2. **Refresh the page**
3. **You should see all your files!**

**Verify:**
- ✅ `app.py` is there
- ✅ `README.md` is there
- ✅ `.gitignore` is there
- ✅ `.env` is **NOT** there (this is correct!)

---

## ✅ Success!

Your app is now on GitHub! 🎉

---

## 🔄 Making Updates Later

When you change your code:

```powershell
git add .
git commit -m "Description of changes"
git push
```

---

## 🆘 Common Issues

### "git: command not found"
- **Solution:** Install Git (see Step 0)

### "Repository not found"
- **Solution:** Check the repository URL is correct
- Make sure you typed your GitHub username correctly

### "Authentication failed"
- **Solution:** Use Personal Access Token, not password
- Make sure token has `repo` permissions

### ".env file is being committed"
- **Solution:** 
  ```powershell
  git reset HEAD .env
  git rm --cached .env
  ```
  Then check your `.gitignore` file

### "Permission denied"
- **Solution:** 
  - Verify your GitHub username
  - Check repository name is correct
  - Make sure you have write access

---

## 📝 Quick Command Reference

```powershell
# Initialize repository
git init

# Add all files
git add .

# Check status
git status

# Commit changes
git commit -m "Your message"

# Connect to GitHub (first time only)
git remote add origin https://github.com/YOUR_USERNAME/ad_verification_app.git
git branch -M main

# Push to GitHub
git push -u origin main

# Future updates
git add .
git commit -m "Update description"
git push
```

---

## 🔐 Security Checklist

Before pushing, always verify:

- [ ] `.env` file is NOT in `git status`
- [ ] `python check_security.py` passes all checks
- [ ] No API keys are hardcoded in source code
- [ ] `.gitignore` includes `.env`

---

**Need more help?** See:
- `GITHUB_UPLOAD_STEPS.md` - Detailed guide
- `SECURITY.md` - Security guidelines
- GitHub Help: https://docs.github.com

