#!/usr/bin/env python3
"""
Lazada Scraper - Selenium 版本
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_lazada(keyword, limit=20):
    """使用 Selenium 爬取 Lazada"""
    url = f"https://www.lazada.co.th/catalog/?q={keyword.replace(' ', '%20')}"
    
    # Chrome 选项
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    results = []
    
    try:
        # 启动浏览器
        print("🚀 Starting Chrome...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # 访问页面
        print(f"📄 Loading: {url}")
        driver.get(url)
        time.sleep(5)
        
        # 等待产品加载
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Bm3ON"))
            )
        except:
            print("⚠️ Products not found, trying alternative selector...")
        
        # 查找产品
        products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
        print(f"📦 Found {len(products)} products")
        
        for prod in products[:limit]:
            try:
                text = prod.text
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                
                if lines:
                    name = lines[0][:50]
                    price = "N/A"
                    for line in lines:
                        if '฿' in line:
                            price = line.strip()
                            break
                    
                    results.append({
                        "name": name,
                        "price": price,
                        "keyword": keyword
                    })
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        results = [{"error": str(e)}]
    
    return results

if __name__ == "__main__":
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "coffee grinder"
    
    print(f"🧪 Lazada Scraper (Selenium)")
    print(f"🔍 Keyword: {keyword}\n")
    
    products = scrape_lazada(keyword)
    
    print(f"\n📊 Results: {len(products)} products\n")
    
    for i, p in enumerate(products[:10], 1):
        if "error" in p:
            print(f"{i}. ❌ {p['error']}")
        else:
            print(f"{i}. {p['name'][:40]}")
            print(f"   💰 {p['price']}")
    
    # 保存
    with open(f"/Users/mac/.openclaw/workspace/data/lazada_{keyword.replace(' ', '_')}.json", "w") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved!")
