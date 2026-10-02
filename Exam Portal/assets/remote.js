/* OMNyra Exam Portal — Supabase remote layer (ES module, static-safe).
 * Loaded AFTER assets/config.js and assets/portal.js on console pages:
 *   <script src="../assets/config.js"></script>
 *   <script src="../assets/portal.js"></script>
 *   <script type="module" src="../assets/remote.js"></script>
 * Exposes window.OmnyraRemote. All methods degrade: when backend is not
 * configured or the probe fails, `mode` is "local" and exam methods throw
 * a coded LOCAL_ONLY error the pages catch to use static JSON + LocalStore.
 */
import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm";

const cfg = (window.OMNYRA_CONFIG || {});
const BACKEND = cfg.BACKEND || "auto";
const URL = cfg.SUPABASE_URL || "";
const ANON = cfg.SUPABASE_ANON_KEY || "";

const api = {
  mode: "local",
  sb: null,
  ready: null,
  configured() { return !!(URL && ANON && URL.startsWith("https://")); }
};

function withTimeout(promise, ms, label) {
  return Promise.race([
    promise,
    new Promise((_, reject) => setTimeout(() => reject(new Error(label || "TIMEOUT")), ms))
  ]);
}

async function boot() {
  if (BACKEND === "local" || !api.configured()) { api.mode = "local"; return api; }
  try {
    const sb = createClient(URL, ANON, { auth: { persistSession: true, autoRefreshToken: true } });
    api.sb = sb;
    // Probe: cheap catalog read proves URL+key+RLS path works. 3s budget.
    await withTimeout(sb.from("exams").select("id", { count: "exact", head: true }), 3000, "PROBE_TIMEOUT");
    api.mode = "remote";
  } catch (e) {
    api.mode = BACKEND === "supabase" ? "remote-error" : "local";
    if (BACKEND === "supabase") console.error("[OmnyraRemote] forced remote boot failed:", e);
  }
  return api;
}
api.ready = boot();

function needSb() {
  if (api.mode !== "remote" || !api.sb) {
    const err = new Error("LOCAL_ONLY");
    err.code = "LOCAL_ONLY";
    throw err;
  }
  return api.sb;
}

/* ---------------- auth (magic-link, no passwords) ---------------- */
/* Admin magic-link (unchanged). Students use email+password below. */
async function sendLink(email, redirectTo) {
  const sb = needSb();
  const { error } = await sb.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: redirectTo || window.location.href }
  });
  if (error) throw error;
}

async function handleCallback() {
  // Supabase email links return ?code=… (PKCE). Exchange it once per load.
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");
  if (!code || api.mode !== "remote" || !api.sb) return null;
  try {
    const { data, error } = await api.sb.auth.exchangeCodeForSession(code);
    if (error) throw error;
    // Clean the URL so refresh doesn't replay the exchange.
    const url = new URL(window.location.href);
    url.searchParams.delete("code");
    window.history.replaceState({}, "", url.toString());
    return data.session || null;
  } catch (e) {
    console.warn("[OmnyraRemote] code exchange failed:", e);
    return null;
  }
}

async function getSession() {
  if (api.mode !== "remote" || !api.sb) return null;
  const { data } = await api.sb.auth.getSession();
  return data.session || null;
}

async function signOut() {
  // Server sign-out with a timeout race — then ALWAYS clear local session
  // artifacts so a hung request can never trap the user in a signed-in loop.
  if (api.sb) {
    try {
      await withTimeout(api.sb.auth.signOut({ scope: "local" }), 3000, "SIGNOUT_TIMEOUT");
    } catch (e) {}
  }
  try {
    const drop = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && (k.indexOf("sb-") === 0 || k === "omnyra.exam.activeAttempt")) drop.push(k);
    }
    drop.forEach(k => localStorage.removeItem(k));
  } catch (e) {}
}

async function getProfile() {
  const sb = needSb();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return null;
  const { data, error } = await sb.from("profiles").select("id,email,display_name,role").eq("id", user.id).maybeSingle();
  if (error) throw error;
  return data || { id: user.id, email: user.email, display_name: "", role: "student" };
}

async function isAdmin() {
  try {
    const p = await getProfile();
    return !!(p && p.role === "admin");
  } catch (e) { return false; }
}

/* Admin email allowlist (assets/config.js ADMIN_EMAILS). Empty = open. */
function adminAllowlist() {
  const list = (window.OMNYRA_CONFIG && window.OMNYRA_CONFIG.ADMIN_EMAILS) || [];
  return list.map(e => String(e).toLowerCase());
}
function isAdminEmail(email) {
  const list = adminAllowlist();
  if (!list.length) return true;
  return list.indexOf(String(email || "").toLowerCase()) !== -1;
}
function notAdminError() {
  const e = new Error("NOT_ADMIN");
  e.code = "NOT_ADMIN";
  return e;
}

