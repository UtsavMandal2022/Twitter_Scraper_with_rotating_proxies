from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient
from datetime import datetime
import uuid
import random
import os
from dotenv import load_dotenv

load_dotenv()

# # MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trending_topics']

def random_proxy():
    with open('valid_proxies.txt') as f:
        proxies = f.readlines()
        return random.choice(proxies)
    

def fetch_trending_topics():
        # Set up the Chrome WebDriver
    service = Service('chromedriver')  # Adjust the path to your chromedriver
    #use proxymesh for rotating proxies
    proxy = random_proxy()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(service=service
                            #   , options=chrome_options
                              )
    
    
    # Twitter credentials
    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')
    
    # print(username, password)
    # Navigate to the Twitter login page
    driver.get('https://twitter.com/login')
    
    # Wait for the username input to be present and enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    )
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    
    # Wait for the password input to be present and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for login to complete and the home page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Home timeline"]'))
    )
    
    # Navigate to the Explore page
    driver.get('https://x.com/explore/tabs/for-you')
    
    # Wait until the parent div is present
    time.sleep(5)
    parent_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Explore"]'))
    )
    
    # Find all span elements within the parent div
    span_elements = parent_div.find_elements(By.TAG_NAME, 'span')
    
    # Filter spans based on font size
    filtered_spans = []
    for span in span_elements:
        font_size = span.value_of_css_property('font-size')
        if font_size == '15px':
            filtered_spans.append(span.text.strip())
    
    filtered_spans = list(set(filtered_spans))
    # only keep the text starting with a hashtag
    filtered_spans = [text for text in filtered_spans if text.startswith('#')]
    print(filtered_spans)
    if len(filtered_spans) >= 5:
        top_5_texts = filtered_spans[:5]
    else: 
        top_5_texts = filtered_spans
    
    # Print the top 5 texts
    for text in top_5_texts:
        print(text)
    
    # Close the browser
    driver.quit()
    
    now = datetime.now()
    
    # Format the date and time according to your desired format string
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S") 
    
    document = {
                'id': str(uuid.uuid4()),
                'timestamp': formatted_datetime,
                'topics': top_5_texts
            }
    
    # print(document)
    collection.insert_one(document)
    # select proxy upto the :
    proxy = proxy.split(':')[0]
    return {'timestamp': document['timestamp'], 'topics': document['topics'], 'proxy':proxy.split(':')[0]}
    
def dummy():
    time.sleep(3)
    document1= {'id': '02a06115-b61e-42ff-b6a9-2dc3b15d8c51', 'timestamp': '2024-06-12 16:31:44', 'topics': ['#Bhubaneswar', '#IndianArmy', '#GitHubConstellation', '#Italy', '#FireAccident']}
    document1['proxy'] = random_proxy()
    proxy=document1['proxy']
    document1['proxy']=proxy.split(':')[0]
    return document1

# if __name__ == '__main__':
#     print(fetch_trending_topics())
#     print(dummy())