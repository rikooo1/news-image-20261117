// news-image-20261117 entry — Tuesday 17 November 2026 front page.
// The image is pre-rendered deterministically by render.py and committed as entry.png.
// This program only copies those exact bytes to /output/entry.png (no network, no randomness).
import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const buf = readFileSync(src);
if (buf.length > 1024 * 1024) throw new Error('entry.png exceeds 1 MiB');
if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error('entry.png is not a PNG');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(src, join(outDir, 'entry.png'));
console.log(`wrote entry.png (${statSync(src).size} bytes)`);
