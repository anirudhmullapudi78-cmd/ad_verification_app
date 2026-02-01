# Step-by-Step Guide: Upload Your App to GitHub

Follow these steps in order to create a GitHub repository and upload your app.

## Prerequisites

- GitHub account (create one at https://github.com if you don't have one)
- Git installed on your computer (check with: `git --version`)

---

## Step 1: Verify Security (IMPORTANT!)

Before uploading, make sure your API keys are protected:

```powershell
python check_security.py
```

✅ If all checks pass, continue to Step 2.

---

## Step 2: Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
git init
```

This creates a new Git repository in your project folder.

---

## Step 3: Add All Files

Add all your files to Git:

```powershell
git add .
```

---

## Step 4: Verify .env is NOT Being Committed

**CRITICAL:** Check that your `.env` file (with API keys) is NOT being committed:

```powershell
git status
```

**What to look for:**
- ✅ `.env` should NOT appear in the list of files to be committed
- ✅ If `.env` exists, it should show as "Untracked files" or not appear at all
- ❌ If `.env` appears in "Changes to be committed", STOP and check your `.gitignore`

**If `.env` is being tracked, remove it:**
```powershell
git reset HEAD .env
git rm --cached .env
```

---

## Step 5: Make Your First Commit

Create your first commit with all the files:

```powershell
git commit -m "Initial commit: Ad Verification App"
```

---

## Step 6: Create GitHub Repository (On GitHub Website)

1. **Go to GitHub.com** and sign in to your account

2. **Click the "+" icon** in the top right corner
   - Select "New repository"

3. **Fill in the repository details:**
   - **Repository name:** `ad_verification_app` (or any name you prefer)
   - **Description:** "Web application for verifying and analyzing online advertisements"
   - **Visibility:** 
     - Choose **Public** (anyone can see it) or **Private** (only you can see it)
   - **IMPORTANT:** 
     - ❌ **DO NOT** check "Add a README file" (you already have one)
     - ❌ **DO NOT** check "Add .gitignore" (you already have one)
     - ❌ **DO NOT** check "Choose a license" (unless you want to add one)
   
4. **Click "Create repository"**

5. **After creating, GitHub will show you setup instructions**
   - You'll see a page with commands - we'll use the "push an existing repository" option

---

## Step 7: Connect Your Local Repository to GitHub

Copy the repository URL from GitHub (it looks like: `https://github.com/YOUR_USERNAME/ad_verification_app.git`)

Then run these commands in PowerShell:

```powershell
# Add GitHub as remote repository (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/ad_verification_app.git

# Rename branch to 'main' (GitHub's default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Note:** You'll be prompted for your GitHub username and password/token.

---

## Step 8: Authentication (If Required)

If Git asks for credentials:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` permissions
3. Use the token as your password when prompted

### Option B: GitHub CLI (Alternative)
```powershell
# Install GitHub CLI, then:
gh auth login
```

---

## Step 9: Verify Upload

1. **Refresh your GitHub repository page**
2. **You should see all your files** uploaded
3. **Verify `.env` is NOT there** (it should be missing, which is correct!)

---

## ✅ Success Checklist

After uploading, verify:

- [ ] All your code files are on GitHub
- [ ] `README.md` is visible
- [ ] `.gitignore` is present
- [ ] `.env` file is **NOT** visible (this is correct!)
- [ ] No API keys are exposed in the code

---

## 🎉 You're Done!

Your app is now on GitHub! Others can:
- View your code
- Clone the repository
- Contribute (if public)

---

## 🔄 Making Future Updates

When you make changes to your code:

```powershell
# 1. Check what changed
git status

# 2. Add changed files
git add .

# 3. Commit with a message
git commit -m "Description of your changes"

# 4. Push to GitHub
git push
```

---

## 🆘 Troubleshooting

### "Repository not found" error
- Check that the repository URL is correct
- Make sure you have access to the repository

### "Authentication failed"
- Use a Personal Access Token instead of password
- Make sure your token has `repo` permissions

### ".env file was committed"
- See `SECURITY.md` for instructions on removing it from Git history
- **Immediately revoke and regenerate your API keys**

### "Permission denied"
- Check your GitHub username and repository name
- Verify you have write access to the repository

---

## 📚 Next Steps

- Add a license file (if you want)
- Set up GitHub Actions for CI/CD (optional)
- Add collaborators (if working with others)
- Create releases/tags for versions

---

## 🔐 Security Reminder

**Always remember:**
- Never commit `.env` files
- Never hardcode API keys
- Run `python check_security.py` before each push
- If in doubt, check `git status` before committing

---

**Need help?** Check:
- `SECURITY.md` - Security guidelines
- `GITHUB_SETUP.md` - Additional setup info
- GitHub Docs: https://docs.github.com

