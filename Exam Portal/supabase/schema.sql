-- ============================================================
-- OMNyra Exam Portal — schema v1 (Supabase / Postgres 15+)
-- Run in Supabase SQL Editor in TWO steps:
--   Step 1: this file (DDL + RLS + views + RPCs + profile trigger)
--   Step 2: create project region us-east-1 or eu-west-2, enable
--           Email magic-link auth, set Site URL to
--           https://omnyragroup.online (see BACKEND.md §6).
-- Safe to re-run (IF NOT EXISTS / OR REPLACE / DROP POLICY IF EXISTS).
-- Source-of-truth: Exam Portal/BACKEND.md §2.2 + §2.3 + §6 step 4.
-- ============================================================
create extension if not exists "pgcrypto";
create extension if not exists "citext";

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
  id               text primary key,
  title            text not null,
  description      text not null default '',
  duration_minutes int  not null check (duration_minutes between 1 and 600),
  pass_percent     numeric(5,2) not null default 70 check (pass_percent between 0 and 100),
  version          text not null default '1970-01-01',
  status           text not null default 'draft' check (status in ('draft','published','archived')),
  created_by       uuid references public.profiles(id),
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now()
);

-- ---- questions: canonical bank (answers live ONLY here) ----
create table if not exists public.questions (
  id            uuid primary key default gen_random_uuid(),
  exam_id       text not null references public.exams(id) on delete cascade,
  slug          text not null,
  stem          text not null,
  options       jsonb not null,
  correct_index smallint not null check (correct_index between 0 and 3),
  rationale     text not null,
  topic         text not null default 'General',
  difficulty    text not null default 'medium' check (difficulty in ('easy','medium','hard')),
  marks         int  not null default 1 check (marks between 1 and 100),
  position      int  not null default 0,
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
  question_order uuid[] not null default '{}',
  started_at    timestamptz not null default now(),
  expires_at    timestamptz not null,
  submitted_at  timestamptz,
  graded_at     timestamptz,
  score         numeric(8,2),
  max_score     numeric(8,2),
  percent       numeric(5,2),
  passed        boolean,
  client_token  uuid not null default gen_random_uuid(),
  updated_at    timestamptz not null default now()
);

-- One ACTIVE attempt per student per exam (concurrent-attempt guard)
create unique index if not exists uniq_active_attempt
  on public.attempts (student_id, exam_id)
  where status in ('created','in-progress','autosaved');

create index if not exists idx_attempts_student on public.attempts (student_id, updated_at desc);
create index if not exists idx_attempts_exam_status on public.attempts (exam_id, status);

-- ---- attempt_answers: one row per question per attempt ----
create table if not exists public.attempt_answers (
  attempt_id     uuid not null references public.attempts(id) on delete cascade,
  question_id    uuid not null references public.questions(id) on delete cascade,
  selected_index smallint check (selected_index between 0 and 3),
  is_correct     boolean,
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

-- ============================================================
-- RLS + secure view + grading RPCs
-- ============================================================
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

-- Answer-stripped view: the ONLY question surface for students.
-- SECURITY DEFINER semantics (security_invoker = false): the view runs with
-- the owner's rights and bypasses RLS on the underlying tables, exposing ONLY
-- the listed columns. Students have NO direct access to questions (no student
-- policy exists there), so correct_index/rationale can never leak pre-submit.
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
  select * into v_new from public.attempts
   where student_id = auth.uid() and exam_id = p_exam_id
     and status in ('created','in-progress','autosaved')
   order by updated_at desc limit 1;
  return v_new;
end $$;

-- ============================================================
-- RPC: submit_attempt(p_attempt_id) — idempotent, server grades
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

  if v_a.status = 'graded' then
    return jsonb_build_object('attemptId', v_a.id, 'score', v_a.score, 'maxScore', v_a.max_score,
                              'percent', v_a.percent, 'passed', v_a.passed, 'replayed', true);
  end if;
  if v_a.status not in ('created','in-progress','autosaved','submitted') then
    raise exception 'ATTEMPT_NOT_SUBMITTABLE:%', v_a.status;
  end if;

  v_late := now() > v_a.expires_at;

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

-- ============================================================
-- RPC: attempt_review(p_attempt_id) — post-grade rationale reveal
-- Returns the graded attempt + answers + bank rows (with correct_index /
-- rationale) ONLY for the owner's graded attempt (or admin). Called by the
-- result page; pre-submit the answers table is unreachable to students.
-- ============================================================
create or replace function public.attempt_review(p_attempt_id uuid)
returns jsonb
language plpgsql security definer set search_path = public as $$
declare
  v_a   public.attempts%rowtype;
  v_out jsonb;
begin
  if auth.uid() is null then raise exception 'NOT_AUTHENTICATED'; end if;

  select * into v_a from public.attempts where id = p_attempt_id;
  if not found then raise exception 'ATTEMPT_NOT_FOUND'; end if;
  if v_a.student_id <> auth.uid() and not public.is_admin() then raise exception 'NOT_OWNER'; end if;
  if v_a.status <> 'graded' then
    raise exception 'NOT_GRADED';
  end if;

  select jsonb_build_object(
    'attempt', jsonb_build_object('id', v_a.id, 'exam_id', v_a.exam_id, 'status', v_a.status,
      'score', v_a.score, 'max_score', v_a.max_score, 'percent', v_a.percent,
      'passed', v_a.passed, 'submitted_at', v_a.submitted_at,
      'question_order', v_a.question_order),
    'answers', coalesce((
      select jsonb_agg(jsonb_build_object('question_id', aa.question_id,
        'selected_index', aa.selected_index, 'is_correct', aa.is_correct))
      from public.attempt_answers aa where aa.attempt_id = v_a.id), '[]'::jsonb),
    'bank', coalesce((
      select jsonb_agg(jsonb_build_object('id', q.id, 'slug', q.slug, 'stem', q.stem,
        'options', q.options, 'correct_index', q.correct_index, 'rationale', q.rationale,
        'topic', q.topic, 'difficulty', q.difficulty, 'marks', q.marks, 'position', q.position)
        order by q.position)
      from public.questions q where q.exam_id = v_a.exam_id), '[]'::jsonb)
  ) into v_out;
  return v_out;
end $$;

-- ============================================================
-- Auto-profile trigger: every magic-link signup gets a profiles row
-- ============================================================
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
