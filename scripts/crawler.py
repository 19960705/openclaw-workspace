#!/usr/bin/env python3
"""
Keonho Crawler Service - 通用爬虫工具
用法:
  crawler.py scrape <url> [--selector CSS] [--format text|json|markdown]
  crawler.py search <query> [--engine brave|google] [--count N]
  crawler.py feed <url> [--count N]
  crawler.py batch <urls_file> [--selector CSS]
  crawler.py monitor <url> [--selector CSS] [--interval 60]
"""

import sys
import json
import argparse
import hashlib
import time
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import httpx
import feedparser

# ─── 配置 ───
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / "cache" / "crawler"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
TIMEOUT = 30

# ─── 工具函数 ───
def get_headers(extra=None):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if extra:
        headers.update(extra)
    return headers

def cache_key(url):
    return hashlib.md5(url.encode()).hexdigest()

def get_cached(url, max_age=3600):
    """获取缓存内容，max_age 秒"""
    cache_file = CACHE_DIR / f"{cache_key(url)}.json"
    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        if time.time() - data.get("ts", 0) < max_age:
            return data.get("content")
    return None

def set_cache(url, content):
    cache_file = CACHE_DIR / f"{cache_key(url)}.json"
    cache_file.write_text(json.dumps({"url": url, "ts": time.time(), "content": content}, ensure_ascii=False))


# ─── 核心功能 ───

def scrape(url, selector=None, format="text", cache=True, cache_age=3600):
    """抓取网页内容"""
    if cache:
        cached = get_cached(url, cache_age)
        if cached:
            return {"source": "cache", "url": url, "content": cached}

    try:
        resp = requests.get(url, headers=get_headers(), timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
    except Exception as e:
        return {"error": str(e), "url": url}

    soup = BeautifulSoup(resp.text, "lxml")

    # 移除脚本和样式
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    if selector:
        elements = soup.select(selector)
        if not elements:
            return {"error": f"选择器 '{selector}' 未匹配到内容", "url": url}
        
        if format == "json":
            results = []
            for el in elements:
                item = {"text": el.get_text(strip=True)}
                if el.get("href"):
                    item["href"] = el["href"]
                if el.get("src"):
                    item["src"] = el["src"]
                results.append(item)
            content = results
        else:
            content = "\n".join(el.get_text(strip=True) for el in elements)
    else:
        if format == "json":
            # 提取结构化数据
            content = {
                "title": soup.title.string if soup.title else "",
                "meta_description": "",
                "headings": [],
                "paragraphs": [],
                "links": [],
                "images": [],
            }
            meta_desc = soup.find("meta", {"name": "description"})
            if meta_desc:
                content["meta_description"] = meta_desc.get("content", "")
            
            for h in soup.find_all(["h1", "h2", "h3"]):
                content["headings"].append({"level": h.name, "text": h.get_text(strip=True)})
            
            for p in soup.find_all("p")[:20]:
                text = p.get_text(strip=True)
                if len(text) > 20:
                    content["paragraphs"].append(text)
            
            for a in soup.find_all("a", href=True)[:30]:
                text = a.get_text(strip=True)
                if text:
                    content["links"].append({"text": text, "href": a["href"]})
            
            for img in soup.find_all("img", src=True)[:10]:
                content["images"].append({"alt": img.get("alt", ""), "src": img["src"]})
        
        elif format == "markdown":
            content = html_to_markdown(soup)
        else:
            content = soup.get_text(separator="\n", strip=True)
            # 压缩多余空行
            lines = [l for l in content.split("\n") if l.strip()]
            content = "\n".join(lines[:200])

    if cache and isinstance(content, str):
        set_cache(url, content)

    return {"source": "live", "url": url, "content": content, "status": resp.status_code}


def html_to_markdown(soup):
    """简单的 HTML 转 Markdown"""
    lines = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
        text = el.get_text(strip=True)
        if not text:
            continue
        if el.name == "h1":
            lines.append(f"# {text}")
        elif el.name == "h2":
            lines.append(f"## {text}")
        elif el.name == "h3":
            lines.append(f"### {text}")
        elif el.name == "h4":
            lines.append(f"#### {text}")
        elif el.name == "li":
            lines.append(f"- {text}")
        elif el.name == "blockquote":
            lines.append(f"> {text}")
        else:
            lines.append(text)
    return "\n\n".join(lines[:150])


def search_brave(query, count=10):
    """使用 Brave Search API 搜索"""
    api_key = os.environ.get("BRAVE_API_KEY", "BSAexUq__e18ZAIYCrgYIDFBxyHEp8j")
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    }
    params = {"q": query, "count": min(count, 20)}
    
    try:
        resp = requests.get("https://api.search.brave.com/res/v1/web/search", 
                          headers=headers, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": str(e)}

    results = []
    for item in data.get("web", {}).get("results", [])[:count]:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "age": item.get("age", ""),
        })
    
    return {"query": query, "count": len(results), "results": results}


