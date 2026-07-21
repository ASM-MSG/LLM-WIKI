#!/usr/bin/env node
/**
 * raw-guard — Layer 1 immutability guardrail.
 * PreToolUse(Edit|Write|MultiEdit|Bash).
 * - Edit/MultiEdit on raw/ → block
 * - Write overwriting existing raw/ → block (new raw allowed)
 * - Bash rm/shred/truncate or > redirection into raw/ → block
 * Exit 2 = block.
 */
const fs = require('fs');
const path = require('path');

let raw = '';
try { raw = fs.readFileSync(0, 'utf8'); } catch (_) {}
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
raw = raw.trim();

let data = {};
try { data = JSON.parse(raw || '{}'); } catch (_) {}

const tool = data.tool_name || '';
const ti = data.tool_input || {};
function block(msg) { console.error('🚫 ' + msg); process.exit(2); }

const fp = ti.file_path || ti.filePath || '';
const norm = String(fp).replace(/\\/g, '/');
if (/(^|\/)raw\//i.test(norm)) {
  if (tool === 'Edit' || tool === 'MultiEdit') {
    block('raw/ is immutable (Layer 1). Do NOT edit raw sources. Edit the compiled note, or add a NEW raw file.');
  }
  if (tool === 'Write') {
    let exists = false;
    try { exists = fs.existsSync(path.resolve(fp)); } catch (_) {}
    if (exists) block('raw/ is immutable (Layer 1). This raw file already exists — overwriting is blocked.');
  }
}
if (tool === 'Bash') {
  const cmd = String(ti.command || '');
  const rmRaw = /\b(rm|shred|truncate)\b[^|;&\n]*\braw\//i.test(cmd);
  const redirRaw = />>?\s*["']?[^\s"'|;&]*\braw\//i.test(cmd);
  if (rmRaw || redirRaw) {
    block('raw/ is immutable (Layer 1). Deleting/truncating or > into raw/ is blocked. (mv rename OK; new files OK.)');
  }
}
process.exit(0);
