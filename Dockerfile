# Build stage
FROM python:3.9-slim AS builder

# Set working directory
WORKDIR /app

# Clone the repository
RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/hrtsv/Ipmi-nVidiaGPU-FanManager.git .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy built app from builder
COPY --from=builder /app /app requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ipmitool \
    && rm -rf /var/lib/apt/lists/*
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8443

# Run the application
CMD ["python", "app.py"]