def parse_feed(url, count=10):
    """解析 RSS/Atom Feed"""
    cached = get_cached(f"feed:{url}", 1800)
    if cached:
        return {"source": "cache", "feed_url": url, "entries": json.loads(cached)[:count]}

    try:
        feed = feedparser.parse(url, agent=USER_AGENT)
    except Exception as e:
        return {"error": str(e)}

    entries = []
    for entry in feed.entries[:count]:
        item = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": "",
        }
        summary = entry.get("summary", "")
        if summary:
            soup = BeautifulSoup(summary, "lxml")
            item["summary"] = soup.get_text(strip=True)[:500]
        entries.append(item)

    set_cache(f"feed:{url}", json.dumps(entries, ensure_ascii=False))

    return {
        "source": "live",
        "feed_url": url,
        "feed_title": feed.feed.get("title", ""),
        "count": len(entries),
        "entries": entries,
    }


def batch_scrape(urls, selector=None, format="text"):
    """批量抓取"""
    results = []
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
        result = scrape(url, selector=selector, format=format)
        results.append(result)
    return {"count": len(results), "results": results}


def monitor(url, selector=None, interval=60, output_file=None):
    """监控页面变化"""
    state_file = CACHE_DIR / f"monitor_{cache_key(url)}.json"
    
    result = scrape(url, selector=selector, format="text", cache=False)
    if "error" in result:
        return result
    
    current_content = result.get("content", "")
    current_hash = hashlib.md5(current_content.encode()).hexdigest()
    
    previous = {}
    if state_file.exists():
        previous = json.loads(state_file.read_text())
    
    changed = previous.get("hash") != current_hash
    
    state = {
        "url": url,
        "hash": current_hash,
        "last_check": datetime.now(timezone.utc).isoformat(),
        "changed": changed,
        "content_preview": current_content[:500],
    }
    state_file.write_text(json.dumps(state, ensure_ascii=False))
    
    if changed and previous.get("hash"):
        state["previous_preview"] = previous.get("content_preview", "")[:200]
    
    return state


def extract_products(url):
    """提取电商产品信息（通用）"""
    result = scrape(url, format="json", cache=True, cache_age=7200)
    if "error" in result:
        return result
    
    # 尝试从 JSON-LD 提取
    try:
        resp = requests.get(url, headers=get_headers(), timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "lxml")
        
        products = []
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if item.get("@type") in ("Product", "IndividualProduct"):
                            products.append(extract_product_data(item))
                elif data.get("@type") in ("Product", "IndividualProduct"):
                    products.append(extract_product_data(data))
            except:
                pass
        
        if products:
            return {"url": url, "products": products}
        
        # Fallback: 从页面结构提取
        return {"url": url, "structured_data": result.get("content")}
    
    except Exception as e:
        return {"error": str(e)}


def extract_product_data(data):
    """从 JSON-LD 提取产品数据"""
    product = {
        "name": data.get("name", ""),
        "description": data.get("description", "")[:200],
        "brand": "",
        "price": "",
        "currency": "",
        "rating": "",
        "image": "",
    }
    
    brand = data.get("brand", {})
    if isinstance(brand, dict):
        product["brand"] = brand.get("name", "")
    
    offers = data.get("offers", {})
    if isinstance(offers, dict):
        product["price"] = offers.get("price", "")
        product["currency"] = offers.get("priceCurrency", "")
    elif isinstance(offers, list) and offers:
        product["price"] = offers[0].get("price", "")
        product["currency"] = offers[0].get("priceCurrency", "")
    
    rating = data.get("aggregateRating", {})
    if isinstance(rating, dict):
        product["rating"] = f"{rating.get('ratingValue', '')}/5 ({rating.get('reviewCount', '')} reviews)"
    
    product["image"] = data.get("image", "")
    if isinstance(product["image"], list):
        product["image"] = product["image"][0] if product["image"] else ""
    
    return product


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description="Keonho Crawler Service")
    subparsers = parser.add_subparsers(dest="command")
    
    # scrape
    sp = subparsers.add_parser("scrape", help="抓取网页")
    sp.add_argument("url")
    sp.add_argument("--selector", "-s", help="CSS 选择器")
    sp.add_argument("--format", "-f", choices=["text", "json", "markdown"], default="text")
    sp.add_argument("--no-cache", action="store_true")
    
    # search
    sp = subparsers.add_parser("search", help="搜索")
    sp.add_argument("query")
    sp.add_argument("--count", "-n", type=int, default=10)
    
    # feed
    sp = subparsers.add_parser("feed", help="解析 RSS Feed")
    sp.add_argument("url")
    sp.add_argument("--count", "-n", type=int, default=10)
    
    # batch
    sp = subparsers.add_parser("batch", help="批量抓取")
    sp.add_argument("urls_file", help="URL 列表文件，每行一个")
    sp.add_argument("--selector", "-s")
    sp.add_argument("--format", "-f", choices=["text", "json", "markdown"], default="text")
    
    # monitor
    sp = subparsers.add_parser("monitor", help="监控页面变化")
    sp.add_argument("url")
    sp.add_argument("--selector", "-s")
    
    # products
    sp = subparsers.add_parser("products", help="提取产品信息")
    sp.add_argument("url")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "scrape":
        result = scrape(args.url, selector=args.selector, format=args.format, 
                       cache=not args.no_cache)
    elif args.command == "search":
        result = search_brave(args.query, count=args.count)
    elif args.command == "feed":
        result = parse_feed(args.url, count=args.count)
    elif args.command == "batch":
        with open(args.urls_file) as f:
            urls = f.readlines()
        result = batch_scrape(urls, selector=args.selector, format=args.format)
    elif args.command == "monitor":
        result = monitor(args.url, selector=args.selector)
    elif args.command == "products":
        result = extract_products(args.url)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
