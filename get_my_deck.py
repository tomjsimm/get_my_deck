import os
import requests
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

browser_options = Options()
browser_options.add_argument("--headless")
url = "https://store.steampowered.com/sale/steamdeckrefurbished"

def log(message):
    print(f"{datetime.now()}: {message}")

def start():
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=browser_options)
    driver.get(url)
    return driver

def refresh(driver):
    driver.get(url)

def quit(driver):
    driver.quit()

def send_signal_message(deck, signal_api_url, signal_number, send_to_number):
    log("Sending Signal message reminder...")
    message = f"{deck} in Stock https://store.steampowered.com/sale/steamdeckrefurbished"
    payload = {
        "message": message,
        "number": signal_number,
        "recipients": [send_to_number]
    }
    response = requests.post(f"{signal_api_url}/v2/send", json=payload)
    log(f"Signal API response: {response.status_code} - {response.text}")
    if response.status_code in [200, 201]:
        log("Signal message sent successfully.")
    else:
        log(f"Failed to send Signal message: {response.text}")

def check_deck_status(deck, signal_api_url, signal_number, send_to_number):
    deck = deck.strip()
    deckname = deck.split(" - ")[0]
    if "add" in deck.lower():
        log(f"{deckname} - In Stock")
        send_signal_message(deckname, signal_api_url, signal_number, send_to_number)
        status = 1
    else:
        log(f"{deckname} - Out of Stock")
        status = 0
    return status

def runner(driver, signal_api_url, signal_number, send_to_number):
    all_btn = driver.find_elements(By.XPATH, "//*[@id='SaleSection_33131']")
    if not all_btn:
        log("No elements found with the given XPath.")
        return 0, 0
    x = all_btn[0].text
    decks = x.split("\n")
    status_512gb = 0
    status_1tb = 0
    for i in range(0, len(decks), 3):
        deck = decks[i]
        if "512 GB OLED" in deck:
            status_512gb = check_deck_status(deck, signal_api_url, signal_number, send_to_number)
        elif "1TB OLED" in deck:
            status_1tb = check_deck_status(deck, signal_api_url, signal_number, send_to_number)
    return status_512gb, status_1tb

def get_my_deck(signal_api_url, signal_number, send_to_number, test_message, refresh_time):
    if test_message:
        send_signal_message("Test Deck", signal_api_url, signal_number, send_to_number)
        log("Test message sent. Exiting...")
        return

    start_time = 10
    driver = start()
    time.sleep(start_time)  # Wait for the page to load
    log("Started Scraper")
    while True:
        try:
            sd512, sd1024 = runner(driver, signal_api_url, signal_number, send_to_number)
            if sd512 or sd1024:
                log("Deck is in stock! Exiting...")
                quit(driver)
                break
            refresh(driver)
            log(f"Reloading page in {refresh_time} seconds...")
            time.sleep(refresh_time)  # Refresh the page once per minute
        except Exception as e:
            log(f"Exception occurred: {e}")
            quit(driver)
            driver = start()

if __name__ == "__main__":
    signal_api_url = os.getenv('SIGNAL_API_URL')
    signal_number = os.getenv('SIGNAL_NUMBER')
    send_to_number = os.getenv('SEND_TO_NUMBER')
    test_message = os.getenv('TEST_MESSAGE', 'false').lower() == 'true'
    refresh_time = int(os.getenv('REFRESH_TIME', 3600))

    get_my_deck(signal_api_url, signal_number, send_to_number, test_message, refresh_time)
