import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import urllib.parse

# Configure paths
webdriver_path = 'chromedriver.exe'  # Path to your chromedriver.exe
chrome_exe_path = r'chrome-win64.old\\chrome.exe'  # Path to your chrome.exe

# Initialize ChromeOptions
options = webdriver.ChromeOptions()
options.binary_location = chrome_exe_path  # Set the path to chrome.exe

# Use a natural Chrome user-agent string
natural_user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/116.0.5845.110 Safari/537.36"
)
options.add_argument(f"user-agent={natural_user_agent}")

# Add other necessary Chrome options
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--disable-usb")

# Optional: Run in headless mode (can remove for debugging)
# options.add_argument("--headless")

# Function to load dynamic content
def load_page(url):
    driver.get(url)
    time.sleep(3)  # Initial wait for the page to load

    # Wait until the <body> tag is present (ensure the page content is fully loaded)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Page content loaded.")
    except Exception as e:
        print(f"Error loading page: {e}")

# Function to scrape and save all visible text using BeautifulSoup
def scrape_all_text(url):
    try:
        # Load the page
        load_page(url)

        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract all visible text from the page
        page_text = soup.get_text(separator='\n', strip=True)  # Separate text by new lines

        # Generate filename using website name and timestamp
        website_name = urllib.parse.urlparse(url).netloc.replace('.', '_')
        timestamp = int(time.time())
        filename = f"{website_name}-{timestamp}.txt"

        # Save the extracted text content to a file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_text)

        print(f"Saved all visible text content to: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

# Main function to handle URL input or argument
if __name__ == "__main__":
    # Check if a URL is provided as an argument
    # Example: python scrape.py https://simonzhao.com
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # If no URL is provided, prompt the user to enter a URL
        url = input("Please enter the URL: ")

    # Call the scrape function with the provided or entered URL
    # Initialize WebDriver
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    scrape_all_text(url)
