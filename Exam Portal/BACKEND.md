# OMNyra Exam Portal — Backend & Session Architecture

**Status:** v1 contract (static-first, backend-optional) · **Owner:** Backend Architect
**Constraint (hard):** Production hosting is **GitHub Pages only** (static). No always-on Node server, no secrets in repo.
**UI boundary:** Do NOT change `index.html` / `exam.html` / `result.html` / `admin.html` styling — this doc covers data contracts, backend option, and session design only. UI stays static per `design.md` + `brand-guidelines.md`.
**Frontend coordination:** a parallel Frontend Developer agent owns the HTML pages and the `LocalStore` (`localStorage` keys `omnyra.exam.*`). This doc is the contract they code against.

---

## 0. Design decisions up front

1. **Static-first, backend-optional.** The portal must work fully offline/local on GitHub Pages on day one (pure-Git question files + `localStorage`). The backend lights up later **without changing the question contract**.
2. **No custom passwords in v1.** Auth (when backend is on) is Supabase Auth **email magic-link** (or OAuth). No password storage, no custom session cookies to secure.
3. **Answers are never trusted from the client when a backend exists.** The client only ever receives questions *without* `correctIndex`/`rationale`; grading happens in a `SECURITY DEFINER` RPC. In pure-static v1 (public repo JSON), answers are present by necessity — so v1 is explicitly **low-stakes practice only**, with reveal-after-submit discipline (see §3.6).
4. **One active attempt per student per exam.** Enforced in the DB (partial unique index) *and* in the client (resume-before-create).
5. **All dynamic calls degrade to local-only.** Every remote call is wrapped in try/catch with a `LocalStore` fallback. No remote call may break page render on GitHub Pages.

---

## 1. Backend recommendation

### 1.1 Comparison (free tier, Sep 2026 pricing landscape)

| Criterion | **Supabase ✅ PRIMARY** | Firebase (Spark) | Cloudflare D1 + Workers + Pages | Google Sheets / Apps Script | Pure-Git (JSON in repo + PR flow) ⭐ FALLBACK / v1-static |
|---|---|---|---|---|---|
| (a) Admin adds question sets **without code deploy** | ✅ Yes — `admin.html` → `supabase-js` INSERT (or CSV import), or Supabase Table Editor; appears in catalog instantly | ✅ Yes — console / client SDK write | ⚠️ DIY — must build + deploy a Worker API first; D1 dashboard is SQL-only, not admin-friendly | ✅ Yes — edit a Sheet (but fragile, see security) | ⚠️ Needs a commit+merge (PR flow). Reviewable, but it *is* a deploy |
| (b) Cross-device progress | ✅ Yes — Postgres `attempts` / `progress` keyed by `auth.users.id` | ✅ Yes — Firestore per-uid docs | ✅ Yes — D1 tables keyed by user id | ❌ No — no identity, no reliable per-user store | ❌ No — `localStorage` is per-browser only |
| (c) Answers served securely | ✅ Yes — `questions_public` view omits `correct_index`/`rationale`; grading in server RPC (see §2.4, §3.6) | ✅ Possible — security rules + Cloud Function grading, but more moving parts | ✅ Possible — Worker strips answers + grades server-side (you write it all) | ❌ No — anyone with the endpoint/Sheet link reads answers | ❌ No (public repo) — mitigated by post-submit-reveal only; **low-stakes only** |
| (d) Multiple concurrent exams | ✅ Trivial — `exam_id` on every row; catalog is a table/query | ✅ Trivial — per-exam collections | ✅ Trivial — `WHERE exam_id` | ⚠️ One tab per exam, quota-limited | ✅ Trivial — one JSON file per exam + `manifest.json` |
| (e) Session mgmt (login, attempt token, expiry, resume, anti-double-submit) | ✅ Auth + `attempts` lifecycle + `expires_at` + idempotent submit RPC | ✅ Auth + Firestore + Functions | ⚠️ DIY — bring your own auth (Clerk/WorkOS/Supabase Auth) + write session logic | ❌ No sessions, no expiry enforcement | ⚠️ Client-only pseudo-sessions (UUID + `localStorage`, no enforcement) |
| Free-tier headroom (approx) | 500 MB DB · 1 GB storage · 2 GB bandwidth · **50k MAU** · unlimited API* | 1 GB Firestore · **50k reads / 20k writes per day** · Auth free | D1 5 GB · **5M reads / 100k writes per day** · Workers 100k req/day | Quotas per execution (6 min), URL-fetch limits | Unlimited (repo size limits only) |
| Admin skill required | Low — spreadsheet-like Table Editor + SQL provided below | Low-medium — console + rules language | Medium-high — `wrangler`, migrations, Worker code | Very low (but unsafe) | Low — edit JSON, open PR |
| Pages compatibility | ✅ `supabase-js` via CDN ESM, anon key is public-by-design (RLS protects) | ✅ Firebase CDN SDK | ✅ `fetch()` to Worker URL | ✅ `fetch()` to Apps Script URL | ✅ Natively static |

\* Supabase free-tier numbers move; treat as order-of-magnitude. The free tier comfortably covers hundreds of students × dozens of attempts. Only egress-heavy media would push limits — the exam portal is text/JSON.

### 1.2 Pick

- **PRIMARY: Supabase (Postgres + Auth + Edge/RPC).** It is the *only* free option that satisfies **all five** requirements (a–e) with the least custom code: relational fit for exams/questions/attempts, RLS for answer hiding, email-link auth with zero password work, instant no-deploy admin writes, and a CDN SDK that runs on GitHub Pages. The `service_role` key never leaves the server/dashboard; the frontend only ever holds the **publishable anon key**, which is safe *because* RLS denies everything it should.
- **FALLBACK / SHIP-TODAY: pure-Git (versioned JSON + `manifest.json`).** Zero cost, zero backend, works on Pages right now, doubles as the durable question source-of-truth *even after* Supabase is on (admin authors JSON → validator → commit *and/or* DB insert). Limits are explicit: no cross-device progress, no true answer hiding, client-side grading only.

### 1.3 Cost / limits note (primary)

- Supabase Free: ~500 MB Postgres, 1 GB file storage, ~2 GB bandwidth/mo, ~50k monthly active users. An exam attempt is a few KB of JSON — **tens of thousands of attempts/mo fit**. Upgrade path is pay-as-you-grow (Pro) with zero code change; the contract below is portable to self-hosted Postgres.
- If cohort exceeds free egress (unlikely for text Q&A), move question JSON to Supabase Storage (CDN-cached) or keep serving the Git-hosted JSON (free via Pages) and use Supabase only for auth/attempts/grades — hybrid is supported by the `Store` interface (§5).

### 1.4 Data residency note

