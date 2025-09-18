#!/bin/bash

export INFERENCE_API_KEY=$(cat ../.env | cut -d'=' -f2)
base64 -i ../sample.pdf -o sample.b64
curl -X POST https://delicate-bird-c901.sam-b0c.workers.dev/classify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INFERENCE_API_KEY" \
  -d "{\"document\": \"$(cat sample.b64)\", \"additional_labels\": [\"Receipt\", \"Bill\"]}" | jq .
rm sample.b64
