#!/usr/bin/env node
/**
 * canon-guard — canon 문서 수정/삭제를 막되,
 * 직전 사용자 발화에 승인 문구가 있으면 1회 통과.
 */
const fs = require('fs');
const path = require('path');

const CANON_BASENAMES = ['GOAL.md', 'ICP.md', 'VALUE.md', 'SCHEMA.md', 'glossary.md'];
const approvalRe = (b) => new RegExp('APPROVE\\s+CANON\\s*:?\\s*' + b.replace('.', '\\.'), 'i');

let raw = ''; try { raw = fs.readFileSync(0, 'utf8'); } catch (e) {}
let input = {}; try { input = JSON.parse(raw); } catch (e) { process.exit(0); }

const ti = input.tool_input || {};
const targets = [];
if (ti.file_path) targets.push(ti.file_path);
if (ti.notebook_path) targets.push(ti.notebook_path);
if (ti.command) for (const b of CANON_BASENAMES) if (ti.command.includes(b)) targets.push(b);

function canonHit(t) {
  const base = path.basename(t);
  if (CANON_BASENAMES.includes(base)) return base;
  try {
    if (fs.existsSync(t)) {
      const head = fs.readFileSync(t, 'utf8').slice(0, 800);
      if (/^---[\s\S]*?\bclass:\s*canon\b[\s\S]*?---/m.test(head)) return base;
    }
  } catch (e) {}
  return null;
}
const hits = [...new Set(targets.map(canonHit).filter(Boolean))];
if (hits.length === 0) process.exit(0);

function lastUserText() {
  try {
    const tp = input.transcript_path;
    if (!tp || !fs.existsSync(tp)) return '';
    const lines = fs.readFileSync(tp, 'utf8').trim().split(/\r?\n/);
    for (let i = lines.length - 1; i >= 0; i--) {
      let e; try { e = JSON.parse(lines[i]); } catch (_) { continue; }
      if (e.type !== 'user' || !e.message) continue;
      const c = e.message.content;
      if (typeof c === 'string') return c;
      if (Array.isArray(c)) {
        const txt = c.filter(x => x && x.type === 'text').map(x => x.text).join('\n');
        if (!txt && c.some(x => x && x.type === 'tool_result')) continue;
        return txt;
      }
    }
  } catch (e) {}
  return '';
}
const userText = lastUserText();
const notApproved = hits.filter(b => !approvalRe(b).test(userText));
if (notApproved.length === 0) process.exit(0);

process.stderr.write([
  `🛑 CANON GUARD: "${notApproved.join(', ')}" 은(는) 단일 진실(canon) 문서다. 자동 수정 금지.`,
  ``,
  `지금 작업을 멈추고 사용자에게 제시하라:`,
  `  1) 어떤 canon 파일을·왜 바꾸는지   2) 정확한 변경(before→after diff)`,
  `사용자가 아래를 그대로 입력하기 전엔 재시도하지 마라:`,
  notApproved.map(b => `     APPROVE CANON: ${b}`).join('\n'),
  ``,
  `승인 문구를 스스로 만들거나 마커 파일로 우회하지 마라. 승인은 오직 사용자의 입력이어야 한다.`,
].join('\n') + '\n');
process.exit(2);
