// news-image-20261125 — validated publisher for the 25 Nov 2026 front page.
//
// The artwork lives in entry.png beside this file (drawn at build time by
// draw.py). This program checks the PNG strictly, then copies it
// byte-for-byte to the output directory so repeat runs are identical.
//
// Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1_048_576; // 1 MiB hard limit from the bounty spec
const MAX_DIMENSION = 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(message) {
  console.error(`entry.png rejected: ${message}`);
  process.exit(1);
}

function readU32BE(buf, offset) {
  return (
    buf[offset] * 2 ** 24 +
    buf[offset + 1] * 2 ** 16 +
    buf[offset + 2] * 2 ** 8 +
    buf[offset + 3]
  );
}

function validatePng(buf) {
  if (buf.length === 0) fail("file is empty");
  if (buf.length > MAX_BYTES) {
    fail(`file is ${buf.length} bytes, over the ${MAX_BYTES}-byte limit`);
  }
  if (buf.length < 33) fail("file is too short to hold a PNG header");

  for (let i = 0; i < PNG_SIGNATURE.length; i += 1) {
    if (buf[i] !== PNG_SIGNATURE[i]) {
      fail(`bad PNG signature at byte ${i}`);
    }
  }

  // The first chunk must be IHDR: length 13, type "IHDR".
  const ihdrLength = readU32BE(buf, 8);
  const ihdrType = buf.toString("ascii", 12, 16);
  if (ihdrType !== "IHDR" || ihdrLength !== 13) {
    fail(`first chunk is ${ihdrType}/${ihdrLength}, expected IHDR/13`);
  }

  // A complete PNG ends with an IEND chunk: length 0, type "IEND",
  // then its CRC. Reject truncated files that pass the header checks.
  const tailType = buf.toString("ascii", buf.length - 8, buf.length - 4);
  if (readU32BE(buf, buf.length - 12) !== 0 || tailType !== "IEND") {
    fail("missing IEND chunk at end of file (truncated PNG?)");
  }

  const width = readU32BE(buf, 16);
  const height = readU32BE(buf, 20);
  if (width < 1 || height < 1) fail(`invalid dimensions ${width}x${height}`);
  if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
    fail(`dimensions ${width}x${height} exceed ${MAX_DIMENSION}x${MAX_DIMENSION}`);
  }
  return { width, height };
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(here, "entry.png");

  let data;
  try {
    data = readFileSync(sourcePath);
  } catch (err) {
    fail(`cannot read ${sourcePath}: ${err.message}`);
  }

  const { width, height } = validatePng(data);

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, "entry.png");
  writeFileSync(outPath, data);

  console.log(
    `published ${outPath}: ${width}x${height} PNG, ${data.length} bytes`,
  );
}

main();
