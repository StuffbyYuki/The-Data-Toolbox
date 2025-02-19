# Change the base image to manylinux_2_24
FROM quay.io/pypa/manylinux_2_34_x86_64

ENV PATH="/opt/python/cp312-cp312/bin:$PATH"

# Install uv
RUN pip install uv

WORKDIR /app

# Copy only the necessary files for dependency installation first
COPY pyproject.toml /app/

# Install dependencies
RUN uv sync

# Copy only the necessary files for dependency installation first
COPY . /app

# Set PYTHONPATH to include current directory
ENV PYTHONPATH=/app

# Build argument with default value
ARG FILE_TYPE=csv

# Set as environment variable so it's available at runtime
ENV FILE_TYPE=${FILE_TYPE}

# Set the command (using shell form for environment variable expansion)
CMD uv run python duckdb_vs_polars_vs_fireducks --file-type $FILE_TYPE