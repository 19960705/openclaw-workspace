#!/usr/bin/env python3
"""
Lazada Scraper - 优化版
- 增加重试机制
- 更好的错误处理
- 多浏览器支持
"""
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_chrome_options():
    """获取 Chrome 选项"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument(f"--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120,125)}.0.0.0 Safari/537.36")
    return options

def scrape_lazada(keyword, limit=20, max_retries=3):
    """使用 Selenium 爬取 Lazada - 优化版"""
    url = f"https://www.lazada.co.th/catalog/?q={keyword.replace(' ', '%20')}"
    
    for attempt in range(max_retries):
        results = []
        driver = None
        
        try:
            print(f" 尝试 {attempt + 1}/{max_retries}...")
            
            # 启动浏览器
            driver = webdriver.Chrome(options=get_chrome_options())
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # 访问页面
            driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            # 滚动页面加载更多
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 500)")
                time.sleep(1)
            
            # 查找产品
            products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
            print(f" 找到 {len(products)} 个产品")
            
            for prod in products[:limit]:
                try:
                    text = prod.text
                    if not text.strip():
                        continue
                    
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
                    continue
            
            # 成功就退出
            if results:
                break
            
        except Exception as e:
            print(f" 错误: {str(e)[:50]}")
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        # 等待后重试
        if attempt < max_retries - 1:
            wait_time = random.uniform(5, 15)
            print(f" 等待 {wait_time:.1f}秒后重试...")
            time.sleep(wait_time)
    
    return results

def main():
    import sys
    
    keyword = sys.argv[1] if len(sys.argv) > 1 else "coffee grinder"
    
    print(f"🧪 Lazada Scraper 优化版")
    print(f"🔍 Keyword: {keyword}\n")
    
    products = scrape_lazada(keyword)
    
    print(f"\n📊 结果: {len(products)} 个产品\n")
    
    for i, p in enumerate(products[:10], 1):
        if "error" in p:
            print(f"{i}. ❌ {p['error']}")
        else:
            print(f"{i}. {p['name'][:40]}")
            print(f"   💰 {p['price']}")
    
    # 保存
    filename = f"lazada_{keyword.replace(' ', '_')}.json"
    filepath = f"/Users/mac/.openclaw/workspace/data/{filename}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved: {filepath}")

if __name__ == "__main__":
    main()
