#!/usr/bin/env python3
import base64
import requests

with open("../.env", "r") as f:
    API_KEY = f.read().strip().split("=")[1]

with open("../sample.pdf", "rb") as f:
    file_b64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://delicate-bird-c901.sam-b0c.workers.dev/classify",
    json={
        "document": file_b64,
        "additional_labels": ["Invoice", "Contract"]
    },
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
)

result = response.json()
print(result["labels"], result["metadata"])
