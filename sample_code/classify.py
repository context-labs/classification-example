#!/usr/bin/env python3
import os
import base64
from typing import Dict, List, Any, Optional
import requests

API_URL = "https://delicate-bird-c901.sam-b0c.workers.dev/classify"
API_KEY = os.getenv("INFERENCE_API_KEY", "")

def classify_document(file_path: str, additional_labels: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Classify a document using the Dropbox document classification API.

    Args:
        file_path: Path to the PDF file to classify
        additional_labels: Optional list of additional labels to consider

    Returns:
        Dict containing 'labels' and 'metadata' keys
    """
    with open(file_path, "rb") as f:
        file_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        API_URL,
        json={
            "document": file_b64,
            "additional_labels": additional_labels or []
        },
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Request failed ({response.status_code}): {response.text}")

    return response.json()


if __name__ == "__main__":
    result = classify_document("../sample.pdf", ["Invoice", "Contract"])
    print(result.get("labels"), result.get("metadata"))
