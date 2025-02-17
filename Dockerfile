FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update -y && \
    apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy only the necessary files for dependency installation first
COPY . /app

# Install dependencies
RUN uv sync

# Set PYTHONPATH to include current directory
ENV PYTHONPATH=/app

# Command to run the application
CMD ["uv", "run", "python", "duckdb_vs_polars_vs_fireducks", "&&", "open", "output.png"]