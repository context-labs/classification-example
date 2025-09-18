#!/usr/bin/env npx ts-node
import * as fs from "fs";

const API_KEY = fs.readFileSync("../.env", "utf8").split("=")[1].trim();
const fileBase64 = fs.readFileSync("../sample.pdf", { encoding: "base64" });

const response = await fetch("https://delicate-bird-c901.sam-b0c.workers.dev/classify", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    document: fileBase64,
    additional_labels: ["Invoice", "Contract"],
  }),
});

const result = await response.json() as { labels: string[]; metadata: any };
console.log(result.labels, result.metadata);
