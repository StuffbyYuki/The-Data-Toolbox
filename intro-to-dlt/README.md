# Intro to dlt

This project demonstrates how to use the Data Load Tool (DLT) library to create a simple yet powerful data pipeline that extracts motor vehicle collision data from the NYC Open Data API.

## Project Description

This pipeline:
- Connects to the NYC Open Data API
- Extracts motor vehicle collision data
- Implements pagination to handle large datasets
- Writes the data to the S3/local filesystem in Parquet format

## Requirements

- Python 3.8+
- Required packages (see `requirements.txt`)

## Setup Instructions

1. Clone this repository
   ```
   git clone <repository-url>
   cd intro-to-dlt
   ```

2. Choose one of the following setup methods:

   ### Option A: Using Dev Container (Recommended)
   
   This project includes a dev container configuration for a consistent development environment.
   
   **Prerequisites:**
   - [VS Code](https://code.visualstudio.com/)
   - [Docker](https://www.docker.com/products/docker-desktop)
   - [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   
   **Steps:**
   1. Open this project in VS Code
   2. When prompted, click "Reopen in Container" (or press F1 and select "Remote-Containers: Reopen in Container")
   3. The container will build and configure the development environment automatically
   4. Create a `.env` file with your environment variables: `cp .env.example .env`
   
   ### Option B: Manual Setup
   
   Create and activate a virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies

   Using pip:
   ```
   pip install -r requirements.txt
   ```

   Using uv (faster alternative):
   ```
   pip install uv  # Install uv first if you don't have it
   uv pip install -r requirements.txt
   
   # Or if you already have uv.lock file
   uv sync
   ```

4. Create a `.env` file with any necessary environment variables
   ```
   cp env.example .env
   ```

## Running the Pipeline

To run the data pipeline, simply execute:
```
python rest_api_pipeline.py  # or uv run python rest_api_pipeline.py with uv
```

The extracted data will be stored in the `.dlt` directory in Parquet format.

## Project Structure

```
intro-to-dlt/
├── .devcontainer/          # Development container configuration
│   ├── devcontainer.json   # VS Code devcontainer settings
│   └── Dockerfile          # Container definition
├── .dlt/                   # DLT configuration directory
│   ├── config.toml         # DLT configuration settings
│   └── secrets.toml        # Secure storage for credentials
├── .env                    # Environment variables file
├── .env.example            # Example environment variables file
├── .gitignore              # Git ignore patterns
├── .python-version         # Python version specification for pyenv
├── pyproject.toml          # Python project configuration
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── rest_api_pipeline.py    # Main pipeline code for NYC Open Data
└── uv.lock                 # Lock file for uv package manager
```

## Customizing the Pipeline

To extract different datasets from NYC Open Data:
1. Find the dataset ID on the [NYC Open Data portal](https://data.cityofnewyork.us/)
2. Replace the dataset ID in the `client.paginate()` method in `rest_api_pipeline.py`
3. Adjust pagination settings as needed for your specific dataset

## Advanced Usage

- Modify the `dlt.pipeline()` configuration to use different destinations (e.g., database, cloud storage)
- Add transformations to the pipeline using DLT's transformation capabilities
- Implement incremental loading by modifying the resource configuration
