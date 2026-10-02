-- ============================================================
-- OMNyra Exam Portal — invite emails tracking (migration v3)
-- Run AFTER migration_exam_access.sql in Supabase SQL Editor.
-- Safe to re-run.
--
-- Adds exam_invites.emailed_at: stamped by the `send-invites` Edge
-- Function whenever an invite email is accepted for delivery by
-- Supabase Auth (sent via the Gmail custom SMTP). Existing select
-- policies already cover the row, so no RLS change is needed.
-- ============================================================
alter table public.exam_invites
  add column if not exists emailed_at timestamptz;
