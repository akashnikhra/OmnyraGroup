# OMNyra Group — Interactive Landing Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two interactive landing pages (`Website/index.html` dark + `Website/light.html` light) with Three.js hero lattice, GSAP scroll animations, responsive nav, and a mailto:/wa.me contact form — per the approved design spec.

**Architecture:** Two standalone HTML entry points share a single `assets/styles.css`, `assets/lattice.js` (Three.js hero hexagonal lattice), and `assets/interactions.js` (GSAP ScrollTrigger reveals, nav, cursor, form, theme toggle). No framework, no build step. Theme is baked via `<html data-theme="dark|light">`; the toggle button navigates between the two files. All brand tokens defined as CSS custom properties in `:root` (dark) with `[data-theme="light"]` overrides.

**Tech Stack:** Vanilla HTML/CSS/JS. Three.js (ES module via import map, pinned to v0.160.0). GSAP + ScrollTrigger (CDN, `defer`). Inter via Google Fonts (300/400/500/600/700/800). No npm, no bundler.

**Verification approach:** This is a static marketing site with no test framework. Each task ends with manual browser verification steps. Final verification uses Lighthouse ≥ 90 on Performance, Accessibility, Best Practices, SEO.

**Spec:** `docs/superpowers/specs/2026-08-16-omnyra-landing-pages-design.md`

---

## File Map

| File | Responsibility |
|------|----------------|
| `Website/index.html` | Dark theme entry. `<html data-theme="dark">`. Full 8-section markup, nav, footer. CDN links. |
| `Website/light.html` | Light theme entry. `<html data-theme="light">`. Same structure, light tokens. |
| `Website/assets/styles.css` | All CSS: theme tokens, base components, section layouts, responsive breakpoints, motion-reduced overrides. |
| `Website/assets/lattice.js` | Three.js hero hexagonal lattice. ES module. Theme-aware. IntersectionObserver pause. |
| `Website/assets/interactions.js` | GSAP ScrollTrigger, sticky nav, hamburger menu, theme toggle, custom cursor, magnetic CTAs, card tilt, section signature motions, contact form composer, prefers-reduced-motion. |

---

### Task 1: Scaffold file structure and HTML skeletons

**Files:**
- Create: `Website/assets/styles.css`
- Create: `Website/assets/lattice.js`
- Create: `Website/assets/interactions.js`
- Create: `Website/index.html`
- Create: `Website/light.html`

- [ ] **Step 1: Create `Website/assets/styles.css` with theme token definitions**

Write the following to `Website/assets/styles.css`. This establishes the entire design system as CSS custom properties. Dark theme is the default under `:root`; light overrides go under `[data-theme="light"]`.

See spec §3.1, §4.1, §4.3 for the full token set. Key tokens:

```css
:root {
  --carbon-foundation: #0D1117;
  --deep-carbon: #161B22;
  --hex-blue: #00A8E8;
  --junction-blue: #0077B6;
  --chrome-lattice: #8B949E;
  --steel: #C9D1D9;
  --white: #FFFFFF;
  --signal-red: #F85149;
  --bg-primary: var(--carbon-foundation);
  --bg-surface: var(--deep-carbon);
  --text-primary: var(--white);
  --text-secondary: var(--chrome-lattice);
  --border-color: rgba(201, 209, 217, 0.12);
  --accent-gradient: linear-gradient(90deg, var(--hex-blue) 0%, var(--junction-blue) 100%);
  --dark-bg-gradient: linear-gradient(135deg, var(--carbon-foundation) 0%, var(--deep-carbon) 100%);
  --light-bg-gradient: linear-gradient(135deg, #f8f9fa 0%, #ffffff 50%, #f0f4f8 100%);
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px; --space-lg: 24px;
  --space-xl: 32px; --space-2xl: 40px; --space-3xl: 60px;
  --radius-sm: 6px; --radius-md: 8px; --radius-lg: 12px;
  --radius-xl: 16px; --radius-full: 50%;
  --shadow-sm: 0 2px 10px rgba(0,0,0,0.1);
  --shadow-md: 0 10px 40px rgba(0,0,0,0.1);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.15);
  --shadow-xl: 0 20px 60px rgba(0,0,0,0.2);
  --max-w: 1200px;
  --nav-h: 80px;
  --nav-h-shrunk: 64px;
}

[data-theme="light"] {
  --bg-primary: #ffffff;
  --bg-surface: #f8f9fa;
  --text-primary: var(--carbon-foundation);
  --text-secondary: #5a6577;
  --border-color: rgba(201, 209, 217, 0.5);
  --shadow-sm: 0 2px 10px rgba(0,0,0,0.06);
  --shadow-md: 0 10px 40px rgba(0,0,0,0.06);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.08);
  --shadow-xl: 0 20px 60px rgba(0,0,0,0.1);
}
```

- [ ] **Step 2: Create empty `lattice.js` and `interactions.js` scaffolds**

Write to `Website/assets/lattice.js`:
```js
// OMNyra Group — Hero Hexagonal Lattice (Three.js)
// Placeholder — implemented in Task 9
console.log('[lattice] loaded');
```

Write to `Website/assets/interactions.js`:
```js
// OMNyra Group — Interactions (GSAP, nav, cursor, form, toggle)
// Placeholder — implemented in Task 10-11
console.log('[interactions] loaded');
```

- [ ] **Step 3: Create `Website/index.html` (dark theme) with full HTML structure**

Write a complete `index.html` with `<html lang="en" data-theme="dark">`. The file must include:

