import time
import difflib
import asyncio
from utils.notifications import send_mail
from scrape import WebScraper


def compare_texts(text1, text2):
    diff = difflib.unified_diff(
        text1.splitlines(),
        text2.splitlines(),
        lineterm="",
        fromfile="first_scrape",
        tofile="second_scrape",
    )
    return "\n".join(diff)


# TODO: Define CLI (use argparse library)
# Check # of arguments and if a URL is provided as an argument
# Example: python3 main.py https://simonzhao.com


DELAY = 2  # in seconds

EMAIL_TO = "ccandau@ucsc.edu"
URL = "https://simonzhao.com"


async def main():
    with WebScraper() as scraper:
        while True:
            first = scraper.scrape_all_text(
                "https://simonzhao.com"
            )  # CHANGE TO URL VARIABLE
            print(
                f"First scrape completed. Waiting {DELAY} seconds before second scrape..."
            )

            await asyncio.sleep(DELAY)

            second = scraper.scrape_all_text(
                "https://example.com"
            )  # CHANGE TO URL VARIABLE
            print("Second scrape completed.")

            if first is None or second is None:
                print("An error occurred during scraping.")
            elif first == second:
                print("No change detected.")
            else:

                print("Change detected. Sending email notification.")
                diff = compare_texts(first, second)
                subject = "WebWatch Change Report"
                send_mail(
                    subject,
                    f"Changes have been detected on {URL}.\n\n {diff}",
                    [f"{EMAIL_TO}"],
                )
                break


if __name__ == "__main__":
    asyncio.run(main())