- Supabase project region is **chosen once at project creation** and cannot be changed on free tier. Primary markets are US & UK → create the project in **`us-east-1` (N. Virginia)** or **`eu-west-2` (London)**. All PII stored is minimal by design (email + display name + attempt rows; no payment/health data). For GDPR (UK/EU students) + India DPDP awareness: document the region in the privacy notice, set `auth` email templates accordingly, and use the `profiles` table only for operational fields (no sensitive attributes). Backups/PITR retention differs by plan — keep the Git JSON files as the restorable question source regardless.

### 1.5 Why not the others (primary)

- **Firebase:** viable, but Firestore daily read/write caps (50k/20k) bind sooner than Supabase's model under exam bursts (one attempt = many reads); security-rules-based answer hiding is more error-prone than a SQL view + RLS; relational exam data (exams → questions → attempts → answers) is more natural in Postgres; grading Functions add a second deploy surface.
- **Cloudflare D1/Workers:** best raw free quotas and edge latency, but **no built-in auth or admin UI** — you build session management and the admin write API yourself. Right long-term scale-out candidate; wrong v1 for a team with no backend headcount. Keep as the *second* fallback if Supabase ever becomes unsuitable.
- **Google Sheets/Apps Script:** familiar authoring, but **no RLS/answer security**, quota/timeout fragility, concurrent-write races, and PII-in-spreadsheets compliance risk. Use Sheets at most as an *authoring scratchpad* that exports to the validated JSON contract — never as the runtime DB.
- **Pure-Git as primary:** perfect v1-static ship vehicle, but fails (b), (c), (e) by construction. Hence fallback, not primary.

---

## 2. Data model

### 2.1 Field-name contract (frontend ↔ DB mapping — READ THIS)

The **shared JSON contract is camelCase** (what `manifest.json`, question files, and `LocalStore` use). The **DB is snake_case** (Postgres convention). `RemoteStore` maps between them; `LocalStore` uses the JSON names verbatim.

| JSON (files / LocalStore / catalog) | Postgres column | Notes |
|---|---|---|
| `id` | `questions.slug` | Per-exam unique slug, e.g. `grc-001`. DB PK is a separate `uuid`; slug is `UNIQUE(exam_id, slug)` |
| `question` | `questions.stem` | Stem text |
| `options` | `questions.options` (`jsonb`, 4 strings) | Order is canonical; per-attempt shuffle stored separately |
| `correctIndex` | `questions.correct_index` (`smallint`) | **Never sent to student clients** (view omits it) |
| `rationale` | `questions.rationale` | **Never sent pre-submit**; returned with grading result |
| `topic` | `questions.topic` | Free text, e.g. `ISO 27001` |
| `difficulty` | `questions.difficulty` | `easy` \| `medium` \| `hard` |
| `marks` | `questions.marks` | Positive int |
| `examId` / exam `id` | `exams.id` (`text` slug, e.g. `grc-fundamentals`) | Same slug in manifest + DB |
| `durationMinutes` | `exams.duration_minutes` | `passPercent` → `pass_percent` |

### 2.2 Postgres DDL (Supabase — run once in SQL Editor)

```sql
-- ============================================================
-- OMNyra Exam Portal — schema v1 (Supabase / Postgres 15+)
-- Run in Supabase SQL Editor. Safe to re-run (IF NOT EXISTS).
-- ============================================================
create extension if not exists "pgcrypto";

-- ---- profiles: 1 row per auth user ----
create table if not exists public.profiles (
  id           uuid primary key references auth.users(id) on delete cascade,
  email        citext not null,
  display_name text,
  role         text not null default 'student' check (role in ('student','admin')),
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

-- ---- exams: one row per exam (catalog) ----
create table if not exists public.exams (
  id               text primary key,               -- slug, == manifest id, e.g. 'grc-fundamentals'
  title            text not null,
  description      text not null default '',
  duration_minutes int  not null check (duration_minutes between 1 and 600),
  pass_percent     numeric(5,2) not null default 70 check (pass_percent between 0 and 100),
  version          text not null default '1970-01-01',  -- YYYY-MM-DD, == file version
  status           text not null default 'draft' check (status in ('draft','published','archived')),
  created_by       uuid references public.profiles(id),
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now()
);

-- ---- questions: canonical bank (answers live ONLY here) ----
create table if not exists public.questions (
  id            uuid primary key default gen_random_uuid(),
  exam_id       text not null references public.exams(id) on delete cascade,
  slug          text not null,                     -- == JSON `id`, e.g. 'grc-001'
  stem          text not null,                     -- == JSON `question`
  options       jsonb not null,                    -- exactly 4 strings
  correct_index smallint not null check (correct_index between 0 and 3),
  rationale     text not null,
  topic         text not null default 'General',
  difficulty    text not null default 'medium' check (difficulty in ('easy','medium','hard')),
  marks         int  not null default 1 check (marks between 1 and 100),
  position      int  not null default 0,           -- author order within exam
  version       text not null default '1970-01-01',
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (exam_id, slug),
  constraint options_is_4_strings check (
    jsonb_typeof(options) = 'array' and jsonb_array_length(options) = 4
  )
);

-- ---- attempts: one row per sitting ----
create table if not exists public.attempts (
  id            uuid primary key default gen_random_uuid(),
  student_id    uuid not null references public.profiles(id) on delete cascade,
  exam_id       text not null references public.exams(id) on delete cascade,
  status        text not null default 'created'
                check (status in ('created','in-progress','autosaved','submitted','graded','expired')),
  seed          bigint not null default (floor(random()*9223372036854775807)::bigint),
  question_order uuid[] not null default '{}',     -- shuffled question uuids for this attempt
  started_at    timestamptz not null default now(),
  expires_at    timestamptz not null,              -- set by start RPC = started + duration + grace
  submitted_at  timestamptz,
  graded_at     timestamptz,
  score         numeric(8,2),
  max_score     numeric(8,2),
  percent       numeric(5,2),
  passed        boolean,
  client_token  uuid not null default gen_random_uuid(), -- idempotency / resume key (see §3.3)
  updated_at    timestamptz not null default now()
);

-- One ACTIVE attempt per student per exam (concurrent-attempt guard, §3.5)
create unique index if not exists uniq_active_attempt
  on public.attempts (student_id, exam_id)
  where status in ('created','in-progress','autosaved');

create index if not exists idx_attempts_student on public.attempts (student_id, updated_at desc);
create index if not exists idx_attempts_exam_status on public.attempts (exam_id, status);

-- ---- attempt_answers: one row per question per attempt ----
create table if not exists public.attempt_answers (
  attempt_id     uuid not null references public.attempts(id) on delete cascade,
  question_id    uuid not null references public.questions(id) on delete cascade,
  selected_index smallint check (selected_index between 0 and 3), -- NULL = unanswered
  is_correct     boolean,                            -- set at grading time only
  answered_at    timestamptz not null default now(),
  primary key (attempt_id, question_id)
);
create index if not exists idx_answers_attempt on public.attempt_answers (attempt_id);

-- ---- progress: rollup per student per exam (written by grading RPC) ----
create table if not exists public.progress (
  student_id     uuid not null references public.profiles(id) on delete cascade,
  exam_id        text not null references public.exams(id) on delete cascade,
  attempts_count int not null default 0,
  best_percent   numeric(5,2),
  last_attempt_id uuid references public.attempts(id) on delete set null,
  last_status    text,
  updated_at     timestamptz not null default now(),
  primary key (student_id, exam_id)
);

create index if not exists idx_questions_exam_pos on public.questions (exam_id, position);
```

