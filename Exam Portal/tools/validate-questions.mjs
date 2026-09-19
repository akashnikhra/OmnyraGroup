#!/usr/bin/env node
/**
 * OMNyra Exam Portal — question-set validator (zero dependencies).
 *
 * Usage:
 *   node Exam Portal/tools/validate-questions.mjs <file.json> [more.json ...]
 *
 * Accepts either:
 *   A) Envelope format: { examId, title, version, durationMinutes, passPercent, questions: [...] }
 *   B) Bare array format: [ {...question...}, ... ]
 *
 * Question contract (required — mirrors admin.html#validate canonical rules):
 *   id           : non-empty unique string (slug, e.g. "q01", "grc-001")
 *   question     : non-empty string (>= 10 chars)
 *   options      : array of exactly 4 non-empty distinct strings
 *   correctIndex : integer 0..3
 *   rationale    : non-empty string (>= 10 chars)
 *   topic        : non-empty string (e.g. "TPRM")
 *   difficulty   : "easy" | "medium" | "hard"
 *   marks        : integer 1..100
 *
 * Envelope fields: examId + title + questions are REQUIRED.
 *   version (any non-empty string; "YYYY-MM-DD" recommended for dated
 *   versioning), durationMinutes (int 1-600) and passPercent (0-100) are
 *   RECOMMENDED — missing/non-standard values emit warnings, not errors,
 *   so existing fixtures (e.g. semver versions) keep passing.
 *
 * Exit code: 0 = all files valid (warnings allowed), 1 = any failure.
 */

import { readFileSync } from "node:fs";

const DIFFICULTIES = new Set(["easy", "medium", "hard"]);

function isNonEmptyString(v) {
  return typeof v === "string" && v.trim().length > 0;
}

function validateQuestion(q, index, seenIds) {
  const errs = [];
  const where = `questions[${index}]${q && q.id ? ` (${q.id})` : ""}`;

  if (!q || typeof q !== "object" || Array.isArray(q)) {
    return [`${where}: must be an object`];
  }

  // id
  if (!isNonEmptyString(q.id)) {
    errs.push(`${where}.id: required non-empty string`);
  } else if (!/^[A-Za-z0-9][A-Za-z0-9-_:.]{0,120}$/.test(q.id.trim())) {
    errs.push(`${where}.id: must be 1-121 chars, alphanumerics plus - _ : .`);
  } else if (seenIds.has(q.id.trim())) {
    errs.push(`${where}.id: duplicate id "${q.id.trim()}"`);
  } else {
    seenIds.add(q.id.trim());
  }

  // question stem
  if (!isNonEmptyString(q.question)) {
    errs.push(`${where}.question: required non-empty string`);
  } else if (q.question.trim().length < 10) {
    errs.push(`${where}.question: must be >= 10 chars`);
  }

  // options
  if (!Array.isArray(q.options)) {
    errs.push(`${where}.options: required array of exactly 4 strings`);
  } else if (q.options.length !== 4) {
    errs.push(`${where}.options: must have exactly 4 entries (got ${q.options.length})`);
  } else {
    const norm = [];
    q.options.forEach((opt, i) => {
      if (!isNonEmptyString(opt)) {
        errs.push(`${where}.options[${i}]: must be a non-empty string`);
      } else {
        norm.push(opt.trim().toLowerCase());
      }
    });
    if (norm.length === 4 && new Set(norm).size !== 4) {
      errs.push(`${where}.options: all 4 options must be distinct (case-insensitive)`);
    }
  }

  // correctIndex
  if (typeof q.correctIndex !== "number" || !Number.isInteger(q.correctIndex)) {
    errs.push(`${where}.correctIndex: required integer 0-3`);
  } else if (q.correctIndex < 0 || q.correctIndex > 3) {
    errs.push(`${where}.correctIndex: must be 0-3 (got ${q.correctIndex})`);
  }

  // rationale
  if (!isNonEmptyString(q.rationale)) {
    errs.push(`${where}.rationale: required non-empty string`);
  } else if (q.rationale.trim().length < 10) {
    errs.push(`${where}.rationale: must be >= 10 chars (explain WHY)`);
  }

  // topic
  if (!isNonEmptyString(q.topic)) {
    errs.push(`${where}.topic: required non-empty string (e.g. "Risk Management")`);
  }

  // difficulty
  if (!isNonEmptyString(q.difficulty)) {
    errs.push(`${where}.difficulty: required, one of easy|medium|hard`);
  } else if (!DIFFICULTIES.has(q.difficulty.trim().toLowerCase())) {
    errs.push(`${where}.difficulty: must be one of easy|medium|hard (got "${q.difficulty}")`);
  }

  // marks
  if (typeof q.marks !== "number" || !Number.isInteger(q.marks)) {
    errs.push(`${where}.marks: required positive integer`);
  } else if (q.marks < 1 || q.marks > 100) {
    errs.push(`${where}.marks: must be 1-100 (got ${q.marks})`);
  }

  return errs;
}

