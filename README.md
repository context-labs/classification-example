# Document Classification

Classify documents (PDF, images, Word) with Gemma 3 27B. Under the hood, it uses [structured outputs](https://docs.inference.net/features/structured-outputs) to match the labels given.

> **Note**
> This endpoint does not use the OpenAI SDK. Call it directly with HTTPS.

## Endpoint

- **Method**: `POST`
- **Path**: `/classify/document`

## Request
```json
{
  "document": "base64_encoded_document_string",
  "fileType": "pdf",
  "additionalLabels": ["Custom Label 1", "Custom Label 2"]
}
```

- **document**: Required. Base64-encoded contents of the file. Data URLs are also supported; the API strips any prefix like `data:application/pdf;base64,` automatically.
- **fileType**: Required. File type of the document ("pdf" or "docx").
- **additionalLabels**: Optional. Array of extra labels to merge with the default set.

> Note, currently this endpoint only accepts pdf and docx files.

### Supported document types

- PDFs (`application/pdf`) - specify `"fileType": "pdf"`
- Office documents (DOCX) - specify `"fileType": "docx"`

If the document cannot be parsed or converted to an image, the endpoint returns a `400` error.

## Process flow
When you submit a Base64 document, this is what happens. The Cloudflare worker:

1. Receives document upload as Base64
2. Converts document pages to one or more images
3. Sends images and combined labels (default + additional) to Gemma 3 27B
4. Parses model output and returns matched labels

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

The following labels are included by default. You can extend or narrow this set using `additionalLabels`.

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

## API Key Setup

To use this API, you need an Inference.net API key. You can get one by:

1. Visiting [inference.net](https://inference.net)
2. Signing up for an account
3. Generating an API key in your [dashboard](https://inference.net/dashboard/api-keys)

## Examples

Set your API key first:

```bash
export INFERENCE_API_KEY=inference-33056b2318064e79a308ec7731e44df0
```

Prepare a Base64 file (macOS/Linux):

```bash
base64 -i ./examples/sample.pdf -o ./examples/sample.b64
```

### Quick Test with Sample PDF

This curl requests takes in a sample invoice that we have already converted to base64.

```bash
# Test with additional labels
curl -X POST https://api.inference.net/classify/document \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INFERENCE_API_KEY" \
  -d "{\"document\": \"$(cat examples/sample.b64)\", \"fileType\": \"pdf\", \"additionalLabels\": [\"Receipt\", \"Bill\"]}" | jq .
```

### Converting PDF to Base64

```bash
# macOS/Linux
base64 -i document.pdf -o document.b64
```

### TypeScript (Node)

```javascript
import * as fs from "fs";

const fileBase64 = fs.readFileSync("examples/sample.pdf", { encoding: "base64" });

const response = await fetch("https://api.inference.net/classify/document", {
  method: "POST",
  headers: {
    "Authorization": "Bearer inference-33056b2318064e79a308ec7731e44df0",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    document: fileBase64,
    fileType: "pdf",
    additionalLabels: ["Invoice", "Contract"],
  }),
});

const result = await response.json();
console.log(result.labels, result.metadata);
```

### Python

```python
import base64
import requests

with open("examples/sample.pdf", "rb") as f:
    file_b64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://api.inference.net/classify/document",
    json={
        "document": file_b64,
        "fileType": "pdf",
        "additionalLabels": ["Invoice", "Contract"]
    },
    headers={
        "Authorization": "Bearer inference-33056b2318064e79a308ec7731e44df0",
        "Content-Type": "application/json",
    }
)

result = response.json()
print(result["labels"], result["metadata"])
```

## API Behavior and Limits

### Performance Expectations & Service Limits

> **Note**
> This API is is not yet ready for production workloads. It is intended for evaluation and development purposes only.

**API Timeouts:**
- since we only use the first 5 pages anyway for this endpoint, it's recommended you only submit 5 pages of your documents to avoid failures.

### Key Limitations

**Page Processing Limit:**
- The API will only analyze the **first 5 pages** of any PDF
- If your document is longer, content beyond page 5 will be **ignored**, which may affect classification accuracy

**File Size Limit:**
- The maximum allowed file size is **10MB**
- Requests with larger documents will be rejected immediately with a `DOCUMENT_TOO_LARGE` error

**Unsupported Content:**
- The API cannot process password-protected or encrypted PDFs
- Corrupted or non-standard PDF files may fail during conversion

### Error Handling

The API returns structured error responses with specific error codes. Here's a comprehensive guide:

| Error Code | HTTP Status | Common Cause | Recommended Action for User |
|------------|-------------|--------------|-----------------------------|
| `UNAUTHORIZED` | 401 | The Authorization header is missing, malformed, or contains an invalid key | Ensure you are sending a `Bearer <YOUR_INFERENCENET_API_KEY>` header with a valid key |
| `DOCUMENT_TOO_LARGE` | 413 | The submitted document exceeds the 10MB file size limit | Reduce the file size of your document before encoding it to base64. Consider compressing images within the PDF if possible |
| `INVALID_DOCUMENT_FORMAT` | 415 | The base64 string does not represent a valid PDF file | Verify that the document is a valid PDF and that the base64 encoding is correct. The API does not support encrypted or password-protected PDFs |
| `EMPTY_PDF` | 422 | The PDF was successfully processed but found to contain zero pages | Check your source document to ensure it is not empty or corrupted |
| `PDF_CONVERSION_FAILED` | 502 | The external PDF conversion service (PDF.co) could not process the file | This usually indicates a corrupted or non-standard PDF. Try re-saving the PDF from a trusted source and submit it again |
| `CLASSIFICATION_FAILED` | 502 | The AI model failed to analyze the images and return a classification | This may be a temporary issue with the AI service. Please retry your request. If the problem persists, the document may be unclassifiable (e.g., blank pages) |
| `INTERNAL_ERROR` | 500 | An unexpected error occurred on the server | This is a server-side issue. Please wait a moment and retry your request. Use the correlationId from the response if you need to report the issue |

### Error Response Format

All errors return a consistent JSON structure:

```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

## Notes & best practices

- Keep label lists concise and mutually exclusive when possible
- Merge defaults + `additionalLabels` to extend coverage without losing core categories
- Monitor the `processingTimeMs` field to optimize your usage patterns
