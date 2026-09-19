/* OMNyra Exam Portal — shared frontend helpers (static v1, no backend calls).
 * Storage is isolated behind a `Store` interface. v1 ships `LocalStore`
 * (localStorage, keys namespaced `omnyra.exam.*`).
 * // TODO: RemoteStore — implement the same interface against the future
 * // free backend (see README § Integration) and swap in one line:
 * //   const store = new RemoteStore({ baseUrl: API_BASE_URL });
 */
(function () {
  'use strict';

  var NS = 'omnyra.exam.';
  var MANIFEST_URL = window.OMNYRA_MANIFEST_URL || 'questions/manifest.json'; // canonical catalog (BACKEND.md §2.5)
  var IMG_BASE = window.OMNYRA_IMG_BASE || '';
  var K = {
    theme: NS + 'theme',
    student: NS + 'student',
    profile: NS + 'profile',       // backend-canonical display profile {displayName,email,savedAt}
    catalog: NS + 'catalog',       // cached manifest (read-through; server is source of truth later)
    activeAttempt: NS + 'activeAttempt',
    attemptPrefix: NS + 'attempt.',
    progress: NS + 'progress'
  };

  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0;
      return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
  }
  function nowIso() { return new Date().toISOString(); }
  function safeParse(raw, fb) { try { return raw == null ? fb : JSON.parse(raw); } catch (e) { return fb; } }

  /* ---------------- Store interface ----------------
   * get(key, fallback) / set(key, value) / remove(key)
   * getAttempt(id) / saveAttempt(a) / clearAttempt(id)
   * getProgress() / saveProgress(p) — see README schemas.
   */
  function LocalStore() {}
  LocalStore.prototype.get = function (key, fb) { return safeParse(localStorage.getItem(key), fb === undefined ? null : fb); };
  LocalStore.prototype.set = function (key, value) { localStorage.setItem(key, JSON.stringify(value)); };
  LocalStore.prototype.remove = function (key) { localStorage.removeItem(key); };
  LocalStore.prototype.getAttempt = function (id) { return this.get(K.attemptPrefix + id, null); };
  LocalStore.prototype.saveAttempt = function (a) { this.set(K.attemptPrefix + a.attemptId, a); };
  LocalStore.prototype.clearAttempt = function (id) { this.remove(K.attemptPrefix + id); };
  LocalStore.prototype.getProgress = function () { return this.get(K.progress, {}); };
  LocalStore.prototype.saveProgress = function (p) { this.set(K.progress, p); };

  // TODO: RemoteStore — future backend adapter. Must implement the same
  // methods and translate them to REST calls (see README § Integration).
  // function RemoteStore(opts) { this.baseUrl = opts.baseUrl; }
  // RemoteStore.prototype.getAttempt = async function (id) { ... };

  var store = new LocalStore();
  var API_BASE_URL = null; // TODO: set when backend exists; v1 makes zero network calls.

  /* ---------------- theme (mirrors main site: html[data-theme]) ----------------
   * Light is the default/first-class theme. A saved preference in
   * `omnyra.exam.theme` ("light"|"dark") always wins; fresh profiles get light.
   */
  var LOGOS = { dark: IMG_BASE + 'img/Monochrome_white-transparent.png', light: IMG_BASE + 'img/primary-logo-transparent.png' };
  var DEFAULT_THEME = 'light';
  function currentTheme() { return document.documentElement.getAttribute('data-theme') || DEFAULT_THEME; }
  function syncThemeToggles(t) {
    var label = t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
    ['themeToggle', 'mobileThemeToggle'].forEach(function (id) {
      var b = document.getElementById(id);
      if (b) {
        b.setAttribute('aria-label', label);
        b.setAttribute('title', label);
        b.setAttribute('data-state', t);
        b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
      }
    });
  }
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem(K.theme, JSON.stringify(t)); } catch (e) {}
    document.querySelectorAll('[data-logo-swap]').forEach(function (img) {
      img.src = t === 'light' ? LOGOS.light : LOGOS.dark;
    });
    syncThemeToggles(t);
  }
  function initTheme() {
    var saved = safeParse(localStorage.getItem(K.theme), null);
    applyTheme(saved === 'light' || saved === 'dark' ? saved : DEFAULT_THEME);
    ['themeToggle', 'mobileThemeToggle'].forEach(function (id) {
      var b = document.getElementById(id);
      if (b) b.addEventListener('click', function () {
        applyTheme(currentTheme() === 'dark' ? 'light' : 'dark');
      });
    });
  }

  /* ---------------- nav (hamburger like main site) ---------------- */
  function initNav() {
    var btn = document.getElementById('hamburger');
    var menu = document.getElementById('mobileMenu');
    if (!btn || !menu) return;
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.remove('open'); });
    });
  }

  /* ---------------- catalog (canonical: questions/manifest.json) ----------------
   * Normalizes manifest entries to {id,title,description,durationMinutes,
   * passPercent,questionFile,status,open}. `open` is true for status
   * "published" or "open"; anything else renders as Coming soon.
   * Caches the raw manifest under omnyra.exam.catalog (read-through).
   * TODO(RemoteStore): listExams() hits the catalog API; same normalized shape.
   */
  function normalizeExam(e, base) {
    var st = String(e.status || 'draft').toLowerCase();
    return {
      id: e.id, title: e.title, description: e.description || '',
      durationMinutes: Number(e.durationMinutes) || 30,
      passPercent: (e.passPercent !== undefined ? Number(e.passPercent) : 70),
      questionFile: e.file ? (base + e.file) : null,
      version: e.version, questionCount: e.questionCount,
      status: st, open: (st === 'published' || st === 'open')
    };
  }
  function loadCatalog() {
    // Remote-first when the Supabase layer booted in remote mode;
    // static manifest is the guaranteed fallback (GitHub Pages offline).
    var R = window.OmnyraRemote;
    if (R && typeof R.mode === "function" && R.mode() === "remote" && typeof R.listExams === "function") {
      return R.ready.then(function () {
        return R.listExams().catch(function () { return loadCatalogStatic(); });
      }).then(function (exams) {
        if (exams && exams.length) return exams;
        return loadCatalogStatic();
      });
    }
    return loadCatalogStatic();
  }
  function loadCatalogStatic() {
    return fetch(MANIFEST_URL, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (data) {
      try { store.set(K.catalog, { at: nowIso(), data: data }); } catch (e) {}
      // catalogBase is relative to the manifest file itself (questions/),
      // NOT to the portal root — resolve against the manifest directory.
      var manifestDir = MANIFEST_URL.slice(0, MANIFEST_URL.lastIndexOf('/') + 1);
      var base = (manifestDir + (data.catalogBase || './')).replace(/\/\.\//g, '/');
      return (data.exams || []).map(function (e) { return normalizeExam(e, base); });
    });
  }
  /* ---------------- student session (v1: name/email, no password) ----------------
   * TODO(auth): replace `getStudent/saveStudent` with a backend session
   * (httpOnly cookie / JWT) without changing call sites.
   */
  function studentKey(s) { return ((s && s.email) || (s && s.name) || (s && s.displayName) || 'guest').toLowerCase(); }
  function getStudent() { return store.get(K.student, null) || store.get(K.profile, null); }
  function saveStudent(s) {
    var norm = { name: s.name || s.displayName || '', email: s.email || '', savedAt: s.savedAt || nowIso() };
    store.set(K.student, norm);
    // Mirror backend-canonical profile shape (BACKEND.md §2.6) so RemoteStore can adopt it verbatim.
    store.set(K.profile, { displayName: norm.name, email: norm.email, savedAt: norm.savedAt });
  }
  function ensureStudent(formIds) {
    var existing = getStudent();
    if (existing && (existing.name || existing.displayName)) return existing;
    return null;
  }

  /* ---------------- progress ---------------- */
  function recordResult(examId, pct, passed, total, correct) {
    var s = getStudent();
    var key = studentKey(s);
    var all = store.getProgress();
    if (!all[key]) all[key] = {};
    var prev = all[key][examId] || { best: 0, attempts: 0, history: [] };
    prev.attempts += 1;
    prev.best = Math.max(prev.best, pct);
    prev.lastAt = nowIso();
    prev.history.push({ at: nowIso(), pct: pct, passed: passed, score: correct + '/' + total });
    prev.history = prev.history.slice(-20);
    all[key][examId] = prev;
    store.saveProgress(all);
    return prev;
  }
  function getProgressFor(examId) {
    var all = store.getProgress();
    return (all[studentKey(getStudent())] || {})[examId] || null;
  }

  /* ---------------- misc UI ---------------- */
  var toastTimer = null;
  function toast(msg) {
    var el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove('show'); }, 2600);
  }
  function openModal(id) { var m = document.getElementById(id); if (m) m.classList.add('open'); }
  function closeModal(id) { var m = document.getElementById(id); if (m) m.classList.remove('open'); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ---------------- seeded shuffle (stable per-attempt order) ----------------
   * mulberry32 PRNG + Fisher–Yates. Same seed = same order (resume-safe).
   */
  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function shuffleSeeded(arr, seed) {
    var out = arr.slice();
    var rand = mulberry32(seed);
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(rand() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  /* ---------------- inactivity watchdog (30 min) ----------------
   * Calls onWarn() after 30 min without pointer/key activity.
   * Returns a stop() function. No-ops gracefully if tab hidden.
   */
  var INACTIVITY_MS = 30 * 60 * 1000;
  function watchInactivity(onWarn) {
    var t = null;
    function reset() {
      clearTimeout(t);
      t = setTimeout(onWarn, INACTIVITY_MS);
    }
    ['pointerdown', 'keydown', 'touchstart', 'wheel'].forEach(function (ev) {
      window.addEventListener(ev, reset, { passive: true });
    });
    reset();
    return function stop() { clearTimeout(t); };
  }

  /* ---------------- questions: remote-first, static fallback ----------------
   * Remote mode streams answer-stripped rows from questions_public (no
   * correctIndex/rationale pre-submit). Local mode fetches the static file.
   * Always resolves to { questions, source: "remote"|"static" }.
   */
  function loadQuestions(exam) {
    var R = window.OmnyraRemote;
    function viaStatic() {
      if (!exam.questionFile) return Promise.reject(new Error("NO_STATIC_FILE"));
      return fetch(exam.questionFile, { cache: 'no-store' }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      }).then(function (qset) { return { questions: qset.questions || [], source: "static" }; });
    }
    if (R && typeof R.mode === "function" && R.mode() === "remote" && typeof R.getQuestions === "function") {
      return R.ready.then(function () {
        return R.getQuestions(exam.id).then(function (rows) {
          if (rows && rows.length) return { questions: rows, source: "remote" };
          return viaStatic();
        }).catch(function () { return viaStatic(); });
      });
    }
    return viaStatic();
  }
  function friendlyError(e) {
    var msg = (e && e.message) || String(e);
    var map = {
      NOT_AUTHENTICATED: "Please sign in again — your session expired.",
      EXAM_NOT_FOUND: "This exam no longer exists.",
      EXAM_NOT_PUBLISHED: "This exam is not open right now.",
      EXAM_HAS_NO_QUESTIONS: "This exam has no questions yet.",
      ATTEMPT_NOT_FOUND: "Session not found. Start the exam again from the catalog.",
      NOT_OWNER: "This session belongs to a different account.",
      NOT_ADMIN: "This area needs an admin account.",
      LOCAL_ONLY: "Backend unavailable — running locally. Progress stays on this device."
    };
    if (msg.indexOf("PROBE_TIMEOUT") !== -1) return map.LOCAL_ONLY;
    return map[msg] || msg;
  }

  window.OmnyraPortal = {
    K: K, store: store, API_BASE_URL: API_BASE_URL, MANIFEST_URL: MANIFEST_URL,
    uuid: uuid, nowIso: nowIso, esc: esc,
    initTheme: initTheme, applyTheme: applyTheme, currentTheme: currentTheme,
    initNav: initNav,
    loadCatalog: loadCatalog, loadCatalogStatic: loadCatalogStatic, loadQuestions: loadQuestions,
    normalizeExam: normalizeExam, friendlyError: friendlyError,
    mulberry32: mulberry32, shuffleSeeded: shuffleSeeded,
    getStudent: getStudent, saveStudent: saveStudent, ensureStudent: ensureStudent, studentKey: studentKey,
    recordResult: recordResult, getProgressFor: getProgressFor,
    toast: toast, openModal: openModal, closeModal: closeModal,
    watchInactivity: watchInactivity, INACTIVITY_MS: INACTIVITY_MS
  };
})();
