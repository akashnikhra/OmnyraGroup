# AIGP Mock Tests from 460 MCQs — Design (Option A)

Date: 2026-10-03 | Status: approved sections §1–§4 | Source: `Exam Portal/AIGP Exam/` (4 docx, 460 scenario MCQs)

## Goal
Create multiple separate AIGP mock tests mirroring the real AIGP certification pattern
(100 multiple-choice/scenario questions, max 3h = 2.75h testing + 15-min break,
85 scored + 15 unscored, scaled 100–500 pass at 300) with Udemy-style pre-exam
instructions (Images 1–5 provided by user). Exam-only + instructions scope.

## Context (verified)
- Set1 `AIGP_Practice_Questions.docx` (67 KB): 150 Qs, 150 `Domain: NN - Name`, 150 explanations, 150 green-marked correct + 150-cell answer table.
- Set2 `AIGP_Practice_Questions_Set2.docx` (69 KB): same counts, different domains.
- Set3 `AIGP_Practice_Questions_Set3.docx` (32 KB): 60 Qs, 60 explanations, NO domain lines.
- Set4 `AIGP_Practice_Questions_Set4.docx` (55 KB): 100 Qs, `Domain: D1–D4` short codes.
- Screenshots: Udemy Practice Test 1 — Practice mode (instant check-answer, domain filter,
  bookmark/skip, pause/resume, retake) vs Exam mode (timed, palette, finish, results with
  green correct answer). Reference only; Practice mode is OUT of scope.
- Portal: static-first + Supabase; question contract in `Exam Portal/BACKEND.md` §2.4 and
  `tools/validate-questions.mjs`; catalog `questions/manifest.json`; runners
  `exam.html` + `student/exam.html` (timer, palette, autosave 15s, submit modal);
  results `result.html` + `student/result.html`. Existing `questions/aigp-mock-1.v2026-09-19.json`
  (100 items) is untouched.

## Decision log
- Split: rebalance all 460 (not per-set blocks).
- Length: switch from requested 150Q to real-exam 100Q → 4 × 100 + 60 spare.
- Timing/pass: 165 min testing window, `passPercent: 70` documented proxy for scaled 300/500.
- Modes: exam-only + pre-exam instruction screen. No instant-feedback practice mode.

## §1 Data split & file contract (APPROVED — separate mocks, no shared Qs)
- Stratified rebalance per 100Q mock: ~33 Set1 + ~33 Set2 + ~13 Set3 + ~21 Set4, fixed-seed
  shuffle so domains intermix. Leftover 60 (~17/17/8/18) → `aigp-spare-pool.json` (validated,
  NOT cataloged) for future rotation.
- `topic` = source `Domain:` string verbatim; Set3 → `General`. No re-taxonomy.
- New IDs `aigp-practice-1..4`; files `questions/aigp-practice-N.v2026-10-04.json`;
  `examId` matches file; `title: AIGP Practice Mock N`; `version: 2026-10-04`;
  `durationMinutes: 165`; `passPercent: 70`; `status: published`; per-Q
  `difficulty: medium`, `marks: 1`, `correctIndex` from green-mark cross-checked against
  answer table, `rationale` from `Explanation:`.
- Manifest: 4 new published entries + bumped `updatedAt`. Spare pool not listed.

## §2 Pre-exam instruction screen (APPROVED, amended 2026-10-05: timer starts at Begin test)
Untimed instruction screen on `student/exam.html` (`exam.html?exam=<id>`, no attempt
created, no ticking timer). The timed attempt — and its server deadline
`attempt.startedAt + durationMinutes` — is created only when Begin test is clicked
(`start_attempt` moved from catalog Start to Begin; resume-or-create handled on the
pre-start screen, no backend/RPC changes). Copy: "The timer starts when you click
Begin test — reading this screen is untimed." `?attempt=` sessions boot straight
into questions. Text:
“AIGP Practice Mock N — 100 questions | 2 hours 45 minutes | 70% required to pass
(≈ proxy for scaled 300). You can pause and resume later. You can retake as many times
as you like. Progress bar shows progress + time remaining; you may still finish after
timeout. Flag for review or skip and return via palette. Click Begin test to reveal
questions; Finish test to finish and see results.”

## §3 Runner + results (APPROVED)
Reuse runner exactly: countdown, progress bar, Answered/Unanswered/Flagged palette,
flag + Skip, Finish modal with counts, 15s autosave, timeout auto-submit, resume via
`activeAttempt`. Results: score ring + topic breakdown (raw Domain strings) + per-question
review (stem, your answer, green correct answer, rationale). Retake = fresh attempt,
fixed order by default. No grading/RPC changes.

## §4 Validation, rollout & scope limits (APPROVED)
- Each JSON must pass `node tools/validate-questions.mjs` (exit 0): 100 Qs, unique kebab
  IDs, stem ≥10ch, 4 distinct options, `correctIndex` green-vs-table match, rationale ≥10ch,
  manifest id/version/count consistency.
- Commit new JSONs + spare pool + manifest bump. Smoke test: catalog → instruction →
  timer → submit → graded results with green correct + rationale → retake. Supabase seed
  later via `admin.html` Path A; no schema/RPC change.
- Ambiguity rule: any failing question is held out and replaced by next spare from same
  source set; never ship a validator failure.
- OUT of scope (deferred Option B): instant-feedback practice mode, domain filter,
  true 85/15 unscored split, scaled 100–500 scoring, break timer.

## Self-review
- Placeholders: none — all counts, IDs, durations, copy finalized above.
- Consistency: §1 (4×100 separate) ↔ §4 (manifest/validation) ↔ §2/§3 (100Q/165min wording) aligned.
- Scope: single plan-sized (JSON conversion + manifest + instruction/results polish); no backend migration.
- Ambiguity: pass mapping explicitly a documented 70% proxy, not true scaled scoring.
