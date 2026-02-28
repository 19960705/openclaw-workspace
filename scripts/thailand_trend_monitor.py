#!/usr/bin/env python3
"""
Thailand Trend Monitor - 更具体的品类
"""
import json
import time
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("/Users/mac/.openclaw/workspace/data/trends")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def scrape_lazada(keyword, limit=10):
    """使用 Selenium 爬取 Lazada"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    
    url = f"https://www.lazada.co.th/catalog/?q={keyword.replace(' ', '%20')}"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    results = []
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        time.sleep(5)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Bm3ON"))
            )
        except:
            pass
        
        products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
        
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
                    
                    results.append({"name": name, "price": price})
            except:
                continue
        
        driver.quit()
        
    except Exception as e:
        results = [{"error": str(e)}]
    
    return results

def run_monitor():
    print(f"🕕 Thailand Trend Monitor - {datetime.now()}")
    
    # 更具体的关键词
    keywords = [
        "แก้วกาแฟ",       # 咖啡杯
        "ถ้วยเอสเพรสโซ",  # 意式浓缩杯
        "ช้อนกาแฟ",       # 咖啡勺
        "ตะกร้ากาแฟ",     # 咖啡篮
        "ฝาครอบกาแฟ"      # 咖啡盖
    ]
    
    lazada_data = {}
    
    for kw in keywords:
        print(f"🔍 Scraping: {kw}")
        lazada_data[kw] = scrape_lazada(kw, limit=5)
    
    # 保存
    data = {
        "timestamp": datetime.now().isoformat(),
        "lazada": lazada_data
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = DATA_DIR / f"thailand_trends_{timestamp}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved: {filepath}")
    
    return data

if __name__ == "__main__":
    run_monitor()
