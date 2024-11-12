#!/bin/bash

cd /workspaces/WebWatch/backend

# Install the dependencies globally
pip install --no-cache-dir -r requirements.txt

# Install packages
apt-get update
# Dependencies for Chrome and Chromedriver
apt-get install -y libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# Download Chrome
cd scraper-linux64 && ./downloadchrome.sh

cd /workspaces/WebWatch/backend

# Run the server
uvicorn server:app --reload --host 0.0.0.0 --port 8000