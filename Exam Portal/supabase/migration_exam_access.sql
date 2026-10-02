-- ============================================================
-- OMNyra Exam Portal — invite-only student access (migration v2)
-- Run AFTER supabase/schema.sql in Supabase SQL Editor.
-- Safe to re-run (IF NOT EXISTS / OR REPLACE / DROP POLICY IF EXISTS).
--
-- What this adds (see BACKEND.md §2 + new §10):
--   exam_codes   — admin-created batch codes, exactly ONE exam per code,
--                   reusable across many students.
--   exam_invites — one row per (email, exam_code); exam assignment is
--                   MANDATORY (exam_code NOT NULL, no orphan emails).
--   RPCs         — check_invite / validate_invite (anon-safe pre-auth
--                   checks), claim_invites (post-login rollup),
--                   start_attempt hardened with NOT_INVITED guard.
-- Auth model: students use email+password (Supabase Auth). Inbox ownership
-- is proven by the confirmation email (sent from omnyra.training@gmail.com
-- via custom SMTP, see SUPABASE_SETUP.md). Authorization = invite row.
-- ============================================================

-- ---- exam_codes: one code → exactly one exam (reusable batch) ----
create table if not exists public.exam_codes (
  code          text primary key,              -- e.g. 'GRC-AUG-01' (stored UPPER, [A-Z0-9-]{4,32})
  exam_id       text not null references public.exams(id) on delete cascade,
  label         text not null default '',
  active        boolean not null default true,
  expires_at    timestamptz,                   -- NULL = never expires
  created_by    uuid references public.profiles(id),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  constraint exam_code_format check (code ~ '^[A-Z0-9][A-Z0-9-]{3,31}$')
);
create index if not exists idx_exam_codes_exam on public.exam_codes (exam_id);

-- ---- exam_invites: email + exam_code (code mandatory by construction) ----
create table if not exists public.exam_invites (
  id            uuid primary key default gen_random_uuid(),
  email         citext not null,               -- invited student email (lowercase compare)
  exam_code     text not null references public.exam_codes(code) on delete cascade,
  exam_id       text not null references public.exams(id) on delete cascade,
  status        text not null default 'invited' check (status in ('invited','registered','revoked')),
  created_by    uuid references public.profiles(id),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (email, exam_code)
);
create index if not exists idx_invites_email on public.exam_invites (email);
create index if not exists idx_invites_code on public.exam_invites (exam_code);
create index if not exists idx_invites_exam on public.exam_invites (exam_id);

alter table public.exam_codes   enable row level security;
alter table public.exam_invites enable row level security;

-- Admin helper already exists (public.is_admin()); reuse it.

-- ---- exam_codes policies ----
drop policy if exists "admin all exam_codes" on public.exam_codes;
drop policy if exists "own codes read" on public.exam_codes;
create policy "admin all exam_codes" on public.exam_codes for all
  using (public.is_admin()) with check (public.is_admin());
-- Authenticated students read only codes they are invited to (for catalog labels).
create policy "own codes read" on public.exam_codes for select
  using (exists (select 1 from public.exam_invites i
                 where i.exam_code = public.exam_codes.code
                   and i.email = (auth.jwt() ->> 'email')::citext
                   and i.status <> 'revoked'));

-- ---- exam_invites policies ----
drop policy if exists "admin all invites" on public.exam_invites;
drop policy if exists "own invites read" on public.exam_invites;
create policy "admin all invites" on public.exam_invites for all
  using (public.is_admin()) with check (public.is_admin());
create policy "own invites read" on public.exam_invites for select
  using (email = (auth.jwt() ->> 'email')::citext);

-- ============================================================
-- RPC: check_invite(p_email) — anon-safe boolean pre-check.
-- Returns true iff a non-revoked invite with an active, unexpired
-- code exists for this email. Leaks only a boolean (no exam list).
-- ============================================================
create or replace function public.check_invite(p_email citext)
returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.exam_invites i
    join public.exam_codes c on c.code = i.exam_code
    where i.email = p_email
      and i.status <> 'revoked'
      and c.active = true
      and (c.expires_at is null or c.expires_at > now())
  );
$$;
grant execute on function public.check_invite(citext) to anon, authenticated;

-- ============================================================
-- RPC: validate_invite(p_email, p_code) — anon-safe pair check used
-- on the password-setup screen. Returns the bound exam_id, or raises
-- NOT_INVITED / CODE_INACTIVE / CODE_EXPIRED / INVITE_REVOKED.
-- ============================================================
create or replace function public.validate_invite(p_email citext, p_code text)
returns text
language plpgsql stable security definer set search_path = public as $$
declare
  v_code public.exam_codes%rowtype;
  v_inv  public.exam_invites%rowtype;
begin
  select * into v_code from public.exam_codes where code = upper(trim(p_code));
  if not found then raise exception 'NOT_INVITED'; end if;
  if v_code.active = false then raise exception 'CODE_INACTIVE'; end if;
  if v_code.expires_at is not null and v_code.expires_at <= now() then
    raise exception 'CODE_EXPIRED';
  end if;
  select * into v_inv from public.exam_invites
   where email = p_email and exam_code = v_code.code;
  if not found then raise exception 'NOT_INVITED'; end if;
  if v_inv.status = 'revoked' then raise exception 'INVITE_REVOKED'; end if;
  return v_code.exam_id;
end $$;
grant execute on function public.validate_invite(citext, text) to anon, authenticated;

-- ============================================================
-- RPC: claim_invites() — post-login rollup. Marks my 'invited' rows
-- 'registered' (admin visibility). Idempotent.
-- ============================================================
create or replace function public.claim_invites()
returns integer
language plpgsql security definer set search_path = public as $$
declare
  v_n integer := 0;
begin
  if auth.uid() is null then raise exception 'NOT_AUTHENTICATED'; end if;
  update public.exam_invites
     set status = 'registered', updated_at = now()
   where email = (auth.jwt() ->> 'email')::citext
     and status = 'invited';
  get diagnostics v_n = row_count;
  return v_n;
end $$;
grant execute on function public.claim_invites() to authenticated;

-- ============================================================
-- Harden start_attempt with invite authorization.
-- Inserts this guard right after the EXAM_NOT_PUBLISHED check;
-- original function body is otherwise unchanged (re-created here so
-- the migration is self-contained).
-- ============================================================
create or replace function public.start_attempt(p_exam_id text)
returns public.attempts
language plpgsql security definer set search_path = public as $$
declare
  v_exam   public.exams%rowtype;
  v_active public.attempts%rowtype;
  v_new    public.attempts%rowtype;
  v_email  citext;
begin
  if auth.uid() is null then raise exception 'NOT_AUTHENTICATED'; end if;

  select * into v_exam from public.exams where id = p_exam_id;
  if not found then raise exception 'EXAM_NOT_FOUND'; end if;
  if v_exam.status <> 'published' then raise exception 'EXAM_NOT_PUBLISHED'; end if;

  -- Invite-only guard: admins bypass; students need a live invite.
  -- (Local-only static mode has no backend, so this only affects remote.)
  if not public.is_admin() then
    v_email := (auth.jwt() ->> 'email')::citext;
    if not exists (
      select 1 from public.exam_invites i
      join public.exam_codes c on c.code = i.exam_code
      where i.email = v_email and i.exam_id = p_exam_id
        and i.status <> 'revoked'
        and c.active = true
        and (c.expires_at is null or c.expires_at > now())
    ) then
      raise exception 'NOT_INVITED';
    end if;
  end if;

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
