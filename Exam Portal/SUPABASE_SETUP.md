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
Then paste **`supabase/migration_exam_access.sql`** → Run (invite-only
student access: `exam_codes` + `exam_invites`, anon-safe
`check_invite`/`validate_invite` RPCs, `claim_invites()`, and the
`NOT_INVITED` guard inside `start_attempt`).
Then paste **`supabase/migration_exam_access_v3.sql`** → Run (adds
`exam_invites.emailed_at` for invite-mail tracking). Safe to re-run.

## 3. Enable password auth + your Gmail sender
1. Authentication → Providers → enable **Email** (keep magic-link for
   admins; students use **email + password** with confirmation ON —
   "Confirm email" must stay enabled: the confirmation click is the
   inbox-ownership proof before password login works).
2. Authentication → Emails → SMTP Settings → enable custom SMTP:
   host `smtp.gmail.com:587`, user `omnyra.training@gmail.com`, password =
   a Gmail **App Password** (Google Account → Security → 2-Step Verification
   → App passwords). All student mail (confirmation + invites) then comes
   from your address, not Supabase default.
3. Authentication → URL Configuration → set Site URL to
   `https://omnyragroup.online` and add ALL of these redirects (bare + `www`
   hosts — invite links carry the admin page's host and Supabase rejects the
   click when that exact host is missing):
   `https://omnyragroup.online/Exam Portal/student/**`,
   `https://omnyragroup.online/Exam Portal/admin/**`,
   `https://www.omnyragroup.online/Exam Portal/student/**`,
   `https://www.omnyragroup.online/Exam Portal/admin/**`,
   `https://omnyragroup.online/**`.
   (Optional local dev: add `http://localhost:8123/Exam Portal/**`.)
4. Brand BOTH student mail templates (paste the repo files verbatim, then Save):
   - **Confirm signup** ← `supabase/templates/confirm-signup.html`, subject
     `Confirm your email for {{ .Data.exam_title }}` (students who register via
     the First-time form; exam context comes from signup `user_metadata`).
   - **Invite user** ← `supabase/templates/invite.html` (admin Email button;
     see §5b). Verify each persists with a page reload — unsaved template edits
     are the #1 cause of "email still shows old text" reports.

## 4. Make yourself admin
1. Sign in once via `Exam Portal/admin/login.html` (creates your profile row).
2. Table Editor → `profiles` → set your row `role = 'admin'`.

Admin entry is gated twice: the `ADMIN_EMAILS` allowlist in
`Exam Portal/assets/config.js` (add/remove addresses there — currently the two
owner emails) plus `profiles.role = 'admin'` in the DB (server-enforced by RLS).

## 5b. Deploy the invite-mail function (one-time)
Admin → Access → **Email** buttons call the `send-invites` Edge Function,
which sends each student a Supabase "Invite" email via your Gmail SMTP.
Until deployed, those buttons report "function not deployed" (the manual
setup-form flow still works).
```powershell
npm i -g supabase
supabase login
supabase link --project-ref xdlbimqzhmjkpheowyrh
supabase functions deploy send-invites
```
No secrets to set — the runtime provides `SUPABASE_URL` / `ANON` /
`SERVICE_ROLE` itself, and the service key never touches the repo.
Then brand the mail: Authentication → Emails → Templates → **Invite user**
(paste `supabase/templates/invite.html`; subject
`You're invited: {{ .Data.exam_title }} — set your password`).
The template renders the student's assigned exam dynamically
(`{{ .Data.exam_title }}` + `{{ .Data.exam_code }}` come from the
send-invites function per invite) — do NOT hardcode "GRC mock exam".

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

## 7. Smoke test (invite-only)
1. Admin Console → Access → create code (e.g. `GRC-AUG-01` → exam
   `grc-fundamentals`) → add your own test email with that code (single
   or `questions/template-invites.csv` bulk upload).
2. Student login → First-time tab → registered email + exam code + new
   password → confirmation email arrives from `omnyra.training@gmail.com`
   → click link (inbox proof) → Log in tab → catalog shows ONLY the
   assigned exam.
3. Start → answer → wait 15s (autosave label changes) → submit → grade →
   retry. Uninvited email on setup shows "no access"; revoked invite
   blocks start (`NOT_INVITED`); admin account on student pages is rerouted.
4. Legacy checks still hold: second submit replays stored grade
   (`replayed:true`); with the network blocked the portal falls back to
   local mode with the offline banner.

## Notes
- Answers are never sent to students pre-submit: `questions_public` omits
  `correct_index`/`rationale`; grading is server-side in `submit_attempt`.
- Exam duration is server-enforced (`expires_at = started + duration + 15 min
  grace); the client auto-submits at the duration mark.
- PII is minimal (email + display name + attempts). Document the Supabase
  region in the privacy notice for GDPR/DPDP awareness.
