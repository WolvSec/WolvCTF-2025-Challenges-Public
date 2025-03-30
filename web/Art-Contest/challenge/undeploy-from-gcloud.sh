#!/bin/bash

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=web-challenges-453514
GCLOUD_ARTIFACT_REPOSITORY=locker

CHAL_NAME=art-contest

gcloud run services delete $CHAL_NAME --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT
