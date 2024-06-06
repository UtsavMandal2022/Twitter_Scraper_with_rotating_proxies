from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import datetime

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time according to your desired format string
formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Example format string

# Print the formatted date and time
print(formatted_datetime)
def random_proxy():
    with open('valid_proxies.txt') as f:
        proxies = f.readlines()
        return random.choice(proxies)
    
# print(random_proxy())

def main():
    chrome_options = webdriver.ChromeOptions()
    proxy=random_proxy()
    print(proxy)
    print(chrome_options.arguments)
    proxy='us-ca.proxymesh.com:31280'
    chrome_options.add_argument(f'--proxy-server={proxy}')
    url='https://x.com/home'
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    time.sleep(200)
    browser.quit()

main()