#!/usr/bin/env python3
"""
EvoMap HTTP Retry Capsule - Universal HTTP retry with exponential backoff
Based on: sha256:6c8b2bef4652d5113cc802b6995a8e9f5da8b5b1ffe3d6bc639e2ca8ce27edec
"""

import requests
import time
import random
from typing import Callable, Any, Optional
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def retry_with_backoff(
    func: Callable,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    timeout: float = 30.0
) -> Any:
    """
    Execute function with exponential backoff retry.
    
    Args:
        func: Function to execute (should return requests.Response or similar)
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential calculation
        jitter: Add random jitter to prevent thundering herd
        timeout: Request timeout in seconds
    
    Returns:
        Result of func() if successful
    
    Raises:
        Last exception if all retries exhausted
    """
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            result = func()
            
            # Check for rate limit (429)
            if hasattr(result, 'status_code'):
                if result.status_code == 429:
                    # Parse Retry-After header if present
                    retry_after = result.headers.get('Retry-After')
                    if retry_after:
                        delay = float(retry_after)
                    else:
                        delay = base_delay * (exponential_base ** attempt)
                    print(f"Rate limited, waiting {delay}s...")
                    time.sleep(delay)
                    continue
                
                # Retry on 5xx errors
                if 500 <= result.status_code < 600:
                    delay = base_delay * (exponential_base ** attempt)
                    if jitter:
                        delay *= (0.5 + random.random())
                    delay = min(delay, max_delay)
                    print(f"Server error {result.status_code}, retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue
            
            return result
            
        except requests.exceptions.Timeout as e:
            last_exception = e
            delay = base_delay * (exponential_base ** attempt)
            if jitter:
                delay *= (0.5 + random.random())
            delay = min(delay, max_delay)
            print(f"Timeout (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay:.1f}s...")
            time.sleep(delay)
            
        except requests.exceptions.ConnectionError as e:
            last_exception = e
            delay = base_delay * (exponential_base ** attempt)
            if jitter:
                delay *= (0.5 + random.random())
            delay = min(delay, max_delay)
            print(f"Connection error (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay:.1f}s...")
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            last_exception = e
            delay = base_delay * (exponential_base ** attempt)
            if jitter:
                delay *= (0.5 + random.random())
            delay = min(delay, max_delay)
            print(f"Request error: {e}, retrying in {delay:.1f}s...")
            time.sleep(delay)
    
    raise last_exception


def fetch_with_retry(url: str, **kwargs) -> requests.Response:
    """
    Convenience function to fetch URL with retry.
    
    Usage:
        resp = fetch_with_retry("https://api.example.com/data")
        print(resp.json())
    """
    kwargs.setdefault('timeout', 30)
    kwargs.setdefault('verify', False)
    
    def _request():
        return requests.get(url, **kwargs)
    
    return retry_with_backoff(_request)


def post_with_retry(url: str, **kwargs) -> requests.Response:
    """
    Convenience function to POST to URL with retry.
    
    Usage:
        resp = post_with_retry("https://api.example.com/data", json={"key": "value"})
        print(resp.json())
    """
    kwargs.setdefault('timeout', 30)
    kwargs.setdefault('verify', False)
    
    def _request():
        return requests.post(url, **kwargs)
    
    return retry_with_backoff(_request)


if __name__ == "__main__":
    # Demo usage
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Fetching {url} with retry...")
        try:
            resp = fetch_with_retry(url)
            print(f"Success! Status: {resp.status_code}")
            print(f"Content: {resp.text[:200]}...")
        except Exception as e:
            print(f"Failed: {e}")
    else:
        print("Usage: python retry.py <url>")
