"""Configuration settings for the benchmark."""

from pathlib import Path

# Base data directory
DATA_DIR = Path("data")

# Main data file path
DATA_FILE_PATH = DATA_DIR / "2021_Yellow_Taxi_Trip_Data.csv"

# Convert to string for compatibility with all libraries
DATA_FILE_PATH_STR = str(DATA_FILE_PATH) 