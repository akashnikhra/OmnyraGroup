// OMNyra Exam Portal — send-invites Edge Function.
//
// Why this exists: the portal is static (GitHub Pages) and cannot send
// mail itself. When an admin clicks "Email" in Admin → Access, the browser
// calls this function, which uses the SERVICE_ROLE key (server-side only,
// never in the repo) to send each student a Supabase "Invite" email via
// the already-configured Gmail custom SMTP. The invite link lands on
// student/login.html?invited=1&examCode=<CODE> where the student proves
// inbox ownership and sets a password.
//
// Deploy (needs Supabase CLI + project link; no extra secrets —
// SUPABASE_URL / ANON / SERVICE_ROLE are provided by the runtime):
//   supabase login
//   supabase link --project-ref xdlbimqzhmjkpheowyrh
//   supabase functions deploy send-invites
//
// Auth model: caller must present their own user JWT; the function checks
// profiles.role = 'admin' (DB role is the gate, same as RLS). Invite rows
// are re-read server-side — the client cannot invent recipients.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

// Redirect target must be OUR student login page (production or localhost
// dev) — never an open redirect. The exam code rides along as examCode
// (named to avoid colliding with Supabase's own ?code= PKCE param).
function safeRedirect(base: string, code: string): string {
  const b = String(base || "");
  const prod = /^https:\/\/(www\.)?omnyragroup\.online\/.*student\/login\.html$/.test(b);
  const local = /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/.*student\/login\.html$/.test(b);
  if (!prod && !local) throw new Error("BAD_REDIRECT");
  const sep = b.includes("?") ? "&" : "?";
  return `${b}${sep}invited=1&examCode=${encodeURIComponent(code)}`;
}

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method !== "POST") return json({ error: "METHOD_NOT_ALLOWED" }, 405);

  try {
    const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
    const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
    const ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY") ?? "";
    if (!SUPABASE_URL || !SERVICE_KEY) return json({ error: "MISCONFIGURED" }, 500);

    const authHeader = req.headers.get("Authorization") ?? "";
    const caller = createClient(SUPABASE_URL, ANON_KEY, {
      global: { headers: { Authorization: authHeader } },
    });
    const {
      data: { user },
    } = await caller.auth.getUser();
    if (!user) return json({ error: "NOT_AUTHENTICATED" }, 401);

    const svc = createClient(SUPABASE_URL, SERVICE_KEY);
    const { data: profile } = await svc
      .from("profiles")
      .select("role")
      .eq("id", user.id)
      .maybeSingle();
    if (!profile || profile.role !== "admin") return json({ error: "NOT_ADMIN" }, 403);

    const { inviteIds, redirectBase } = await req.json();
    const ids: string[] = Array.isArray(inviteIds)
      ? inviteIds.filter(Boolean).slice(0, 200)
      : [];
    if (!ids.length) return json({ error: "NO_INVITES" }, 400);

    const { data: invites, error: e1 } = await svc
      .from("exam_invites")
      .select("id,email,exam_code,exam_id,status")
      .in("id", ids);
    if (e1) throw e1;

    const results: Array<Record<string, string>> = [];
    for (const inv of invites ?? []) {
      try {
        if (inv.status === "revoked") {
          results.push({ id: inv.id, email: String(inv.email), status: "skipped_revoked" });
          continue;
        }
        const { data: code } = await svc
          .from("exam_codes")
          .select("code,active,expires_at")
          .eq("code", inv.exam_code)
          .maybeSingle();
        if (
          !code || code.active === false ||
          (code.expires_at && new Date(code.expires_at).getTime() <= Date.now())
        ) {
          results.push({ id: inv.id, email: String(inv.email), status: "skipped_code_inactive" });
          continue;
        }
        const { data: exam } = await svc
          .from("exams")
          .select("title")
          .eq("id", inv.exam_id)
          .maybeSingle();
        const redirectTo = safeRedirect(String(redirectBase || ""), String(inv.exam_code));
        const { error: invErr } = await svc.auth.admin.inviteUserByEmail(String(inv.email), {
          redirectTo,
          data: {
            exam_code: String(inv.exam_code),
            exam_title: (exam && exam.title) || String(inv.exam_id),
          },
        });
        if (invErr) {
          const msg = String(invErr.message || "");
          if (/already registered|already exists|already been registered/i.test(msg)) {
            // Account exists: authorization still comes from the invite row,
            // so the student can use setup/login directly — nothing to send.
            results.push({ id: inv.id, email: String(inv.email), status: "already_registered" });
          } else {
            results.push({ id: inv.id, email: String(inv.email), status: "failed", detail: msg });
          }
          continue;
        }
        const now = new Date().toISOString();
        await svc
          .from("exam_invites")
          .update({ emailed_at: now, updated_at: now })
          .eq("id", inv.id);
        results.push({ id: inv.id, email: String(inv.email), status: "sent" });
      } catch (err) {
        results.push({
          id: inv.id,
          email: String(inv.email),
          status: "failed",
          detail: String((err as Error)?.message || err),
        });
      }
    }
    return json({ results });
  } catch (e) {
    return json(
      { error: "EMAIL_SEND_FAILED", detail: String((e as Error)?.message || e) },
      500,
    );
  }
});
