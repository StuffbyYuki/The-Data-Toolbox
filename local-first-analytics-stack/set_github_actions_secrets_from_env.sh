#!/usr/bin/env bash
set -euo pipefail

# Sets the GitHub Actions secrets required by:
# - `local-first-analytics-stack/sqlmesh/config.yaml` (SQLMesh)
# - `local-first-analytics-stack/dlt/rest_api_pipeline.py` (dlt)
#
# Requirements:
# - GitHub CLI installed: https://cli.github.com/
# - Authenticated: `gh auth login`
# - Secrets are sourced from your current shell environment (recommended) OR an env file.
#
# Usage:
#   ./set_github_actions_secrets_from_env.sh [OWNER/REPO]
#
# Optional:
#   ENV_FILE=local-first-analytics-stack/.env ./scripts/set_github_actions_secrets_from_env.sh OWNER/REPO
#
# Notes:
# - This script NEVER prints secret values.
# - It will fail if a required variable is missing.

REPO="${1:-}"
if [[ -z "${REPO}" ]]; then
  # Default to the current git repo's `origin` remote.
  # Supports:
  # - git@github.com:OWNER/REPO.git
  # - https://github.com/OWNER/REPO.git
  if git_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    origin_url="$(git -C "${git_root}" remote get-url origin 2>/dev/null || true)"
    if [[ -n "${origin_url}" ]]; then
      # Strip scheme/host prefixes and optional .git suffix
      origin_url="${origin_url%.git}"
      origin_url="${origin_url#git@github.com:}"
      origin_url="${origin_url#https://github.com/}"
      origin_url="${origin_url#http://github.com/}"
      REPO="${origin_url}"
    fi
  fi
fi

if [[ -z "${REPO}" ]]; then
  echo "Usage: $0 [OWNER/REPO]"
  echo "Tip: run this inside a git repo with an 'origin' remote set, or pass OWNER/REPO explicitly."
  exit 1
fi

ENV_FILE="${ENV_FILE:-}"
if [[ -n "${ENV_FILE}" ]]; then
  # Load KEY=VALUE lines (skips comments/blank lines).
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

require() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required env var: ${name}"
    exit 1
  fi
}

# Required by `local-first-analytics-stack/sqlmesh/config.yaml`
SQLMESH_VARS=(
  POSTGRES_HOST
  POSTGRES_PORT
  POSTGRES_DB
  POSTGRES_USER
  POSTGRES_PASSWORD
  # Optional but recommended for other tools (like dlt) that prefer a DSN.
  # If present, we will also set it as a GitHub secret.
  # POSTGRES_CONNECTION_STRING
  DUCKLAKE_DATA_PATH
  DUCKLAKE_NAME
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_REGION
  R2_S3_ENDPOINT
)

for v in "${SQLMESH_VARS[@]}"; do
  require "${v}"
done

OPTIONAL_VARS=(
  # Convenience DSN (often copied from Neon directly)
  POSTGRES_CONNECTION_STRING

  # dlt: REST API auth (NYC Open Data app token). If empty, Socrata will still work but may be rate-limited.
  SOURCES__REST_API__NYC_OPEN_DATA_APP_TOKEN

  # dlt DuckLake destination (dlthub) - include if you want to configure dlt purely via env vars in CI.
  DESTINATION__DUCKLAKE__CREDENTIALS__CATALOG
  DESTINATION__DUCKLAKE__CREDENTIALS__STORAGE__BUCKET_URL
  DESTINATION__DUCKLAKE__CREDENTIALS__ENDPOINT_URL
  DESTINATION__DUCKLAKE__CREDENTIALS__AWS_ACCESS_KEY_ID
  DESTINATION__DUCKLAKE__CREDENTIALS__AWS_SECRET_ACCESS_KEY
  DESTINATION__DUCKLAKE__CREDENTIALS__REGION_NAME
  DESTINATION__DUCKLAKE__CREDENTIALS__DUCKLAKE_NAME
)

echo "Setting ${#SQLMESH_VARS[@]} required SQLMesh secrets on ${REPO}..."

for v in "${SQLMESH_VARS[@]}"; do
  # Use stdin to avoid leaking values in process lists.
  printf "%s" "${!v}" | gh secret set "${v}" --repo "${REPO}" --app actions
done

echo "Setting optional secrets if present in your environment..."
for v in "${OPTIONAL_VARS[@]}"; do
  if [[ -n "${!v:-}" ]]; then
    printf "%s" "${!v}" | gh secret set "${v}" --repo "${REPO}" --app actions
  fi
done

echo "Done."


