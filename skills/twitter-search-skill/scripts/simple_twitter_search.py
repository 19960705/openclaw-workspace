#!/usr/bin/env python3
"""
Twitter/X Search for OpenClaw

Simple Twitter search using Brave Search API as the primary method.
Falls back to direct X.com links when API is not available.

Usage:
    python twitter_search.py "search query" [--limit N]
"""

import argparse
import json
import os
import sys
from urllib.parse import quote
from typing import List, Dict, Any

try:
    import requests
except ImportError:
    print("Error: Install requests: pip install requests")
    sys.exit(1)


BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"


def get_brave_api_key() -> str:
    """Get Brave API key from environment or config."""
    key = os.environ.get("BRAVE_API_KEY")

    # Try to read from openclaw config
    if not key:
        config_path = os.path.expanduser("~/.openclaw/.env")
        if os.path.exists(config_path):
            with open(config_path) as f:
                for line in f:
                    if line.startswith("BRAVE_API_KEY="):
                        key = line.strip().split("=", 1)[1]
                        break

    return key


def search_twitter_brave(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Search Twitter/X using Brave Search.
    """
    api_key = get_brave_api_key()

    if not api_key:
        return []

    # Modify query to focus on Twitter/X
    twitter_query = f"{query} site:x.com OR site:twitter.com"

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }

    params = {
        "q": twitter_query,
        "count": min(limit, 50),
        "extra_search_params": "source:social"  # Try to get social results
    }

    try:
        response = requests.get(
            BRAVE_API_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            results = []

            for item in data.get("web", {}).get("results", []):
                url = item.get("url", "")
                # Filter for Twitter/X URLs
                if "x.com" in url or "twitter.com" in url:
                    results.append({
                        "title": item.get("title", ""),
                        "url": url,
                        "description": item.get("description", "")[:300],
                        "domain": item.get("domain", ""),
                        "published_at": item.get("published_at", ""),
                        "type": item.get("type", "")
                    })

            return results

    except requests.exceptions.RequestException:
        pass

    return []


def create_search_link(query: str) -> str:
    """Create direct X.com search link."""
    encoded = quote(query)
    return f"https://x.com/search?q={encoded}&f=live"


def main():
    parser = argparse.ArgumentParser(
        description="Search Twitter/X posts"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--link-only", action="store_true", help="Only show search link")

    args = parser.parse_args()

    if args.link_only:
        print(create_search_link(args.query))
        return

    results = search_twitter_brave(args.query, args.limit)

    if args.json:
        output = {
            "query": args.query,
            "count": len(results),
            "search_link": create_search_link(args.query),
            "results": results
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if not results:
        print(f"No results found from API.")
        print(f"\nDirect search link:")
        print(f"  {create_search_link(args.query)}")
        sys.exit(0)

    print(f"Found {len(results)} results for: {args.query}")
    print("-" * 70)

    for i, item in enumerate(results, 1):
        title = item.get("title", "No title")
        url = item.get("url", "")
        desc = item.get("description", "")[:150]

        print(f"{i}. {title}")
        if desc:
            print(f"   {desc}...")
        print(f"   {url}")
        print()

    print(f"\nDirect search: {create_search_link(args.query)}")


if __name__ == "__main__":
    main()
