# Use the official Python image as a base image
FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install geckodriver
ARG TARGETARCH
RUN echo "Architecture: $TARGETARCH" \
    && if [ "$TARGETARCH" = "amd64" ]; then \
    curl -f -LO https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz; \
    tar -xzf geckodriver-v0.35.0-linux64.tar.gz; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
    curl -f -LO https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz; \
    tar -xzf geckodriver-v0.35.0-linux-aarch64.tar.gz; \
    else \
    echo "Unsupported architecture: $TARGETARCH"; exit 1; \
    fi \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-*.tar.gz

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the Docker image
COPY get_my_deck.py .

# Set the entry point to run the Python script
ENTRYPOINT ["python", "get_my_deck.py"]