### 2.3 RLS + secure view + grading RPC

```sql
-- Enable RLS everywhere
alter table public.profiles         enable row level security;
alter table public.exams            enable row level security;
alter table public.questions        enable row level security;
alter table public.attempts         enable row level security;
alter table public.attempt_answers  enable row level security;
alter table public.progress         enable row level security;

-- Admin helper (reads JWT role via profiles; SECURITY DEFINER, locked search_path)
create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.profiles p
                 where p.id = auth.uid() and p.role = 'admin');
$$;

-- ---- profiles ----
drop policy if exists "own profile read"   on public.profiles;
drop policy if exists "own profile update" on public.profiles;
drop policy if exists "admin all profiles" on public.profiles;
create policy "own profile read"   on public.profiles for select using (id = auth.uid() or public.is_admin());
create policy "own profile update" on public.profiles for update using (id = auth.uid() or public.is_admin());
create policy "admin all profiles" on public.profiles for all    using (public.is_admin()) with check (public.is_admin());
-- NOTE: profile rows are created by a trigger on auth.users (see setup §6 step 4) or by first-login upsert.

-- ---- exams ----
drop policy if exists "read published exams" on public.exams;
drop policy if exists "admin write exams"    on public.exams;
create policy "read published exams" on public.exams for select
  using (status = 'published' or public.is_admin());
create policy "admin write exams" on public.exams for all
  using (public.is_admin()) with check (public.is_admin());

-- ---- questions: NO direct student reads (answers would leak) ----
drop policy if exists "admin all questions" on public.questions;
create policy "admin all questions" on public.questions for all
  using (public.is_admin()) with check (public.is_admin());
-- Students read ONLY via the answer-stripped view below.

-- Answer-stripped view: the ONLY question surface for students.
-- Definer semantics (security_invoker = false) + explicit grant: students read
-- the listed columns only; they have NO policy on questions itself, so
-- correct_index/rationale can never leak pre-submit.
create or replace view public.questions_public
with (security_invoker = false) as
select q.id, q.exam_id, q.slug, q.stem, q.options, q.topic, q.difficulty, q.marks, q.position, q.version
from public.questions q
join public.exams e on e.id = q.exam_id
where e.status = 'published';
grant select on public.questions_public to anon, authenticated;

-- ---- attempts ----
drop policy if exists "own attempts"   on public.attempts;
drop policy if exists "admin attempts" on public.attempts;
create policy "own attempts" on public.attempts for all
  using (student_id = auth.uid()) with check (student_id = auth.uid());
create policy "admin attempts" on public.attempts for all
  using (public.is_admin()) with check (public.is_admin());

-- ---- attempt_answers (only on own attempts) ----
drop policy if exists "own answers"   on public.attempt_answers;
drop policy if exists "admin answers" on public.attempt_answers;
create policy "own answers" on public.attempt_answers for all
  using (exists (select 1 from public.attempts a
                 where a.id = attempt_id and a.student_id = auth.uid()))
  with check (exists (select 1 from public.attempts a
                 where a.id = attempt_id and a.student_id = auth.uid()));
create policy "admin answers" on public.attempt_answers for all
  using (public.is_admin()) with check (public.is_admin());

-- ---- progress (students read own; writes happen in grading RPC) ----
drop policy if exists "own progress read" on public.progress;
drop policy if exists "admin progress"    on public.progress;
create policy "own progress read" on public.progress for select using (student_id = auth.uid());
create policy "admin progress"    on public.progress for all
  using (public.is_admin()) with check (public.is_admin());

-- ============================================================
-- RPC: start_attempt(p_exam_id) — idempotent, enforces 1-active
-- Returns the active-or-new attempt row.
-- ============================================================
create or replace function public.start_attempt(p_exam_id text)
returns public.attempts
language plpgsql security definer set search_path = public as $$
declare
  v_exam   public.exams%rowtype;
  v_active public.attempts%rowtype;
  v_new    public.attempts%rowtype;
begin
  if auth.uid() is null then raise exception 'NOT_AUTHENTICATED'; end if;

  select * into v_exam from public.exams where id = p_exam_id;
  if not found then raise exception 'EXAM_NOT_FOUND'; end if;
  if v_exam.status <> 'published' then raise exception 'EXAM_NOT_PUBLISHED'; end if;

  -- Resume existing active attempt (concurrent guard)
  select * into v_active from public.attempts
   where student_id = auth.uid() and exam_id = p_exam_id
     and status in ('created','in-progress','autosaved')
   order by updated_at desc limit 1;
  if found then
    update public.attempts set status = 'in-progress', updated_at = now()
     where id = v_active.id;
    select * into v_new from public.attempts where id = v_active.id;
    return v_new;
  end if;

  -- Fresh attempt: shuffled order + expiry baked server-side
  insert into public.attempts (student_id, exam_id, status, question_order, expires_at)
  select auth.uid(), p_exam_id, 'in-progress',
         coalesce(array_agg(q.id order by random()), '{}'),
         now() + (v_exam.duration_minutes || ' minutes')::interval + interval '15 minutes'
  from public.questions q where q.exam_id = p_exam_id
  returning * into v_new;

  if coalesce(array_length(v_new.question_order,1),0) = 0 then
    raise exception 'EXAM_HAS_NO_QUESTIONS';
  end if;
  return v_new;
exception when unique_violation then
  -- Lost a race with another tab: return the winner.
  select * into v_new from public.attempts
   where student_id = auth.uid() and exam_id = p_exam_id
     and status in ('created','in-progress','autosaved')
   order by updated_at desc limit 1;
  return v_new;
end $$;

-- ============================================================
-- RPC: submit_attempt(p_attempt_id) — idempotent, server grades
-- Anti-double-submit: second call returns the stored grade.
-- ============================================================
create or replace function public.submit_attempt(p_attempt_id uuid)
returns jsonb
language plpgsql security definer set search_path = public as $$
declare
  v_a    public.attempts%rowtype;
  v_exam public.exams%rowtype;
  v_score numeric(8,2) := 0; v_max numeric(8,2) := 0;
  v_pct  numeric(5,2); v_passed boolean; v_late boolean := false;
begin
  if auth.uid() is null then raise exception 'NOT_AUTHENTICATED'; end if;

  select * into v_a from public.attempts where id = p_attempt_id;
  if not found then raise exception 'ATTEMPT_NOT_FOUND'; end if;
  if v_a.student_id <> auth.uid() and not public.is_admin() then raise exception 'NOT_OWNER'; end if;
  select * into v_exam from public.exams where id = v_a.exam_id;

  -- Idempotent replay: already graded → return stored result (anti-double-submit)
  if v_a.status = 'graded' then
    return jsonb_build_object('attemptId', v_a.id, 'score', v_a.score, 'maxScore', v_a.max_score,
                              'percent', v_a.percent, 'passed', v_a.passed, 'replayed', true);
  end if;
  if v_a.status not in ('created','in-progress','autosaved','submitted') then
    raise exception 'ATTEMPT_NOT_SUBMITTABLE:%', v_a.status;
  end if;

  v_late := now() > v_a.expires_at;  -- accepted but flagged; policy: grade-as-is

  -- Grade: join answers to bank (server side — client never saw correct_index)
  with g as (
    select q.marks,
           (aa.selected_index is not null and aa.selected_index = q.correct_index) as ok
    from public.questions q
    left join public.attempt_answers aa
      on aa.question_id = q.id and aa.attempt_id = v_a.id
    where q.exam_id = v_a.exam_id
  )
  select coalesce(sum(case when ok then marks else 0 end),0),
         coalesce(sum(marks),0)
    into v_score, v_max from g;

  v_pct := case when v_max > 0 then round(100.0*v_score/v_max, 2) else 0 end;
  v_passed := v_pct >= v_exam.pass_percent;

  -- Stamp per-answer correctness (powers rationale review on result page)
  update public.attempt_answers aa
     set is_correct = (aa.selected_index = q.correct_index)
    from public.questions q
   where aa.attempt_id = v_a.id and aa.question_id = q.id;

  update public.attempts set status='graded', submitted_at=coalesce(submitted_at, now()),
    graded_at=now(), score=v_score, max_score=v_max, percent=v_pct, passed=v_passed,
    updated_at=now() where id = v_a.id;

  insert into public.progress (student_id, exam_id, attempts_count, best_percent, last_attempt_id, last_status)
  values (v_a.student_id, v_a.exam_id, 1, v_pct, v_a.id, 'graded')
  on conflict (student_id, exam_id) do update set
    attempts_count = public.progress.attempts_count + 1,
    best_percent   = greatest(coalesce(public.progress.best_percent,0), v_pct),
    last_attempt_id = excluded.last_attempt_id, last_status='graded', updated_at=now();

  return jsonb_build_object('attemptId', v_a.id, 'score', v_score, 'maxScore', v_max,
                            'percent', v_pct, 'passed', v_passed, 'late', v_late, 'replayed', false);
end $$;
```

