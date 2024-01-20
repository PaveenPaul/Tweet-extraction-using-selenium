import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as Chromeservice
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import csv
import getpass

def extract_data(card):
    username = card.find_element(By.XPATH,'.//span').text
    handle = card.find_element(By.XPATH,'.//span[contains(text(), "@")]').text
    created_date = card.find_element(By.XPATH,'//time').get_attribute('datetime')
    tweet_text_element = card.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
    likes_element = card.find_element(By.XPATH, '//div[@data-testid="like"]').text
    tweet = (username, handle, created_date, tweet_text_element, likes_element)
    return tweet

def start_scraping(hashtag = "#Python"):
    password = getpass.getpass("Enter your password: ")
    driver = webdriver.Chrome(service = Chromeservice(ChromeDriverManager().install()))
    driver.get('https://twitter.com/i/flow/login')
    driver.maximize_window()
    time.sleep(7)
    driver.find_element(By.XPATH,"//input[@name='text']").send_keys('********')#add your Email
    time.sleep(1)
    driver.find_element(By.XPATH,'//div[6]').click()
    time.sleep(5)
    driver.find_element(By.XPATH,"//input[@name='text']").send_keys('*******') #add yourusername
    time.sleep(1)
    driver.find_element(By.XPATH,"//span[contains(text(),'Next')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH,"//input[@name='password']").send_keys(password)#enter password
    time.sleep(1)
    driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]").click()
    time.sleep(12)
    print("seaching for the word")

    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    
    search = driver.find_element(By.XPATH,"//input[@placeholder='Search']")
    search.send_keys(hashtag)
    search.send_keys(Keys.ENTER)
    time.sleep(8)
    driver.find_element(By.LINK_TEXT, 'Latest').click()
    time.sleep(8)
    scrolling = True
    
    while scrolling:
        pages = driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
        for card in pages:
            tweet = extract_data(card)
            if tweet:
                tweet_id = " ".join(tweet)
                if tweet_id not in tweet_ids:
                    data.append(tweet)
                    
        scroll_attempts = 0
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            current_position = driver.execute_script("return window.pageYOffset;")
            if current_position == last_position:
                scroll_attempts += 1
                
                if scroll_attempts >= 3:
                    scrolling = False
                    break
                
                else:
                    time.sleep(3)
            else:
                last_position = current_position
                break
            if len(data) >= 500:
                break
    with open("fscraper.csv", 'w', encoding='utf8') as file:
        headers = ["username","handle","created_date","tweet_text_element","likes_element"]
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(list(set(data)))
        
        
start_scraping("#Python")