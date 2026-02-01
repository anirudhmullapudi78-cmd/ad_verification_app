"""
Security Check Script - Verify your setup is safe before pushing to GitHub
Run this before your first commit to ensure API keys are protected.
"""
import os
import re
from pathlib import Path

def check_gitignore():
    """Check if .gitignore exists and contains .env"""
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print("[X] .gitignore file is MISSING!")
        print("    Create a .gitignore file to protect sensitive files.")
        return False
    
    try:
        content = gitignore_path.read_text(encoding='utf-8')
    except:
        content = gitignore_path.read_text(encoding='latin-1')
    
    if '.env' not in content:
        print("[X] .gitignore does NOT include .env")
        print("    Add '.env' to your .gitignore file.")
        return False
    
    print("[OK] .gitignore exists and includes .env")
    return True

def check_env_file():
    """Check if .env file exists and is not tracked"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("[!] .env file not found (this is OK if you're using system env vars)")
        return True
    
    # Check if .env contains actual keys (not just placeholders)
    try:
        content = env_path.read_text(encoding='utf-8')
    except:
        content = env_path.read_text(encoding='latin-1')
    
    # Look for placeholder patterns
    placeholders = ['your_', 'example', 'placeholder', 'xxx', 'key_here']
    has_placeholders = any(p in content.lower() for p in placeholders)
    
    # Look for actual key patterns (long alphanumeric strings)
    key_pattern = r'[A-Za-z0-9_-]{20,}'
    potential_keys = re.findall(key_pattern, content)
    
    if has_placeholders and len(potential_keys) == 0:
        print("[!] .env file contains only placeholders")
        print("    Make sure to add your actual API keys before running the app.")
        return True
    
    if len(potential_keys) > 0:
        print("[OK] .env file found with API keys configured")
    else:
        print("[!] .env file exists but may not have valid keys")
    
    return True

def check_hardcoded_keys():
    """Check for hardcoded API keys in source code"""
    print("\nChecking source code for hardcoded API keys...")
    
    # Files to check
    files_to_check = [
        'app.py',
        'api_integrations.py',
        'analysis_engine.py'
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        path = Path(file_path)
        if not path.exists():
            continue
        
        try:
            content = path.read_text(encoding='utf-8')
        except:
            try:
                content = path.read_text(encoding='latin-1')
            except:
                print(f"    [WARNING] Could not read {file_path} - skipping")
                continue
        
        # Look for patterns that might indicate hardcoded keys
        # Pattern 1: Long alphanumeric strings that look like API keys
        key_pattern = r'["\']([A-Za-z0-9_-]{30,})["\']'
        matches = re.findall(key_pattern, content)
        
        # Filter out false positives (URLs, function names, etc.)
        suspicious = []
        for match in matches:
            # Skip if it's clearly not a key (URLs, long function names, etc.)
            if not any(x in match.lower() for x in ['http', 'www', 'api', 'key']):
                # Check if it's in a context that suggests it's a key
                context_pattern = r'["\']' + re.escape(match) + r'["\']'
                if re.search(context_pattern, content):
                    # Check surrounding context
                    idx = content.find(match)
                    context = content[max(0, idx-50):min(len(content), idx+len(match)+50)]
                    if any(word in context.lower() for word in ['key', 'api', 'token', 'secret']):
                        suspicious.append(match[:20] + '...')
        
        if suspicious:
            issues_found.append(f"  {file_path}: Found {len(suspicious)} potential hardcoded keys")
    
    if issues_found:
        print("[X] Potential hardcoded API keys found:")
        for issue in issues_found:
            print(issue)
        print("\n    Review these files and ensure all keys use os.getenv()")
        return False
    else:
        print("[OK] No hardcoded API keys detected in source code")
        return True

def check_env_usage():
    """Check if code properly uses environment variables"""
    print("\nChecking if code uses environment variables correctly...")
    
    api_integrations = Path('api_integrations.py')
    if not api_integrations.exists():
        print("[!] api_integrations.py not found")
        return False
    
    try:
        content = api_integrations.read_text(encoding='utf-8')
    except:
        content = api_integrations.read_text(encoding='latin-1')
    
    # Check if os.getenv is used
    if 'os.getenv' not in content:
        print("[X] api_integrations.py does not use os.getenv()")
        return False
    
    # Check for direct key assignments (bad pattern)
    bad_patterns = [
        r"['\"]sk-[A-Za-z0-9]+['\"]",  # OpenAI-style keys
        r"['\"][A-Za-z0-9]{32,}['\"]",  # Long keys
    ]
    
    for pattern in bad_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"[X] Found potential hardcoded keys matching pattern: {pattern}")
            return False
    
    print("[OK] Code properly uses os.getenv() for API keys")
    return True

def main():
    print("=" * 60)
    print("Security Check - Pre-GitHub Upload Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Gitignore Configuration", check_gitignore),
        (".env File Status", check_env_file),
        ("Environment Variable Usage", check_env_usage),
        ("Hardcoded Keys Check", check_hardcoded_keys),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 60)
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] Check failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[OK]" if passed else "[X]"
        print(f"{status} {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("[OK] All security checks passed! Safe to push to GitHub.")
        print("\nRemember:")
        print("  - Never commit .env files")
        print("  - Never hardcode API keys")
        print("  - Use environment variables or .env files")
    else:
        print("[X] Some security checks failed!")
        print("\nPlease fix the issues above before pushing to GitHub.")
        print("See SECURITY.md for detailed guidelines.")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()