**Why this is safe:** `questions.correct_index`/`rationale` have *no* student-readable policy and the view omits them, so even with a leaked anon key an attacker cannot SELECT answers. Grading reads the bank inside a `SECURITY DEFINER` function that checks ownership — the client submits only `selected_index` values.

### 2.4 Versioned Git JSON format (fallback + source-of-truth)

Files live in `Exam Portal/questions/`. Dated snapshots use `questions/<exam-id>.v<YYYY-MM-DD>.json`; the shipped sample uses the friendly alias `sample-grc-fundamentals.json` (same schema) so the frontend team has a stable fixture. `version` is an **opaque string**: semver (`1.0.0`, as used by `admin.html` + the sample set) and dates (`2026-09-14`) are both accepted — the validator only *warns* on non-date versions. `durationMinutes`/`passPercent` are recommended (frontend defaults 30/70 when absent).

**Envelope schema** (validated by `tools/validate-questions.mjs`):

```jsonc
{
  "examId": "grc-fundamentals",          // kebab-case slug == DB exams.id == manifest id
  "title": "GRC Fundamentals — Sample Set",
  "description": "…",
  "version": "1.0.0",                    // opaque string; semver or YYYY-MM-DD (validator warns on non-date)
  "durationMinutes": 30,                 // 1..600, recommended (default 30 when absent)
  "passPercent": 70,                     // 0..100, recommended (default 70 when absent)
  "status": "published",                 // draft|published|archived
  "questions": [
    {
      "id": "q01",                       // unique within file == DB slug
      "question": "Stem text…",
      "options": ["A", "B", "C", "D"],   // exactly 4, distinct
      "correctIndex": 0,                 // 0..3
      "rationale": "Why A is right…",
      "topic": "Governance",
      "difficulty": "easy",              // easy|medium|hard
      "marks": 1                         // 1..100
    }
  ]
}
```

**`manifest.json`** (catalog — `exam.html`/`index.html` read this, never a directory listing):

```jsonc
{
  "version": 1,
  "updatedAt": "2026-09-14T00:00:00Z",
  "catalogBase": "./",
  "exams": [
    {
      "id": "grc-fundamentals",
      "title": "GRC Fundamentals — Sample Set",
      "file": "sample-grc-fundamentals.json",
      "version": "1.0.0",
      "questionCount": 10,
      "durationMinutes": 30,
      "passPercent": 70,
      "status": "published"
    }
  ]
}
```

Rules: `manifest.id` ≡ file `examId` ≡ DB `exams.id`; `manifest.version` ≡ file `version`; `questionCount` ≡ `questions.length`. The validator checks file internals; a CI/PR check (or admin.html pre-upload) should assert manifest↔file consistency.

### 2.5 Canonical catalog (single file, normalized at the boundary)

The portal ships **one** catalog file — `questions/manifest.json` (this is intentional; a second runtime copy was removed to eliminate drift). All pages read it via `portal.js loadCatalog()`:

| File | Role | Entry fields | Read by |
|---|---|---|---|
| `questions/manifest.json` | **Canonical catalog** (source-of-truth) | `{ id, title, description?, file, version, questionCount, durationMinutes, passPercent, status: "published"\|"draft"\|"archived" }` + top-level `{ version, updatedAt, catalogBase }` | `portal.js loadCatalog()` (read-through cache in `omnyra.exam.catalog`), admin flows |

`portal.js normalizeExam()` unifies entries into `{ id, title, description, durationMinutes, passPercent, questionFile, version, questionCount, status, open }` where `questionFile = catalogBase + file` and `open = (status === "published" || status === "open")`. **Backend rule:** `RemoteStore.listExams()` returns this normalized shape from the `exams` table; the manifest becomes a generated artifact (CI renders it from the DB or from `questions/`). Until then: when adding an exam, update `questions/manifest.json` only (Path B checklist) — there is no second file to keep in sync.

Legacy aliases (do not use in new code — map at the boundary only): `durationMin` ≡ `durationMinutes`, `passingPct` ≡ `passPercent`, `questionFile` ≡ `catalogBase + file`, `open` ≡ published-status.

### 2.6 Identity / profile shape (backend-canonical)

