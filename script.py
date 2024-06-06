from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace these with your actual Twitter login credentials
USERNAME = ''
PASSWORD = ''

# Initialize the Chrome WebDriver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome()

try:
    # Open Twitter login page
    driver.get('https://twitter.com/login')

    # Wait until the username field is present and input username
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'session[username_or_email]'))
    ).send_keys(USERNAME)

    # Input password
    driver.find_element(By.NAME, 'session[password]').send_keys(PASSWORD)

    # Submit the login form
    driver.find_element(By.NAME, 'session[password]').send_keys(Keys.RETURN)

    # Wait until the home page is loaded by checking for the presence of the "What's happening" section
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//section[@aria-labelledby="accessible-list-0"]'))
    )

    # Get the "What's happening" section
    whats_happening_section = driver.find_element(By.XPATH, '//section[@aria-labelledby="accessible-list-0"]')

    # Get the top 5 items from the "What's happening" section
    top_items = whats_happening_section.find_elements(By.XPATH, './/div[@data-testid="trend"]')[:5]

    for index, item in enumerate(top_items, start=1):
        # Extract and print the text content of each item
        print(f"Item {index}: {item.text}")

finally:
    # Close the WebDriver
    driver.quit()
