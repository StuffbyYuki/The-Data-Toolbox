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

# Command to run the application
CMD ["uv", "run", "python", "duckdb_vs_polars_vs_fireducks"]