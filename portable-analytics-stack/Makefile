.PHONY: help sync dlt-ingest dlt-pipeline-info sqlmesh-info sqlmesh-migrate sqlmesh-plan sqlmesh-plan-dev sqlmesh-run sqlmesh-run-dev sqlmesh-fetchdf sqlmesh-ui daily-run set-gh-secrets

# Use bash so we can reliably `set -a` and source env files in targets.
SHELL := /usr/bin/env bash

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ENV_FILE ?= $(ROOT)/.env
DEV ?= dev
QUERY ?=

# Load $(ENV_FILE) into the process environment for a single command.
# (Similar to python-dotenv / `dotenv run -- ...`, but implemented as a shell snippet.)
define WITH_ENV
set -a; [[ -f "$(ENV_FILE)" ]] && . "$(ENV_FILE)"; set +a;
endef

help:
	@echo ""
	@echo "portable-analytics-stack"
	@echo ""
	@echo "Targets:"
	@echo "  make sync           - Install/sync Python deps with uv"
	@echo "  make dlt-ingest     - Run dlt ingestion (NYC Open Data -> DuckLake)"
	@echo "  make dlt-pipeline-info       - Show dlt pipeline info (nyc_open_data_pipeline)"
	@echo "  make sqlmesh-info   - Run sqlmesh info"
	@echo "  make sqlmesh-plan   - Run sqlmesh plan (interactive)"
	@echo "  make sqlmesh-plan-dev [DEV=dev_name] - Run sqlmesh plan for a dev env (defaults to dev)"
	@echo "  make sqlmesh-run    - Run sqlmesh run prod"
	@echo "  make sqlmesh-run-dev [DEV=dev_name]  - Run sqlmesh run for a dev env (defaults to dev)"
	@echo "  make sqlmesh-fetchdf QUERY='select * from ...' - Run sqlmesh fetchdf with a SQL query"
	@echo "  make sqlmesh-ui     - Run sqlmesh UI"
	@echo "  make daily-run      - dlt ingest + sqlmesh migrate + sqlmesh run prod"
	@echo "  make set-gh-secrets - Push required GitHub Actions secrets from .env (requires gh)"
	@echo ""

sync:
	cd "$(ROOT)" && uv sync

dlt-ingest:
	@$(WITH_ENV) cd "$(ROOT)/dlt" && uv run python rest_api_pipeline.py

dlt-pipeline-info:
	@$(WITH_ENV) cd "$(ROOT)/dlt" && uv run dlt pipeline nyc_open_data_pipeline info

sqlmesh-info:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh info

sqlmesh-migrate:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh migrate

sqlmesh-plan:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh plan

sqlmesh-plan-dev:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh plan "$(DEV)"

sqlmesh-run:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh run prod

sqlmesh-run-dev:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh run "$(DEV)"

sqlmesh-fetchdf:
	@if [[ -z "$(strip $(QUERY))" ]]; then \
		echo "ERROR: QUERY is required"; \
		echo "Usage: make sqlmesh-fetchdf QUERY='select * from ...'"; \
		exit 2; \
	fi
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh fetchdf "$(QUERY)"

sqlmesh-ui:
	@$(WITH_ENV) cd "$(ROOT)/sqlmesh" && uv run sqlmesh ui

daily-run: dlt-ingest sqlmesh-migrate sqlmesh-run

set-gh-secrets:
	cd "$(ROOT)" && ENV_FILE="$(ROOT)/.env" ./set_github_actions_secrets_from_env.sh