**`<head>` (spec §7):**
- `<meta charset="UTF-8">` and viewport meta
- `<title>`: "OMNyra Group — GRC Training & Risk Advisory"
- `<meta name="description">`: "Practitioner-led GRC training. 35 hours live training across GRC, TPRM, ISO 27001, Risk Management, Data Privacy, AI Cybersecurity. Mock interviews, resume guidance, career mentorship. US & UK."
- `<link rel="canonical" href="https://omnyragroup.online/">`
- `<link rel="alternate" hreflang="en" href="https://omnyragroup.online/">`
- Open Graph + Twitter card meta tags
- `<link rel="icon" href="../favicon.png" type="image/png">`
- Google Fonts link for Inter (weights 300,400,500,600,700,800, display=swap)
- `<link rel="stylesheet" href="assets/styles.css">`
- Schema.org Organization JSON-LD (see existing root index.html for reference)
- Three.js import map pinned to `three@0.160.0`

**`<body>`:**
- `<header class="site-nav" id="site-nav">` with nav-inner containing:
  - Logo: `<img src="../img/Monochrome_white-transparent.png" height="40">` + wordmark
  - `<nav class="nav-links">` with 8 links (Home→hero, Why Us→why, Programs→programs, Who It's For→who, Careers→careers, Pricing→pricing, Process→process, Contact→contact)
  - Theme toggle button (moon SVG icon for dark theme)
  - Hamburger button (3 spans)
- Mobile menu overlay (`<div class="mobile-menu">` with X close button + all 8 nav links)
- `<section class="hero" id="hero">` with `<canvas id="lattice">`, hero-inner grid (text column + visual column), scroll-cue chevron
- `<main>` with all 8 section stubs (`<section id="why">` through `<section id="contact">`)
- Footer with 3-column grid (logo+tagline, nav links, contact links) + bottom row (copyright + back-to-top)
- Script tags: GSAP CDN (defer), ScrollTrigger CDN (defer), lattice.js (type=module), interactions.js (defer)

**Content for all 8 sections** — write the full HTML for each section following the exact content in the design spec:
- §5.1: Hero (eyebrow, headline with gradient-text on "Future", subhead, two segmented CTAs, secondary CTA, 3 stat counters)
- §5.2: Why OMNyra (6 cards with SVG icons: practitioner-led, 35hrs, mock interviews, resume, case studies, mentorship)
- §5.3: Programs (6 program cards with indexes 01-06, titles, values, pills, expandable bullets, hex marks)
- §5.4: Who It's For (2 pathway cards with hex marks, labels, outcomes, program pills, CTAs)
- §5.5: Career Outcomes (6 role hexagons with tooltips, 4 career stats)
- §5.6: Pricing (2 pricing cards with prices/badges/CTAs, 6-item inclusions grid)
- §5.7: Process (4 steps with large step numbers, titles, copy, icons)
- §5.8: Contact (form with name/email/phone/persona-selector/message/submit, fallback link row, success state, contact details card)

Use `data-reveal` attribute on every section and card for GSAP ScrollTrigger.

- [ ] **Step 4: Create `Website/light.html`**

Copy `index.html` into `light.html`, then change:
- `data-theme="dark"` → `data-theme="light"`
- Theme toggle SVG: swap moon to sun icon
- Nav logo: `Monochrome_white-transparent.png` → `primary-logo-transparent.png`
- Footer logo: same swap

- [ ] **Step 5: Commit**

```bash
git add Website/index.html Website/light.html Website/assets/styles.css Website/assets/lattice.js Website/assets/interactions.js
git commit -m "chore: scaffold landing page file structure and HTML skeletons"
```

- [ ] **Step 6: Verify both files load**

Open `Website/index.html` in Chrome. Confirm: dark background, Inter font loads, nav renders, all 8 sections visible, footer renders, no JS errors. Open `Website/light.html` — confirm white/light background, light logo in nav.

---

### Task 2: Write styles.css — base reset, typography, components, nav

**Files:**
- Modify: `Website/assets/styles.css`

- [ ] **Step 1: Append base reset, typography, and utility classes**

Append after the token block. Include:
- `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
- `html { scroll-behavior: smooth; scroll-padding-top: var(--nav-h); }`
- Body: font-family, font-size 16px, line-height 1.6, color text-primary, background dark-bg-gradient, background-attachment fixed, font-smoothing
- `[data-theme="light"] body { background: var(--light-bg-gradient); }`
- img reset, link reset
- `.container` with max-width, margin auto, responsive padding
- Section rhythm: `section { padding-block: 48px }` scaling to 96px on desktop
- `.gradient-text` using background-clip

- [ ] **Step 2: Append base components (spec §4.3)**

Write: `.section-head`, `.section-eyebrow` (12px uppercase letter-spacing 1px Chrome Lattice), `.section-title` (clamp 28-40px, weight 700), `.accent-bar` (3px gradient 60px), `.cta-primary` (14px/28px padding, gradient bg, white, 13px uppercase), `.cta-ghost` (same padding, steel border, transparent), `.card` (24px padding, 12px radius, bg-surface, steel border, shadow-sm), `.pill` (6px/14px, 4px radius, chrome lattice text on gray bg)

- [ ] **Step 3: Append nav styles (spec §4.2)**

Write:
- `.site-nav` fixed, full width, z-index 1000, height var(--nav-h)
- `.site-nav.scrolled` — height shrunk, backdrop-filter blur(12px), background semi-transparent, border-bottom
- `.nav-inner` — flex, space-between, max-width container
- `.nav-logo` — flex with gap, `.nav-wordmark` hidden below 1024px
- `.nav-links` — hidden on mobile, flex with gap on desktop ≥768px
- `.nav-link` — 12px uppercase, letter-spacing 1px, color text-secondary, active::after accent underline
- `.theme-toggle` — 32px round, transparent bg
- `.hamburger` — 3 spans, hidden on desktop, animated on open
- `.mobile-menu` — fixed inset 0, z-index 999, opacity transition, flex centered
- `.mobile-menu.open` — opacity 1, pointer-events auto
- `.mobile-menu-links a` — 24px weight 600

- [ ] **Step 4: Commit**

```bash
git add Website/assets/styles.css
git commit -m "feat: add base reset, typography, components, and nav styles"
```

- [ ] **Step 5: Verify nav renders**

Open `index.html` in Chrome. Confirm: nav spans full width, links visible on desktop, hamburger visible on mobile (375px viewport), theme toggle renders as moon. Scroll down — nav shrinks and gains backdrop blur.

---

### Task 3: Write styles.css — hero section styles

**Files:**
- Modify: `Website/assets/styles.css`

- [ ] **Step 1: Append hero styles (spec §5.1)**

Write:
- `.hero` — position relative, min-height 100vh, flex center, padding-top nav-h, overflow hidden
- `.hero #lattice` — absolute inset 0, z-index 0, pointer-events none
- `.hero-inner` — grid, z-index 1, responsive columns (1fr on mobile, 55%/45% on ≥1024px)
- `.hero-eyebrow` — 12px, weight 500, uppercase, letter-spacing 2px, text-secondary
- `.hero-headline` — clamp 36-64px, weight 700, line-height 1.15
- `.hero-subhead` — 18px, weight 400, text-secondary, max-width 540px
- `.hero-ctas` — flex with gap, wrap
- `.hero-secondary-cta` — 14px, hex-blue
- `.hero-stats` — flex with gap 2xl
- `.stat-number` — 32px weight 700; `.stat-suffix` — 20px weight 300 hex-blue; `.stat-label` — 12px uppercase text-secondary
- `.hero-visual` — hidden on mobile, flex center on ≥1024px
- `.scroll-cue` — absolute bottom 32px, centered, bounce animation

- [ ] **Step 2: Commit**

```bash
git add Website/assets/styles.css
git commit -m "feat: add hero section styles with responsive split layout"
```

- [ ] **Step 3: Verify hero layout**

Open at 1440px: split layout, headline, CTAs side by side, stats row. Resize to 375px: single column, stacked vertically.

---

### Task 4: Write styles.css — all section-specific styles

**Files:**
- Modify: `Website/assets/styles.css`

- [ ] **Step 1: Append Why OMNyra styles (spec §5.2)**

Write: `#why .cards-grid` (auto-fit, minmax 280px), `.why-card` (flex column), `.card-icon` (56×56, rounded-xl, rgba hex-blue 0.10 bg), `.card-title` (20px weight 600), `.card-copy` (14px text-secondary)

- [ ] **Step 2: Append Programs styles (spec §5.3)**

Write: `#programs .programs-grid` (auto-fit, minmax 320px), `.program-card` (padding xl, rounded-xl, gradient border via mask, overflow hidden), `.program-index` (64px weight 200 chrome lattice), `.program-title` (22px weight 600), `.program-value` (14px), `.program-footer` (flex space-between), `.program-hex` (32×32, rotate on hover), `.program-expanded` (max-height 0 → 200px), `.program-expanded ul/list/li` with hex-blue dash prefix

- [ ] **Step 3: Append Who It's For styles (spec §5.4)**

Write: `#who .pathways` (grid 1fr → 2-col on desktop), `.pathway-card` (padding xl, bg-surface, border, flex column center text), `.pathway-hex` (80×80), `.pathway-label` (18px weight 600), `.pathway-outcome` (16px text-secondary), `.pathway-programs` (flex wrap pills), `.pathway-connect` (absolute horizontal gradient line, scaleX 0, hidden on mobile)

- [ ] **Step 4: Append Career Outcomes styles (spec §5.5)**

Write: `#careers .hex-lattice` (flex wrap center), `.role-hex` (140×140, clip-path hexagon, bg-surface, hover fills gradient), `.role-title` (14px weight 600), `.role-tooltip` (absolute below, opacity 0→1 on hover), `.career-stats` (grid 2-col → 4-col on desktop)

- [ ] **Step 5: Append Pricing styles (spec §5.6)**

Write: `#pricing .pricing-grid` (grid 1fr → 2-col), `.pricing-card` (padding xl, bg-surface, border), `.pricing-card.primary::before` (gradient top bar 3px), `.pricing-badge` (pill, rgba hex-blue bg), `.pricing-price` (72px weight 700), `.pricing-original` (24px line-through), `.inclusions-grid` (auto-fit minmax 240px), `.inclusion-item` (flex with check mark)

- [ ] **Step 6: Append Process styles (spec §5.7)**

Write: `.process-step` (grid, border-left 4px), `.step-number` (clamp 48-120px weight 200 chrome lattice), `.step-title` (28px weight 600), `.step-copy` (16px text-secondary), `.step-icon` (32×32, svg stroke hex-blue), `.process-flow::before` (absolute vertical accent line, height animated by GSAP)

- [ ] **Step 7: Append Contact styles (spec §5.8)**

Write: `#contact .contact-grid` (grid 1fr → 55%/45%), `.contact-form` (padding xl, bg-surface, focus-within glow), `.form-group`, `.form-label` (14px uppercase letter-spacing 1.5px), `.form-input/.form-textarea` (border-bottom steel, focus gradient border-image), `.persona-selector` (flex gap), `.persona-option` (pill buttons, selected state hex-blue), `.form-submit` (full-width), `.form-error` (signal-red, hidden by default), `.form-success` (hidden, centered), `.contact-details` (flex column gap), `.contact-item` (flex with icon)

- [ ] **Step 8: Append Footer styles**

Write: `.site-footer` (border-top, position relative), `.site-footer::before` (hex pattern bg at 4% opacity), `.footer-inner` (grid 1fr → 3-col), `.footer-tagline` (12px uppercase), `.footer-nav` (flex wrap), `.footer-contact` (14px text-secondary), `.footer-bottom` (flex space-between, border-top)

- [ ] **Step 9: Append Custom Cursor styles (spec §6.4)**

Write: `#cursor` (fixed, 16px round, hex-blue, pointer-events none, z-index 9999, mix-blend-mode difference), `#cursor.visible` (opacity 1), `#cursor.hovering` (40px, gradient bg), `@media (pointer: coarse) { #cursor { display: none } }`

- [ ] **Step 10: Append utility classes**

Write: `[data-reveal] { opacity: 0; transform: translateY(30px); will-change: transform, opacity; }`, `[data-reveal].revealed { opacity: 1; transform: none; }`, `[data-motion="reduced"] [data-reveal] { opacity: 1; transform: none; }`, `[data-motion="reduced"] .scroll-cue { animation: none; }`, `[data-motion="reduced"] #cursor { display: none !important; }`

- [ ] **Step 11: Commit**

```bash
git add Website/assets/styles.css
git commit -m "feat: add all section styles, cursor, and reduced-motion overrides"
```

- [ ] **Step 12: Verify all styles load**

Open `index.html` in Chrome. Scroll through all 8 sections. Confirm no CSS parse errors in DevTools Console → Errors. Each section should have visible content, correct colors, and responsive grid layouts. Resize to 375px — confirm mobile layouts.

---

### Task 5: Write lattice.js — Three.js Hero Hexagonal Lattice

**Files:**
- Modify: `Website/assets/lattice.js`

Replace the placeholder content with the full implementation.

- [ ] **Step 1: Write Three.js scene setup and renderer**

```js
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
```

Get the `#lattice` canvas element. Check `document.documentElement.dataset.theme` for dark/light. Check `window.matchMedia('(prefers-reduced-motion: reduce)')` and set `data-motion` on `<html>`.

Create `THREE.Scene`, `THREE.PerspectiveCamera` (fov 50, positioned at z=30), `THREE.WebGLRenderer` (antialias, alpha, pixelRatio capped at 2, clearColor transparent).

If dark theme: create `EffectComposer` with `RenderPass` + `UnrealBloomPass` (strength 0.6, radius 0.4, threshold 0.85).

- [ ] **Step 2: Build hexagonal lattice geometry**

Create 80–120 hexagons as `THREE.LineSegments`:
- Hex radius = 1.2, hex height = sqrt(3) * radius
- Arrange in a honeycomb grid (10 cols × 8 rows), offset every other row by half hex width
- Use `THREE.BufferGeometry` with position attributes for each hex's 6 edges
- Stroke color: dark theme = `#00A8E8` at ~50% opacity; light theme = `#0077B6` at ~40% opacity
- ~10% of hexes get a filled material (gradient-ish via `THREE.MeshBasicMaterial`) as the "lit graduates"

- [ ] **Step 3: Add watermark texture**

Load `icon-only-transparent.png` as a `THREE.Texture` via `THREE.TextureLoader`. Create a `THREE.PlaneGeometry(8, 8)` with `THREE.MeshBasicMaterial` using the texture, opacity 0.08 (dark) / 0.04 (light), transparent true. Position behind the hex grid.

- [ ] **Step 4: Implement animation loop**

In `requestAnimationFrame` loop:
- Rotate hex group: `rotation.y += 0.001` (slow continuous Y rotation)
- Z bob: `group.position.z = Math.sin(Date.now() * 0.001) * 0.3`
- Mouse parallax (desktop only): track `mouse.x`, `mouse.y` (normalized -1 to 1 from center). Lerp `group.rotation.x` toward `mouse.y * 0.15` at rate 0.05. Lerp `group.rotation.y` toward `mouse.x * 0.15` at rate 0.05.
- If dark theme + composer: `composer.render()`. Otherwise: `renderer.render(scene, camera)`.
- If `prefers-reduced-motion`: skip rotation, skip mouse parallax, render once and stop.

- [ ] **Step 5: Add hero assembly animation (load timeline)**

On load, hexagons start at random positions scattered off-screen (`x: ±8, y: ±8, z: ±5`) and animate to their lattice positions over 1.2s with `power3.out` easing. Use GSAP timeline imported from the global `gsap` (loaded via CDN before this module):

```js
// Hex positions were stored in an array during geometry creation
// Each hex tween: { x: targetX, y: targetY, z: 0 }, duration: 1.2, ease: "power3.out", stagger: 0.01
```

- [ ] **Step 6: Add IntersectionObserver pause**

```js
const observer = new IntersectionObserver(
  ([entry]) => {
    if (entry.isIntersecting) {
      renderer.setAnimationLoop(animate);
    } else {
      renderer.setAnimationLoop(null); // stops the loop
    }
  },
  { threshold: 0 }
);
observer.observe(canvas);
```

- [ ] **Step 7: Add scroll-driven fade out**

Use GSAP ScrollTrigger (global, already loaded via CDN) to scrub the lattice opacity from 1 → 0 as the user scrolls past the hero:

```js
gsap.to(canvas, {
  opacity: 0,
  scale: 1.2,
  scrollTrigger: {
    trigger: '.hero',
    start: 'top top',
    end: 'bottom top',
    scrub: 1
  }
});
```

- [ ] **Step 8: Handle resize**

```js
window.addEventListener('resize', () => {
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  if (composer) composer.setSize(w, h);
});
```

- [ ] **Step 9: Commit**

```bash
git add Website/assets/lattice.js
git commit -m "feat: implement Three.js hero hexagonal lattice with bloom and parallax"
```

- [ ] **Step 10: Verify lattice renders**

Open `index.html` in Chrome. Confirm: hexagonal lattice visible in hero area on desktop (1440px), slow rotation animation, subtle glow (bloom), mouse movement creates parallax. Scroll down — lattice fades out. Resize to 375px — lattice not visible in hero (full-bleed background, hidden on mobile by CSS). Check `prefers-reduced-motion` — disable via Chrome DevTools (Rendering panel) → confirm static render, no animation.

---

### Task 6: Write interactions.js — GSAP reveals + sticky nav + mobile menu

**Files:**
- Modify: `Website/assets/interactions.js`

- [ ] **Step 1: Wait for GSAP and ScrollTrigger to load, then register**

```js
document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    console.warn('[interactions] GSAP not loaded');
    return;
  }
  gsap.registerPlugin(ScrollTrigger);
  initReveals();
  initStickyNav();
  initMobileMenu();
  initThemeToggle();
  initCustomCursor();
  initMagneticButtons();
  initCardTilt();
  initProgramExpand();
  initContactForm();
  initCounters();
  initReducedMotion();
});
```

- [ ] **Step 2: Implement `initReveals()` — section + card fade-up**

```js
function initReveals() {
  const reveals = document.querySelectorAll('[data-reveal]');
  reveals.forEach(el => {
    gsap.fromTo(el,
      { opacity: 0, y: 30 },
      {
        opacity: 1, y: 0,
        duration: 0.6,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          toggleActions: 'play none none none'
        }
      }
    );
  });
}
```

- [ ] **Step 3: Implement `initStickyNav()` — scroll-based nav shrink + backdrop**

```js
function initStickyNav() {
  const nav = document.getElementById('site-nav');
  ScrollTrigger.create({
    trigger: '.hero',
    start: 'bottom top+=80',
    onEnter: () => nav.classList.add('scrolled'),
    onLeaveBack: () => nav.classList.remove('scrolled')
  });

  // Active section tracking
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  sections.forEach(section => {
    ScrollTrigger.create({
      trigger: section,
      start: 'top center',
      end: 'bottom center',
      onEnter: () => setActiveLink(section.id),
      onEnterBack: () => setActiveLink(section.id)
    });
  });
  function setActiveLink(id) {
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === '#' + id);
    });
  }
}
```

- [ ] **Step 4: Implement `initMobileMenu()` — hamburger toggle**

```js
function initMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const menu = document.getElementById('mobile-menu');
  const closeBtn = document.getElementById('mobile-menu-close');
  const links = menu.querySelectorAll('a');

  function openMenu() {
    hamburger.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    menu.classList.add('open');
    menu.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    menu.classList.remove('open');
    menu.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  hamburger.addEventListener('click', openMenu);
  closeBtn.addEventListener('click', closeMenu);
  links.forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('open')) closeMenu();
  });
}
```

- [ ] **Step 5: Commit**

```bash
git add Website/assets/interactions.js
git commit -m "feat: add GSAP reveals, sticky nav, and mobile menu"
```

- [ ] **Step 6: Verify reveals and nav**

Open `index.html`. Scroll slowly — each section and card should fade up as it enters the viewport. Scroll past hero — nav shrinks and gains backdrop blur. Scroll back up — nav returns to full height. Click hamburger on mobile (375px) — full-screen overlay opens with all links. Click a link — overlay closes and page scrolls to section. Press Escape — overlay closes.

---

### Task 7: Write interactions.js — theme toggle + custom cursor + magnetic buttons

**Files:**
- Modify: `Website/assets/interactions.js`

- [ ] **Step 1: Implement `initThemeToggle()` — navigate to opposite file**

```js
function initThemeToggle() {
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) return;
  toggle.addEventListener('click', () => {
    const isDark = document.documentElement.dataset.theme === 'dark';
    const next = isDark ? 'light.html' : 'index.html';
    location.href = next + location.hash;
  });
}
```

- [ ] **Step 2: Implement `initCustomCursor()` — trailing dot on desktop**

```js
function initCustomCursor() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  const cursor = document.createElement('div');
  cursor.id = 'cursor';
  document.body.appendChild(cursor);

  let mouseX = 0, mouseY = 0, cursorX = 0, cursorY = 0;

  document.addEventListener('mousemove', e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursor.classList.add('visible');
  });

  document.addEventListener('mouseleave', () => cursor.classList.remove('visible'));

  function animate() {
    cursorX += (mouseX - cursorX) * 0.15;
    cursorY += (mouseY - cursorY) * 0.15;
    cursor.style.transform = `translate(${cursorX - 8}px, ${cursorY - 8}px)`;
    requestAnimationFrame(animate);
  }
  animate();

  // Hover detection
  const hoverTargets = document.querySelectorAll('a, button, .card, .program-card, .role-hex, .pathway-card');
  hoverTargets.forEach(el => {
    el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
  });
}
```

- [ ] **Step 3: Implement `initMagneticButtons()` — CTA buttons follow cursor within radius**

```js
function initMagneticButtons() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  const magnetics = document.querySelectorAll('.magnetic');
  magnetics.forEach(el => {
    el.addEventListener('mousemove', e => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      gsap.to(el, { x: x * 0.3, y: y * 0.3, duration: 0.3, ease: 'power2.out' });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' });
    });
  });
}
```

- [ ] **Step 4: Implement `initCardTilt()` — 3D perspective tilt on hover (desktop)**

```js
function initCardTilt() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  const cards = document.querySelectorAll('.why-card, .program-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      gsap.to(card, {
        rotateX: -y * 8,
        rotateY: x * 8,
        transformPerspective: 800,
        duration: 0.3,
        ease: 'power2.out'
      });
    });
    card.addEventListener('mouseleave', () => {
      gsap.to(card, { rotateX: 0, rotateY: 0, duration: 0.5, ease: 'power2.out' });
    });
  });
}
```

- [ ] **Step 5: Commit**

```bash
git add Website/assets/interactions.js
git commit -m "feat: add theme toggle, custom cursor, magnetic buttons, card tilt"
```

- [ ] **Step 6: Verify toggle, cursor, and tilt**

Click theme toggle — page navigates to `light.html`, hash preserved. Click again — returns to `index.html`. Move mouse — trailing hex-blue dot follows. Hover CTA buttons — buttons shift toward cursor, spring back on leave. Hover Why-OMNyra cards — cards tilt in 3D perspective.

---

### Task 8: Write interactions.js — section signature motions

**Files:**
- Modify: `Website/assets/interactions.js`

- [ ] **Step 1: Implement Programs scroll-scrubbed hex draw (spec §5.3)**

```js
function initProgramsMotion() {
  const programCards = document.querySelectorAll('.program-card');
  programCards.forEach(card => {
    const hex = card.querySelector('.program-hex svg polygon');
    if (!hex) return;
    const length = hex.getTotalLength ? hex.getTotalLength() : 500;
    gsap.set(hex, { strokeDasharray: length, strokeDashoffset: length });
    gsap.to(hex, {
      strokeDashoffset: 0,
      scrollTrigger: {
        trigger: card,
        start: 'top 80%',
        end: 'top 30%',
        scrub: 1
      }
    });
  });
}
```

- [ ] **Step 2: Implement Programs card dim siblings on hover**

```js
function initProgramHover() {
  const grid = document.querySelector('.programs-grid');
  if (!grid) return;
  const cards = grid.querySelectorAll('.program-card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      cards.forEach(c => {
        if (c !== card) gsap.to(c, { opacity: 0.5, duration: 0.3 });
      });
    });
    card.addEventListener('mouseleave', () => {
      cards.forEach(c => gsap.to(c, { opacity: 1, duration: 0.3 }));
    });
  });
}
```

- [ ] **Step 3: Implement Who It's For pathways converge (spec §5.4)**

```js
function initPathwaysMotion() {
  const leftCard = document.querySelector('.pathway-card:first-child');
  const rightCard = document.querySelector('.pathway-card:last-child');
  const connectLine = document.querySelector('.pathway-connect');
  if (!leftCard || !rightCard) return;

  const tl = gsap.timeline({
    scrollTrigger: { trigger: '#who .pathways', start: 'top 75%' }
  });
  tl.fromTo(leftCard, { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.9, ease: 'power3.out' })
    .fromTo(rightCard, { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.9, ease: 'power3.out' }, '<')
    .to(connectLine, { scaleX: 1, duration: 0.8, ease: 'power2.inOut' }, '-=0.3');
}
```

- [ ] **Step 4: Implement Career hexagons assemble (spec §5.5)**

```js
function initCareersMotion() {
  const hexes = document.querySelectorAll('.role-hex');
  hexes.forEach((hex, i) => {
    gsap.fromTo(hex,
      { x: (Math.random() - 0.5) * 1200, y: (Math.random() - 0.5) * 800, rotation: (Math.random() - 0.5) * 360, opacity: 0 },
      {
        x: 0, y: 0, rotation: 0, opacity: 1,
        duration: 1.2,
        ease: 'elastic.out(1, 0.6)',
        delay: i * 0.08,
        scrollTrigger: { trigger: '#careers .hex-lattice', start: 'top 80%' }
      }
    );
  });
}
```

- [ ] **Step 5: Implement Pricing count-up + badge pulse (spec §5.6)**

```js
function initPricingMotion() {
  const cards = document.querySelectorAll('.pricing-card');
  cards.forEach((card, i) => {
    gsap.fromTo(card,
      { scale: 0.85, opacity: 0, rotationZ: i === 0 ? -2 : 2 },
      {
        scale: 1, opacity: 0, rotationZ: 0,
        duration: 0.7,
        ease: 'power3.out',
        scrollTrigger: { trigger: '#pricing', start: 'top 75%' }
      }
    );
  });
}
```

- [ ] **Step 6: Implement Process sticky-stack (spec §5.7)**

```js
function initProcessMotion() {
  const steps = document.querySelectorAll('.process-step');
  const accentLine = document.querySelector('.process-flow');
  if (!steps.length) return;

  ScrollTrigger.create({
    trigger: '#process .process-flow',
    start: 'top center',
    end: 'bottom center',
    onUpdate: self => {
      const progress = self.progress;
      if (accentLine) accentLine.style.setProperty('--progress', progress);
      steps.forEach((step, i) => {
        const threshold = (i + 1) / steps.length;
        if (progress >= threshold) {
          step.querySelector('.step-number').style.color = 'var(--hex-blue)';
        } else {
          step.querySelector('.step-number').style.color = 'var(--chrome-lattice)';
        }
      });
    }
  });
}
```

- [ ] **Step 7: Implement Contact CRT scroll lock (spec §5.8)**

```js
function initContactMotion() {
  const contactSection = document.getElementById('contact');
  if (!contactSection) return;

  // Stagger reveal for form + details
  const formGroups = contactSection.querySelectorAll('.form-group');
  gsap.fromTo(formGroups,
    { opacity: 0, y: 20 },
    {
      opacity: 1, y: 0,
      stagger: 0.1,
      duration: 0.5,
      ease: 'power3.out',
      scrollTrigger: { trigger: '#contact', start: 'top 70%' }
    }
  );
}
```

- [ ] **Step 8: Commit**

```bash
git add Website/assets/interactions.js
git commit -m "feat: add section signature motions — programs hex, pathways, careers, pricing, process, contact"
```

- [ ] **Step 9: Verify all signature motions**

Scroll through each section. Programs: hex marks draw in as you scroll. Who It's For: cards slide in from sides, connecting line draws. Careers: hexagons fly in from scattered positions. Pricing: cards scale in, price numbers count up. Process: step numbers turn blue as you scroll through. Contact: form fields stagger in.

---

### Task 9: Write interactions.js — contact form composer + expandable cards + counters + reduced motion

**Files:**
- Modify: `Website/assets/interactions.js`

- [ ] **Step 1: Implement `initProgramExpand()` — click-to-expand cards**

```js
function initProgramExpand() {
  const cards = document.querySelectorAll('.program-card');
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const wasExpanded = card.classList.contains('expanded');
      // Close all others
      cards.forEach(c => c.classList.remove('expanded'));
      if (!wasExpanded) card.classList.add('expanded');
    });
  });
}
```

- [ ] **Step 2: Implement `initContactForm()` — mailto:/wa.me composer (spec §5.8, D11)**

```js
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  // Persona selector
  const personaBtns = document.querySelectorAll('.persona-option');
  let selectedPersona = null;
  personaBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      personaBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      selectedPersona = btn.dataset.persona;
      document.getElementById('error-persona').classList.remove('visible');
    });
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true;

    const name = document.getElementById('form-name');
    const email = document.getElementById('form-email');
    const phone = document.getElementById('form-phone');
    const message = document.getElementById('form-message');

    // Validate name
    if (!name.value.trim()) {
      document.getElementById('error-name').classList.add('visible');
      valid = false;
    } else {
      document.getElementById('error-name').classList.remove('visible');
    }

    // Validate email
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRe.test(email.value.trim())) {
      document.getElementById('error-email').classList.add('visible');
      valid = false;
    } else {
      document.getElementById('error-email').classList.remove('visible');
    }

    // Validate persona
    if (!selectedPersona) {
      document.getElementById('error-persona').classList.add('visible');
      valid = false;
    }

    if (!valid) return;

    // Compose message
    const lines = [
      `Name: ${name.value.trim()}`,
      `Email: ${email.value.trim()}`,
      phone.value.trim() ? `Phone: ${phone.value.trim()}` : null,
      `Persona: ${selectedPersona === 'new' ? 'New to GRC' : 'Working professional'}`,
      message.value.trim() ? `\nMessage: ${message.value.trim()}` : null
    ].filter(Boolean);
    const body = encodeURIComponent(lines.join('\n'));
    const subject = encodeURIComponent('GRC Training Inquiry');

    // Route based on persona
    let url;
    if (selectedPersona === 'new') {
      url = `mailto:omnyra.training@gmail.com?subject=${subject}&body=${body}`;
    } else {
      const waText = encodeURIComponent(
        `Hi, I'm interested in GRC training.\n\nName: ${name.value.trim()}\nEmail: ${email.value.trim()}${phone.value.trim() ? '\nPhone: ' + phone.value.trim() : ''}\n${message.value.trim() ? 'Message: ' + message.value.trim() : ''}`
      );
      url = `https://wa.me/919063370816?text=${waText}`;
    }

    // Show success state
    form.style.display = 'none';
    document.getElementById('form-success').classList.add('visible');

    // Open URL
    window.open(url, '_blank');
  });
}
```

- [ ] **Step 3: Implement `initCounters()` — animated count-up for stat numbers**

```js
function initCounters() {
  const counters = document.querySelectorAll('[data-target]');
  counters.forEach(el => {
    const target = parseInt(el.dataset.target, 10);
    gsap.fromTo(el,
      { innerText: 0 },
      {
        innerText: target,
        duration: 1.5,
        ease: 'power2.out',
        snap: { innerText: 1 },
        scrollTrigger: {
          trigger: el,
          start: 'top 85%'
        }
      }
    );
  });
}
```

- [ ] **Step 4: Implement `initReducedMotion()` — disable all motion when reduced**

```js
function initReducedMotion() {
  const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  function apply(reduced) {
    document.documentElement.dataset.motion = reduced ? 'reduced' : 'full';
    if (reduced) {
      ScrollTrigger.getAll().forEach(st => st.kill());
      gsap.globalTimeline.clear();
    }
  }
  apply(mq.matches);
  mq.addEventListener('change', e => apply(e.matches));
}
```

- [ ] **Step 5: Commit**

```bash
git add Website/assets/interactions.js
git commit -m "feat: add contact form composer, program expand, counters, reduced-motion"
```

- [ ] **Step 6: Verify form and expand**

Click a Programs card — "What you'll learn" bullets expand below. Click again — collapses. Click a different card — previous collapses, new one expands. Fill in the contact form (name, email, select persona) — submit → success state shows "Message ready!" and a mailto/wa.me URL opens. Try submitting without name — error pill appears. Try submitting without persona — error pill appears. Try submitting with invalid email — error pill appears.

---

### Task 10: Add section-specific GSAP signature motions to interactions.js

**Files:**
- Modify: `Website/assets/interactions.js`

This task adds the remaining signature motions that were declared in Tasks 6-9 but need the full initialization call wiring.

- [ ] **Step 1: Wire all signature motion init calls into the DOMContentLoaded block**

In the `initReveals()` call block from Task 6, add calls for all signature motions:

```js
initProgramsMotion();  // hex stroke draw
initProgramHover();    // dim siblings
initPathwaysMotion();  // slide in + connecting line
initCareersMotion();   // hex assemble
initPricingMotion();   // scale + count-up
initProcessMotion();   // sticky stack
initContactMotion();   // stagger reveal
```

Ensure the function definitions (from Tasks 8-9) are placed before the DOMContentLoaded call block, or restructure so all functions are defined before invocation.

- [ ] **Step 2: Commit**

```bash
git add Website/assets/interactions.js
git commit -m "feat: wire all signature motion initialization calls"
```

- [ ] **Step 3: Verify complete motion flow**

Scroll from top to bottom of `index.html`. Every section should have at least one signature motion:
1. Hero: lattice assembles, headline words stagger in
2. Why OMNyra: cards fade up with scroll-trigger
3. Programs: hex marks draw in, cards tilt on hover
4. Who It's For: cards slide in from sides, connecting line draws
5. Careers: hexagons fly in from scatter
6. Pricing: cards scale in, prices count up
7. Process: step numbers turn blue progressively
8. Contact: form fields stagger in, submit button glows

---

### Task 11: SEO + meta + JSON-LD final pass

**Files:**
- Modify: `Website/index.html`
- Modify: `Website/light.html`

- [ ] **Step 1: Verify `<head>` completeness in both files**

Ensure both files have:
- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- `<title>` with "OMNyra Group — GRC Training & Risk Advisory"
- `<meta name="description">` (see spec §7 for exact text)
- `<link rel="canonical" href="https://omnyragroup.online/">`
- `<link rel="alternate" hreflang="en">` pointing to the other file
- `<link rel="icon" href="../favicon.png" type="image/png">`
- Open Graph meta tags (og:title, og:description, og:image, og:url, og:type)
- Twitter card meta tags
- Schema.org Organization JSON-LD in `<script type="application/ld+json">`
- Google Fonts preconnect + Inter font link
- Three.js import map

- [ ] **Step 2: Verify all images have alt text**

Check every `<img>` tag has a meaningful `alt` attribute. The nav logos should have `alt="OMNyra Group"`. The favicon should not appear in body.

- [ ] **Step 3: Verify all links have href**

Every `<a>` tag must have an `href` (even if it's `#`). No empty hrefs.

