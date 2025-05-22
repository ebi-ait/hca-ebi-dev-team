#!/bin/bash
set -e
trap 'catch $? $LINENO' EXIT

catch() {
  if [ "$1" != "0" ]; then
    log_info "ERROR: Error $1 occurred on $0:$2"
  fi
}

INGEST_KUBE_REPO=../../../ingest-kube-deployment
INGEST_API_URL=https://api.ingest.archive.data.humancellatlas.org
DEPLOYMENT_STAGE=prod

# See possible statuses in commitXyzEvent urls in
# https://github.com/ebi-ait/ingest-core/blob/master/src/main/java/org/humancellatlas/ingest/submission/web/SubmissionController.java#L292
# https://github.com/ebi-ait/ingest-core/blob/master/src/main/java/org/humancellatlas/ingest/core/web/Links.java#L60
NEW_STATUS=Valid

function usage() {
    echo "$0: command line arguments:"
    grep '##' "$0" | grep -v sed | sed -e 's/).*##/:/'
}

[ -f ".env" ] && source .env

while getopts s:t:mn:he: flag
do
    case "${flag}" in
        s) SUBMISSION_ID=${OPTARG};; ## submission id/uuid
        t) INGEST_TOKEN=${OPTARG};;  ## ingest token
        n) NEW_STATUS=${OPTARG};;    ## new status. see SubmissionController in ingest-core
        e) DEPLOYMENT_STAGE=${OPTARG};;    ## environment: dev, staging, prod (default)
#        m) SUBMIT_ACTIONS=Export_Metadata;; ## submit actions. see SubmissionController#submitEnvelopeRequest
        h) usage && exit 1;;
        ?) usage && exit 1;;
        *) usage && exit 1;;
    esac
done

# mandatory parameters
[ -z "$SUBMISSION_ID" ] && echo "missing submission id/uuid" && usage && exit 1
[ -z "$INGEST_TOKEN" ] && echo "missing ingest token" && usage && exit 1


# build ingest api url
ENV_URL_MARKER=
if [[ $DEPLOYMENT_STAGE == "dev" ]]
then
  ENV_URL_MARKER=dev.
elif [[ $DEPLOYMENT_STAGE == "staging" ]]
then
  ENV_URL_MARKER=staging.
fi
INGEST_API_URL=https://api.ingest.${ENV_URL_MARKER}archive.data.humancellatlas.org
INGEST_UI_URL=https://${ENV_URL_MARKER}contribute.data.humancellatlas.org


# ANSI colors for clear log messages
GRN='\033[0;32m'
YLW='\033[1;33m'
PRP='\033[0;35m'
NC='\033[0m' # No Color

log_info() {
  msg=$1
  echo -e "${YLW}$0${NC}\t${PRP}$(date -Iseconds)${NC}\tINFO\t${GRN}${msg}${NC}"
}

if grep - <<< ${SUBMISSION_ID}; then
  log_info "using submission uuid"
  SUBMISSION_UUID=${SUBMISSION_ID}
  SUBMISSION_URL=$(curl --header "Authorization: Bearer ${INGEST_TOKEN}" "${INGEST_API_URL}/submissionEnvelopes/search/findByUuidUuid?uuid=${SUBMISSION_UUID}" | jq --raw-output "._links.self.href")
else
  log_info "using submission id"
  SUBMISSION_URL=${INGEST_API_URL}/submissionEnvelopes/${SUBMISSION_ID}
  # shellcheck disable=SC2086
  SUBMISSION_UUID=$(curl "$SUBMISSION_URL" | jq '.uuid.uuid' | sed 's/"//g')
fi

log_info "looking for submission ${SUBMISSION_ID}"
log_info "SUBMISSION_URL: ${SUBMISSION_URL}"
curl --head \
     --fail \
     --header "Authorization: Bearer ${INGEST_TOKEN}" \
     "${SUBMISSION_URL}"

log_info "set submission to ${NEW_STATUS}"

curl --request PUT \
     --header "Authorization: Bearer ${INGEST_TOKEN}" \
     --head \
     --fail \
     -o "set_status.output.txt" \
     "${SUBMISSION_URL}/commit${NEW_STATUS}Event"

log_info "load ${DEPLOYMENT_STAGE} environment configuration"
source "${INGEST_KUBE_REPO}/config/environment_${DEPLOYMENT_STAGE}"

log_info "change to ${DEPLOYMENT_STAGE} k8s cluster"
kubectx "ingest-eks-${DEPLOYMENT_STAGE}"

log_info "change to ${DEPLOYMENT_STAGE} namespace"
kubens "${DEPLOYMENT_STAGE}-environment"

log_info "restart state-tracking"
kubectl rollout restart deployment ingest-state-tracking

log_info "inspect the submission using the api on ${SUBMISSION_URL}"

log_info "go to ui to work on ${INGEST_UI_URL}/submissions/detail?uuid=${SUBMISSION_UUID}"
if [[ $SUBMIT_ACTIONS == Export* ]]
then
  log_info "re-export submission. action: $SUBMIT_ACTIONS"
  curl --request PUT \
       --header "Authorization: Bearer ${INGEST_TOKEN}" \
       --header 'Content-Type: application/json' \
       --data-raw "[\"${SUBMIT_ACTIONS}\"]" \
       -o "submit.output.txt" \
       "${SUBMISSION_URL}/submissionEvent"
fi
log_info "done"
