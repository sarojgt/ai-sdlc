#!/usr/bin/env node
import fs from "node:fs";
import process from "node:process";
// The core build validates diagram grammars without the browser sanitization
// adapter. This keeps the mandatory parser gate browser-free; rendering remains
// a separate optional Mermaid CLI concern.
import mermaid from "mermaid/dist/mermaid.core.mjs";

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error("Usage: node validate.mjs <markdown-file> [...]");
  process.exit(2);
}

mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
const blockPattern = /```mermaid\s*\n([\s\S]*?)```/gi;
let failures = 0;

for (const filename of files) {
  const text = fs.readFileSync(filename, "utf8");
  const blocks = [...text.matchAll(blockPattern)];
  for (let index = 0; index < blocks.length; index += 1) {
    const source = blocks[index][1].trim();
    try {
      await mermaid.parse(source, { suppressErrors: false });
      console.log(`Mermaid diagram ${index + 1} valid: ${filename}`);
    } catch (error) {
      failures += 1;
      console.error(`Mermaid diagram ${index + 1} invalid: ${filename}`);
      console.error(error instanceof Error ? error.message : String(error));
    }
  }
}

if (failures > 0) process.exit(1);