- [ ] **Step 4: Commit**

```bash
git add Website/index.html Website/light.html
git commit -m "docs: verify SEO meta, JSON-LD, and accessibility in both theme files"
```

- [ ] **Step 5: Validate JSON-LD**

Open Chrome DevTools → Elements → search for `application/ld+json`. Copy the JSON and paste into https://validator.schema.org/. Confirm: no errors, Organization type recognized, all required fields present.

---

### Task 12: Performance + Lighthouse + final verification

**Files:** (no new files — this is a verification pass)

- [ ] **Step 1: Verify asset weight budget (spec §6.7)**

Run in terminal:
```bash
wc -c Website/index.html Website/light.html Website/assets/styles.css Website/assets/lattice.js Website/assets/interactions.js
```
Expected: index.html and light.html each < 20KB (markup only), styles.css < 30KB, lattice.js + interactions.js combined < 40KB.

- [ ] **Step 2: Verify CDN loads without errors**

Open `index.html` in Chrome → Network tab. Confirm:
- Inter font loads from Google Fonts (check for `fonts.googleapis.com` and `fonts.gstatic.com` requests)
- Three.js loads from unpkg (check for `unpkg.com/three@0.160.0` request)
- GSAP loads from cdnjs (check for `cdnjs.cloudflare.com/ajax/libs/gsap` request)
- No 404s, no mixed content warnings

