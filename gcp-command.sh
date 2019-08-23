#!/bin/bash
gcloud scheduler jobs create pubsub update-splash-page-JOB \
    --topic=update-splash-page \
    --message-body="update-splash-page" \
    --schedule="5 0 * * *"   # run five minutes after midnight, every day

# Script to deploy the cloud function at GCP
gcloud functions deploy update-splash-page \
    --entry-point main_function \
    --runtime python37 \
    --trigger-topic update-splash-page \
    --env-vars-file=variables.yaml

gcloud pubsub topics publish update-splash-page --message "test"
