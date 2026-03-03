# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /bot

# Copy bot code first (so pip cache works better)
COPY . .

# Install system dependencies (using ntpsec replacement)
RUN apt-get update && apt-get install -y \
    ntpsec-ntpdate \
    && rm -rf /var/lib/apt/lists/*

# Sync time with NTP server (optional, just in case)
RUN ntpdate pool.ntp.org || true

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python", "main.py"]