- [ ] **Step 3: Verify prefers-reduced-motion**

In Chrome DevTools → Rendering panel → check "Emulate CSS `prefers-reduced-motion: reduce`". Reload page. Confirm:
- No Three.js animation (static hex grid)
- No GSAP scroll animations (all elements visible immediately)
- No custom cursor
- No bounce animation on scroll-cue
- `.scroll-cue` animation is disabled

- [ ] **Step 4: Run Lighthouse on desktop**

In Chrome DevTools → Lighthouse tab:
- Mode: Navigation
- Device: Desktop
- Categories: Performance, Accessibility, Best Practices, SEO (all checked)
- Run Lighthouse audit on `Website/index.html`

Target: **≥ 90 on all four categories.**

If Performance < 90:
- Check for render-blocking resources (move fonts to preconnect, ensure `defer` on scripts)
- Check for large DOM (should be < 1500 nodes)
- Check for CLS (should be 0 with proper `width`/`height` on canvas and images)
- Check for LCP (should be < 2.5s — likely the headline text)

If Accessibility < 90:
- Check all images have alt text
- Check all form inputs have labels
- Check color contrast (especially Chrome Lattice text on dark backgrounds — ensure ≥ 4.5:1 ratio at 14px+)
- Check all interactive elements have visible focus styles
- Check heading hierarchy (h1 → h2 → h3, no skipped levels)

