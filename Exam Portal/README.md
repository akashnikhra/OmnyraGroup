# OMNyra Exam Portal (Supabase-backed, static-hosted)

Timed GRC mock exams for OMNyra training students. **Static hosting (GitHub Pages) + Supabase BaaS** — vanilla HTML/CSS/JS, no build step, no bundler. Works local-only when `assets/config.js` is empty, and lights up Auth + server timing/grading when configured. See `SUPABASE_SETUP.md` (~20 min) and the canonical spec in `BACKEND.md`.

## Consoles (separate logins, separate areas)

| Console | Entry | Pages |
|---------|-------|-------|
| Student | `index.html` → `student/login.html` | `student/index.html` (catalog), `student/exam.html?attempt=<uuid>&remote=1`, `student/result.html`, `student/login.html` |
| Admin | `index.html` → `admin/login.html` | `admin/index.html` (dashboard), `admin/upload.html` (validate + publish), `admin/login.html` |

Student and admin areas never cross-link (except Main Site). Backend session = Supabase JWT; admin area additionally requires `profiles.role = 'admin'`.
Legacy flat pages (`index.html` v1 home, `exam.html`, `result.html`, `admin.html`) remain as the local-only fallback/uploader.

## Files (created by Frontend Developer)

| File | Purpose |
|------|---------|
| `index.html` | Portal home: header + theme toggle, student identity, progress cards, exam catalog grid, footer |
| `exam.html?attempt=<uuid>` | Timed runner: MCQ rendering, palette, flag-for-review, 15s auto-save, submit modal, timeout auto-submit |
| `result.html?attempt=<uuid>` | Score ring, topic breakdown, per-question review with rationale, retry (new attempt) |
| `admin.html` | Drag-drop JSON/CSV upload → validate (same rules as `tools/validate-questions.mjs`) → live preview → versioned JSON download + commit steps |
| `student/` | Separate Student Console (`login.html`, `index.html`, `exam.html`, `result.html`) — magic-link session, remote-first catalog/questions/attempts via `OmnyraRemote`, local fallback |
| `admin/` | Separate Admin Console (`login.html` role-gated, `index.html` dashboard, `students.html` per-student progress, `upload.html` validate + publish-to-DB + Git-backup download) |
| `assets/config.js` + `assets/remote.js` | Deploy-time anon coordinates + Supabase Auth/exam APIs (`window.OmnyraRemote`); empty keys = local-only |
| `supabase/schema.sql` | Runnable DDL + RLS + RPCs (source: `BACKEND.md`); see `SUPABASE_SETUP.md` |
| `assets/portal.css` | Brand tokens (`:root` per `design.md`), dark/light via `html[data-theme]`, responsive + hamburger nav |
| `assets/portal.js` | Shared: `Store`/`LocalStore`, `loadCatalog()`, theme, session, progress, inactivity watchdog, toast/modal |
| `README.md` | This file: schemas + run + integration points |

## Files owned by Backend Architect (touched minimally)

| File | Change | Reason |
|------|--------|--------|
| `questions/manifest.json` | Added 3 `draft` catalog entries (TPRM, ISO 27001, Privacy) | Task requires a multi-exam catalog grid; `published` entry untouched |
| `questions/sample-grc-fundamentals.json` | None (backend already modernized envelope) | Validator PASS confirmed |

## Run locally

```powershell
# from repo root — serves the whole site incl. portal JSON fetches
python -m http.server 8123
# then open http://localhost:8123/Exam%20Portal/index.html
```

## Data contract (canonical — matches BACKEND.md)

### Question set file (`questions/<exam-id>.json`)

Envelope: `examId, title, description?, version, durationMinutes, passPercent, status?, questions[]`.

**Question** — all fields required (validated by `tools/validate-questions.mjs` AND `admin.html`):

| Field | Type | Rule |
|-------|------|------|
| `id` | string | 1–121 chars, `[A-Za-z0-9-_:.]`, unique in set |
| `question` | string | ≥10 chars |
| `options` | string[4] | exactly 4, non-empty, distinct (case-insensitive) |
| `correctIndex` | 0–3 | integer |
| `rationale` | string | ≥10 chars, shown on result page only |
| `topic` | string | e.g. `TPRM` (drives breakdown) |
| `difficulty` | `easy`\|`medium`\|`hard` | label only in v1 |
| `marks` | int 1–100 | weighting; score = earned/total marks |

1–500 questions per file. CSV upload columns: `id,question,optionA,optionB,optionC,optionD,correctIndex,rationale,topic,difficulty,marks` (`correctIndex` 0-based; legacy `option1..option4` accepted on upload with warning).

### Catalog (`questions/manifest.json`, `MANIFEST_URL = questions/manifest.json`)

```jsonc
{ "version": 1, "updatedAt": "ISO-8601", "catalogBase": "./",
  "exams": [{ "id": "grc-fundamentals", "title": "…", "description": "…",
    "file": "sample-grc-fundamentals.json", "version": "…",
    "questionCount": 10, "durationMinutes": 30, "passPercent": 70,
    "status": "published" // "published" = open; anything else = Coming soon
  }] }
```

