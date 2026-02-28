#!/usr/bin/env python3
"""
Lazada Scraper for Thailand E-commerce
"""
import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def scrape_lazada(keyword, limit=20):
    """Scrape products from Lazada Thailand"""
    url = f"https://www.lazada.co.th/catalog/?q={keyword.replace(' ', '%20')}"
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        
        products = page.query_selector_all(".Bm3ON")
        
        for prod in products[:limit]:
            try:
                text = prod.inner_text()
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                
                if lines:
                    name = lines[0]
                    price = "N/A"
                    for line in lines:
                        if '฿' in line:
                            price = line.strip()
                            break
                    
                    results.append({
                        "name": name,
                        "price": price,
                        "keyword": keyword,
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                pass
        
        browser.close()
    
    return results

if __name__ == "__main__":
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "coffee grinder"
    products = scrape_lazada(keyword)
    
    print(f"\n📊 Lazada 搜索: {keyword}")
    print(f"找到 {len(products)} 个产品\n")
    
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['name'][:45]}")
        print(f"   💰 {p['price']}")
    
    # Save to JSON
    with open(f"/Users/mac/.openclaw/workspace/data/lazada_{keyword.replace(' ', '_')}.json", "w") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 已保存到 data/lazada_{keyword.replace(' ', '_')}.json")