- [ ] **Step 5: Run Lighthouse on mobile**

Switch to mobile device in Lighthouse. Target ≥ 85 on all categories (mobile is stricter).

- [ ] **Step 6: Cross-browser smoke test**

Test in:
- Chrome (latest) — primary
- Firefox (latest) — check backdrop-filter, clip-path hexagons
- Safari (latest) — check -webkit-backdrop-filter, -webkit-mask for gradient borders
- Mobile Chrome (Android) — check hamburger menu, touch targets
- Mobile Safari (iOS) — check viewport height (100vh issue), touch interactions

For each: load page, scroll through all 8 sections, check nav, check mobile menu, check theme toggle, check contact form submit.

- [ ] **Step 7: Final commit (if any fixes were needed)**

```bash
git add -A
git commit -m "chore: final performance and accessibility fixes for Lighthouse ≥ 90"
```

---

## Completion Checklist

After all 12 tasks are complete, verify:

- [ ] `Website/index.html` renders all 8 sections with correct dark theme colors
- [ ] `Website/light.html` renders all 8 sections with correct light theme colors
- [ ] Theme toggle navigates between files, preserving hash
- [ ] Three.js hex lattice renders in hero only, respects reduced-motion, pauses off-screen
- [ ] All 8 section signature motions work on desktop Chrome at ≥ 60fps
- [ ] Custom cursor visible on desktop, hidden on touch
- [ ] Mobile hamburger menu opens overlay, closes on link tap or Escape
- [ ] Contact form validates, composes mailto:/wa.me URL, shows success state — no backend, no network request
- [ ] All focusable elements have visible focus ring
- [ ] prefers-reduced-motion snaps to final states
- [ ] SEO + JSON-LD present and valid in both files
- [ ] Asset weight budget met
- [ ] Lighthouse ≥ 90 on all four categories (desktop)
- [ ] Git history is clean with meaningful commit messages per task
