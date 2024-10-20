import time
import difflib
from scrape import WebScraper


    # CLI Setup
    # Check # of arguments and if a URL is provided as an argument
    # Example: python3 main.py https://simonzhao.com

def compare_texts(text1, text2):
    diff = difflib.unified_diff(
        text1.splitlines(), 
        text2.splitlines(), 
        lineterm='', 
        fromfile='first_scrape', 
        tofile='second_scrape'
    )
    return '\n'.join(diff)

if __name__ == "__main__":

    # TODO: Define CLI (use argparse library)

    DELAY = 2 # in seconds

    with WebScraper() as scraper:
        while True:
            first = scraper.scrape_all_text("https://simonzhao.com")
            print(f"First scrape completed. Waiting {DELAY} seconds before second scrape...")
            # TODO: Look into more advanced time scheduling techniques (instead of sleep)

            time.sleep(DELAY)

            #second = scraper.scrape_all_text("https://example.com")
            second = scraper.scrape_all_text("https://simonzhao.com")
            print("Second scrape completed.")

            if first is None or second is None:
                print("An error occurred during scraping.")
            elif first == second:
                print("No change detected.")
            else:
                print("Change detected.")
                diff = compare_texts(first, second)
                print("Differences:")
                print(diff)
                break