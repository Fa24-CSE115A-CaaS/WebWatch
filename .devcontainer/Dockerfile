FROM python:3.13.0-bookworm

# List the files to verify requirements.txt is present
RUN pwd && ls -la

# Copy the requirements file into the image
COPY requirements.txt .

# Install the dependencies globally
RUN pip install --no-cache-dir -r requirements.txt