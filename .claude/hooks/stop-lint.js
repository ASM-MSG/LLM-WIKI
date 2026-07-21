#!/usr/bin/env node
const { execFileSync } = require('child_process');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const LINT = path.join(__dirname, '..', 'skills', 'wiki-lint', 'lint.js');
try {
  execFileSync('node', [LINT, '.'], { cwd: ROOT, encoding: 'utf8' });
} catch (e) {
  if (e && e.stdout) process.stderr.write(e.stdout.toString());
  else if (e && e.message) process.stderr.write('stop-lint: ' + e.message + '\n');
}
process.exit(0);
