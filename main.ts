// news-image-20261117 entry — Tuesday 17 November 2026 front page.
// Pre-rendered deterministically by render.py; this program copies the exact bytes.
import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const buf = readFileSync(src);
if (buf.length > 1024 * 1024) throw new Error('entry.png exceeds 1 MiB');
if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error('entry.png is not a PNG');
if (buf.readUInt32BE(16) !== 1024 || buf.readUInt32BE(20) !== 1024) throw new Error('entry.png must be 1024x1024');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(src, join(outDir, 'entry.png'));
console.log(`wrote entry.png (${statSync(src).size} bytes)`);
