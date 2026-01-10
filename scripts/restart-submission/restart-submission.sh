#!/bin/bash
set -e
trap 'catch $? $LINENO' ERR

catch() {
  log_info "ERROR: Error $1 occurred on $0:$2"
}

INGEST_KUBE_REPO=../../../ingest-kube-deployment
INGEST_API_URL=https://api.ingest.archive.data.humancellatlas.org
INGEST_UI_URL=https://contribute.data.humancellatlas.org
DEPLOYMENT_STAGE=prod

# See possible statuses in commitXyxEvent urls in
# https://github.com/ebi-ait/ingest-core/blob/master/src/main/java/org/humancellatlas/ingest/submission/web/SubmissionController.java#L292
# https://github.com/ebi-ait/ingest-core/blob/master/src/main/java/org/humancellatlas/ingest/core/web/Links.java#L60
NEW_STATUS=Valid

function usage() {
    echo "$0: command line arguments:"
    grep '##' "$0" | grep -v sed | sed -e 's/).*##/:/'
}

while getopts s:t:mn:h flag
do
    case "${flag}" in
        s) SUBMISSION_ID=${OPTARG};; ## submission id (not uuid)
        t) INGEST_TOKEN=${OPTARG};;  ## ingest token
        n) NEW_STATUS=${OPTARG};;    ## new status. see SubmissionController
        m) SUBMIT_ACTIONS=Export_Metadata;; ## submit actions. see SubmissionController#submitEnvelopeRequest
        h) usage && exit 1;;
        ?) usage && exit 1;;
        *) usage && exit 1;;
    esac
done



[ -z "$SUBMISSION_ID" ] && echo "missing submission id" && usage && exit 1
[ -z "$INGEST_TOKEN" ] && echo "missing ingest token" && usage && exit 1

# ANSI colors for clear log messages
GRN='\033[0;32m'
YLW='\033[1;33m'
PRP='\033[0;35m'
NC='\033[0m' # No Color

log_info() {
  msg=$1
  echo -e "${YLW}$0${NC}\t${PRP}$(date -Iseconds)${NC}\tINFO\t${GRN}${msg}${NC}"
}
log_info "looking for submission ${SUBMISSION_ID}"
curl --head \
     --fail \
     "${INGEST_API_URL}/submissionEnvelopes/${SUBMISSION_ID}"

log_info "set submission to ${NEW_STATUS}"

curl --request PUT \
     --header "Authorization: Bearer ${INGEST_TOKEN}" \
     --head \
     --verbose \
     --fail \
     -o "set_status.output.txt" \
     "${INGEST_API_URL}/submissionEnvelopes/${SUBMISSION_ID}/commit${NEW_STATUS}Event"

log_info "load ${DEPLOYMENT_STAGE} environment configuration"
source "${INGEST_KUBE_REPO}/config/environment_${DEPLOYMENT_STAGE}"

log_info "change to ${DEPLOYMENT_STAGE} k8s cluster"
kubectx "ingest-eks-${DEPLOYMENT_STAGE}"

log_info "restart state-tracking"
kubectl rollout restart deployment ingest-state-tracking

log_info "inspect the submission using hte api on ${INGEST_API_URL}/submissionEnvelopes/${SUBMISSION_ID}"
log_info "go to ui to work on ${INGEST_UI_URL}/submissions/detail?${SUBMISSION_ID}"

if [[ $SUBMIT_ACTIONS == "Export" ]]
then
  log_info "re-export submission"
  #curl -X PUT \
  #     -H "Authorization: Bearer ${INGEST_TOKEN}" \
  #     -d "[${SUBMIT_ACTIONS}]" \
  #     -o "submit.output.txt" \
  #     "${INGEST_API_URL}/submissionEnvelopes/${SUBMISSION_ID}/submissionEvent"
fi
log_info "done"