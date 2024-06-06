from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import uuid

app = Flask(__name__)

# MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trending_topics']

# Replace these with your actual Twitter login credentials
USERNAME = 'your_twitter_username'
PASSWORD = 'your_twitter_password'

def fetch_trending_topics():
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    topics = []
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

        for item in top_items:
            topics.append(item.text)

        # Save to MongoDB with a unique ID and timestamp
        document = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now(),
            'topics': topics
        }
        collection.insert_one(document)

    finally:
        # Close the WebDriver
        driver.quit()
    
    return topics

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_topics', methods=['GET'])
def fetch_topics():
    topics = fetch_trending_topics()
    return jsonify(topics)

if __name__ == '__main__':
    app.run(debug=True)
