import sys
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from constants.scrape import ALLOWED_ATTRIBUTES
import time
import urllib.parse

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class WebScraper:
    def __init__(
        self, webdriver_path=None, chrome_exe_path=None, ublock_origin_path=None
    ):
        # Determine the base directory of the script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Set default paths if not provided
        if webdriver_path is None:
            webdriver_path = os.path.join(
                base_dir, "scraper-linux64/chrome/chromedriver-linux64/chromedriver"
            )
        if chrome_exe_path is None:
            chrome_exe_path = os.path.join(
                base_dir, "scraper-linux64/chrome/chrome-linux64/chrome"
            )
        if ublock_origin_path is None:
            ublock_origin_path = os.path.join(
                base_dir, "scraper-linux64/chrome/uBlock0.chromium"
            )

        self.webdriver_path = webdriver_path
        self.chrome_exe_path = chrome_exe_path
        self.ublock_origin_path = ublock_origin_path
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
            "Chrome/130.0.6723.58 Safari/537.36"
        )
        options.add_argument(f"user-agent={natural_user_agent}")

        # Add other necessary Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument("--single-process")
        options.add_argument("--disk-cache-size=0")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")

        # Add uBlock Origin extension
        if self.ublock_origin_path:
            options.add_argument(f"--load-extension={self.ublock_origin_path}")
            logging.info("uBlock Origin extension added.")

        # Disable images and videos if specified
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.video": 2,
            "profile.default_content_setting_values.images": 2,
            "profile.default_content_setting_values.video": 2,
        }

        # options.add_experimental_option("prefs", prefs)

        # Initialize WebDriver
        service = Service(self.webdriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def _reinitialize_driver(self):
        if self.driver:
            self.driver.quit()
        self.driver = self._initialize_driver()

    def load_page(self, url, retries=5):
        for attempt in range(retries):
            try:
                self.driver.get(str(url))
                # Wait for the body element to be present
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(0.25)  # Wait for any additional content to load
                logging.info("Page content loaded.")
                return
            except Exception as e:
                logging.error(f"Error loading page on attempt {attempt + 1}: {e}")
                if "disconnected" in str(e):
                    logging.info("Reinitializing driver due to disconnection.")
                    self._reinitialize_driver()
                if attempt < retries - 1:
                    time.sleep(0.2)  # Wait before retrying
                else:
                    raise

    def scrape_all_text(self, url):
        try:
            start_time = time.time()

            # Load the page
            load_start_time = time.time()
            self.load_page(url)
            load_end_time = time.time()
            load_time_log = (
                f"Time to load page: {load_end_time - load_start_time:.5f} seconds\n"
            )

            # Get the page source and parse it with BeautifulSoup
            parse_start_time = time.time()
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            parse_end_time = time.time()
            parse_time_log = (
                f"Time to parse page: {parse_end_time - parse_start_time:.5f} seconds\n"
            )

            # Extract all visible text from the page
            extract_start_time = time.time()
            page_text = soup.get_text(
                separator="\n", strip=True
            )  # Separate text by new lines
            extract_end_time = time.time()
            extract_time_log = f"Time to extract text: {extract_end_time - extract_start_time:.5f} seconds\n"

            end_time = time.time()
            total_time_log = (
                f"Total time for scrape_all_text: {end_time - start_time:.5f} seconds\n"
            )

            # Append log messages to page_text
            log_text = (
                f"\n{load_time_log}{parse_time_log}{extract_time_log}{total_time_log}"
            )

            logging.info(load_time_log.strip())
            logging.info(parse_time_log.strip())
            logging.info(extract_time_log.strip())
            logging.info(total_time_log.strip())

            """ Write timing log
            with open("timing_log.txt", "w", encoding="utf-8") as f:
                f.write(log_text)
            """

            return page_text

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return f"An error occurred: {e}"

    def scrape_by_xpath(self, url, xpath):
        try:
            start_time = time.time()

            # Load the page
            load_start_time = time.time()

            self.load_page(url)

            load_end_time = time.time()
            load_time_log = (
                f"Time to load page: {load_end_time - load_start_time:.5f} seconds\n"
            )

            # Get the page source and parse it with BeautifulSoup
            parse_start_time = time.time()

            el = self.driver.find_element(By.XPATH, xpath)
            html_src = el.get_attribute("outerHTML")
            soup = BeautifulSoup(html_src, "html.parser")

            parse_end_time = time.time()
            parse_time_log = (
                f"Time to parse page: {parse_end_time - parse_start_time:.5f} seconds\n"
            )

            # Extract all visible text from the page
            extract_start_time = time.time()

            for tag in soup.find_all(True):
                tag_attrs = {}
                for attr in ALLOWED_ATTRIBUTES:
                    if attr in tag.attrs:
                        tag_attrs[attr] = tag.attrs[attr]
                tag.attrs = tag_attrs

            extract_end_time = time.time()
            extract_time_log = f"Time to extract text: {extract_end_time - extract_start_time:.5f} seconds\n"
            end_time = time.time()
            total_time_log = (
                f"Total time for scrape_all_text: {end_time - start_time:.5f} seconds\n"
            )

            # Append log messages to page_text
            log_text = (
                f"\n{load_time_log}{parse_time_log}{extract_time_log}{total_time_log}"
            )

            """ Write timing log
            with open("timing_log.txt", "w", encoding="utf-8") as f:
                f.write(log_text)
            """
            return str(soup)

        except Exception as e:
            return f"An error occurred: {e}"

    def scrape_to_file(self, url):
        try:
            page_text = self.scrape_all_text(url)
            print(page_text)

            # Generate filename using website name and timestamp
            website_name = urllib.parse.urlparse(url).netloc.replace(".", "_")
            page_text = self.scrape_all_text(url)
            print(page_text)
            filename = f"scraper-linux64/scrapes/{website_name}-{int(time.time())}.txt"

            if not os.path.exists("scraper-linux64/scrapes"):
                os.makedirs("scraper-linux64/scrapes")

            # Save the extracted text content to a file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(page_text)

            logging.info(f"Saved all visible text content to: {filename}")
        except Exception as e:
            logging.error(f"Failed to scrape to file: {e}")


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
        try:
            scraper.scrape_to_file(url)
        except Exception as e:
            logging.error(f"Task encountered an error while scraping {url}: {e}")
