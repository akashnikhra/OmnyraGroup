#!/usr/bin/env node
/**
 * OMNyra Exam Portal — CSV → JSON converter (zero dependencies, Node 18+).
 *
 * Converts an admin-authored CSV question set into the canonical versioned
 * JSON envelope validated by tools/validate-questions.mjs.
 *
 * Usage:
 *   node "Exam Portal/tools/csv-to-json.mjs" <input.csv> [--out <output.json>] [envelope flags]
 *
 * Envelope flags (the CSV carries QUESTIONS ONLY — the exam-level envelope
 * comes from filename inference + these flags + admin form fields):
 *   --examId <slug>            kebab-case slug, e.g. tprm-essentials
 *   --title <string>           e.g. "TPRM Essentials — Set A"
 *   --description <string>     optional blurb (omitted from output when empty)
 *   --version <YYYY-MM-DD>     defaults to filename .v<date> or today (UTC)
 *   --durationMinutes <1-600>  default 30
 *   --passPercent <0-100>      default 70
 *   --status <draft|published|archived>  default published
 *   --out <file>               write JSON to file (default: stdout)
 *   --help                     print usage and exit 0
 *
 * CSV contract (canonical header — must match EXACTLY after trim):
 *   id,question,optionA,optionB,optionC,optionD,correctIndex,rationale,topic,difficulty,marks
 * Legacy header `id,question,option1,option2,option3,option4,...` (as emitted
 * by older admin.html downloads) is accepted with a warning and mapped 1:1.
 *
 * Format: UTF-8 (BOM-tolerant), comma delimiter, RFC4180 double-quote
 * quoting (quoted commas/newlines/"" escapes supported). Full-line `#`
 * comments and blank lines are ignored. Difficulty accepts
 * beginner|intermediate|advanced (mapped to easy|medium|hard) as well as
 * easy|medium|hard directly; output is always the canonical easy|medium|hard
 * so the validator passes unchanged.
 *
 * Validation mirrors tools/validate-questions.mjs + admin.html#validate
 * (same thresholds: question/rationale >= 10 chars, 4 distinct options,
 * correctIndex 0-3, marks int 1-100, 1-500 rows, unique ids). KEEP IN SYNC
 * with those two if rules change — this file intentionally duplicates (not
 * imports) the rules so the validator CLI stays byte-for-byte backward
 * compatible.
 *
 * Exit code: 0 = converted (warnings allowed), 1 = failure. Errors are
 * row-numbered: `row <n> (line <m>) [<id>]: <message>`.
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, basename } from "node:path";

const CANONICAL_HEADER = [
  "id", "question",
  "optionA", "optionB", "optionC", "optionD",
  "correctIndex", "rationale", "topic", "difficulty", "marks",
];
const LEGACY_HEADER = [
  "id", "question",
  "option1", "option2", "option3", "option4",
  "correctIndex", "rationale", "topic", "difficulty", "marks",
];

// CSV difficulty → canonical JSON difficulty (validator accepts only the values).
const DIFFICULTY_MAP = {
  beginner: "easy",
  intermediate: "medium",
  advanced: "hard",
  easy: "easy",
  medium: "medium",
  hard: "hard",
};

const TEMPLATE_BASENAMES = new Set(["template", "template-with-examples", "question-template"]);
const ID_RE = /^[A-Za-z0-9][A-Za-z0-9-_:.]{0,120}$/;
const SLUG_RE = /^[a-z0-9][a-z0-9-]{1,60}$/;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const FILENAME_RE = /^(.*)\.v(\d{4}-\d{2}-\d{2})\.csv$/i;
const PLACEHOLDER_RE = /replace-me|fill-me/i;

function usage() {
  return [
    "Usage: node tools/csv-to-json.mjs <input.csv> [--out <output.json>] [envelope flags]",
    "",
    "  --examId <slug>            kebab-case exam slug (default: inferred from",
    "                             questions/<exam-id>.vYYYY-MM-DD.csv, else 'new-exam')",
    "  --title <string>           exam title (default: 'Untitled Set')",
    "  --description <string>     optional blurb (default: omitted)",
    "  --version <YYYY-MM-DD>     default: filename .v<date> or today (UTC)",
    "  --durationMinutes <1-600>  default 30",
    "  --passPercent <0-100>      default 70",
    "  --status <draft|published|archived>  default published",
    "  --out <file>               write JSON to file (default: stdout)",
    "  --help                     print this help and exit 0",
    "",
    "Example:",
    '  node tools/csv-to-json.mjs questions/tprm-essentials.v2026-09-14.csv \\',
    '    --examId tprm-essentials --title "TPRM Essentials — Set A" \\',
    "    --out questions/tprm-essentials.v2026-09-14.json",
  ].join("\n");
}

function parseArgs(argv) {
  const opts = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") return { help: true };
    if (a.startsWith("--")) {
      const eq = a.indexOf("=");
      const key = eq === -1 ? a.slice(2) : a.slice(2, eq);
      let val = eq === -1 ? argv[++i] : a.slice(eq + 1);
      if (val === undefined) return { error: `missing value for ${a}` };
      if (!["out", "examId", "title", "description", "version", "durationMinutes", "passPercent", "status"].includes(key)) {
        return { error: `unknown argument --${key}\n${usage()}` };
      }
      opts[key] = val;
    } else {
      positional.push(a);
    }
  }
  return { opts, positional };
}

/**
 * RFC4180 record parser. Returns [{ cells: string[], line: number }]
 * where `line` is the 1-based source line the record starts on.
 * Normalizes CRLF/CR to LF first (bare CR inside fields is not preserved).
 */
