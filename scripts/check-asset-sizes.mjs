// Fails the build if any asset exceeds Cloudflare Workers' 25 MiB per-asset limit.
import { readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const LIMIT = 25 * 1024 * 1024;
const root = process.argv[2] ?? 'dist';

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? walk(path) : [path];
  });
}

const oversized = walk(root)
  .map((path) => ({ path, size: statSync(path).size }))
  .filter((file) => file.size > LIMIT)
  .sort((a, b) => b.size - a.size);

if (oversized.length > 0) {
  console.error(`\n✘ ${oversized.length} asset(s) exceed the 25 MiB Cloudflare Workers limit:\n`);
  for (const { path, size } of oversized) {
    console.error(`  ${relative(root, path)} — ${(size / 1048576).toFixed(1)} MiB`);
  }
  console.error('\nCompress or remove them before deploying.\n');
  process.exit(1);
}

console.log(`✔ All assets in ${root}/ are under 25 MiB.`);
