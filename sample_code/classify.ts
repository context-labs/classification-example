#!/usr/bin/env npx ts-node
import * as fs from "node:fs";

// Read API key from .env file
const API_KEY = fs.readFileSync("../.env", "utf8").split("=")[1].trim();

const API_URL = "https://delicate-bird-c901.sam-b0c.workers.dev/classify";

async function classifyDocument(filePath: string, additional_labels: string[] = []) {
  const fileBase64 = fs.readFileSync(filePath, { encoding: "base64" });
  const resp = await fetch(API_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document: fileBase64,
      additional_labels,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`Request failed (${resp.status}): ${text}`);
  }

  const data = (await resp.json()) as {
    labels: string[];
    metadata: Record<string, unknown>;
  };
  return data;
}

(async () => {
  const { labels, metadata } = await classifyDocument("../sample.pdf", ["Invoice", "Contract"]);
  console.log(labels, metadata);
})();