v1-static stores the student under `omnyra.exam.student` as `{ name, email, savedAt }` and mirrors a backend-canonical profile under `omnyra.exam.profile` as `{ displayName, email, savedAt }` (see `portal.js saveStudent`). The server user key is derived by `studentKey()`: `lowercase(email || name || displayName || "guest")`.

**Backend rule:** Supabase `auth.users.id` replaces `studentKey()` as the identity; `profiles` row is `{ id, email, display_name, role }` (§2.2). On first remote login, `RemoteStore` migrates: `display_name = profile.displayName || student.name`, `email` verified from the magic-link (never trust the local string — README integration point 2). Local `omnyra.exam.progress` history (keyed by old `studentKey`) is namespaced per key, so nothing collides; best-attempt rollup is recomputed server-side in `progress` (§2.3 RPC).

---

## 3. Session management design

### 3.1 Auth flow (v1 — no custom passwords)

**With backend (Supabase Auth, email magic-link):**

```
student enters email → supabase.auth.signInWithOtp({ email }) → clicks link in inbox
  → Pages URL receives ?code=… → supabase.auth.exchangeCodeForSession / getSession()
  → JWT (access_token) held in memory by supabase-js (persisted to localStorage by SDK)
  → upsert public.profiles { id: auth.uid(), email } → catalog/attempt APIs allowed by RLS
```

- No passwords, no reset flows, no credential storage in repo. Magic-link expiry default 1h; rate-limit OTP resends client-side (60s cooldown).
- Admin role is a **flag in `profiles.role`** set manually in Supabase dashboard (never self-assignable — no RLS policy allows a user to set `role='admin'`).
- **Without backend (v1-static):** no login at all. Student optionally enters a display name stored as `omnyra.exam.student` (auto-mirrored to `omnyra.exam.profile`, §2.6). All data stays in `localStorage`; cross-device is explicitly unsupported (banner copy in §8).

### 3.2 Attempt lifecycle (state machine)

```
created ──▶ in-progress ──▶ autosaved ──┐
   │             │              │        │  submit_attempt() / auto-submit on expiry
   │             │              ▼        ▼
   │             └──── autosave every 15s + on answer ──▶ submitted ──▶ graded
   │                                                        │              │
   └── abandoned (no activity, never submitted)             │              ├──▶ progress rollup
      → expired (now > expires_at, unsubmitted) ◀──────────┘              └──▶ rationale review unlocked
```

- `created`: row exists, timer not acknowledged yet (transient; `start_attempt` returns `in-progress` immediately in v1).
- `in-progress` ⇄ `autosaved`: client writes answers (debounced 500ms, heartbeat 15s); each write flips `updated_at` and (heuristically) `autosaved`. Server does not distinguish them semantically — both mean "active".
- `submitted`: terminal intake (client stops timer, POSTs final answers, calls `submit_attempt`). Kept as a distinct value only for observability; the RPC moves straight to `graded`.
- `graded`: terminal, scored, idempotent replays return stored grade (anti-double-submit).
- `expired`: enforced **server-side** (`now() > expires_at` flags `late:true`, grades as-is) and **client-side** (timer auto-submits; resume blocked past `expires_at` + 24h review window).

### 3.3 Token format

| Token | Format | Carries | Lifetime |
|---|---|---|---|
| Supabase session JWT | `sb-<project>-auth-token` (SDK-managed) | `sub` = `auth.uid()`, `role: authenticated` | Access ~1h, auto-refreshed by SDK |
| Attempt id | UUIDv4 (`attempts.id`) | The attempt's primary key; ownership proven by JWT+RLS, not by secrecy | Until graded + review window |
| `client_token` | UUIDv4 (`attempts.client_token`) | Idempotency key for create/submit retries; stored in `omnyra.exam.attempt.<id>` | Same as attempt |
| v1-static pseudo-session | `crypto.randomUUID()` in `localStorage` | Resume key only — **no security meaning** (document as such) | Per-browser |

Never put `correctIndex`/rationale, service keys, or other users' ids in any token or URL. Attempt ids in URLs are fine (RLS gates reads).

### 3.4 Timeout / inactivity rules

| Rule | Value | Enforced by |
|---|---|---|
| Exam duration | `exams.duration_minutes` (default 30–60) | Server `expires_at` = `started_at + duration + 15 min grace`; client countdown |
| Autosave | every **15s** + on-answer debounce **500ms** | Client; server `updated_at` |
| Inactivity nudge | no answer + no focus for **10 min** → banner "still there?" (timer keeps running) | Client only |
| Hard auto-submit | at `expires_at − grace` client auto-submits; server grades as-is after `expires_at` (`late:true`) | Both |
| Resume window | active attempt resumable while `now < expires_at`; graded review available **30 days** | Server check + client redirect |
| Magic-link / JWT | link 1h; access token ~1h auto-refresh | Supabase Auth |

### 3.5 Resume + concurrent-attempt guard

- **Resume:** on `exam.html` load, `RemoteStore.getActiveAttempt(examId)` (or local key scan in static mode). If an `in-progress`/`autosaved` attempt exists and `now < expires_at`, restore `question_order` + saved answers and restart the timer at `expires_at − now`. Else start fresh via `start_attempt()` (RPC returns the existing active row on races — see `unique_violation` handler).
- **Guard:** `uniq_active_attempt` partial unique index (§2.2) makes double-start impossible even with two tabs racing; the loser receives the winner's row. Client mirrors this: disable Start while a create is in flight; re-check `localStorage` before calling.
- **Anti-double-submit:** submit button disables on first click; request carries `client_token`; server `submit_attempt` is idempotent (`graded` → replay stored grade, `replayed:true`). Retries/network replays can never create a second grade.

### 3.6 Anti-cheating minimums (honest matrix)

| Control | With backend (Supabase) | v1-static (no backend) |
|---|---|---|
| Answer hiding | ✅ Real — view omits answers; grading server-side | ❌ Impossible (public JSON) — **mitigate**: keep full set in memory, render stem+options only, reveal `correctIndex`/`rationale` **only post-submit** on `result.html`; never pre-render hidden DOM nodes |
| Shuffle | ✅ Server seed + stored `question_order` (stable across resume) | ✅ Client `mulberry32(seed)` per attempt; seed in `localStorage` |
| Option shuffle | Recommended — store per-attempt map when added (v1.1) | Recommended — shuffle display order, map back on submit |
| Grading | ✅ Server RPC (authoritative) | Client-side (advisory; label scores "practice only") |
| Attempt token | ✅ JWT + attempt UUID + expiry enforced | Obfuscated resume key only — no enforcement |
| Copy/paste, timer | Discourage (CSS `user-select`, timer), don't pretend to prevent | Same |
| **Policy line** | Suitable for coached mocks | **Do not use v1-static for certification decisions** |

---

## 4. Admin publish flow

### Path A — with backend (no code deploy)

