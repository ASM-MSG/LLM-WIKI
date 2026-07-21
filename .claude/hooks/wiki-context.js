#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

let raw = '';
try { raw = fs.readFileSync(0, 'utf8'); } catch (_) {}
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
let data = {};
try { data = JSON.parse(raw || '{}'); } catch (_) {}
const prompt = String(data.prompt || '').trim();
if (!prompt) process.exit(0);
const promptLC = prompt.toLowerCase();

// 메타작업이면 주입 생략
const SKIP = /(스킬\s*(제작|만들|작성|추가|수정)|\bskill\b|\bhook\b|훅\b|\.claude|settings\.json|wiki-(lint|ingest|archive)|frontmatter)/i;
if (SKIP.test(prompt)) process.exit(0);

const ROOT = process.env.CLAUDE_PROJECT_DIR || path.resolve(__dirname, '..', '..');
const SEARCH_DIRS = ['00-inbox','01-product','02-planning','03-specs',
                     '04-decisions','05-meetings','06-research',
                     '07-individual','90-archive'];

function walk(dir, out) {
  let ents = [];
  try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch (_) { return; }
  for (const e of ents) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile() && e.name.toLowerCase().endsWith('.md')) out.push(p);
  }
}
const files = [];
for (const d of SEARCH_DIRS) walk(path.join(ROOT, d), files);

function arrayField(fm, key) {
  const m = fm.match(new RegExp('^' + key + ':\\s*\\[([^\\]]*)\\]', 'm'));
  if (!m) return [];
  return m[1].split(',').map(s => s.replace(/['"]/g, '').trim()).filter(Boolean);
}
function scalarField(fm, key) {
  const m = fm.match(new RegExp('^' + key + ':\\s*(.+)$', 'm'));
  return m ? m[1].replace(/['"]/g, '').trim() : '';
}
const promptTokens = new Set((promptLC.match(/[a-z0-9]+|[가-힣]+/g) || []).filter(t => t.length >= 2));

const hits = [];
for (const file of files) {
  let txt = '';
  try { txt = fs.readFileSync(file, 'utf8'); } catch (_) { continue; }
  const fmMatch = txt.match(/^---\n([\s\S]*?)\n---/);
  const fm = fmMatch ? fmMatch[1] : '';
  const title = scalarField(fm, 'title');
  const source = scalarField(fm, 'source');
  const author = scalarField(fm, 'author');
  const terms = [...arrayField(fm, 'aliases'), ...arrayField(fm, 'keywords')];

  let score = 0;
  const matched = new Set();
  const scoreTerm = (term, fullBonus) => {
    const t = term.toLowerCase();
    if (t.length < 2) return;
    if (promptLC.includes(t)) { score += fullBonus; matched.add(term); return; }
    const parts = t.split(/\s+/).filter(p => p.length >= 2);
    if (parts.length < 2) return;
    let pm = 0;
    for (const p of parts) if (promptLC.includes(p)) pm++;
    if (pm >= 2) { score += pm; matched.add(term); }
  };
  for (const term of terms) scoreTerm(term, Math.min(term.length, 8));
  if (title) scoreTerm(title, 10);

  const qsec = txt.match(/##\s*이 노트로 답할 수 있는 질문([\s\S]*?)(\n##\s|$)/);
  if (qsec) {
    const qTokens = qsec[1].toLowerCase().match(/[a-z0-9]+|[가-힣]+/g) || [];
    let overlap = 0;
    for (const qt of qTokens) if (qt.length >= 2 && promptTokens.has(qt)) overlap++;
    score += Math.min(overlap, 6);
  }
  if (score >= 3) {
    hits.push({ rel: path.relative(ROOT, file).replace(/\\/g, '/'), source, author, score, matched: [...matched].slice(0, 6) });
  }
}

if (!hits.length) {
  process.stdout.write('[WIKI] 이 질문과 직접 매칭되는 compiled 노트를 찾지 못했습니다. index.md를 직접 확인하거나, 위키에 근거가 없으면 답변에 "위키에 근거 없음"을 명시하세요.\n');
  process.exit(0);
}

// 팀 노트와 개인 의견(07-individual)을 분리
const teamHits = hits.filter(h => !h.rel.startsWith('07-individual/')).sort((a, b) => b.score - a.score);
const indivHits = hits.filter(h => h.rel.startsWith('07-individual/')).sort((a, b) => b.score - a.score);

let out = '';
if (teamHits.length) {
  out += '[WIKI HITS — 답하기 전에 아래 노트를 Read하고 source(raw 경로)를 인용해 답하라]\n';
  for (const h of teamHits.slice(0, 6)) {
    out += `- ${h.rel}\n`;
    if (h.source) out += `    source: ${h.source}\n`;
    if (h.matched.length) out += `    매칭: ${h.matched.join(', ')}\n`;
  }
}
if (indivHits.length) {
  out += (teamHits.length ? '\n' : '') + '[개인 의견 — 참고용·낮은 우선순위 (팀 합의/canon 아님)]\n';
  for (const h of indivHits.slice(0, 3)) {
    out += `- ${h.rel}${h.author ? ` (작성자: ${h.author})` : ''}\n`;
    if (h.source) out += `    source: ${h.source}\n`;
    if (h.matched.length) out += `    매칭: ${h.matched.join(', ')}\n`;
  }
}
out += '규칙: 위 노트를 근거로 종합하고 raw 출처를 인용할 것. 위 노트에 근거가 없는 내용은 "위키에 근거 없음"으로 명시. ';
out += '개인 의견 블록은 팀 근거(canon/log/decision)와 구분해 "~님의 개인 의견(참고)"임을 밝히고 참고로만 인용.\n';
process.stdout.write(out);
process.exit(0);
