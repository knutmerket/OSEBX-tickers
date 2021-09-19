"""
Script to fetch (and download) OSEBX tickers

Relies on scraping with selenum, will need to be altered if the page is significantly altered (or moved).
"""

import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("https://live.euronext.com/nb/markets/oslo/equities-by-index/osebx")

# Open the drop-down ("Aktive kolonner")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dt-button"))).click()

# Select the "Ticker" checkbox to display ticker data
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ticker')]"))).click()

rows = driver.find_elements(By.TAG_NAME, "tr")

tickers = []

# Skipping the first row because we it contains the "Ticker" header
for row in rows[1:]:
    ticker = row.find_element(By.CLASS_NAME, "text-right")
    tickers.append(ticker.text)
    
# Need to add a .OL suffix to the tickers for this to work with Yahoo Finance
yf_tickers = [ticker + ".OL" for ticker in tickers]

# Write csv file containing one "column" for tickers and one for YF suffixed tickers
with open("tickers.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(tickers, yf_tickers))