/* Guards for console pages. Local-only mode passes through (v1 name/email).
 * Remote mode: no session → redirect to the console's own login page. */
async function requireStudent(loginHref) {
  await api.ready;
  if (api.mode !== "remote") return { mode: "local", session: null };
  await handleCallback();
  const session = await getSession();
  if (!session) { window.location.replace(loginHref || "login.html"); return null; }
  return { mode: "remote", session };
}

async function requireAdmin(loginHref) {
  await api.ready;
  if (api.mode !== "remote") return { mode: "local", session: null, admin: false };
  await handleCallback();
  const session = await getSession();
  if (!session) { window.location.replace(loginHref || "login.html"); return null; }
  const email = session.user && session.user.email;
  if (!isAdminEmail(email)) {
    await signOut();
    throw notAdminError();
  }
  const admin = await isAdmin();
  if (!admin) {
    await signOut();
    const err = new Error("NOT_ADMIN");
    err.code = "NOT_ADMIN";
    throw err;
  }
  return { mode: "remote", session, admin: true };
}

/* ---------------- student password auth (invite-only) ----------------
 * Flow: admin invites (email + exam_code, code mandatory) → student opens
 * login.html → Setup tab (email + exam code + new password) → we validate
 * the pair via validate_invite RPC (anon-safe) → signUp (Supabase sends the
 * confirmation email from omnyra.training@gmail.com via custom SMTP — this
 * click PROVES inbox ownership) → student clicks link → Login tab
 * (email + password) → claim_invites() → catalog filtered to assigned exams.
 * Uninvited emails are rejected before any account is created.
 */
function validEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(email || "").trim());
}

async function checkInvite(email) {
  const sb = needSb();
  const { data, error } = await sb.rpc("check_invite", { p_email: String(email).trim() });
  if (error) throw error;
  return !!data;
}

async function validateInvite(email, code) {
  const sb = needSb();
  const { data, error } = await sb.rpc("validate_invite", {
    p_email: String(email).trim(),
    p_code: String(code).trim()
  });
  if (error) throw error;
  return data; // bound exam_id
}

async function signUpWithPassword(email, code, password, redirectTo) {
  const sb = needSb();
  if (!validEmail(email)) { const e = new Error("BAD_EMAIL"); e.code = "BAD_EMAIL"; throw e; }
  if (String(password || "").length < 8) { const e = new Error("WEAK_PASSWORD"); e.code = "WEAK_PASSWORD"; throw e; }
  // Pair must exist before we create any account (also enforced server-side).
  await validateInvite(email, code);
  const { data, error } = await sb.auth.signUp({
    email: String(email).trim(),
    password,
    options: { emailRedirectTo: redirectTo || window.location.href }
  });
  if (error) throw error;
  return data; // user must now click the confirmation email (inbox proof)
}

async function signInWithPassword(email, password) {
  const sb = needSb();
  const { data, error } = await sb.auth.signInWithPassword({
    email: String(email).trim(),
    password
  });
  if (error) throw error;
  return data.session || null;
}

async function claimInvites() {
  const sb = needSb();
  const { data, error } = await sb.rpc("claim_invites");
  if (error) throw error;
  return data || 0;
}

/* Exams this signed-in student may take (invite rows, live codes only). */
async function myExamIds() {
  const sb = needSb();
  const { data: { user } } = await sb.auth.getUser();
  if (!user || !user.email) return [];
  const { data: inv, error: e1 } = await sb.from("exam_invites")
    .select("exam_id,exam_code")
    .eq("email", user.email)
    .neq("status", "revoked");
  if (e1) throw e1;
  const rows = inv || [];
  if (!rows.length) return [];
  const wanted = [...new Set(rows.map(r => r.exam_code))];
  const { data: codeRows, error: e2 } = await sb.from("exam_codes")
    .select("code,active,expires_at")
    .in("code", wanted);
  // No code-read policy for students except via "own codes read" (invite join);
  // if that policy blocks the direct read, fall back to trusting invite rows
  // (server still enforces NOT_INVITED in start_attempt).
  let live = null;
  if (!e2) {
    live = new Set((codeRows || [])
      .filter(c => c.active !== false && (!c.expires_at || new Date(c.expires_at).getTime() > Date.now()))
      .map(c => c.code));
  }
  const ids = new Set();
  rows.forEach(r => {
    if (live && !live.has(r.exam_code)) return;
    ids.add(r.exam_id);
  });
  return [...ids];
}

