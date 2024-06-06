import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Configuration
PROXYMESH_API_URL = 'http://utsav_og:utsav_og@torn@us-west.proxy.proxymesh.com:31280'
TWITTER_URL = 'https://twitter.com/'

def get_new_proxy():
    # Fetch a new proxy from ProxyMesh
    response = requests.get(PROXYMESH_API_URL)
    if response.status_code == 200:
        proxy_address = response.text.strip()
        return proxy_address
    else:
        raise Exception("Failed to fetch proxy from ProxyMesh")

def setup_driver(proxy_address):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless for faster execution
    chrome_options.add_argument('--disable-gpu')
    
    # Set up the proxy
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_address
    proxy.ssl_proxy = proxy_address
    
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    proxy.add_to_capabilities(capabilities)
    
    driver = webdriver.Chrome(desired_capabilities=capabilities, options=chrome_options)
    return driver

def fetch_trending_topics(driver):
    driver.get(TWITTER_URL)
    time.sleep(5)  # Wait for the page to load
    
    trending_topics = []
    
    try:
        # Adjust the XPATH to match the "What's Happening" section
        elements = driver.find_elements(By.XPATH, "//section[@aria-labelledby='accessible-list-0']//div[@dir='ltr']")
        for i, element in enumerate(elements):
            if i >= 5:
                break
            trending_topics.append(element.text)
    except Exception as e:
        print(f"Error fetching trending topics: {e}")
    
    return trending_topics

def main():
    proxy_address = get_new_proxy()
    driver = setup_driver(proxy_address)
    
    try:
        trending_topics = fetch_trending_topics(driver)
        print("Top 5 Trending Topics on Twitter:")
        for idx, topic in enumerate(trending_topics):
            print(f"{idx + 1}. {topic}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
