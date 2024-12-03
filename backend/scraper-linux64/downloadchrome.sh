#!/bin/bash

# Change directory
cd scraper-linux64

# Create the chrome directory if it doesn't exist
mkdir -p chrome

# Check and download Chrome
if [ ! -d "chrome/chrome-linux64" ]; then
  echo "Downloading Chrome..."
  wget -q https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.58/linux64/chrome-linux64.zip -O chrome/chrome-linux64.zip
  echo "Unpacking Chrome..."
  unzip -q -o chrome/chrome-linux64.zip -d chrome
  rm chrome/chrome-linux64.zip
else
  echo "Chrome is already downloaded and unpacked."
fi

# Check and download ChromeDriver
if [ ! -f "chrome/chromedriver-linux64/chromedriver" ]; then
  echo "Downloading ChromeDriver..."
  wget -q https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.58/linux64/chromedriver-linux64.zip -O chrome/chromedriver-linux64.zip
  echo "Unpacking ChromeDriver..."
  unzip -q -o chrome/chromedriver-linux64.zip -d chrome
  rm chrome/chromedriver-linux64.zip
else
  echo "ChromeDriver is already downloaded and unpacked."
fi

# Check and download uBlock Origin
if [ ! -d "chrome/uBlock0.chromium" ]; then
  echo "Downloading uBlock Origin..."
  wget -q https://github.com/gorhill/uBlock/releases/download/1.61.2/uBlock0_1.61.2.chromium.zip -O chrome/uBlock.zip
  echo "Unpacking uBlock Origin..."
  unzip -q -o chrome/uBlock.zip -d chrome
  rm chrome/uBlock.zip
else
  echo "uBlock Origin is already downloaded and unpacked."
fi

echo "Chrome, ChromeDriver, and uBlock Origin have been checked, downloaded, and unpacked as needed."
