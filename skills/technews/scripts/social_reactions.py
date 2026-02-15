#!/usr/bin/env python3
"""
Social Reactions - Finds and highlights social media reactions to articles
Uses Brave Search to find Twitter discussions as primary method.
"""

import json
import os
import re
from urllib.parse import quote
from typing import List, Dict, Optional
import requests

# Twitter search via Brave Search (uses Brave API)
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"


def find_twitter_reactions(article_title: str, article_url: str, max_results: int = 3) -> List[Dict]:
    """
    Search for Twitter reactions to an article using Brave Search.
    Falls back to direct search URL if API key is not available.
    """
    reactions = []

    # Extract keywords from title
    keywords = [w.strip('".,!?()[]{}') for w in article_title.split() if len(w) > 3]
    if not keywords:
        keywords = article_title.split()[:3]
    query = " ".join(keywords[:5])

    # Try Brave Search API if available
    api_key = None
    try:
        api_key = os.environ.get("BRAVE_API_KEY")
    except Exception:
        pass

    if api_key:
        try:
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": api_key
            }
            params = {
                "q": f"{query} site:x.com OR site:twitter.com",
                "count": max_results,
                "extra_search_params": "engagement_type:social"
            }

            response = requests.get(BRAVE_SEARCH_URL, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                for result in data.get("web", {}).get("results", [])[:max_results]:
                    reactions.append({
                        "platform": "twitter",
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "description": result.get("description", "")[:200],
                        "source": "brave_search"
                    })
        except Exception:
            pass

    # Fallback: return search URLs
    if not reactions:
        reactions.append({
            "platform": "twitter",
            "search_url": f"https://x.com/search?q={quote(query)}&f=live",
            "note": "Automated search unavailable - direct Twitter search link provided",
            "query": query
        })

    return reactions


def find_hacker_news(article_url: str) -> Optional[Dict]:
    """Check if article was posted on Hacker News."""
    # HN Algolia API
    hn_api = "https://hn.algolia.com/api/v1/search"
    
    try:
        # Extract domain for searching
        domain_match = re.search(r'https?://([^/]+)', article_url)
        if not domain_match:
            return None
        
        domain = domain_match.group(1)
        response = requests.get(
            hn_api,
            params={"query": domain, "tags": "story", "hitsPerPage": 1},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("hits"):
                hit = data["hits"][0]
                return {
                    "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "title": hit.get("title"),
                    "points": hit.get("points"),
                    "comment_count": hit.get("numComments")
                }
    except Exception:
        pass
    
    return None


def extract_spicy_tweets(content: str) -> List[str]:
    """Extract potential hot takes from article content."""
    # Look for quotes, controversial statements in article
    spicy_bits = []
    
    # Find quoted text
    quotes = re.findall(r'"([^"]+)"', content)
    
    # Look for strong opinion words
    opinion_words = ["criticized", "praised", "controversial", "scandal", "lawsuit", 
                     "breakthrough", "revolutionary", "disaster", "failure", "success"]
    
    for quote in quotes[:5]:  # Limit to 5 quotes
        if any(word in quote.lower() for word in opinion_words):
            spicy_bits.append(f'"{quote}"')
    
    return spicy_bits


def analyze_reactions(articles: List[Dict]) -> List[Dict]:
    """Analyze social reactions for a list of articles."""
    analyzed = []
    
    for article in articles:
        if not article.get("success"):
            analyzed.append(article)
            continue
        
        title = article.get("title", "")
        url = article.get("url", "")
        content = article.get("content", "")
        
        # Find HN posts
        hn_data = find_hacker_news(url)
        
        # Extract spicy quotes
        spicy = extract_spicy_tweets(content)
        
        article["reactions"] = {
            "hacker_news": hn_data,
            "spicy_quotes": spicy,
            "twitter_search": find_twitter_reactions(title, url)
        }
        
        analyzed.append(article)
    
    return analyzed


def main():
    """Main entry point."""
    import sys
    
    input_data = json.loads(sys.stdin.read())
    articles = input_data.get("articles", [])
    
    if not articles:
        print(json.dumps({"error": "No articles provided"}))
        return
    
    analyzed = analyze_reactions(articles)
    print(json.dumps({"analyzed": analyzed}))


if __name__ == "__main__":
    main()
