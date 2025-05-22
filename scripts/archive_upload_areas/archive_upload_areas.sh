#!/usr/bin/env bash

set -euo pipefail

# Load environment variables
source .env

: "${INGEST_URL:?Missing INGEST_URL in .env}"
: "${INGEST_TOKEN:?Missing INGEST_TOKEN in .env}"

# Configuration
PROJECT_PAGE_SIZE=500
AUTH_HEADER="Authorization: Bearer ${INGEST_TOKEN}"
TARGET_STORAGE_CLASS=GLACIER
WRANGLING_STATE=PUBLISHED_IN_DCP
CUTOFF_UPDATE_DATE=$(date -v -6m "+%Y-%m-%dT%H:%M:%SZ")
INGEST_KUBE_REPO=../../../ingest-kube-deployment

# Functions
fetch_projects() {
  curl --silent \
    --location --max-time 10 \
    --fail --show-error \
    "${INGEST_URL}/projects/query" \
    --url-query operator=and \
    --url-query size="${PROJECT_PAGE_SIZE}" \
    --header "Content-Type: application/json" \
    --header "${AUTH_HEADER}" \
    --data "[{\"field\":\"wranglingState\",\"operator\":\"IS\",\"value\":\"${WRANGLING_STATE}\"}]" \
    | tee output_01_fetch_projects.txt
}

filter_old_projects() {
  jq -r --arg date "$CUTOFF_UPDATE_DATE" '
    ._embedded.projects
    | map(select(.updateDate < $date))
    | map(._links.submissionEnvelopes.href)
    | .[]
  ' \
  | tee output_02_filter_old_projects.txt
}

fetch_submission_staging_locations() {
  xargs -n1 curl -s | jq -r '
    select(._embedded?)
    ._embedded.submissionEnvelopes[0].stagingDetails.stagingAreaLocation.value
  ' \
  | tee output_03_fetch_submission_staging_locations.txt
}

generate_archive_s3_staging_areas_cmd() {
  xargs -n1 -I{} echo aws s3 cp "{}" "{}" \
    --recursive \
    --storage-class $TARGET_STORAGE_CLASS \
    --metadata-directive COPY \
  | tee output_04_archive_s3_staging_areas.txt

}

# Main script logic

echo "Archiving s3 upload areas of submissions with status $WRANGLING_STATE older than $CUTOFF_UPDATE_DATE"

fetch_projects \
  | filter_old_projects \
  | fetch_submission_staging_locations \
  | generate_archive_s3_staging_areas_cmd

echo "Archival of s3 upload areas done complete."
