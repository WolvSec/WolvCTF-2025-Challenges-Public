#!/bin/bash
docker build ./challenge -t compactsubscription:1.0
docker create --name CompactSubscriptionBuilder compactsubscription:1.0
docker cp CompactSubscriptionBuilder:/decoder .

cp challenge/messages .
tar -czf dis.tar.gz decoder messages