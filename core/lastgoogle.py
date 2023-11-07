from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver with Chrome
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

chromedriver_path = "C:/webdrivers/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# URL to scrape
url = "https://www.google.com/travel/search?q=google%20reviews%20for%20hotels&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4597339%2C4757164%2C4814050%2C4864715%2C4874190%2C4886480%2C4893075%2C4924070%2C4965990%2C4990494%2C72298667%2C72302247%2C72310433%2C72313836%2C72317059%2C72321071%2C72354856&hl=en-IN&gl=in&cs=1&ssta=1&ts=CAESCAoCCAMKAggDGh4SHBIUCgcI5w8QCRgeEgcI5w8QChgBGAEyBAgAEAAqBwoFOgNJTlI&qs=CAEyJ0Noa0k3c09MbExXUXpmNFhHZzB2Wnk4eE1XUm1NRGh0WjJobkVBRTgKQgkJ7uGCUoM0_RdCCQmz1viQEb16iUIJCSgXFIo34NDF&ap=aAG6AQdyZXZpZXdz&ictx=1&sa=X"
# Open the URL
driver.get(url)

# Scroll down to load more reviews (you may need to adjust the number of scrolls)
scroll_count = 10
for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Wait for the reviews to load
wait = WebDriverWait(driver, 40)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kVathc")))

# Extract page source with loaded reviews
page_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find and extract the reviewer names, review text, and ratings
reviews = soup.find_all('div', class_='Svr5cf bKhjM')
for i, review in enumerate(reviews[:20], start=1):
    date = review.select_one('.iUtr1.CQYfx').text.strip()
    reviewer_name = review.find('a', class_='DHIhE QB2Jof').text.strip()
    rating = review.find('div', class_='GDWaad').text.strip()
    review_text = review.find('div', class_='K7oBsc').text.strip()
    print(f"Review {i}:")
    print(f"Reviewer Name: {reviewer_name}")
    print(f"Rating: {rating}")
    print(f"Review Text: {review_text}")
    print(f"Date: {date}")
    print()

# Close the browser
driver.quit()
