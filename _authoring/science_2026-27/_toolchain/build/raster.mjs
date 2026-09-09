import fs from 'node:fs/promises';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const sharp = require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const [src,dest]=process.argv.slice(2);
await sharp(await fs.readFile(src),{density:170}).png().toFile(dest);