function parseCsvRecords(text) {
  const src = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  const records = [];
  let field = "";
  let row = [];
  let inQuotes = false;
  let line = 1;
  let recordLine = 1;
  let cellHasContent = false; // any char (incl. quotes/whitespace) seen in current record

  function endField() {
    row.push(field);
    field = "";
  }
  function endRecord() {
    // Only keep records that had content; pure-empty trailing newline yields nothing.
    if (cellHasContent || row.length > 0) records.push({ cells: row, line: recordLine });
    row = [];
    cellHasContent = false;
    recordLine = line + 1; // next record starts after this newline (adjusted below for \n handling)
  }

  for (let i = 0; i < src.length; i++) {
    const c = src[i];
    if (inQuotes) {
      if (c === '"') {
        if (src[i + 1] === '"') { field += '"'; cellHasContent = true; i++; }
        else inQuotes = false;
      } else {
        field += c;
        cellHasContent = true;
        if (c === "\n") line++;
      }
    } else if (c === '"') {
      inQuotes = true;
      cellHasContent = true;
    } else if (c === ",") {
      endField();
    } else if (c === "\n") {
      endField();
      // recordLine already set; fix: record started at recordLine
      if (cellHasContent || row.some((x) => x !== "")) {
        records.push({ cells: row, line: recordLine });
      }
      row = [];
      field = "";
      cellHasContent = false;
      line++;
      recordLine = line;
    } else {
      field += c;
      if (c !== " " && c !== "\t") cellHasContent = true;
      else if (field.trim() !== "" || row.length > 0) cellHasContent = true;
      // whitespace-only fields still count once the record has any cell boundary
    }
  }
  if (inQuotes) throw new Error("unterminated quoted field (missing closing \")");
  endField();
  if (cellHasContent || row.some((x) => x !== "")) records.push({ cells: row, line: recordLine });

  // Drop the phantom empty record from a single trailing newline: handled above
  // by the cellHasContent guard. Filter whitespace-only blank records here.
  return records.filter((r) => r.cells.some((c) => c.trim() !== "") || r.cells[0].trim().startsWith("#"));
}

function isCommentRecord(rec) {
  return rec.cells[0].trim().startsWith("#");
}

function todayUtc() {
  return new Date().toISOString().slice(0, 10);
}

function fail(input, errors, warnings) {
  for (const w of warnings) console.error(`   ~ ${w}`);
  console.error(`FAIL  ${input}  (${errors.length} error${errors.length === 1 ? "" : "s"})`);
  for (const e of errors) console.error(`   - ${e}`);
  process.exit(1);
}

