#!/bin/bash

API_URL=$VITE_BASE_URL

if [ -z "$API_URL" ]; then
  API_URL="http://localhost:8002"
fi

curl "$API_URL/"
printf "\n"

curl "$API_URL/auth/test"
printf "\n"
curl -X POST "$API_URL/auth/create-test-user"
printf "\n"

curl "$API_URL/files/test"
printf "\n"
curl -X POST "$API_URL/files/create-test-file"
printf "\n"

curl "$API_URL/shares/test"
printf "\n"
curl -X POST "$API_URL/shares/create-test-share"
printf "\n"

curl "$API_URL/webhooks/test"
printf "\n"
curl -X POST "$API_URL/webhooks/create-test-webhook"
printf "\n"
