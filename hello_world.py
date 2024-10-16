import sys

try: 
    import selenium
except ImportError:
    print("Selenium is not installed. Check DevContainer setup.")
    sys.exit(1)

print("hello WebWatch!!")

print("Selenium version: ", selenium.__version__)
