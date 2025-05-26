#!/usr/bin/env bash

# Scriptdir is the directory in which this script resides
SCRIPTDIR="$(pwd)"

# DOTENV is the gitignored .env file for the current user
DOTENV="$SCRIPTDIR/.env"

# the KEYSDIR is the gitignored directory for sensitive data
KEYSDIR="creds"
test -d "$KEYSDIR" || mkdir "$KEYSDIR"
grep -s -q "$KEYSDIR" .gitignore || echo "${KEYSDIR}/" >> .gitignore

# The GCP Project ID
PROJECT_ID=cytoreason

verify_current_kube_context () {
    KUBECONFIG="$KUBECONFIGFILE" kubectl config current-context | grep "$1"
    if [[ $? -ne 0 ]]; then
        echo "SERIOUS ERROR! Failed to set context for cluster $1"
        exit 1
    fi
}

# set the kubectl context to where the secret is hosted
echo "*** Setting up kubectl context ***"
KUBECONFIGFILE="${KEYSDIR}/kubeconfig"
KUBECLUSTER="infra-platform-v2"
KUBECONFIG="$KUBECONFIGFILE" gcloud container clusters get-credentials "$KUBECLUSTER" --zone "europe-west1-b" --project cytoreason

# get the credentials for the service agent which will be used to authenticate
# store them in the gitignored directory:
GOOGLE_APPLICATION_CREDENTIALS="${KEYSDIR}/credentials.json"
KUBECONFIG="$KUBECONFIGFILE" kubectl -n default get secret ci-image-builder -o 'go-template={{index .data "credentials.json" }}' -n default | base64 -d > "$GOOGLE_APPLICATION_CREDENTIALS"

rm -f "$DOTENV"

echo "*** Creating gitignored $DOTENV ***"
echo "GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}" >> "$DOTENV"

echo "LAKEFS_REPO_NAME=e2poc" >> "$DOTENV"
# The GKE cluster in which cyto-cc workflows run
K8S_JOBS_CLUSTER=cyto-cc-production-jobs
K8S_JOBS_CLUSTER_ZONE=europe-west1-b

echo "***Retrieving credentials for authentication to $K8S_JOBS_CLUSTER cluster***"
KUBECONFIG="$KUBECONFIGFILE" gcloud container clusters get-credentials "$K8S_JOBS_CLUSTER" --zone "$K8S_JOBS_CLUSTER_ZONE" --project "$PROJECT_ID" && verify_current_kube_context "$K8S_JOBS_CLUSTER"

LAKEFS_HOST=`KUBECONFIG="$KUBECONFIGFILE" kubectl -n default get secrets lakefs-secrets -o 'go-template={{index .data "LAKEFS_HOST"}}' | base64 -d`
echo "LAKEFS_HOST=$LAKEFS_HOST" >> "$DOTENV"

LAKEFS_USERNAME=`KUBECONFIG="$KUBECONFIGFILE" kubectl -n default get secrets lakefs-secrets -o 'go-template={{index .data "LAKEFS_USERNAME"}}' | base64 -d`
echo "LAKEFS_USERNAME=$LAKEFS_USERNAME" >> "$DOTENV"

LAKEFS_PASSWORD=`KUBECONFIG="$KUBECONFIGFILE" kubectl -n default get secrets lakefs-secrets -o 'go-template={{index .data "LAKEFS_PASSWORD"}}' | base64 -d`
echo "LAKEFS_PASSWORD=$LAKEFS_PASSWORD" >> "$DOTENV"

echo "*** $DOTENV created ***"

gcloud auth configure-docker --quiet eu.gcr.io
