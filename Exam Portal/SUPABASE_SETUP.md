# OMNyra Exam Portal — Supabase Setup (~20 min, free tier)

Hosting stays **GitHub Pages (static)**. Supabase is the backend behind the
static consoles: Postgres + email magic-link Auth + RLS + two RPCs. The portal
works **local-only** until this is done (all pages degrade gracefully).

## 1. Create the project
1. supabase.com → New project → region **`us-east-1`** or **`eu-west-2`**
   (primary markets US & UK; region is fixed on free tier).
2. Save the DB password in a vault — never in the repo.

## 2. Run the schema
Supabase Dashboard → SQL Editor → paste **`supabase/schema.sql`** → Run.
It creates `profiles`, `exams`, `questions`, `attempts`, `attempt_answers`,
`progress`, the `questions_public` answer-stripped view, `start_attempt` /
`submit_attempt` RPCs, RLS policies, and the auto-profile trigger. Safe to re-run.

## 3. Enable magic-link auth
Authentication → Providers → enable **Email (OTP / magic link)**.
Set Site URL to `https://omnyragroup.online` and add redirect
`https://omnyragroup.online/Exam Portal/student/**` and
`https://omnyragroup.online/Exam Portal/admin/**`.
(Optional local dev: add `http://localhost:8123/Exam Portal/**`.)

## 4. Make yourself admin
1. Sign in once via `Exam Portal/admin/login.html` (creates your profile row).
2. Table Editor → `profiles` → set your row `role = 'admin'`.

Admin entry is gated twice: the `ADMIN_EMAILS` allowlist in
`Exam Portal/assets/config.js` (add/remove addresses there — currently the two
owner emails) plus `profiles.role = 'admin'` in the DB (server-enforced by RLS).

## 5. Wire the static config
Copy the **publishable anon key** + project URL (Project Settings → API) into
the **deployed** `Exam Portal/assets/config.js`:
`SUPABASE_URL`, `SUPABASE_ANON_KEY`. `BACKEND` stays `"auto"`.
Never commit `service_role` anywhere.

## 6. Seed questions
Admin Console → Upload → drop the validated CSV/JSON → **Publish to live
database** (instant) → **Download Git-backup JSON** → commit under
`Exam Portal/questions/` so Git stays the restorable source.
(Or run the SQL bulk path per `BACKEND.md` §2.1.)

## 7. Smoke test
Student magic-link login → start → answer → wait 15s (autosave label changes)
→ submit → grade → retry. Then: second submit replays stored grade
(`replayed:true`); admin login with a student account is rejected; with the
network blocked the portal falls back to local mode with the offline banner.

## Notes
- Answers are never sent to students pre-submit: `questions_public` omits
  `correct_index`/`rationale`; grading is server-side in `submit_attempt`.
- Exam duration is server-enforced (`expires_at = started + duration + 15 min
  grace); the client auto-submits at the duration mark.
- PII is minimal (email + display name + attempts). Document the Supabase
  region in the privacy notice for GDPR/DPDP awareness.