1. Admin signs in (magic-link) with a `profiles.role='admin'` account.
2. `admin.html` → parses uploaded **JSON** (envelope schema §2.4) or **CSV** (format template + rules §4.1) → runs the **same rules as the validator** client-side → shows row-level errors, blocks publish on failure.
3. On success: upsert `exams` row → upsert `questions` rows (`on conflict (exam_id, slug) do update`) with bumped `version` → exam appears in catalog instantly (no deploy).
4. Keep the Git file as backup: download the validated JSON and commit it (`questions/<exam-id>.v<date>.json` + manifest bump) so Git stays the restorable source.

**CSV columns:** canonical header `id,question,optionA,optionB,optionC,optionD,correctIndex,rationale,topic,difficulty,marks` — full spec, fill rules, converter CLI, and the legacy `option1..4` note live in §4.1. `correctIndex` is 0-based.

### Path B — zero-backend fallback (works today)

1. Admin builds JSON (or CSV→JSON via `admin.html` converter or `node "Exam Portal/tools/csv-to-json.mjs" … --out …`, §4.1) → clicks **Download validated JSON** (or takes the CLI `--out` file).
2. Commit to `Exam Portal/questions/<exam-id>.v<version>.json` (dated snapshot or semver alias), update `questions/manifest.json` (`id, title, file, version, questionCount, durationMinutes, passPercent`, `status: "published"`, plus top-level `updatedAt`) — the single catalog file; see §2.5.
3. Open PR → reviewer runs `node "Exam Portal/tools/validate-questions.mjs" "Exam Portal/questions/<file>.json"` → merge → GitHub Pages serves it; catalog picks it up with zero code change.

### 4.1 CSV authoring contract — format template + converter

Admin authors who prefer spreadsheets use two checked-in files (exact names — UI links must match, §9):

| File | Role |
|---|---|
| `questions/template.csv` | **Fill-me guide**: `#` help line + canonical header + ONE placeholder row. Intentionally **fails** conversion (`contains placeholder text …`) until every `REPLACE-ME`/`FILL-ME` is replaced. Copy it to `questions/<exam-id>.vYYYY-MM-DD.csv` and fill it in. |
| `questions/template-with-examples.csv` | **Convertible reference**: header + 3 realistic rows (GRC foundations / TPRM / ISO 27001) with full rationales. Converts and passes the validator as-is. |
| `tools/csv-to-json.mjs` | **Zero-dep converter** (Node 18+): RFC4180 parse (quoted commas/newlines/`""` escapes, BOM-tolerant; `#` comments + blank lines skipped) → same row rules as the validator + `admin.html` → canonical JSON envelope to stdout or `--out`. Exit 0 pass / 1 fail with row-numbered errors (`row <n> (line <m>) [<id>]: <message>`). `validate-questions.mjs` is intentionally untouched (CLI backward compatible — the converter duplicates, not imports, the rules; keep all three in sync if thresholds change). |

**Canonical header (EXACT, case-sensitive, comma delimiter):**
`id,question,optionA,optionB,optionC,optionD,correctIndex,rationale,topic,difficulty,marks`

| Column | Rule (same thresholds as validator + `admin.html#validate`) |
|---|---|
| `id` | Required, unique in file; validator range is `[A-Za-z0-9-_:.]` 1–121 chars; **new rows should use lowercase-hyphen slugs** (`grc-001`) — the converter warns otherwise |
| `question` | Stem text, ≥ 10 chars |
| `optionA..optionD` | Exactly 4, each non-empty, distinct (case-insensitive) |
| `correctIndex` | Integer `0–3` (`0=A, 1=B, 2=C, 3=D`) |
| `rationale` | ≥ 10 chars — why the key wins (shown post-submit only, powers `result.html` review) |
| `topic` | Required label, e.g. `TPRM` (drives score breakdown) |
| `difficulty` | `beginner\|intermediate\|advanced` **or** `easy\|medium\|hard` — the converter maps `beginner→easy, intermediate→medium, advanced→hard`; JSON output is always canonical `easy\|medium\|hard` so the validator passes unchanged |
| `marks` | Integer `1–100` |

Legacy note: older `admin.html` downloads emit `option1..option4`. The converter **accepts** that header with a warning (mapped 1:1); all templates and docs use `optionA..optionD`. Frontend migration: make `admin.html` parse/emit `optionA..optionD` while still accepting `option1..4` for old files (§9 open Q8).

**5 admin fill rules:**
1. **One row = one question; keep the header byte-exact.** Never reorder/rename columns; quote any field containing commas, quotes, or newlines (`"…"`, `""` escape per RFC4180).
2. **Write 4 genuinely distinct options** — duplicated distractors (repeats, case variants) fail validation.
3. **Set `correctIndex` against the letter you mean** (A=0 … D=3) and re-check after any column sort in Excel/Sheets — silent key shifts are the #1 CSV incident.
4. **Explain the key in `rationale`** (≥ 10 chars, full sentence): name the principle + why the distractors lose.
5. **The envelope lives OUTSIDE the CSV.** `examId/title/version/durationMinutes/passPercent` come from the `admin.html` form (Exam id / Version / Duration / Pass percent / Set title) or converter flags; authoring name `questions/<exam-id>.vYYYY-MM-DD.csv`, export `questions/<exam-id>.vYYYY-MM-DD.json`.

**Answer-key handling note:** `correctIndex` + `rationale` ship in the repo JSON by necessity of the pure-Git fallback — therefore **Git-served sets are low-stakes practice only** (reveal-after-submit discipline, §3.6). On the Supabase path the same CSV/JSON is imported server-side and students only ever read the `questions_public` view (answers stripped); grading happens in the `submit_attempt` RPC. Never invent a second key file — one source, two serving modes.

**Path A (backend) CSV upload steps:**
1. Admin → `admin.html` → drop `.csv` (in-browser parse + same rules, row-level errors) → fill envelope fields → **Download versioned JSON** (`<exam-id>.v<date>.json`).
   CLI equivalent (same rules, for terminal/PR use): `node "Exam Portal/tools/csv-to-json.mjs" "Exam Portal/questions/<exam-id>.v<date>.csv" --examId <exam-id> --title "<Title>" --version <date> --out "Exam Portal/questions/<exam-id>.v<date>.json"`.
2. Validate: `node "Exam Portal/tools/validate-questions.mjs" "Exam Portal/questions/<exam-id>.v<date>.json"` — must print PASS.
3. `admin.html` upserts the `exams` + `questions` rows (version bumped) → exam appears in catalog instantly (no deploy).
4. Git backup: commit the JSON + manifest bump (below) so Git stays the restorable source.

