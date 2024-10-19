#!/bin/bash

# Set variables for download URL and target directory
URL="https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.58/win64/chrome-win64.zip"
TARGET_DIR="chrome-win64"

# Check if target directory exists, create if not
if [ ! -d "$TARGET_DIR" ]; then
  echo "Creating target directory: $TARGET_DIR"
  mkdir -p "$TARGET_DIR"
fi

# Download the Chrome zip file
echo "Downloading Chrome..."
curl -o "$TARGET_DIR/chrome-win64.zip" "$URL"

# Check if the download was successful
if [ $? -eq 0 ]; then
  echo "Download completed successfully."
else
  echo "Download failed!"
  exit 1
fi

# Extract the downloaded zip file to the target directory
echo "Extracting Chrome to $TARGET_DIR..."
unzip -o "$TARGET_DIR/chrome-win64.zip" -d "$TARGET_DIR"

# Clean up the zip file after extraction
echo "Cleaning up..."
rm "$TARGET_DIR/chrome-win64.zip"

# Confirm completion
echo "Chrome has been downloaded and extracted to $TARGET_DIR"