async function myInvites() {
  const sb = needSb();
  const { data: { user } } = await sb.auth.getUser();
  if (!user || !user.email) return [];
  const { data, error } = await sb.from("exam_invites")
    .select("id,email,exam_code,exam_id,status,created_at")
    .eq("email", user.email)
    .order("created_at", { ascending: false });
  if (error) throw error;
  return data || [];
}

/* ---------------- admin: exam codes + invites ---------------- */

function normalizeCode(code) {
  return String(code || "").trim().toUpperCase().replace(/\s+/g, "-");
}

async function listExamCodes() {
  const sb = needSb();
  if (!(await isAdmin())) { const e = new Error("NOT_ADMIN"); e.code = "NOT_ADMIN"; throw e; }
  const { data, error } = await sb.from("exam_codes")
    .select("code,exam_id,label,active,expires_at,created_at,updated_at")
    .order("created_at", { ascending: false });
  if (error) throw error;
  return data || [];
}

async function createExamCode({ code, examId, label, expiresAt }) {
  const sb = needSb();
  if (!(await isAdmin())) { const e = new Error("NOT_ADMIN"); e.code = "NOT_ADMIN"; throw e; }
  const c = normalizeCode(code);
  if (!/^[A-Z0-9][A-Z0-9-]{3,31}$/.test(c)) { const e = new Error("BAD_CODE"); e.code = "BAD_CODE"; throw e; }
  if (!examId) { const e = new Error("EXAM_REQUIRED"); e.code = "EXAM_REQUIRED"; throw e; }
  const { data: { user } } = await sb.auth.getUser();
  const { data, error } = await sb.from("exam_codes").upsert({
    code: c, exam_id: examId, label: label || "",
    active: true, expires_at: expiresAt || null,
    created_by: (user && user.id) || null, updated_at: new Date().toISOString()
  }, { onConflict: "code" }).select().single();
  if (error) throw error;
  return data;
}

async function setExamCodeActive(code, active) {
  const sb = needSb();
  if (!(await isAdmin())) { const e = new Error("NOT_ADMIN"); e.code = "NOT_ADMIN"; throw e; }
  const { error } = await sb.from("exam_codes")
    .update({ active: !!active, updated_at: new Date().toISOString() })
    .eq("code", normalizeCode(code));
  if (error) throw error;
}

async function listInvitesAdmin({ code, examId, search, limit } = {}) {
  const sb = needSb();
  if (!(await isAdmin())) throw notAdminError();
  let q = sb.from("exam_invites")
    .select("id,email,exam_code,exam_id,status,created_at,updated_at")
    .order("created_at", { ascending: false })
    .limit(limit || 1000);
  if (code) q = q.eq("exam_code", normalizeCode(code));
  if (examId) q = q.eq("exam_id", examId);
  const { data, error } = await q;
  if (error) throw error;
  let rows = data || [];
  if (search) {
    const s = String(search).toLowerCase();
    rows = rows.filter(r => (r.email || "").toLowerCase().includes(s) || (r.exam_code || "").includes(s.toUpperCase()));
  }
  return rows;
}

/* Bulk/single invite write. exam_code is MANDATORY per row; the code must
 * exist (created first in the Codes section). exam_id is derived from the
 * code so callers cannot bind an email to a mismatched exam. */
async function addInvites(rows) {
  const sb = needSb();
  if (!(await isAdmin())) throw notAdminError();
  const codes = await listExamCodes();
  const byCode = {};
  codes.forEach(c => { byCode[c.code] = c; });
  const { data: { user } } = await sb.auth.getUser();
  const clean = [];
  const errors = [];
  (rows || []).forEach((r, i) => {
    const email = String((r && r.email) || "").trim();
    const code = normalizeCode(r && (r.exam_code || r.code));
    const tag = "row " + (i + 1) + (email ? " (" + email + ")" : "");
    if (!validEmail(email)) { errors.push({ id: tag, msg: "invalid email" }); return; }
    if (!code) { errors.push({ id: tag, msg: "exam_code is required (create the code first)" }); return; }
    const c = byCode[code];
    if (!c) { errors.push({ id: tag, msg: 'unknown exam_code "' + code + '"' }); return; }
    clean.push({
      email, exam_code: code, exam_id: c.exam_id, status: "invited",
      created_by: (user && user.id) || null, updated_at: new Date().toISOString()
    });
  });
  if (errors.length) { const e = new Error("INVITE_ROWS_INVALID"); e.code = "INVITE_ROWS_INVALID"; e.rows = errors; throw e; }
  // Chunked upserts (email, exam_code) — re-invites refresh, never duplicate.
  for (let i = 0; i < clean.length; i += 100) {
    const chunk = clean.slice(i, i + 100);
    const { error } = await sb.from("exam_invites").upsert(chunk, { onConflict: "email,exam_code" });
    if (error) throw error;
  }
  return { count: clean.length };
}

