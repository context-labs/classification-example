# Document Classification

Classify business documents (PDF, images, Word) with Gemma 3 27B

> **Note**
> This endpoint does not use the OpenAI SDK. Call it directly with HTTPS.

## Endpoint

- **Method**: `POST`
- **Path**: `/classify`

## Request

```json
{
  "document": "base64_encoded_document_string",
  "additional_labels": ["Custom Label 1", "Custom Label 2"]
}
```

- **document**: Required. Base64-encoded contents of the file. Data URLs are also supported; the API strips any prefix like `data:application/pdf;base64,` automatically.
- **additional_labels**: Optional. Array of extra labels to merge with the default set.

### Supported document types

- PDFs (`application/pdf`)
- Images (PNG, JPEG, WEBP, TIFF)
- Office documents (DOCX)

If the document cannot be parsed or converted to an image, the endpoint returns a `400` error.

## Process flow

1. Receive document upload as Base64
2. Convert document pages to one or more images
3. Send images and combined labels (default + additional) to Gemma 3 27B
4. Parse model output and return matched labels

## Response

The API returns a JSON object with the following structure:

```json
{
  "labels": ["Memo", "Email Correspondence"],
  "metadata": {
    "processingTimeMs": 6748,
    "pageCount": 4,
    "pdfSizeMB": 0.1361713409423828,
    "pagesProcessed": 4,
    "correlationId": "1758222412597-eg945o7hq",
    "timestamp": "2025-09-18T19:06:59.345Z"
  }
}
```

- **labels**: Array of strings containing the matched document classification labels from the predefined set
- **metadata**: Object containing processing information:
  - `processingTimeMs`: Time taken to process the document in milliseconds
  - `pageCount`: Total number of pages in the PDF
  - `pdfSizeMB`: Size of the PDF file in megabytes
  - `pagesProcessed`: Number of pages that were successfully processed
  - `correlationId`: Unique identifier for the request
  - `timestamp`: ISO 8601 timestamp when the processing completed

## Default labels

The following labels are included by default. You can extend or narrow this set using `additional_labels`.

```
Invoice
Purchase Order
Receipt
Expense Report
Budget Report
Financial Statement
Balance Sheet
Income Statement
Cash Flow Statement
Tax Return
W2 Form
1099 Form
Pay Stub
Credit Note
Debit Note
Contract
Service Level Agreement(SLA)
Non - Disclosure Agreement(NDA)
Terms of Service
Privacy Policy
Memorandum of Understanding(MOU)
Letter of Intent(LOI)
Power of Attorney
Legal Notice
Compliance Report
Audit Report
Risk Assessment
Statement of Work(SOW)
Request for Proposal(RFP)
Request for Information(RFI)
Request for Quotation(RFQ)
Business Plan
Strategic Plan
Operational Procedure
Standard Operating Procedure(SOP)
Work Order
Change Request
Incident Report
Product Requirements Document(PRD)
Technical Specification
Architecture Document
API Documentation
User Manual
Installation Guide
Release Notes
Bug Report
Test Plan
Code Review
Database Schema
Network Diagram
Mermaid Diagram
UML Diagram
Project Charter
Project Plan
Gantt Chart
Status Report
Meeting Minutes
Action Items List
Risk Register
Stakeholder Analysis
Lessons Learned
Post - Mortem Report
Resume / CV
Job Description
Offer Letter
Employment Contract
Performance Review
Training Material
Employee Handbook
Organizational Chart
Leave Request
Timesheet
Benefits Summary
Marketing Plan
Campaign Brief
Brand Guidelines
Press Release
Case Study
White Paper
Product Brochure
Sales Proposal
Customer Testimonial
Market Research Report
Competitor Analysis
Sales Forecast
Email Correspondence
Memo
Newsletter
Presentation
Meeting Agenda
Conference Notes
Webinar Materials
FAQ Document
Quality Assurance Report
ISO Certification
Certificate of Compliance
Inspection Report
Warranty Document
Service Agreement
```

## Examples

Set your API key first:

```bash
export INFERENCE_API_KEY=<my-inference-api-key>
```

Prepare a Base64 file (macOS/Linux):

```bash
base64 -i ./sample.pdf -o ./sample.b64
```

### Quick Test with Sample PDF

This curl requests takes in a sample invoice that we have already converted to base64.

```bash
# Test with additional labels
curl -X POST https://delicate-bird-c901.sam-b0c.workers.dev/classify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INFERENCE_API_KEY" \
  -d "{\"document\": \"$(cat sample.b64)\", \"additional_labels\": [\"Receipt\", \"Bill\"]}" | jq .
```

### Converting PDF to Base64

```bash
# macOS/Linux
base64 -i document.pdf -o document.b64
```

### TypeScript (Node)

```javascript
import * as fs from "fs";

const fileBase64 = fs.readFileSync("sample.pdf", { encoding: "base64" });

const response = await fetch("https://delicate-bird-c901.sam-b0c.workers.dev/classify", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    document: fileBase64,
    additional_labels: ["Invoice", "Contract"],
  }),
});

const result = await response.json();
console.log(result.labels, result.metadata);
```

### Python

```python
import base64
import requests

with open("sample.pdf", "rb") as f:
    file_b64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://delicate-bird-c901.sam-b0c.workers.dev/classify",
    json={
        "document": file_b64,
        "additional_labels": ["Invoice", "Contract"]
    },
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    }
)

result = response.json()
print(result["labels"], result["metadata"])
```

## Notes & best practices

- Keep label lists concise and mutually exclusive when possible
- Merge defaults + `additional_labels` to extend coverage without losing core categories
# classification-example
