#!/usr/bin/env node
/** wiki-lint — 무결성 점검. 사용법: node lint.js <루트>. 종료코드 0=깨끗, 1=문제. */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(process.argv[2] || '.');
const NOTE_DIRS = ['00-inbox', '01-product', '02-planning', '03-specs',
                   '04-decisions', '05-meetings', '06-research',
                   '07-individual', '90-archive'];
const INDEXED_DIRS = ['01-product', '02-planning', '03-specs',
                      '04-decisions', '05-meetings', '06-research'];
const SUPPORT = new Set(['index', 'hot', 'log', 'readme', '_index']);

function walk(dir, out = []) {
  let ents = [];
  try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch (_) { return out; }
  for (const e of ents) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile()) out.push(p);
  }
  return out;
}

const problems = [];
const report = (type, file, msg) =>
  problems.push(`[${type}] ${path.relative(ROOT, file)} — ${msg}`);

// ── compiled 노트 수집 ──
const notes = [];
for (const d of NOTE_DIRS) {
  for (const f of walk(path.join(ROOT, d))) {
    if (f.toLowerCase().endsWith('.md')) notes.push(f);
  }
}
const noteBasenames = new Set(notes.map(f => path.basename(f, '.md')));
['index', 'hot', 'log', 'SCHEMA', 'glossary'].forEach(n => noteBasenames.add(n));

const indexTxt = (() => {
  try { return fs.readFileSync(path.join(ROOT, 'index.md'), 'utf8'); } catch (_) { return ''; }
})();

const sources = new Set();

for (const f of notes) {
  const base = path.basename(f, '.md');
  if (SUPPORT.has(base.toLowerCase())) continue;
  const txt = fs.readFileSync(f, 'utf8');
  const fmMatch = txt.match(/^---\n([\s\S]*?)\n---/);
  const fm = fmMatch ? fmMatch[1] : '';

  // frontmatter: title/source
  if (!/^title:\s*\S/m.test(fm)) report('frontmatter', f, 'title 누락');
  const srcMatch = fm.match(/^source:\s*["']?([^"'\n]+)/m);
  if (!srcMatch) report('frontmatter', f, 'source 누락');
  else srcMatch[1].split(',').forEach(s => sources.add(s.trim().normalize('NFC')));

  // field: product/class (권장)
  if (!/^product:\s*\S/m.test(fm)) report('field', f, 'product 누락 (권장)');
  if (!/^class:\s*\S/m.test(fm)) report('field', f, 'class 누락 (권장)');

  // format: tldr/질문
  if (!/>\s*\[!tldr\]/i.test(txt)) report('format', f, '> [!tldr] 누락');
  if (!/##\s*이 노트로 답할 수 있는 질문/.test(txt)) report('format', f, '## 이 노트로 답할 수 있는 질문 누락');

  // broken-link
  for (const m of txt.matchAll(/\[\[([^\]|#]+)/g)) {
    const target = m[1].trim();
    if (target && !noteBasenames.has(target)) report('broken-link', f, `[[${target}]] 대상 없음`);
  }

  // orphan (01~06만, index.md 미등록)
  const rel = path.relative(ROOT, f).replace(/\\/g, '/');
  if (INDEXED_DIRS.some(d => rel.startsWith(d + '/')) && !indexTxt.includes(base)) {
    report('orphan', f, 'index.md에 미등록');
  }
}

// ── raw 점검 (심볼릭 링크 연결 시에만) ──
const rawDir = path.join(ROOT, 'raw');
let rawOk = false;
try { rawOk = fs.statSync(rawDir).isDirectory(); } catch (_) {}
if (rawOk) {
  for (const f of walk(rawDir)) {
    const base = path.basename(f);
    if (base.startsWith('.')) continue;
    // Drive는 한글 파일명을 NFD로 저장하므로 노트의 NFC 경로와 비교 전 정규화
    const rel = path.relative(ROOT, f).replace(/\\/g, '/').normalize('NFC');
    // 통째로 넣은 폴더(레포 덤프 등)는 폴더명의 날짜 접두사로 갈음 — 내부 파일 리네임은 상대경로 링크를 깨뜨림
    if (!rel.split('/').some(seg => /^\d{4}-\d{2}-\d{2} /.test(seg))) report('raw-naming', f, 'YYYY-MM-DD 접두사 없음');
    if (![...sources].some(s => rel === s || rel.startsWith(s))) {
      report('un-ingested', f, '어떤 노트도 source로 참조하지 않음');
    }
  }
}

if (problems.length) {
  console.log(problems.join('\n'));
  console.log(`\n❌ ${problems.length}개 문제 발견`);
  process.exit(1);
}
console.log('✅ lint 깨끗');
process.exit(0);
