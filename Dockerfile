# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /bot

# Install system dependencies for time sync
RUN apt-get update && apt-get install -y \
    ntpdate \
    && rm -rf /var/lib/apt/lists/*

# Sync container time
RUN ntpdate pool.ntp.org || true

# Copy only requirements first (caching optimization)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot code
COPY . .

# Start the bot
CMD ["python", "main.py"]
