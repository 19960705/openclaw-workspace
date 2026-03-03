#!/usr/bin/env python3
"""
Test Lazada scraping
"""
import json
import time
from datetime import datetime
from pathlib import Path

def test_scrape():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    
    url = "https://www.lazada.co.th/catalog/?q=%E0%B9%81%E0%B8%81%E0%B9%89%E0%B8%A7%E0%B8%81%E0%B8%B2%E0%B9%81%E0%B8%9F"
    
    print(f"Opening: {url}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        time.sleep(8)
        
        print(f"Page source length: {len(driver.page_source)}")
        
        # Try multiple selectors
        selectors = [
            ".Bm3ON",
            ".product-card",
            "[data-item-id]",
            ".product-item",
            ".card-jfy-item"
        ]
        
        for sel in selectors:
            elems = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"Selector {sel}: {len(elems)} elements")
            if elems:
                for i, e in enumerate(elems[:3]):
                    print(f"  {i+1}. {e.text[:100]}")
        
        driver.quit()
        print("Done")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scrape()
