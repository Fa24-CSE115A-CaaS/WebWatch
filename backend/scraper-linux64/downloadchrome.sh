#!/bin/bash

if [ -d "chrome" ]; then
  echo "The 'chrome' directory already exists; no need to download."
  exit 0
fi

# Create the chrome directory if it doesn't exist
mkdir -p chrome

# Download Chrome
echo "Downloading Chrome..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.58/linux64/chrome-linux64.zip -O chrome/chrome-linux64.zip

# Download ChromeDriver
echo "Downloading ChromeDriver..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.58/linux64/chromedriver-linux64.zip -O chrome/chromedriver-linux64.zip

# Unpack Chrome directly into the chrome directory
echo "Unpacking Chrome..."
unzip -q -o chrome/chrome-linux64.zip -d chrome

# Unpack ChromeDriver directly into the chrome directory
echo "Unpacking ChromeDriver..."
unzip -q -o chrome/chromedriver-linux64.zip -d chrome

# Clean up zip files
echo "Cleaning up..."
rm chrome/chrome-linux64.zip
rm chrome/chromedriver-linux64.zip

echo "Chrome and ChromeDriver have been downloaded and unpacked directly into the 'chrome' directory."