`loadCatalog()` normalizes each entry to `{id,title,description,durationMinutes,passPercent,questionFile,version,questionCount,status,open}` (`questionFile = catalogBase + file`) and caches the raw manifest under `omnyra.exam.catalog`.

### Attempt (per session; `attemptId` = backend `client_token`)

```jsonc
{
  "attemptId": "uuid", "examId": "grc-fundamentals", "examTitle": "…",
  "studentId": "email-lowercased", "student": { "name": "…", "email": "…" },
  "startedAt": "ISO-8601", "durationMinutes": 30,
  "answers": { "q01": 1 },    // questionId -> chosen option index
  "flags": { "q03": true },   // flagged for review
  "submittedAt": "ISO-8601|null", "autoSubmitted": false,
  "lastSavedAt": "ISO-8601"
}
```

Deadline = `startedAt + durationMinutes` (client-side; backend must re-derive server-side).

### Progress (per student per exam)

```jsonc
{ "<studentKey>": { "<examId>": {
  "best": 80, "attempts": 2, "lastAt": "ISO-8601",
  "history": [{ "at": "…", "pct": 80, "passed": true, "score": "8/10", "attemptId": "uuid" }]
} } }
```

Writes deduped by `attemptId` so result refreshes don't inflate counts.

### localStorage keys (all `omnyra.exam.*`)

| Key | Value |
|-----|-------|
| `omnyra.exam.theme` | `"dark"` \| `"light"` |
| `omnyra.exam.student` | `{name, email, savedAt}` (UI shape) |
| `omnyra.exam.profile` | `{displayName, email, savedAt}` (backend-canonical mirror, auto-synced on save) |
| `omnyra.exam.catalog` | `{at, data}` cached manifest (read-through) |
| `omnyra.exam.activeAttempt` | attemptId resume pointer (cleared on submit) |
| `omnyra.exam.attempt.<uuid>` | Attempt JSON (= `client_token` row client-side) |
| `omnyra.exam.progress` | Progress JSON |

## Session management (frontend part, v1)

- Identity: name/email form (no password), `crypto.randomUUID()` attempt token per start.
- Resume: `activeAttempt` pointer → banner on `index.html`; reload rehydrates from stored attempt.
- Inactivity: 30-min watchdog → warning modal (timer keeps running, stated in copy).
- Double-submit: `submitted` flag + `submittedAt` redirect; timeout path auto-submits (modal + 8s fallback); backend `uniq_active_attempt` + idempotent submit RPC are the real guards later.
- Answer-hiding (static limit): `exam.html` renders stem + options only; `correctIndex`/`rationale` live in the fetched JSON (unavoidable, public repo) but are never rendered or referenced before `result.html`. **v1 is low-stakes practice only.**

## Integration points / assumptions for Backend Architect

1. **Storage adapter swap** — all persistence goes through `OmnyraPortal.store` (`get/set/remove`, `getAttempt/saveAttempt/clearAttempt`, `getProgress/saveProgress`) plus `loadCatalog()`. `RemoteStore` must implement `{listExams, getExam, getAttempt, saveAttempt, submitAttempt}` per BACKEND.md §5 and additionally serve **answer-stripped** questions pre-submit. Swap the one instantiation in `assets/portal.js` (`// TODO: RemoteStore`). UI code never touches `localStorage` directly.
2. **Keys already aligned** — `profile`, `catalog`, `attempt.<id>`, `progress` match BACKEND.md §8; `student`/`theme`/`activeAttempt` are UI-only extras. Remote mode reuses the same keys as read-through cache.
3. **Auth hook** — replace `getStudent/saveStudent` with Supabase Auth session; `studentKey()` becomes `auth.users.id`; Attempt/Progress already carry `studentId`. Never trust the local email string.
4. **Server grading/timing** — keep keys server-side (`questions_public` view omits `correct_index`/`rationale`); `submit_attempt` RPC returns `{score, maxScore, percent, passed, results[]}`; result page will render from that payload instead of local grading.
5. **Admin publish flow** — v1 ends in `<exam-id>.v<YYYY-MM-DD>.json` download + manual `questions/` commit + `manifest.json` edit + `node tools/validate-questions.mjs` PASS. Backend path: same JSON via `POST` (question-bank API) → versioned rows → catalog API replaces `MANIFEST_URL`. Admin's in-browser rules intentionally mirror the node validator (incl. distinct-options, marks 1–100, kebab-case `examId`).
6. **Manifest drift to watch** — `questionCount`/`updatedAt` are backend-maintained; UI never displays manifest counts as truth (counts come from loaded files). Draft entries carry `file` names that don't exist yet — UI never fetches them (`open === false` gate + `questionFile == null` guard if file omitted).
7. **No secrets in v1** — only name/email in localStorage; zero non-same-origin calls (Google Fonts only). `service_role` never in client (per `.env.example`).
