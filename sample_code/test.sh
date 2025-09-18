#!/bin/bash

# Document Classification API - Shell Script Example
# This script demonstrates how to classify a document using the API

# Set your API key from .env file
export INFERENCE_API_KEY=$(cat ../.env | cut -d'=' -f2)

# Convert sample.pdf to base64
base64 -i ../sample.pdf -o sample.b64

# Test with additional labels
curl -X POST https://delicate-bird-c901.sam-b0c.workers.dev/classify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INFERENCE_API_KEY" \
  -d "{\"document\": \"$(cat sample.b64)\", \"additional_labels\": [\"Receipt\", \"Bill\"]}" | jq .

# Cleanup
rm sample.b64
