#!/usr/bin/env python3
"""
X API Auto Poster (Free Tier)
OAuth 1.0a based posting
"""
import os
import json
import time
import secrets
import base64
import hashlib
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Configuration
CONFIG = {
    "api_key": os.environ.get("X_API_KEY", ""),
    "api_secret": os.environ.get("X_API_SECRET", ""),
    "access_token": os.environ.get("X_ACCESS_TOKEN", ""),
    "access_token_secret": os.environ.get("X_ACCESS_TOKEN_SECRET", ""),
}

def check_config():
    """Check if config is set"""
    print("\n=== X API Config Check ===")
    missing = []
    for key, value in CONFIG.items():
        if not value:
            missing.append(key)
        else:
            print(f"[OK] {key}: {'*' * 10}")
    
    if missing:
        print(f"\nMissing: {', '.join(missing)}")
        return False
    return True

def generate_oauth_header(method, url, params, api_key, api_secret, access_token, access_token_secret):
    """Generate OAuth 1.0a header"""
    # OAuth params
    oauth_params = {
        'oauth_consumer_key': api_key,
        'oauth_token': access_token,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': secrets.token_hex(16),
        'oauth_version': '1.0'
    }
    
    # Merge all params
    all_params = {**params, **oauth_params}
    
    # Sort and encode
    sorted_params = sorted(all_params.items())
    param_string = '&'.join(f'{urllib.parse.quote(str(k))}={urllib.parse.quote(str(v))}' for k, v in sorted_params)
    
    # Signature base string
    signature_base = f'{method}&{urllib.parse.quote(url)}&{urllib.parse.quote(param_string)}'
    
    # Signing key
    signing_key = f'{urllib.parse.quote(api_secret)}&{urllib.parse.quote(access_token_secret)}'
    
    # HMAC-SHA1
    import hmac
    signature = hmac.new(signing_key.encode(), signature_base.encode(), hashlib.sha1).digest()
    oauth_signature = base64.b64encode(signature).decode()
    
    oauth_params['oauth_signature'] = oauth_signature
    
    # Header
    auth_header = 'OAuth ' + ', '.join(
        f'{urllib.parse.quote(k)}="{urllib.parse.quote(v)}"' 
        for k, v in sorted(oauth_params.items())
    )
    
    return auth_header

def post_to_x(text):
    """Post tweet"""
    if not check_config():
        print("\nPlease configure X API keys first!")
        return False
    
    url = "https://api.twitter.com/2/tweets"
    params = {"text": text}
    
    auth_header = generate_oauth_header(
        "POST", url, params,
        CONFIG["api_key"], CONFIG["api_secret"],
        CONFIG["access_token"], CONFIG["access_token_secret"]
    )
    
    import urllib.request
    import json
    
    req = urllib.request.Request(url, data=json.dumps(params).encode())
    req.add_header("Authorization", auth_header)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"\n[Tweet Posted Successfully!]")
            print(f"Tweet ID: {result.get('data', {}).get('id', 'N/A')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"\n[Error] {e.code}: {e.read().decode()}")
        return False

def main():
    print("=" * 50)
    print("[X] X API Auto Poster (Free Tier)")
    print("=" * 50)
    
    if not check_config():
        print("\n" + "=" * 50)
        print("[Setup Instructions]")
        print("=" * 50)
        print("""
1. Go to https://developer.x.com
2. Login/Register
3. Create Project -> Create App
4. Get these keys:
   - API Key
   - API Secret  
   - Access Token
   - Access Token Secret

5. Set environment variables:
   export X_API_KEY="your_api_key"
   export X_API_SECRET="your_api_secret"
   export X_ACCESS_TOKEN="your_access_token"
   export X_ACCESS_TOKEN_SECRET="your_access_token_secret"

6. Run this script again
        """)
        return
    
    # Test post
    test_tweet = "Test tweet from AI Trend Hunter X API!"
    post_to_x(test_tweet)

if __name__ == "__main__":
    main()
