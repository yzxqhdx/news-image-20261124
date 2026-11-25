// Entry program for make.fun competition news-image-20261124.
//
// The image (entry.png) is drawn by draw.py in this repository. The entry
// ships as text files, so the PNG bytes travel as base64 in entry.png.b64
// (a single line); this program decodes them and writes the image to the
// path the grader reads. Base64 decoding is deterministic, so both graded
// runs write exactly the same bytes.
//
// Runs on Node 22 with the standard library only: no network, no
// dependencies, nothing outside this repository.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const encoded = readFileSync(join(repoRoot, "entry.png.b64"), "utf8").trim();
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), Buffer.from(encoded, "base64"));
