/* OMNyra Exam Portal — backend coordinates (deploy-time only).
 * GitHub Pages is static: this file holds NO secrets.
 * - SUPABASE_URL / SUPABASE_ANON_KEY are the publishable values from
 *   Supabase Project Settings → API. Empty strings = local-only mode.
 * - service_role MUST NEVER appear here or in any client JS.
 * - BACKEND: "auto" (probe remote, fall back to local) | "local" (force offline) | "supabase" (force remote, surface errors).
 */
window.OMNYRA_CONFIG = {
  BACKEND: "auto",
  SUPABASE_URL: "https://xdlbimqzhmjkpheowyrh.supabase.co",
  SUPABASE_ANON_KEY: "sb_publishable_Afm_QYeQcMg-_-8L8dwEEA_CFTfiadt",
  API_BASE_URL: null,
  // Admin allowlist: ONLY these emails may use the Admin Console.
  // Add/remove addresses here (lowercase comparison). Empty array = any
  // signed-in account with profiles.role='admin' may enter (not recommended).
  // NOTE: each address must still sign in once, then get profiles.role='admin'
  // in the Supabase Table Editor — the allowlist gates entry, the DB role
  // gates data (defense in depth, enforced server-side by RLS).
  ADMIN_EMAILS: [
    "akashnikhra22@gmail.com",
    "omnyra.training@gmail.com"
  ]
};
