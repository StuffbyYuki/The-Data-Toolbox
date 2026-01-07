.PHONY: help sync dlt-ingest sqlmesh-info sqlmesh-migrate sqlmesh-plan sqlmesh-plan-dev sqlmesh-run sqlmesh-run-dev daily-run set-gh-secrets

# Use bash so we can reliably `set -a` and source env files in targets.
SHELL := /usr/bin/env bash

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ENV_FILE ?= $(ROOT)/.env
DEV ?= dev

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
	@echo "  make sqlmesh-info   - Run sqlmesh info"
	@echo "  make sqlmesh-plan   - Run sqlmesh plan (interactive)"
	@echo "  make sqlmesh-plan-dev [DEV=dev_name] - Run sqlmesh plan for a dev env (defaults to dev)"
	@echo "  make sqlmesh-run    - Run sqlmesh run prod"
	@echo "  make sqlmesh-run-dev [DEV=dev_name]  - Run sqlmesh run for a dev env (defaults to dev)"
	@echo "  make daily-run      - dlt ingest + sqlmesh migrate + sqlmesh run prod"
	@echo "  make set-gh-secrets - Push required GitHub Actions secrets from .env (requires gh)"
	@echo ""

sync:
	cd "$(ROOT)" && uv sync

dlt-ingest:
	@$(WITH_ENV) cd "$(ROOT)/dlt" && uv run python rest_api_pipeline.py

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

daily-run: dlt-ingest sqlmesh-migrate sqlmesh-run

set-gh-secrets:
	cd "$(ROOT)" && ENV_FILE="$(ROOT)/.env" ./set_github_actions_secrets_from_env.sh


