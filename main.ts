// Entry program for the make.fun news-image-20261124 competition.
//
// draw.py in this repository draws the image. The entry ships as text
// files, so the PNG bytes travel as base64 in entry.png.b64 (one long
// line); this program decodes that file and writes the image where the
// grader looks for it. Decoding base64 is deterministic, so the two
// graded runs produce byte-identical files.
//
// Node 22, standard library only. No network, no dependencies, and
// nothing is read from outside this repository.
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const here = dirname(fileURLToPath(import.meta.url));
const dest = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const payload = readFileSync(join(here, "entry.png.b64"), "utf8").trim();
mkdirSync(dest, { recursive: true });
writeFileSync(join(dest, "entry.png"), Buffer.from(payload, "base64"));
