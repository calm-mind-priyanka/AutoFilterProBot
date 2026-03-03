# Base image
FROM python:3.11-slim
# Set working dir
WORKDIR /bot

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set environment variables from Koyeb dashboard
ENV PYTHONUNBUFFERED=1

# Run bot
CMD ["python", "main.py"]
