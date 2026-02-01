# Security Guide - Protecting API Keys

## ⚠️ IMPORTANT: Never Commit API Keys to GitHub!

This repository is configured to protect your API keys. Follow these guidelines to keep your keys safe.

## ✅ What's Already Protected

1. **Code uses environment variables** - All API keys are read from environment variables using `os.getenv()`, not hardcoded
2. **`.gitignore` file** - Prevents sensitive files from being committed:
   - `.env` files (where you store API keys)
   - Cache directories
   - User uploads
   - Logs
   - Verification history

## 🔐 How to Set Up API Keys Safely

### Option 1: Use a `.env` file (Recommended)

1. Create a `.env` file in the project root:
   ```bash
   # Copy the template (if you have one)
   # Or create manually
   ```

2. Add your API keys to `.env`:
   ```env
   SONAR_API_KEY=your_actual_key_here
   WHOIS_API_KEY=your_actual_key_here
   VIRUSTOTAL_API_KEY=your_actual_key_here
   SAFEBROWSING_API_KEY=your_actual_key_here
   IPQUALITYSCORE_API_KEY=your_actual_key_here
   ```

3. **IMPORTANT**: The `.env` file is already in `.gitignore` - it will NOT be committed to GitHub

4. Install python-dotenv to load .env automatically:
   ```bash
   pip install python-dotenv
   ```

5. Update `app.py` to load .env (if not already done):
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Load .env file
   ```

### Option 2: Use Environment Variables Directly

**Windows PowerShell:**
```powershell
$env:SONAR_API_KEY="your_key_here"
$env:WHOIS_API_KEY="your_key_here"
```

**Windows CMD:**
```cmd
set SONAR_API_KEY=your_key_here
set WHOIS_API_KEY=your_key_here
```

**Linux/Mac:**
```bash
export SONAR_API_KEY="your_key_here"
export WHOIS_API_KEY="your_key_here"
```

## ✅ Before Pushing to GitHub

1. **Verify `.gitignore` is working:**
   ```bash
   git status
   ```
   Make sure `.env` does NOT appear in the list of files to be committed

2. **Check for any hardcoded keys:**
   - Search your code for actual API key values
   - Make sure all keys use `os.getenv()` or environment variables

3. **Review what will be committed:**
   ```bash
   git add .
   git status
   ```
   Double-check that no sensitive files are included

## 🚨 If You Accidentally Committed API Keys

If you've already pushed API keys to GitHub:

1. **Immediately revoke and regenerate all exposed API keys** from their respective providers
2. **Remove keys from Git history** (if the repo is public, assume keys are compromised):
   ```bash
   # Remove file from history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (WARNING: This rewrites history)
   git push origin --force --all
   ```
3. **Consider making the repository private** until keys are rotated
4. **Check GitHub's security audit log** for unauthorized access

## 📋 Checklist Before First Commit

- [ ] `.gitignore` file exists and includes `.env`
- [ ] No API keys are hardcoded in source code
- [ ] `.env` file exists locally but is NOT tracked by git
- [ ] `git status` shows `.env` as untracked/ignored
- [ ] All API keys use `os.getenv()` or environment variables
- [ ] README or documentation explains how to set up API keys

## 🔍 Verify Your Setup

Run this to check if `.env` is properly ignored:
```bash
git check-ignore .env
```
If it returns the path, it's being ignored correctly.

## 📝 For Contributors

If someone clones your repository:

1. They need to create their own `.env` file
2. They need to get their own API keys from the providers
3. They should never commit their `.env` file
4. See `API_SETUP_GUIDE.md` for detailed setup instructions

## 🛡️ Additional Security Best Practices

1. **Use different API keys for development and production**
2. **Set up API key rotation** (change keys periodically)
3. **Monitor API usage** for unexpected activity
4. **Use API key restrictions** when available (IP whitelisting, rate limits)
5. **Never share API keys** in chat, email, or documentation
6. **Use secrets management** for production deployments (AWS Secrets Manager, Azure Key Vault, etc.)

## 📚 Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

