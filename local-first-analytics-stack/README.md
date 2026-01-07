## local-first-analytics-stack

A local-first analytics template:

- **Ingest**: `dlt` loads NYC Open Data Motor Vehicle Collisions into DuckLake (Postgres catalog + object storage).
- **Transform**: `SQLMesh` builds models on top of the ingested tables.
- **Automate**: GitHub Actions runs a daily pipeline + a PR CI/CD bot.

### Prerequisites

- **Python 3.12+**
- **uv** (Python package manager)
- A `.env` file at `local-first-analytics-stack/.env` containing the required variables (see below)

Optional:
- **GitHub CLI (`gh`)** if you want to upload secrets to GitHub Actions from your local `.env`.
- **Dev Container** support (VS Code/Cursor + Docker) for a fully reproducible environment.

### 1) Setup

From the repo root:

```bash
cd local-first-analytics-stack
make sync
```

### 2) Configure environment variables

Create `local-first-analytics-stack/.env` with:

- **Postgres (DuckLake catalog + SQLMesh state)**
  - `POSTGRES_HOST`
  - `POSTGRES_PORT`
  - `POSTGRES_DB`
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`
  - (optional but recommended) `POSTGRES_CONNECTION_STRING`

- **Object storage (R2 via S3-compatible API)**
  - `DUCKLAKE_DATA_PATH` (example: `s3://data-toolbox/local-first-analytics-stack/`)
  - `DUCKLAKE_NAME` (the Postgres schema name used for DuckLake metadata)
  - `R2_S3_ENDPOINT` (host only, no scheme; example: `<account>.r2.cloudflarestorage.com`)

- **S3-compatible credentials**
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION` (often `auto`)

- **dlt (optional)**
  - `SOURCES__REST_API__NYC_OPEN_DATA_APP_TOKEN`

### 3) Run ingestion (dlt)
From the local-first-analytics-stack directory:
```bash
make dlt-ingest
# or 
cd dlt
uv run python rest_api_pipeline.py
```

This runs `dlt/rest_api_pipeline.py` and loads data into dataset `nyc_open_data` (table name is `motor_vehicle_collisions`).

### 4) Run SQLMesh
From the local-first-analytics-stack directory:

Sanity check connections:

```bash
make sqlmesh-info
# or
cd sqlmesh
uv run sqlmesh info
```

Apply model changes:

```bash
make sqlmesh-plan
# or
cd sqlmesh
uv run sqlmesh plan
```

Run models:

```bash
make sqlmesh-run
# or
cd sqlmesh
uv run sqlmesh run
```

### 5) GitHub Actions secrets (optional helper)

If you want the CI workflows to run without copying secrets manually, you can push the required secrets from your local `.env` using:

```bash
# From the local-first-analytics-stack directory
make set-gh-secrets
```

### 6) Dev Container (optional)

Open `local-first-analytics-stack/` in VS Code/Cursor and select **“Reopen in Container”**.
The container will install `uv` and run `uv sync` automatically.

### 7) GitHub workflows included

- **Daily pipeline**: `.github/workflows/daily_pipeline.yaml` runs nightly at **00:00 UTC**:
  - dlt ingestion → sqlmesh migrate → sqlmesh run prod
- **SQLMesh CI/CD bot**: `.github/workflows/sqlmesh_cicd.yaml` runs on PRs that touch `local-first-analytics-stack/sqlmesh/**`.


