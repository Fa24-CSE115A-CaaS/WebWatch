import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import urllib.parse

# TODO: Use logging instead of print statements for better debugging

class WebScraper:
    def __init__(self, webdriver_path=None, chrome_exe_path=None):
        # Determine the base directory of the script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Set default paths if not provided
        if webdriver_path is None:
            webdriver_path = os.path.join(base_dir, "scraper_linux64/chrome/chromedriver-linux64/chromedriver")
        if chrome_exe_path is None:
            chrome_exe_path = os.path.join(base_dir, "scraper_linux64/chrome/chrome-linux64/chrome")

        self.webdriver_path = webdriver_path
        self.chrome_exe_path = chrome_exe_path
        self.driver = None

    def __enter__(self):
        self.driver = self._initialize_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def _initialize_driver(self):
        # Initialize ChromeOptions
        options = webdriver.ChromeOptions()
        options.binary_location = self.chrome_exe_path  # Set the path to chrome.exe

        # Use a natural Chrome user-agent string
        natural_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/116.0.5845.110 Safari/537.36"
        )
        options.add_argument(f"user-agent={natural_user_agent}")

        # Add other necessary Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-features=NetworkService")
        options.add_argument("--disable-usb")

        # Optional: Run in headless mode (can remove for debugging)
        # options.add_argument("--headless")

        # Initialize WebDriver
        service = Service(self.webdriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def load_page(self, url):
        self.driver.get(url)
        time.sleep(3)  # Initial wait for the page to load

        # Wait until the <body> tag is present (ensure the page content is fully loaded)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page content loaded.")
        except Exception as e:
            print(f"Error loading page: {e}")

    def scrape_all_text(self, url):
        try:
            # Load the page
            self.load_page(url)

            # Get the page source and parse it with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract all visible text from the page
            page_text = soup.get_text(separator='\n', strip=True)  # Separate text by new lines
            return page_text

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def scrape_to_file(self, url):
        page_text = self.scrape_all_text(url)

        # Generate filename using website name and timestamp
        website_name = urllib.parse.urlparse(url).netloc.replace('.', '_')
        timestamp = int(time.time())
        filename = f"scraper_linux64/scrapes/{website_name}-{timestamp}.txt"

        if not os.path.exists("scraper_linux64/scrapes"):
            os.makedirs("scraper_linux64/scrapes")

        # Save the extracted text content to a file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_text)

        print(f"Saved all visible text content to: {filename}")

# Main function to handle URL input or argument
if __name__ == "__main__":
    # Check if a URL is provided as an argument
    # Example: python scrape.py https://simonzhao.com
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # If no URL is provided, prompt the user to enter a URL
        url = input("Please enter the URL: ")

    with WebScraper() as scraper:
        scraper.scrape_to_file(url)