**Path B (zero-backend) CSV upload steps:** same convert + validate (steps 1–2 above), then:
3. Commit the JSON to `Exam Portal/questions/<exam-id>.v<version>.json`.
4. Manifest update: edit `questions/manifest.json` — add/edit `{ id (= examId), title, file, version (= file version), questionCount (= questions.length), durationMinutes, passPercent, status: "published" }` and bump top-level `updatedAt` to now (ISO-8601). Templates (`template.csv`, `template-with-examples.csv`) are NEVER catalog entries — this change leaves `manifest.json` untouched.
5. Open PR → reviewer re-runs the validator → merge → Pages serves it; catalog picks it up with zero code change.

### Validation rules (single source — also enforced by the script; mirrors `admin.html#validate`)

- Required per question: `id, question, options[4], correctIndex 0-3, rationale, topic, difficulty, marks` (§2.4 types/ranges).
- File: 1–500 questions; unique `id`s; distinct options (case-insensitive); `question`/`rationale` ≥ 10 chars (same threshold as `admin.html` and the validator).
- Envelope: `examId` kebab-case slug; `title` required; `version` required opaque string (date recommended); `durationMinutes` 1–600 and `passPercent` 0–100 recommended (warn-only when absent); `manifest.id/version/count` consistent.
- Strictness split (deliberate): the CLI validator **warns** on non-date versions and missing duration/pass so legacy fixtures (e.g. `sample-grc-fundamentals.json @ 1.0.0`) keep passing; `admin.html` **blocks download** on envelope issues so all *new* sets ship date-versioned with full envelopes.

---

## 5. `Store` interface spec (LocalStore → RemoteStore swap)

