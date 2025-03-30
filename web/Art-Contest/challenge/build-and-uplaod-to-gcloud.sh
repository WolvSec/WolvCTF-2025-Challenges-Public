#!/bin/bash

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=web-challenges-453514
#GCLOUD_PROJECT=vocal-tracer-453900-j6
GCLOUD_ARTIFACT_REPOSITORY=locker

# app vars
CHAL_NAME=art-contest
IMAGE_AND_TAG=$CHAL_NAME:1
GCLOUD_TAG1=$GCLOUD_REGION-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

gcloud builds submit --project=$GCLOUD_PROJECT --tag $GCLOUD_TAG1

gcloud run services delete $CHAL_NAME --quiet --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT

# gcloud run deploy $CHAL_NAME --image=$GCLOUD_TAG1 --allow-unauthenticated --port=3000 --memory=1Gi --max-instances=10 --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT
gcloud run deploy $CHAL_NAME --execution-environment=gen2 --image=$GCLOUD_TAG1 --allow-unauthenticated --port=80 --min-instances=1 --min=1 --max-instances=10 --cpu-boost --session-affinity --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT
