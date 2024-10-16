import selenium

print("hello WebWatch!!")

try:
    print("Selenium version: ", selenium.__version__)
except NameError:
    print("Selenium is not installed. Check DevContainer setup.")