async function setInviteStatus(id, status) {
  const sb = needSb();
  if (!(await isAdmin())) throw notAdminError();
  const st = String(status || "").toLowerCase();
  if (["invited", "registered", "revoked"].indexOf(st) === -1) {
    const e = new Error("BAD_STATUS"); e.code = "BAD_STATUS"; throw e;
  }
  const { error } = await sb.from("exam_invites")
    .update({ status: st, updated_at: new Date().toISOString() })
    .eq("id", id);
  if (error) throw error;
  return st;
}

/* ---------------- catalog + questions (answer-stripped remotely) ---------------- */
function toNormalizedExam(row) {
  return {
    id: row.id, title: row.title, description: row.description || "",
    durationMinutes: Number(row.duration_minutes) || 30,
    passPercent: row.pass_percent !== undefined ? Number(row.pass_percent) : 70,
    questionFile: null, // remote mode streams from questions_public, not static files
    version: row.version, questionCount: row.question_count ?? null,
    status: String(row.status || "published").toLowerCase(), open: true
  };
}

async function listExams() {
  const sb = needSb();
  const { data, error } = await sb.from("exams").select("id,title,description,duration_minutes,pass_percent,version,status").eq("status", "published").order("title");
  if (error) throw error;
  return (data || []).map(toNormalizedExam);
}

async function listExamsAdmin() {
  const sb = needSb();
  if (!(await isAdmin())) { const e = new Error("NOT_ADMIN"); e.code = "NOT_ADMIN"; throw e; }
  const { data, error } = await sb.from("exams").select("id,title,description,duration_minutes,pass_percent,version,status,updated_at").order("updated_at", { ascending: false });
  if (error) throw error;
  return data || [];
}

async function getQuestions(examId) {
  const sb = needSb();
  const { data, error } = await sb.from("questions_public").select("id,exam_id,slug,stem,options,topic,difficulty,marks,position,version").eq("exam_id", examId).order("position");
  if (error) throw error;
  return (data || []).map(q => ({
    qid: q.id, id: q.slug, question: q.stem, options: q.options,
    topic: q.topic, difficulty: q.difficulty, marks: q.marks,
    correctIndex: undefined, rationale: undefined // stripped pre-submit by design
  }));
}

/* ---------------- attempts + grading ---------------- */
async function startAttempt(examId) {
  const sb = needSb();
  const { data, error } = await sb.rpc("start_attempt", { p_exam_id: examId });
  if (error) throw error;
  return data;
}

async function getAttemptById(attemptId) {
  const sb = needSb();
  const { data, error } = await sb.from("attempts").select("*").eq("id", attemptId).maybeSingle();
  if (error) throw error;
  return data || null;
}

async function getActiveAttempt(examId) {
  const sb = needSb();
  const { data, error } = await sb.from("attempts").select("*").eq("exam_id", examId).in("status", ["created", "in-progress", "autosaved"]).order("updated_at", { ascending: false }).limit(1).maybeSingle();
  if (error) throw error;
  return data || null;
}

async function saveAnswers(attemptId, answersByQid) {
  const sb = needSb();
  const rows = Object.entries(answersByQid).map(([question_id, selected_index]) => ({ attempt_id: attemptId, question_id, selected_index }));
  if (!rows.length) return;
  const { error } = await sb.from("attempt_answers").upsert(rows, { onConflict: "attempt_id,question_id" });
  if (error) throw error;
  await sb.from("attempts").update({ status: "autosaved", updated_at: new Date().toISOString() }).eq("id", attemptId);
}

async function loadAnswers(attemptId) {
  const sb = needSb();
  const { data, error } = await sb.from("attempt_answers").select("question_id,selected_index").eq("attempt_id", attemptId);
  if (error) throw error;
  const out = {};
  (data || []).forEach(r => { if (r.selected_index !== null) out[r.question_id] = r.selected_index; });
  return out;
}

async function submitAttempt(attemptId) {
  const sb = needSb();
  const { data, error } = await sb.rpc("submit_attempt", { p_attempt_id: attemptId });
  if (error) throw error;
  return data; // {attemptId,score,maxScore,percent,passed,late,replayed}
}

