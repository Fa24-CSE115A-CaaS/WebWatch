FROM python:3.13.0-bookworm

# Copy the requirements file into the image
COPY backend/requirements.txt .

# Install the dependencies globally
RUN pip install --no-cache-dir -r requirements.txt

# Install packages
RUN apt-get update
# Dependencies for Chrome and Chromedriver
RUN apt-get install -y libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
