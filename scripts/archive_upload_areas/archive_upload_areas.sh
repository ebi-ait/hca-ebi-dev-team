#!/usr/bin/env bash

set -euo pipefail

# Load environment variables
source .env

: "${INGEST_URL:?Missing INGEST_URL in .env}"
: "${INGEST_TOKEN:?Missing INGEST_TOKEN in .env}"
: "${CUTOFF_DATE:?Missing CUTOFF_DATE in .env, format: %Y-%m-%d, e.g. 2025-02-14}"

# Configuration
PROJECT_PAGE_SIZE=600
AUTH_HEADER="Authorization: Bearer ${INGEST_TOKEN}"
TARGET_STORAGE_CLASS=GLACIER
WRANGLING_STATE=PUBLISHED_IN_DCP
#CUTOFF_AGE_MONTHS=3m
CUTOFF_TIMESTAMP=${CUTOFF_DATE}T00:00:00Z

log() {
  local level="$1"
  shift

  # Color palette
  local reset="\033[0m"
  local dim="\033[2m"
  local level_info="\033[1;34m"
  local level_warn="\033[1;33m"
  local level_error="\033[1;31m"
  local func_color="\033[1;36m"
  local message_color="\033[0m"

  # Set level color
  local level_color
  case "$level" in
    INFO) level_color=$level_info ;;
    WARN) level_color=$level_warn ;;
    ERROR) level_color=$level_error ;;
    *) level_color=$reset ;;
  esac

  # Get caller function name
  local caller="${FUNCNAME[1]:-main}"

  # Print formatted log
  echo -e "${dim}[$(date +'%Y-%m-%d %H:%M:%S')]${reset} ${level_color}[$level]${reset} ${func_color}[$caller]${reset} ${message_color}$*${reset}" >&2
}

# Functions
fetch_projects() {
  log INFO "Fetching projects with ${WRANGLING_STATE}..."
  curl --silent \
    --location --max-time 10 \
    --fail --show-error \
    "${INGEST_URL}/projects/query" \
    --url-query operator=and \
    --url-query size="${PROJECT_PAGE_SIZE}" \
    --header "Content-Type: application/json" \
    --header "${AUTH_HEADER}" \
    --data "[{\"field\":\"wranglingState\",\"operator\":\"IS\",\"value\":\"${WRANGLING_STATE}\"}]" \
    | tee output_01_fetch_projects.json
    log INFO There are $(cat output_01_fetch_projects.json | jq .page.totalElements) projects in state ${WRANGLING_STATE}
}

filter_old_projects() {
  log INFO "keeping projects older than $CUTOFF_DATE"
  jq -r \
    --arg date "$CUTOFF_TIMESTAMP" '
      ._embedded.projects
      | map(select(.dcpVersion < $date))
      | map(._links.submissionEnvelopes.href)
      | .[]
    ' \
  | tee output_02_filter_old_projects.txt
  log INFO There are $(cat output_02_filter_old_projects.txt | wc -l) projects updated before $CUTOFF_DATE
}

fetch_submission_staging_locations() {
  log INFO "read submissions' staging areas"
  xargs -n1 curl -s | jq -r '
    select(._embedded?)
    ._embedded.submissionEnvelopes[0].stagingDetails.stagingAreaLocation.value
  ' \
  | tee output_03_fetch_submission_staging_locations.txt
}

generate_archive_s3_staging_areas_cmd() {
  log INFO "generating archive command"
  xargs -n1 -I{} echo aws s3 cp "{}" "{}" \
    --recursive \
    --storage-class $TARGET_STORAGE_CLASS \
    --metadata-directive COPY \
  > output_04_archive_s3_staging_areas.txt
  log info aws s3 update comannds are in output_04_archive_s3_staging_areas.txt
}

clean_outputs() {
  rm -f output_*
}
# Main script logic

log INFO "Archiving s3 upload areas of submissions with status $WRANGLING_STATE older than $CUTOFF_DATE"

clean_outputs \
  && fetch_projects \
  | filter_old_projects \
  | fetch_submission_staging_locations \
  | generate_archive_s3_staging_areas_cmd

log INFO "Archival of s3 upload areas done complete."