async function getReview(attemptId) {
  const sb = needSb();
  // Server-side rationale reveal: allowed only for the owner's graded attempt.
  const { data, error } = await sb.rpc("attempt_review", { p_attempt_id: attemptId });
  if (error) throw error;
  return { attempt: data.attempt, answers: data.answers || [], bank: data.bank || [] };
}

async function getProgress() {
  const sb = needSb();
  const { data, error } = await sb.from("progress").select("exam_id,attempts_count,best_percent,updated_at");
  if (error) throw error;
  return data || [];
}

/* ---------------- admin publish (DB write + Git backup stays in upload page) ---------------- */
async function publishExam(envelope, actorId) {
  const sb = needSb();
  if (!(await isAdmin())) { const e = new Error("NOT_ADMIN"); e.code = "NOT_ADMIN"; throw e; }
  const { data: exam, error: e1 } = await sb.from("exams").upsert({
    id: envelope.examId, title: envelope.title, description: envelope.description || "",
    duration_minutes: envelope.durationMinutes, pass_percent: envelope.passPercent,
    version: envelope.version, status: envelope.status || "published",
    created_by: actorId || null, updated_at: new Date().toISOString()
  }, { onConflict: "id" }).select().single();
  if (e1) throw e1;
  const rows = envelope.questions.map((q, i) => ({
    exam_id: envelope.examId, slug: q.id, stem: q.question, options: q.options,
    correct_index: q.correctIndex, rationale: q.rationale, topic: q.topic || "General",
    difficulty: q.difficulty || "medium", marks: q.marks || 1, position: i, version: envelope.version
  }));
  // Chunked upserts keep large sets under statement limits.
  for (let i = 0; i < rows.length; i += 100) {
    const chunk = rows.slice(i, i + 100);
    const { error } = await sb.from("questions").upsert(chunk, { onConflict: "exam_id,slug" });
    if (error) throw error;
  }
  return { exam, count: rows.length };
}

/* Admin: every student's per-exam progress (attempts, best %, last active),
 * joined to profile emails. Admin-only via the progress + profiles policies. */
async function listStudentProgress() {
  const sb = needSb();
  if (!(await isAdmin())) throw notAdminError();
  const { data: rows, error } = await sb.from("progress")
    .select("student_id,exam_id,attempts_count,best_percent,updated_at")
    .order("updated_at", { ascending: false }).limit(1000);
  if (error) throw error;
  const ids = [...new Set((rows || []).map(r => r.student_id))];
  let profs = [];
  if (ids.length) {
    const { data, error: e2 } = await sb.from("profiles").select("id,email,display_name").in("id", ids);
    if (e2) throw e2;
    profs = data || [];
  }
  const byId = {};
  profs.forEach(p => { byId[p.id] = p; });
  return (rows || []).map(r => ({
    studentId: r.student_id, examId: r.exam_id,
    attempts: r.attempts_count,
    best: r.best_percent !== null ? Math.round(Number(r.best_percent)) : null,
    lastAt: r.updated_at,
    email: (byId[r.student_id] || {}).email || "—",
    displayName: (byId[r.student_id] || {}).display_name || ""
  }));
}

/* Pause / publish / archive an exam. Student catalogs only ever list
 * status='published', so draft/archived vanish from students instantly
 * (new starts are also rejected server-side by start_attempt). */
async function setExamStatus(examId, status) {
  const sb = needSb();
  if (!(await isAdmin())) { const e = new Error("NOT_ADMIN"); e.code = "NOT_ADMIN"; throw e; }
  const st = String(status || "").toLowerCase();
  if (["draft", "published", "archived"].indexOf(st) === -1) {
    const e = new Error("BAD_STATUS"); e.code = "BAD_STATUS"; throw e;
  }
  const { error } = await sb.from("exams")
    .update({ status: st, updated_at: new Date().toISOString() })
    .eq("id", examId);
  if (error) throw error;
  return st;
}

window.OmnyraRemote = {
  ready: api.ready, configured: () => api.configured(),
  mode: () => api.mode,
  get sb() { return api.sb; },
  sendLink, handleCallback, getSession, signOut, getProfile, isAdmin,
  isAdminEmail, adminAllowlist, requireStudent, requireAdmin,
  checkInvite, validateInvite, signUpWithPassword, signInWithPassword, claimInvites,
  myExamIds, myInvites,
  listExamCodes, createExamCode, setExamCodeActive,
  listInvitesAdmin, addInvites, setInviteStatus, normalizeCode,
  listExams, listExamsAdmin, getQuestions,
  startAttempt, getAttemptById, getActiveAttempt, saveAnswers, loadAnswers, submitAttempt, getReview, getProgress,
  publishExam, setExamStatus, listStudentProgress
};
