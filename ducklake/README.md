# DuckLake Project

DuckDB-based data lake with multiple metastore options and Cloudflare R2 integration.

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start PostgreSQL (optional - only needed for local PostgreSQL testing)
docker-compose up postgres -d

# Run scripts
docker-compose run --rm -it python-duckdb-local-app    # DuckDB metastore
docker-compose run --rm -it python-postgres-local-app  # PostgreSQL metastore
docker-compose run --rm -it python-r2-neon-app        # R2 cloud storage
```

### Option 2: Local Development

```bash
# Install dependencies
uv add duckdb python-dotenv
# or
pip install duckdb python-dotenv

# Start PostgreSQL (Docker) - only needed for local PostgreSQL testing
docker-compose up postgres -d

# Run scripts
python ducklake_duckdb_local.py    # DuckDB metastore
python ducklake_postgres_local.py  # PostgreSQL metastore
python ducklake_r2_neon.py         # R2 cloud storage
```

## Environment Variables

Create `.env` file:

```bash
# Neon PostgreSQL (remote) - doesn't have to be neon
HOST=your_neon_host
PORT=5432
USER=ducklake_user
PASSWORD=your_neon_password
DBNAME=ducklake_catalog

# R2 Storage (for ducklake_r2_neon.py) - use whatever remote file storage
R2_ACCESS_KEY_ID=your_key
R2_SECRET_ACCESS_KEY=your_secret
R2_ACCOUNT_ID=your_account
R2_BUCKET_NAME=your_bucket

# Local postgres' creds already defined
LOCAL_HOST=postgres
LOCAL_PORT=5432
LOCAL_USER=ducklake_user
LOCAL_PASSWORD=ducklake_password
LOCAL_DBNAME=ducklake_catalog
```

## Scripts

- `ducklake_duckdb_local.py` - Local DuckDB metastore (no external dependencies)
- `ducklake_postgres_local.py` - Local PostgreSQL metastore with local data storage
- `ducklake_r2_neon.py` - Neon PostgreSQL metastore with Cloudflare R2 cloud storage

## Docker Commands

```bash
# Start PostgreSQL (optional - only needed for local PostgreSQL testing)
docker-compose up postgres -d

# Run individual scripts
docker-compose run --rm -it python-duckdb-local-app
docker-compose run --rm -it python-postgres-local-app
docker-compose run --rm -it python-r2-neon-app

# Clean up
docker-compose down -v
```

## Troubleshooting

```bash
# Check PostgreSQL (if using local)
docker-compose logs postgres

# Test connection
pg_isready -h localhost -p 5432

# Clean containers
docker-compose down -v
```
