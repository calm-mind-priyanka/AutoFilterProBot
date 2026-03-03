# Use slim Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /bot

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . .

# Start the bot
CMD ["python", "main.py"]