function validateEnvelope(doc, label) {
  const errs = [];
  const warnings = [];
  let questions = null;

  if (Array.isArray(doc)) {
    // Bare-array mode: no envelope checks.
    questions = doc;
    if (questions.length === 0) errs.push(`${label}: array must contain >= 1 question`);
    if (questions.length > 500) errs.push(`${label}: max 500 questions per file (got ${questions.length})`);
    return { errs, warnings, questions, mode: "bare-array" };
  }

  if (!doc || typeof doc !== "object") {
    return { errs: [`${label}: root must be an object or an array`], warnings, questions: null, mode: "invalid" };
  }

  // Envelope mode
  if (!isNonEmptyString(doc.examId)) {
    errs.push("examId: required non-empty slug string (e.g. \"grc-fundamentals\")");
  } else if (!/^[a-z0-9][a-z0-9-]{1,60}$/.test(doc.examId.trim())) {
    errs.push(`examId: must be kebab-case slug 2-61 chars (got "${doc.examId}")`);
  }
  if (!isNonEmptyString(doc.title)) errs.push("title: required non-empty string");
  if (!isNonEmptyString(doc.version)) {
    errs.push('version: required non-empty string (date "YYYY-MM-DD" recommended)');
  } else if (!/^\d{4}-\d{2}-\d{2}$/.test(doc.version.trim())) {
    warnings.push(`version: recommend "YYYY-MM-DD" for dated versioning (got "${doc.version}")`);
  }
  if (doc.durationMinutes !== undefined) {
    if (!Number.isInteger(doc.durationMinutes) || doc.durationMinutes <= 0 || doc.durationMinutes > 600) {
      errs.push(`durationMinutes: must be integer 1-600 (got ${doc.durationMinutes})`);
    }
  } else {
    warnings.push("durationMinutes: missing — frontend defaults apply (recommend e.g. 30)");
  }
  if (doc.passPercent !== undefined) {
    if (typeof doc.passPercent !== "number" || doc.passPercent < 0 || doc.passPercent > 100) {
      errs.push(`passPercent: must be 0-100 (got ${doc.passPercent})`);
    }
  } else {
    warnings.push("passPercent: missing — frontend defaults apply (recommend e.g. 70)");
  }
  if (!Array.isArray(doc.questions)) {
    errs.push("questions: required array of question objects");
    return { errs, questions: null, mode: "envelope" };
  }
  questions = doc.questions;
  if (questions.length === 0) errs.push("questions: must contain >= 1 question");
  if (questions.length > 500) errs.push(`questions: max 500 per file (got ${questions.length})`);

  // Optional: cross-check filename hint is done by caller; examId/file consistency checked in BACKEND.md flow.
  return { errs, warnings, questions, mode: "envelope" };
}

function validateFile(path) {
  let raw;
  try {
    raw = readFileSync(path, "utf8").replace(/^﻿/, ""); // strip UTF-8 BOM (Windows editors)
  } catch (e) {
    return { path, ok: false, errors: [`cannot read file: ${e.message}`] };
  }
  let doc;
  try {
    doc = JSON.parse(raw);
  } catch (e) {
    return { path, ok: false, errors: [`invalid JSON: ${e.message}`] };
  }

  const { errs, warnings, questions } = validateEnvelope(doc, path);
  const errors = [...errs];
  if (questions) {
    const seenIds = new Set();
    questions.forEach((q, i) => {
      errors.push(...validateQuestion(q, i, seenIds));
    });
  }
  return { path, ok: errors.length === 0, errors, warnings: warnings || [], count: questions ? questions.length : 0 };
}

// ---- CLI ----
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error("Usage: node tools/validate-questions.mjs <file.json> [more.json ...]");
  process.exit(1);
}

let failed = 0;
for (const path of args) {
  const r = validateFile(path);
  if (r.ok) {
    console.log(`PASS  ${r.path}  (${r.count} question${r.count === 1 ? "" : "s"})`);
    for (const w of r.warnings || []) console.log(`   ~ ${w}`);
  } else {
    failed += 1;
    console.log(`FAIL  ${r.path}  (${r.errors.length} error${r.errors.length === 1 ? "" : "s"})`);
    for (const e of r.errors) console.log(`   - ${e}`);
  }
}
process.exit(failed === 0 ? 0 : 1);