The shipped frontend (`assets/portal.js`, `OmnyraPortal`) already isolates **all** persistence behind one interface — `LocalStore` implements it today, `RemoteStore` (Supabase) implements the **same methods** tomorrow. Selection is runtime, never a fork. UI code must not touch `localStorage` directly (it doesn't — verified).

```js
// Shipped interface (assets/portal.js) — RemoteStore MUST implement these exact methods:
store.get(key, fallback)       // raw read  (keys: OmnyraPortal.K.*)
store.set(key, value)          // raw write
store.remove(key)              // raw delete
store.getAttempt(id)           // → Attempt JSON | null   (K.attemptPrefix + attemptId)
store.saveAttempt(attempt)     // attempt.attemptId is the key
store.clearAttempt(id)         // delete one attempt
store.getProgress()            // → { [studentKey]: { [examId]: { best, attempts, lastAt, history[] } } }
store.saveProgress(progress)   // whole-object write
// Pure helpers (no storage): OmnyraPortal.uuid(), .nowIso(), .loadCatalog(),
// .normalizeExam(), .getStudent(), .saveStudent(), .studentKey(), .recordResult()
```

Key map (`OmnyraPortal.K`, namespace `omnyra.exam.*`): `theme`, `student` (`{name,email,savedAt}`), `profile` (`{displayName,email,savedAt}` — backend-canonical mirror, §2.6), `catalog` (cached manifest read-through), `activeAttempt` (resume pointer), `attemptPrefix + <uuid>` (Attempt JSON per README shape: `{attemptId, examId, examTitle, studentId, student, startedAt, durationMin, answers{}, flags{}, submittedAt, autoSubmitted, lastSavedAt}`), `progress`.

Config (only place backend coordinates live — no keys hardcoded elsewhere):

```js
// Exam Portal/assets/config.js (new file when backend lands; absent in v1-static)
window.OMNYRA_CONFIG = {
  BACKEND: "auto",                       // "auto" | "local" | "supabase"
  SUPABASE_URL: "",                      // e.g. "https://xyzcompany.supabase.co" (deploy-time, see §7)
  SUPABASE_ANON_KEY: "",                 // publishable anon key ONLY — never service_role
  API_BASE_URL: null,                    // REST base if RemoteStore uses REST instead of supabase-js
};
```

Higher-level exam operations used by pages today are composed from the primitives above (`loadCatalog()` + `fetch(questionFile)` + `store.*`); `RemoteStore` keeps those call sites working by translating primitives to Supabase (`supabase-js` v2 via CDN ESM — sketch, no keys in source):

```js
import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm";
const sb = createClient(OMNYRA_CONFIG.SUPABASE_URL, OMNYRA_CONFIG.SUPABASE_ANON_KEY);
// getAttempt/saveAttempt → attempts + attempt_answers rows (RLS: owner-only; §2.3)
//   saveAttempt maps Attempt.answers{qid:idx} → attempt_answers upserts + attempts.status='autosaved'
// getProgress/saveProgress → progress table (reads; writes via submit_attempt RPC rollup)
// loadCatalog() → exams table (status='published') → same normalized shape as normalizeExam()
// submit flow → sb.rpc("submit_attempt", { p_attempt_id }) → {score,maxScore,percent,passed,late,replayed}
//   + per-question review {questionId, selectedIndex, isCorrect, correctIndex, rationale}
//   NOTE: pre-submit question fetch uses questions_public (NO correctIndex/rationale); §2.3
// getStudent/saveStudent → supabase.auth session + profiles row (§2.6 migration)
// All wrapped: try { remote } catch { fallback to LocalStore + banner "offline — progress stays on this device" }
```

**Swap rule:** one instantiation line in `assets/portal.js` (`var store = new LocalStore()` → `BootStore()` returning `RemoteStore` iff `BACKEND !== "local"` **and** `SUPABASE_URL/ANON_KEY` are set **and** a probe query succeeds within 3s; otherwise `LocalStore`). Every remote method catches and degrades to the local equivalent for reads; writes queue a "pending sync" notice rather than throwing.

---

## 6. Setup steps for admin (Supabase, ~20 min, free tier)

1. **Create project:** supabase.com → New project → region **`us-east-1` or `eu-west-2`** (see §1.4) → save the DB password in a vault (not the repo).
2. **Run schema:** SQL Editor → paste **§2.2 DDL**, Run → paste **§2.3 RLS/RPC block**, Run.
3. **Auth:** Authentication → Providers → enable **Email (magic link / OTP)**; set Site URL to `https://omnyragroup.online` and add `https://omnyragroup.online/Exam Portal/**` redirect; customize the email template (OMNyra branding).
4. **Auto-profile trigger** (so every login gets a `profiles` row):
   ```sql
   create or replace function public.handle_new_user()
   returns trigger language plpgsql security definer set search_path = public as $$
   begin
     insert into public.profiles (id, email) values (new.id, new.email)
     on conflict (id) do nothing;
     return new;
   end $$;
   drop trigger if exists on_auth_user_created on auth.users;
   create trigger on_auth_user_created after insert on auth.users
     for each row execute function public.handle_new_user();
   ```
5. **First admin:** sign in once via the site (creates your profile), then in Table Editor set your `profiles.role = 'admin'`.
6. **Keys:** Project Settings → API → copy **publishable anon key** + project URL. These go into the *deployed* `config.js` / Pages secret at deploy time — **never commit `service_role`**.
7. **Seed questions:** `admin.html` (Path A) upload of the validated JSON, or SQL bulk insert mapping §2.1 columns; verify catalog query returns rows via `questions_public`.
8. **Smoke test:** student magic-link login → start → answer → autosave → submit → grade → resume-closed → second-submit replay returns `replayed:true`.
9. **Git backup:** download the seeded JSON, commit under `questions/`, bump `manifest.json`.
10. **Observe:** enable Supabase Auth + Postgres logs; set an alert on failed `submit_attempt` spikes (abuse signal).

---

## 7. Environment variables (`.env.example` — placeholders only)

```ini
# Copy to .env locally. NEVER commit real values. Frontend uses ONLY the ANON key.
SUPABASE_URL=https://xyzcompany.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOi...REPLACE_ME
# service_role stays in Supabase dashboard / server vault ONLY — must never appear in the repo or client JS.
```

## 8. GitHub Pages compatibility checklist

- [x] No build step, no Node runtime, no secrets in repo (`.env.example` placeholders only — verified, no `service_role`/private keys anywhere under `Exam Portal/`).
- [x] `supabase-js` loaded via CDN ESM; all remote calls optional (`BootStore` probe + per-method try/catch → `LocalStore`).
- [x] Question files + `manifest.json` are same-origin static JSON — cacheable, CDN-friendly.
- [x] Offline banner copy: *"Backend unavailable — running locally. Progress stays on this device."*
- [x] Validator has **zero dependencies** (`node tools/validate-questions.mjs …` on stock Node 18+).

## 9. Integration contract + open questions for the Frontend Developer

### Contract (do not rename without updating all four: JSON ↔ BACKEND.md ↔ portal.js ↔ HTML)

- Question fields: `id, question, options[4], correctIndex, rationale, topic, difficulty, marks` (exact casing; `question`/`rationale` lengths ≥10 chars per `admin.html#validate`).
- Envelope: `examId, title, description?, version (opaque), durationMinutes?, passPercent?, status?, questions[]` (defaults 30/70).
- Versioned manifest (`questions/manifest.json`): `{ version, updatedAt, catalogBase, exams: [{ id, title, file, version, questionCount, durationMinutes, passPercent, status }] }` → normalized by `normalizeExam()` (§2.5).
- Runtime catalog (`assets/exams.json`, live in pages): `{ exams: [{ id, title, description, durationMin, passingPct, questionFile, status: "open"|"soon" }] }`.
- `localStorage` keys (`OmnyraPortal.K`): `omnyra.exam.theme|student|profile|catalog|activeAttempt`, `omnyra.exam.attempt.<attemptId>`, `omnyra.exam.progress`. Attempt shape per README; `studentKey() = lowercase(email||name||displayName||"guest")`. Remote mode reuses the same keys as a read-through cache (server is source of truth for grades).
- `assets/config.js` shape per §5 (`window.OMNYRA_CONFIG`); absent/empty `SUPABASE_*` ⇒ local-only, no errors.
- Error codes surfaced from RPCs: `NOT_AUTHENTICATED, EXAM_NOT_FOUND, EXAM_NOT_PUBLISHED, EXAM_HAS_NO_QUESTIONS, ATTEMPT_NOT_FOUND, NOT_OWNER, ATTEMPT_NOT_SUBMITTABLE:<status>` — map to friendly copy; `replayed:true` ⇒ "already submitted" notice, not an error.
- CSV authoring (see §4.1): files `questions/template.csv` (fill-me guide) + `questions/template-with-examples.csv` (convertible reference); header exactly `id,question,optionA,optionB,optionC,optionD,correctIndex,rationale,topic,difficulty,marks`; CLI `node "Exam Portal/tools/csv-to-json.mjs" "Exam Portal/questions/<exam-id>.v<date>.csv" --examId <slug> --title "<Title>" --version <date> --out "Exam Portal/questions/<exam-id>.v<date>.json"` → validator PASS. `admin.html` CSV download buttons MUST link these exact committed paths (no inline-generated `question-template.csv`, no renamed headers) so the links never 404.

### Open questions

1. Catalog convergence: pages read `assets/exams.json` while `portal.js loadCatalog()` reads `questions/manifest.json` — migrate pages to `loadCatalog()` now, or keep both until `RemoteStore` lands (backend recommends: migrate to `loadCatalog()`, generate `exams.json` from the manifest in CI)?
2. Timer source of truth: client countdown vs `expires_at` re-sync interval — propose 30s re-sync once remote; OK?
3. Option-shuffle: ship stem-order only in v1 (current) and add per-question option maps in v1.1, or both now?
4. `result.html` rationale fetch (remote): after `submit_attempt`, separate `attempt_review` query or embed `results[]` in the RPC return (current spec embeds)?
5. Config injection: static `assets/config.js` with empty defaults (admin fills at deploy) vs Pages build-time replace — preference? (Backend recommends static file; nothing committed with real keys.)
6. Name capture: magic-link email only, or optional display-name prompt on first login (feeds `profiles.display_name` + certificates)? (v1 `saveStudent` already captures name — propose keeping the prompt and mapping to `display_name`.)
7. Inactivity: v1 watchdog is 30 min + warning modal, timer keeps running — keep 30 min remote, or align to 10-min nudge (§3.4)?
8. CSV header migration (`admin.html`): (a) parse canonical `optionA..optionD` first, still accept legacy `option1..4` for old files (warn); (b) point the CSV template download button at committed `questions/template.csv` (and link `questions/template-with-examples.csv` beside it) instead of the inline-generated `question-template.csv` blob, so admin always gets the versioned template; (c) confirm envelope defaults stay `new-exam` / `Untitled Set` / today / 30 / 70 to match `csv-to-json.mjs`. OK?
9. README CSV line (Frontend-owned): `README.md` still documents `option1..4` columns — sync it to `optionA..optionD` (+ legacy note) when Q8 lands; backend will not edit frontend docs unilaterally.

---

## Appendix — File map (this change)

```
Exam Portal/
├── BACKEND.md                              ← this doc (architecture + setup + RLS + Store spec)
├── .env.example                            ← placeholder keys only
├── questions/
│   ├── manifest.json                       ← versioned catalog (points at sample file)
│   ├── sample-grc-fundamentals.json        ← 10-question shared-contract fixture (PASSES validator)
│   ├── template.csv                        ← CSV fill-me guide: # help + header + 1 placeholder row (fails conversion until filled)
│   └── template-with-examples.csv          ← CSV worked reference: header + 3 GRC/TPRM/ISO-27001 rows (converts + PASSES)
└── tools/
    ├── validate-questions.mjs              ← zero-dep validator (node 18+; untouched by the CSV change)
    └── csv-to-json.mjs                     ← zero-dep CSV→JSON converter: same row rules, envelope via flags/filename (node 18+)
```

*No UI HTML/CSS touched. No secrets committed. All dynamic behavior degrades to local-only on GitHub Pages.*
