FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p logs reports models data optimization

# Set environment variables
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# Expose port for API (if needed)
EXPOSE 8000

# Default command
CMD ["python", "-m", "trading_bot"]

# Alternative commands for different use cases:
# Run backtest: docker run -v $(pwd)/data:/app/data reinforcetrade python examples/basic_backtest.py
# Train RL: docker run -v $(pwd)/models:/app/models reinforcetrade python examples/train_rl_agent.py
# Run tests: docker run reinforcetrade python -m pytest tests/