function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (parsed.help) {
    console.log(usage());
    process.exit(0);
  }
  if (parsed.error) {
    console.error(parsed.error);
    process.exit(1);
  }
  const { opts, positional } = parsed;
  if (positional.length !== 1) {
    console.error(usage());
    process.exit(1);
  }
  const input = positional[0];
  const warnings = [];
  const errors = [];

  let raw;
  try {
    raw = readFileSync(input, "utf8").replace(/^﻿/, ""); // strip UTF-8 BOM
  } catch (e) {
    console.error(`FAIL  ${input}  (1 error)`);
    console.error(`   - file: cannot read file: ${e.message}`);
    process.exit(1);
  }

  let records;
  try {
    records = parseCsvRecords(raw);
  } catch (e) {
    console.error(`FAIL  ${input}  (1 error)`);
    console.error(`   - file: CSV parse error: ${e.message}`);
    process.exit(1);
  }

  const data = records.filter((r) => !isCommentRecord(r));
  if (data.length === 0) {
    console.error(`FAIL  ${input}  (1 error)`);
    console.error("   - file: CSV needs a header row + at least 1 data row.");
    process.exit(1);
  }

  // ---- header ----
  const headerRec = data[0];
  const header = headerRec.cells.map((h) => h.trim());
  const sameAs = (want) => header.length === want.length && header.every((h, i) => h === want[i]);
  let optKeys;
  if (sameAs(CANONICAL_HEADER)) {
    optKeys = ["optionA", "optionB", "optionC", "optionD"];
  } else if (sameAs(LEGACY_HEADER)) {
    optKeys = ["option1", "option2", "option3", "option4"];
    warnings.push(
      "header: legacy option1..option4 detected — accepted, but prefer canonical optionA..optionD (see questions/template.csv)"
    );
  } else {
    console.error(`FAIL  ${input}  (1 error)`);
    console.error(`   - header (line ${headerRec.line}): expected exactly:`);
    console.error(`     ${CANONICAL_HEADER.join(",")}`);
    console.error(`     got: ${header.join(",")}`);
    process.exit(1);
  }

  // ---- envelope defaults (CSV carries QUESTIONS ONLY) ----
  const base = basename(input).replace(/\.csv$/i, "");
  const m = base.match(FILENAME_RE);
  let examId = opts.examId;
  let version = opts.version;
  if (!examId) {
    if (m) examId = m[1].toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
    else if (!TEMPLATE_BASENAMES.has(base.toLowerCase())) {
      examId = base.toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "") || "new-exam";
      warnings.push(`envelope: examId inferred from filename as "${examId}" — confirm with --examId <slug>`);
    } else {
      examId = "new-exam";
      warnings.push('envelope: template file has no exam slug — using examId "new-exam"; pass --examId <slug> for real publishes');
    }
  }
  if (!version) version = m ? m[2] : todayUtc();
  const title = opts.title !== undefined ? opts.title : "Untitled Set";
  if (opts.title === undefined) warnings.push('envelope: no --title given — using "Untitled Set"');
  const description = opts.description !== undefined ? opts.description : "";
  const durationMinutes = opts.durationMinutes !== undefined ? Number(opts.durationMinutes) : 30;
  const passPercent = opts.passPercent !== undefined ? Number(opts.passPercent) : 70;
  const status = opts.status !== undefined ? opts.status : "published";

  // envelope validation (mirrors validate-questions.mjs envelope rules)
  if (typeof examId !== "string" || examId.trim() === "") errors.push("envelope: examId is required (kebab-case slug, e.g. \"tprm-essentials\")");
  else if (!SLUG_RE.test(examId.trim())) errors.push(`envelope: examId must be a kebab-case slug 2-61 chars (got "${examId}")`);
  if (typeof title !== "string" || title.trim() === "") errors.push("envelope: title is required (pass --title \"...\")");
  if (typeof version !== "string" || version.trim() === "") errors.push("envelope: version is required (pass --version YYYY-MM-DD)");
  else if (!DATE_RE.test(version.trim())) warnings.push(`envelope: recommend version "YYYY-MM-DD" for dated versioning (got "${version}")`);
  if (!Number.isInteger(durationMinutes) || durationMinutes < 1 || durationMinutes > 600) {
    errors.push(`envelope: durationMinutes must be integer 1-600 (got ${opts.durationMinutes})`);
  }
  if (typeof passPercent !== "number" || Number.isNaN(passPercent) || passPercent < 0 || passPercent > 100) {
    errors.push(`envelope: passPercent must be 0-100 (got ${opts.passPercent})`);
  }
  if (!["draft", "published", "archived"].includes(status)) {
    errors.push(`envelope: status must be draft|published|archived (got "${status}")`);
  }

  // ---- rows ----
  const rows = data.slice(1);
  if (rows.length === 0) errors.push("file: CSV needs at least 1 data row below the header.");
  if (rows.length > 500) errors.push(`file: max 500 questions per file (got ${rows.length})`);

  const questions = [];
  const seenIds = new Set();
  let aliasUsed = false;

  rows.forEach((rec, idx) => {
    const rowNum = idx + 1;
    const tag = (id) => `row ${rowNum} (line ${rec.line})${id ? ` [${id}]` : ""}`;
    const cells = rec.cells;
    if (cells.length > header.length) {
      errors.push(`${tag(cells[0].trim())}: expected ${header.length} columns, got ${cells.length} (check for unquoted commas)`);
      return;
    }
    const get = (name) => {
      const i = header.indexOf(name);
      return i === -1 || i >= cells.length ? "" : cells[i];
    };
    const idRaw = get("id").trim();
    const questionRaw = get("question");
    const optsRaw = optKeys.map((k) => get(k));
    const correctRaw = get("correctIndex").trim();
    const rationaleRaw = get("rationale");
    const topicRaw = get("topic");
    const diffRaw = get("difficulty").trim();
    const marksRaw = get("marks").trim();

    // Placeholder guard: template.csv is a fill-me guide, never publishable as-is.
    const haystack = [idRaw, questionRaw, ...optsRaw, rationaleRaw, topicRaw];
    if (haystack.some((v) => PLACEHOLDER_RE.test(String(v)))) {
      errors.push(
        `${tag(idRaw)}: contains placeholder text (REPLACE-ME / FILL-ME) — template.csv is a fill-me guide; replace every placeholder with real content (or copy questions/template-with-examples.csv as a starting point) before converting`
      );
      return;
    }

    // id (same rule as validator; plus lowercase-hyphen recommendation for new slugs)
    let id = null;
    if (idRaw === "") errors.push(`${tag("")}: id: required non-empty string`);
    else if (!ID_RE.test(idRaw)) errors.push(`${tag(idRaw)}: id: must be 1-121 chars, alphanumerics plus - _ : .`);
    else if (seenIds.has(idRaw)) errors.push(`${tag(idRaw)}: id: duplicate id "${idRaw}"`);
    else {
      seenIds.add(idRaw);
      id = idRaw;
      if (!/^[a-z0-9][a-z0-9-]{0,60}$/.test(idRaw)) {
        warnings.push(`${tag(idRaw)}: id: prefer a lowercase-hyphen slug (e.g. grc-001) for new questions`);
      }
    }

    // question stem
    if (questionRaw.trim() === "") errors.push(`${tag(idRaw)}: question: required non-empty string`);
    else if (questionRaw.trim().length < 10) errors.push(`${tag(idRaw)}: question: must be >= 10 chars`);

    // options: exactly 4 non-empty distinct
    const opts = [];
    let optsOk = true;
    if (optsRaw.some((o) => o === undefined)) {
      errors.push(`${tag(idRaw)}: options: required exactly 4 option columns`);
      optsOk = false;
    } else {
      optsRaw.forEach((o, i) => {
        if (o.trim() === "") {
          errors.push(`${tag(idRaw)}: ${optKeys[i]}: must be a non-empty string (exactly 4 options required)`);
          optsOk = false;
        } else opts.push(o.trim());
      });
      if (opts.length === 4 && new Set(opts.map((o) => o.toLowerCase())).size !== 4) {
        errors.push(`${tag(idRaw)}: options: all 4 options must be distinct (case-insensitive)`);
        optsOk = false;
      }
    }

    // correctIndex
    let correctIndex = null;
    if (!/^\d+$/.test(correctRaw)) errors.push(`${tag(idRaw)}: correctIndex: required integer 0-3 (0=A, 1=B, 2=C, 3=D)`);
    else {
      correctIndex = Number(correctRaw);
      if (!Number.isInteger(correctIndex) || correctIndex < 0 || correctIndex > 3) {
        errors.push(`${tag(idRaw)}: correctIndex: must be 0-3 (got ${correctRaw})`);
        correctIndex = null;
      }
    }

    // rationale
    if (rationaleRaw.trim() === "") errors.push(`${tag(idRaw)}: rationale: required non-empty string`);
    else if (rationaleRaw.trim().length < 10) errors.push(`${tag(idRaw)}: rationale: must be >= 10 chars (explain WHY)`);

    // topic
    if (topicRaw.trim() === "") errors.push(`${tag(idRaw)}: topic: required non-empty string (e.g. "TPRM")`);

    // difficulty (alias-tolerant, canonical output)
    let difficulty = null;
    const dKey = diffRaw.toLowerCase();
    if (dKey === "") errors.push(`${tag(idRaw)}: difficulty: required, one of beginner|intermediate|advanced (or easy|medium|hard)`);
    else if (!Object.prototype.hasOwnProperty.call(DIFFICULTY_MAP, dKey)) {
      errors.push(`${tag(idRaw)}: difficulty: must be one of beginner|intermediate|advanced (got "${diffRaw}")`);
    } else {
      difficulty = DIFFICULTY_MAP[dKey];
      if (["beginner", "intermediate", "advanced"].includes(dKey)) aliasUsed = true;
    }

    // marks
    let marks = null;
    if (!/^\d+$/.test(marksRaw)) errors.push(`${tag(idRaw)}: marks: required positive integer`);
    else {
      marks = Number(marksRaw);
      if (!Number.isInteger(marks) || marks < 1 || marks > 100) {
        errors.push(`${tag(idRaw)}: marks: must be 1-100 (got ${marksRaw})`);
        marks = null;
      }
    }

    const rowErrorsBefore = errors.length;
    questions.push({ id, question: questionRaw.trim(), options: opts, correctIndex, rationale: rationaleRaw.trim(), topic: topicRaw.trim(), difficulty, marks, _rowNum: rowNum, _line: rec.line });
    // Remove the speculative push if this row errored (keep output clean on failure path).
    if (errors.length !== rowErrorsBefore) questions.pop();
    void optsOk;
  });

  if (aliasUsed) warnings.push("difficulty: beginner|intermediate|advanced mapped to canonical easy|medium|hard in output");

  if (errors.length > 0) fail(input, errors, warnings);

  const envelope = {
    examId: examId.trim(),
    title: title.trim(),
    ...(description.trim() !== "" ? { description: description.trim() } : {}),
    version: version.trim(),
    durationMinutes,
    passPercent,
    status,
    questions: questions.map(({ _rowNum, _line, ...q }) => q),
  };

  const json = JSON.stringify(envelope, null, 2) + "\n";
  const dest = opts.out;
  if (dest) {
    try {
      mkdirSync(dirname(dest), { recursive: true });
      writeFileSync(dest, json, "utf8");
    } catch (e) {
      console.error(`FAIL  ${input}  (1 error)`);
      console.error(`   - file: cannot write output: ${e.message}`);
      process.exit(1);
    }
    console.error(`PASS  ${input}  →  ${dest}  (${questions.length} question${questions.length === 1 ? "" : "s"}; examId=${envelope.examId} version=${envelope.version})`);
  } else {
    process.stdout.write(json);
    console.error(`PASS  ${input}  (${questions.length} question${questions.length === 1 ? "" : "s"}; examId=${envelope.examId} version=${envelope.version})`);
  }
  for (const w of warnings) console.error(`   ~ ${w}`);
}

main();
