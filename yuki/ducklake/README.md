# DuckLake Project

DuckDB-based data lake with PostgreSQL metastore and Cloudflare R2 integration.

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start PostgreSQL
docker-compose up postgres -d

# Run scripts
docker-compose run --rm -it python-app
docker-compose run --rm -it python-r2-app
```

### Option 2: Local Development

```bash
# Install dependencies
uv add duckdb python-dotenv
# or
pip install duckdb python-dotenv

# Start PostgreSQL (Docker)
docker-compose up postgres -d

# Run scripts
python ducklake_local.py
python ducklake_r2_neon.py
```

## Environment Variables

Create `.env` file:

```bash
# PostgreSQL (local Docker)
HOST=localhost
PORT=5432
USER=ducklake_user
PASSWORD=ducklake_password
DBNAME=ducklake_catalog

# R2 Storage
R2_ACCESS_KEY_ID=your_key
R2_SECRET_ACCESS_KEY=your_secret
R2_ACCOUNT_ID=your_account
R2_BUCKET_NAME=your_bucket
```

## Scripts

- `ducklake_local.py` - Local DuckDB and PostgreSQL testing
- `ducklake_r2_neon.py` - R2 cloud storage and remote PostgreSQL

## Docker Commands

```bash
# Start PostgreSQL
docker-compose up postgres -d

# Run scripts
docker-compose run --rm -it python-app
docker-compose run --rm -it python-r2-app

# Clean up
docker-compose down -v
```

## Troubleshooting

```bash
# Check PostgreSQL
docker-compose logs postgres

# Test connection
pg_isready -h localhost -p 5432

# Clean containers
docker-compose down -v
```
