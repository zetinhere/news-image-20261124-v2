import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Graded entrypoint. The picture is painted at build time by draw.py
// (PIL, no network, no clock, no randomness), so this file just places the
// finished entry.png into the grader's output directory. Copying the same
// bytes twice gives the same output both runs.
const root = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const png = readFileSync(join(root, "entry.png"));
mkdirSync(out, { recursive: true });
writeFileSync(join(out, "entry.png"), png);
