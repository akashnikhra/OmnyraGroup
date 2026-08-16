# OMNyra Group — Interactive Landing Pages Design

- **Status:** Approved (pending user review of written spec)
- **Date:** 2026-08-16
- **Owner:** OMNyra Group (akashnikhra/OmnyraGroup)
- **Scope:** Build the two interactive landing files (`Website/index.html` dark theme + `Website/light.html` light theme) described in `AGENTS.md`, including shared CSS/JS assets, Three.js hero lattice, GSAP scroll animations, and a mailto:/wa.me contact form.

---

## 1. Goals & Non-Goals

### 1.1 Primary goal
Drive visitors to **contact OMNyra via email or WhatsApp** to start a conversation about GRC training ("lead via contact"). No payment is accepted on the page; pricing is informational.

### 1.2 Primary personas (segmented on the page, equal weight)
1. **Aspiring GRC entrants** — students, fresh graduates, career-switchers, international students. Speak to aspiration and career transformation.
2. **Working professionals upskilling** — IT, audit, security, operations professionals adding a GRC specialization. Speak to credentialing and senior roles.

Both personas flow into the same contact funnel at the end.

### 1.3 Non-goals
- No backend, no server-side form handling, no database.
- No payment / checkout integration (pricing is informational only).
- No user accounts, no CMS, no build step, no framework.
- No `light.html` removal (we keep both files as canonical themes).
- No introduction of React, Vite, or any bundler.

---

## 2. Confirmed Decisions

These decisions were made during brainstorming and are binding for this spec:

| # | Decision | Chosen option |
|---|----------|---------------|
| D1 | Primary conversion | Lead via contact (email/WhatsApp chat), not direct purchase |
| D2 | Primary persona | Both personas equally, segmented on the page |
| D3 | Sections | 8 nav sections (see §4) |
| D4 | Theme relationship | Dark = default (`index.html`), light = alternate (`light.html`); toggle navigates between files |
| D5 | Hero layout | Split (text-left / visual-right) |
| D6 | Three.js scope | Hero-only lattice; body sections use static SVG hex pattern |
| D7 | Build approach | **Option A** — two HTML entry files + shared `assets/` folder (CSS/JS) |
| D8 | Theme toggle behavior | Clicking toggle navigates to the other file (preserves `location.hash`) |
| D9 | Motion approach | Stay vanilla: GSAP (ScrollTrigger, timeline, stagger) + Three.js. No React, no Motion library, no shadcn. |
| D10 | Motion intensity | High — every section has at least one signature motion moment |
| D11 | Contact form mechanics | **Option 1** — mailto:/wa.me composer (no backend). Upgrade path to Formspree noted in §10. |

---

## 3. Architecture & File Structure

```
Website/
├── index.html              <-- Dark theme entry. <html data-theme="dark">
├── light.html              <-- Light theme entry. <html data-theme="light">
├── assets/
│   ├── styles.css          <-- Single stylesheet. :root = dark tokens, [data-theme="light"] = light overrides
│   ├── lattice.js          <-- Three.js hero hex-lattice. ES module via import map. Theme-aware. Pauses off-screen.
│   └── interactions.js     <-- GSAP ScrollTrigger reveals, sticky nav, hamburger mobile menu, theme toggle, contact form composer, custom cursor
└── img/                    <-- Existing 5 logo PNGs (already present in repo)
    ├── primary-logo-transparent.png
    ├── Stacked-logo-transparent.png
    ├── icon-only-transparent.png
    ├── Monochrome_dark-transparent.png
    └── Monochrome_white-transparent.png
```

### 3.1 Theme mechanism
- `styles.css` defines the dark palette as default under `:root` (matches brand `design.md`), and the light palette as overrides under `[data-theme="light"]`.
- `index.html` ships with `<html data-theme="dark">` baked into source; `light.html` ships with `<html data-theme="light">`.
- Each URL is the canonical home for one theme (deep-linkable, bookmarkable).

### 3.2 Theme toggle behavior
- A single sun/moon SVG icon button in the nav.
- Dark file shows **moon** (click → navigate to light); light file shows **sun** (click → navigate to dark).
- Click handler preserves the current scroll position by appending `location.hash`:
  ```js
  const next = document.documentElement.dataset.theme === 'dark' ? 'light.html' : 'index.html';
  location.href = next + location.hash;
  ```
- No `localStorage` needed — the file you're on is the source of truth.

### 3.3 CDN dependencies (no npm, no build)
- **Inter** via Google Fonts (`display=swap`), weights 300/400/500/600/700/800.
- **Three.js** via ES module import map pinned to `three@0.160.0` (loaded asynchronously, not blocking initial paint).
- **GSAP** + **ScrollTrigger** via official CDN (`gsap@3.12.5`), loaded with `defer`.

### 3.4 Logo usage (per brand kit)

| Context | Dark theme (`index.html`) | Light theme (`light.html`) |
|---------|----------------------------|----------------------------|
| Nav + footer logo | `Monochrome_white-transparent.png` (40px height) | `primary-logo-transparent.png` (40px height) |
| Hero watermark (inside Three.js scene) | `icon-only-transparent.png` @ 8% opacity, as `THREE.Texture` plane | `icon-only-transparent.png` @ 4% opacity |
| Body section hex pattern bg | Static inline SVG, 6% opacity (Hex Blue stroke) | Static inline SVG, 4% opacity (Junction Blue stroke) |
| Favicon | `icon-only-transparent.png` (copy in repo root as `favicon.png`) | Same |

---

## 4. Global Layout, Nav & Theme System

### 4.1 Container & rhythm
- `--max-w: 1200px` content container, centered. Padding `0 24px` (mobile), `0 40px` (desktop ≥ 768px).
- Section vertical rhythm: `padding-block: 96px` desktop / `64px` tablet / `48px` mobile — consistent across all 8 sections.
- Base type: Inter, `font-size: 16px`, `line-height: 1.6`, weight 400 body / 700 headlines (per `design.md`).
- Body background per theme:
  - Dark: `linear-gradient(135deg, #0D1117 0%, #161B22 100%)` fixed on `body`.
  - Light: `linear-gradient(135deg, #f8f9fa 0%, #ffffff 50%, #f0f4f8 100%)` fixed on `body`.
- Accent gradient (`#00A8E8 → #0077B6`) usage limited to: section-header underline bars, CTAs, divider lines, nav active-indicator. Never used as a chunky fill on body content.

### 4.2 Navigation

**Desktop (≥ 768px):**
```
[logo]  Home  Why Us  Programs  Who It's For  Careers  Pricing  Process  Contact   [theme] ☾
```
- Left: logo (40px height) + wordmark (hidden on tight desktops, visible ≥ 1024px).
- Center/right: nav links, 12px uppercase letter-spacing 1px, weight 500.
- Right edge: theme toggle icon button (32px, `border-radius-full`, no fill).
- Active section indicator: 2px gradient underline below current section's link (driven by ScrollTrigger).
- Scroll behavior: transparent over hero, `rgba(13,17,23,0.85)` + `backdrop-filter: blur(12px)` + 1px Steel bottom border after scrolling past hero. Height shrinks 80px → 64px.

**Mobile (< 768px):**
```
[logo]                                          [theme] [☰]
```
- Hamburger icon only (3-line SVG, stroke 2px, Hex Blue).
- Tap → full-screen overlay menu at `position: fixed`, opaque Carbon Foundation bg, links stacked vertically centered, `48px` line-height, weight 600, fade-in via CSS `opacity` + transform.
- Overlay closes on link tap (smooth-scroll to section) or on `[X]` icon. Closes on `Escape` key.

### 4.3 Base components (defined once in `styles.css`, reused across sections)

| Component | Spec |
|-----------|------|
| `.section-head` | Eyebrow (`12px` uppercase letter-spacing 1px Chrome Lattice) + h2 (`40px` weight 700) + 3px gradient underline 60px wide. |
| `.cta-primary` | Padding `14px 28px`, 8px radius, gradient bg, white text, weight 600, `13px` uppercase letter-spacing 1px. Hover: `translateY -2px` + shadow-lg. |
| `.cta-ghost` | Padding `14px 28px`, 2px Steel border, transparent bg, primary text. Hover: bg `rgba(0,168,232,0.08)`. |
| `.card` | 24px padding, 12px radius, Deep Carbon surface (dark) / white surface (light), 1px Steel border, shadow-sm. |
| `.pill` | `6px 14px` padding, 4px radius, Chrome Lattice text on `rgba(139,148,158,0.12)` bg. For segment labels. |
| `.accent-bar` | 3px gradient bar, 60px wide — section head underline and divider. |
| `.field` | 14px Chrome Lattice label (uppercase letter-spacing 1.5px), transparent input with 1px Steel bottom-border only. On focus: bottom-border becomes gradient (Hex Blue → Junction Blue) growing from `scaleX 0 → 1` origin-left (`0.3s`, `power3.out`). |
| `.tooltip` | Absolute, below trigger, `y 10→0, opacity 0→1` on show (`0.25s`, `power2.out`). |

### 4.4 Accessibility & motion baseline
- All interactive elements: focus-visible outline = 2px Hex Blue offset 2px.
- `prefers-reduced-motion: reduce` → disables Three.js rotation, GSAP reveals snap to final state, custom cursor disabled, scroll-pinned sections become normal flow.
- `<html data-motion="full">` default; JS sets `data-motion="reduced"` if `matchMedia('(prefers-reduced-motion: reduce)')` matches.
- Color contrast: text always `--white` (dark) or `--carbon-foundation` (light). Chrome Lattice only for ≥ 14px secondary text (passes WCAG AA at that size).

---

## 5. Section Specifications

The page has 8 sections, one signature motion moment each, in this order:

| # | Section | nav label | What it does |
|---|---------|-----------|--------------|
| 1 | Hero | Home | Logo + tagline + segmented CTAs ("New to GRC" / "Already in cybersecurity") + Three.js hero lattice + magnetic CTAs + 3 count-up stats |
| 2 | Why OMNyra | Why Us | Six capability cards (practitioner-led, 35 hrs, mock interviews, resume guidance, case studies, mentorship) with scroll-pinned stagger reveal + custom cursor spotlight |
| 3 | Programs | Programs | 6 program tracks (GRC, TPRM, ISO 27001, Risk Mgmt, Data Privacy, AI Cybersecurity) as cards with scroll-scrubbed hex-stroke draw + tilt + 单卡聚焦 (siblings dim) |
| 4 | Who It's For | Who It's For | Two pathway cards (New to GRC / Working pro) slide in from opposite sides + connecting gradient line draws from center outward |
| 5 | Career Outcomes | Careers | Six role hexagons (GRC Analyst, Risk Analyst, TPRM Analyst, Compliance Analyst, ISO 27001 Consultant, Privacy Advocate) assemble from scattered positions + highlight sweep + hover tooltip with salary bands (US/UK) |
| 6 | Pricing & Inclusions | Pricing | Two pricing tiers ($850 individual / $650 group) with count-up reveal + 2×3 inclusions grid with checkmark "rain" reveal |
| 7 | Process | Process | 4 steps (Book → Join → Train → Get placed) as sticky-stack reveal with progress accent line |
| 8 | Contact | Contact | Contact form (mailto:/wa.me composer) + direct contact details card + CRT-style scroll lock + hex map decoration |

### 5.1 Section 1 — Hero (Home)

**Layout:** Split — text-left (55%), visual-right (45%) on ≥ 1024px. Stacks on mobile (text first, lattice canvas behind everything).

**Text column (left):**
1. **Eyebrow** — `12px uppercase letter-spacing 2px`, Chrome Lattice. Text: `"GRC TRAINING & RISK ADVISORY · US & UK"`.
2. **Headline** — `48–64px` fluid `clamp()`, weight 700, white. Two lines:
   - "Empowering Careers."
   - "Securing the **Future**." — the word "Future" in accent gradient via `background-clip: text`, animated draw-in on load.
3. **Subhead** — `18px`, weight 400, Steel (dark) / Chrome Lattice `#5a6577` (light), max-width 540px:
   - "Practitioner-led GRC training that turns students, career-switchers, and working pros into highly sought-after specialists."
4. **Segmented CTAs** — two equally-weighted buttons side by side (16px gap):
   - **"New to GRC"** — ghost button, navigates to `#who`.
   - **"Already in cybersecurity"** — primary gradient button, navigates to `#programs`.
   - Both buttons are **magnetic** (GSAP): cursor within 80px translates the button up to 12px toward cursor; releases with `elastic.out(1, 0.4)` on exit.
5. **Secondary CTA row** — small text link with arrow: "or chat with us →" → opens `#contact`. Hex Blue underline-grow hover.

**Below CTAs — 3-stat row** (count-up on scroll into view, GSAP + ScrollTrigger batch, `power2.out`, 1.5s):
- **35 hrs** Live Training
- **6** Program Tracks
- **$850** Launch Price (from $1000)

**Visual column (right):**
- The Three.js hex-lattice canvas lives here as a contained 480×480px (1:1) element on desktop. On mobile it becomes a full-bleed background behind the stacked text.
- Composition: 80–120 outlined hexagons in a loose honeycomb, each `THREE.LineSegments` with Hex Blue stroke at ~50% opacity. A subset (~10%) of hexes "filled" with a subtle gradient material — these represent "graduates" in the lattice.
- Animation:
  - Continuous slow rotation around Y-axis (0.05 rad/sec) + gentle Z bob (sine wave).
  - On mouse move (desktop only), the whole cluster rotates toward the cursor with damping (lerp 0.05).
  - Scroll-driven: as user scrolls past hero, ScrollTrigger drives the cluster to scale up and fade out (scrub `1`) — hexes "fly past."
  - EffectComposer + UnrealBloomPass glow on lit hexes — dark theme only. Light theme uses cheaper `MeshBasicMaterial` emissive hack.
- `prefers-reduced-motion: reduce` → static render at 3/4 angle, no rotation, no bloom, no scroll scrub.
- Watermark: `icon-only-transparent.png` centered inside the lattice at 8% opacity (dark) / 4% (light), rendered as `THREE.Texture` on a plane behind the hexes.

**GSAP timeline on load** (plays once, staggered):
1. Eyebrow fades up (`0.4s`)
2. Headline words split via manual span-split (`0.06s` stagger, `power3.out`, total `0.8s`)
3. Subhead fades up (`0.5s`, delayed `0.5s`)
4. CTAs fade up + scale-from-0.96 (`0.4s`, stagger `0.1s`, delayed `1s`)
5. Stat row draw-in (`0.4s`, stagger `0.08s`, delayed `1.3s`)
6. Lattice canvas opacity 0 → 1 (`1s`, delayed `0.2s`) + initial "assemble" (hexes fly in from random positions to lattice spots over `1.2s`, `power3.out`)

Hero takes full viewport (`100vh` minus nav), ends with a 1px gradient accent bar + a bouncing scroll-cue chevron.

### 5.2 Section 2 — Why OMNyra

**Layout:** Section head + `2×3` grid of six capability cards (desktop); 1-col stack on mobile.

**Section head:** Eyebrow `"WHY OMNYRA"`, h2 `"Built by practitioners. Made for careers."`, 3px × 60px gradient underline.

**Six cards** (from AGENTS.md "What's Included"):

| # | Title | One-line copy | Icon (inline SVG, stroke Hex Blue) |
|---|-------|----------------|------------------------------------|
| 1 | Practitioner-Led | Taught by working GRC pros, not theorists. | hex-pulse |
| 2 | 35 Hours Live Training | Real-time cohorts, not pre-recorded. | clock |
| 3 | Mock Interviews & Sessions | Practice until the real thing feels easy. | chat |
| 4 | Resume & LinkedIn Guidance | Land the interview before you walk in. | doc |
| 5 | Real-World Case Studies | Learn from actual breaches, audits, frameworks. | folder |
| 6 | Career Mentorship | 1:1 guidance through your transition. | compass |

**Card anatomy:** `.card` base + icon container top (56×56, rounded 14px, bg `rgba(0,168,232,0.10)`, icon 24px centered Hex Blue), title `20px` weight 600, copy `14px` Chrome Lattice (dark) / `#5a6577` (light).
- Hover: GSAP — card lifts `translateY -6px`, shadow grows, icon container fills with accent gradient (bg transitions from `0.10` alpha to `var(--accent-gradient)`), icon stroke switches to white. Duration `0.3s`, `power2.out`.
- Tilt: subtle 3D tilt on mouse move `rotateX/Y ±4°`, `transform: perspective(800px)`. Desktop only. Disabled on touch.

**Motion:**
- Section head reveal: eyebrow + h2 fade-up + accent bar grows from `scaleX 0 → 1` (origin-left, `0.6s`, `power3.out`).
- Cards reveal: scroll-pinned stagger. ScrollTrigger pins the grid for `+=300px`. `ScrollTrigger.batch` animates each card in with `0.08s` stagger: `opacity 0→1, y 60→0, rotateX 8→0`. Duration `0.7s`, `power3.out`. "Dealing cards" feel.
- Custom cursor on desktop: a small Hex Blue trailing dot follows the mouse with `0.15` lerp; grows to 40px and fills accent when hovering `.card`. `mix-blend-mode: difference` on dark theme. Hidden on touch devices (`@media (pointer: coarse)`).
- Icons draw in: each card's SVG icon path animates `stroke-dashoffset` from full to 0 (`0.9s`, `power2.inOut`) when the card reveals.

### 5.3 Section 3 — Programs

**Layout:** Section head + `3×2` grid of six program cards (desktop ≥ 1024px), 2-col tablet, 1-col mobile.

**Section head:** Eyebrow `"PROGRAMS"`, h2 `"Six tracks. Each one a career."`, 3px × 60px gradient underline.

**Six program cards** (the 6 focus areas from AGENTS.md):

| # | Program | One-line value | Tag (pill) |
|---|---------|----------------|------------|
| 1 | GRC Fundamentals | Governance, risk, and compliance end-to-end. | Most popular |
| 2 | Third-Party Risk Management (TPRM) | Vendor risk, due diligence, monitoring. | High demand |
| 3 | ISO 27001 Readiness | ISMS implementation and audit prep. | Hands-on |
| 4 | Risk Management | Enterprise risk frameworks and quantitative methods. | — |
| 5 | Data Privacy & GDPR | Privacy programs, DPIA, cross-border data. | — |
| 6 | AI Cybersecurity | Securing LLMs and ML systems. | Emerging |

**Card anatomy (distinct from Why-OMNyra — premium program card):**
- 1px gradient border (pseudo-element `::before` with gradient bg + mask to render only the border), 16px radius, 28px padding.
- Top: numbered index "01"–"06" in `64px` weight 200 Chrome Lattice.
- Middle: program title `22px` weight 600 + one-line copy `14px` Chrome Lattice.
- Bottom: tag pill (if present) + arrow-link "Explore →" lighting up Hex Blue on hover.
- Right edge: inline SVG hex mark (32px) tinted Hex Blue that rotates on hover `180° → 360°`, `0.6s`, `power2.inOut`.

**Signature motion — "Scroll-scrubbed hex reveal":**
- ScrollTrigger pins the Programs section for `+=500px`.
- Each card's hex mark draws in its `stroke-dashoffset` from `500 → 0`, scrubbed to scroll (hex outline follows user's scroll velocity). Card content (title, copy, arrow) fades up with `0.05s` stagger per card.
- When the section unpins, all hexes complete their draw — feels like "completing a circuit."

**Additional interactivity:**
- Card `tilt-on-hover`: `rotateX/Y ±5°`, `transform: perspective(1000px)`, hex mark `translateZ: 40px` — small in-card parallax.
- Hover a card → other 5 dim to `opacity 0.5` (GSAP siblings). Restores on exit.
- Click a card → expands **in place** (CSS grid row expand + GSAP height anim) to show 3-4 "What you'll learn" bullets. Second click collapses. Pure client-side, no router.

**"What you'll learn" bullet content per program** (shown when card is expanded):

| # | Program | Bullets (3 each) |
|---|---------|-------------------|
| 1 | GRC Fundamentals | Three lines of defense · Risk appetite & tolerance · GRC program design · Regulatory mapping |
| 2 | TPRM | Vendor onboarding & due diligence · Continuous monitoring · Fourth-party risk · SLA & exit strategies |
| 3 | ISO 27001 Readiness | ISMS scope & context · Annex A controls · Internal audit · Certification audit prep |
| 4 | Risk Management | Risk identification & assessment · Risk treatment plans · Quantitative methods (FAIR) · KRIs & reporting |
| 5 | Data Privacy & GDPR | Privacy principles & lawful bases · DPIA · Cross-border transfers · Privacy program operations |
| 6 | AI Cybersecurity | Threat modeling for ML · LLM security risks · Model risk management · AI governance frameworks |

**Parallax:** entire `3×2` grid translates `y: -30px` on scroll-in (ScrollTrigger scrub `0.5`) — feels like the lattice floats inside the section.

### 5.4 Section 4 — Who It's For (segmented pathways)

**Layout:** Section head + two-segment cards side-by-side on desktop (50/50), stack on mobile with vertical divider.

**Section head:** Eyebrow `"WHO IT'S FOR"`, h2 `"Whether you're starting fresh or leveling up."`.

**Two pathways:**

| Left: New to GRC | Right: Already in cybersecurity |
|-------------------|--------------------------------|
| **Who:** Students, Fresh Graduates, Career Switchers, International Students | **Who:** Working Professionals in IT, Audit, Security, Operations |
| **Outcome:** Break into GRC from zero. Get your first GRC Analyst role. | **Outcome:** Add GRC specialization to your existing career. Move into senior/consulting roles. |
| **Recommended programs:** GRC Fundamentals, ISO 27001, Risk Management (as pills) | **Recommended programs:** TPRM, Data Privacy, AI Cybersecurity (as pills) |
| **CTA:** "Start the journey →" (ghost button) → `#contact` | **CTA:** "Plan your next move →" (primary button) → `#contact` |

**Visual treatment:**
- Each pathway in a `.card` with a large outlined hexagon SVG at the top (80px stroke Hex Blue, animated draw-in on scroll).
- Inside the hexagon: persona label (`18px` weight 600, centered) — "Fresh Graduates", "Career Switchers", "Working Pro".
- Below the icon: outcome line (`16px`), recommended programs as pills row, then CTA.
- Connecting gradient line between cards on desktop: `linear-gradient(90deg, transparent, #00A8E8, #0077B6, #00A8E8, transparent)`, 2px. On mobile → vertical gradient divider.

**Signature motion — "Pathways converge":**
- Both pathway cards slide in from opposite sides: left card `x: -120 → 0`, right card `x: 120 → 0`, simultaneously on ScrollTrigger (`0.9s`, `power3.out`, scrub `0.5`).
- The connecting gradient line draws from the center outward: `scaleX 0 → 1` from center (origin `50% 50%`), `0.8s`, `power2.inOut`.
- The hexagon marks on both cards draw in their strokes at the same moment the line completes (synced via GSAP timeline) — implies the two pathways connect through OMNyra.

**Interactivity:**
- Hover on a persona hexagon: subtle pulse (`scale 1 → 1.05 → 1` loop, 1.2s infinite).
- Hovering a program pill inside a pathway cross-references the Programs section — the corresponding program card in §5.3 flashes Hex Blue border for `0.4s` (shared ScrollTrigger `id` mapping, no navigation required).

### 5.5 Section 5 — Career Outcomes

**Layout:** Section head + role-pills row + highlight reels.

**Section head:** Eyebrow `"CAREERS"`, h2 `"Where our graduates land."`.

**Six role titles** (from AGENTS.md "Career Outcomes") as floating hexagon cards in a loose scatter grid (not a uniform grid — matches the lattice motif):

| Role | | Role |
|------|-|------|
| GRC Analyst | | Risk Analyst |
| TPRM Analyst | | Compliance Analyst |
| ISO 27001 Consultant | | Privacy Advocate |

**Visual treatment:**
- Each role inside a hexagon tile (`120px` wide flat-top hex, `clip-path: polygon(25% 5%, 75% 5%, 100% 50%, 75% 95%, 25% 95%, 0 50%)`).
- Hexagon bg: Deep Carbon (dark) / white (light), 1px Steel border. Text: `14px` weight 600 centered inside.
- Six hexagons in an offset 2-row honeycomb pattern (CSS grid with 6 items + negative row-gap + alternating `translateX`) — visually matches the brand honeycomb lattice motif.

**Signature motion — "Hexagons assemble":**
- On scroll-in, six hexagons scatter from outside the viewport and fly to their lattice positions. Each starts at random `x: ±600, y: ±400, rotate: ±180, opacity: 0` and snaps to `x: 0, y: 0, rotate: 0, opacity: 1` with `elastic.out(1, 0.6)`, `1.2s`, stagger `0.08s`.
- After assembly, ScrollTrigger pins the section for `+=200` and a Hex Blue highlight sweep passes across all 6 hexagons in sequence (`0.4s` each, `0.06s` stagger) — `box-shadow` keyframes via GSAP timeline.

**Additional motion:**
- Each hexagon has a continuous subtle float (translateY sine wave ±3px, 2.5s loop, staggered phase per hex).
- On hover: hexagon fills with accent gradient (`0.3s`), text becomes white, and a `.tooltip` appears below showing the salary band in US/UK. Tooltip animates `y: 10 → 0, opacity: 0 → 1`, `0.25s`, `power2.out`.

**Salary band tooltips** (indicative ranges, sourced from US/UK market data; values to be verified by OMNyra before launch):

| Role | US | UK |
|------|-----|-----|
| GRC Analyst | $75–110k | £45–70k |
| Risk Analyst | $80–120k | £50–75k |
| TPRM Analyst | $85–115k | £50–72k |
| Compliance Analyst | $70–105k | £42–65k |
| ISO 27001 Consultant | $90–130k | £55–80k |
| Privacy Advocate | $85–125k | £50–75k |

**Below the hex grid — outcome stats row** (4 stats, count-up on scroll-in, GSAP + ScrollTrigger batch):
- **6** Career paths
- **35 hrs** Live training
- **100%** Practitioner-led
- **∞** Lifetime mentorship framing

### 5.6 Section 6 — Pricing & Inclusions

**Layout:** Section head + two pricing tiers side-by-side (desktop) + below: 2×3 inclusions grid.

**Section head:** Eyebrow `"PRICING"`, h2 `"One price. Everything included."`, subcopy (`16px` Chrome Lattice): "Special launch pricing. Group rates for cohorts of 3+.".

**Two pricing cards** (50/50 on desktop, stack on mobile):

| Left (primary, highlighted): Individual | Right: Group (3 or more) |
|------------------------------------------|---------------------------|
| 3px gradient top border (always-on accent) | 1px Steel top border |
| **$850** (`80px` weight 700) — "from $1000" struck through Chrome Lattice `24px` | **$650** each (`80px` weight 700) — "per person · min 3" Chrome Lattice `16px` |
| "Individual enrollment" subtext | "Team / cohort enrollment" subtext |
| Accent badge: "Launch special — save $150" | Accent badge: "Best for teams of 3+" |
| Primary CTA: "Book a consultation" → `#contact` (mailto default) | Ghost CTA: "Chat about group training" → `#contact` |

**Below the two cards — inclusions grid** (from AGENTS.md "What's Included") rendered as a 2×3 grid of small items (smaller than Why-OMNyra cards, like a checklist):

| ✓ | 35 Hours Live Training | ☑ | Mock Interviews & Sessions |
| ✓ | Resume & LinkedIn Guidance | ☑ | Real-World Case Studies |
| ✓ | Career Mentorship | ☑ | Practitioner-Led Cohorts |

Each item: `14px` title, `12px` Chrome Lattice one-liner, Hex Blue checkmark icon (`16px`) that animates `scale 0 → 1` with `elastic.out(1, 0.5)` on reveal.

**Signature motion — "Price reveal":**
- Both pricing cards start scaled down (`scale: 0.85, opacity: 0`) and slightly rotated (`rotateZ: ±2°`).
- On scroll-in (ScrollTrigger `start: top 75%`), GSAP timeline:
  1. Highlighted (left) card snaps to `scale: 1, rotateZ: 0, opacity: 1`, `power3.out`, `0.7s`.
  2. Right card animates the same with `0.15s` delay.
  3. Price numbers count up from `0 → final` (`1s`, `power2.out`, syncing to the scale-out).
  4. Strikethrough "from $1000" animates `line` width `0 → 100%` across the text after the number settles (`0.4s`, scrubbed).
  5. Accent badges pulse subtly (`scale 1 → 1.04 → 1` loop, 1.6s).
- Inclusions grid reveals as a staggered "check-mark rain": each check icon `scale 0 → 1` elastic in `0.08s` staggered sequence, label fading in 50ms behind each check — feels like features "check themselves off."

**Parallax:** The two pricing cards have inverse parallax — left card `translateY -15px`, right card `+15px` on scroll-in, settling together.

### 5.7 Section 7 — Process / How It Works

**Layout:** Section head + four-step horizontal flow on desktop, vertical timeline on mobile.

**Section head:** Eyebrow `"PROCESS"`, h2 `"How you go from zero to GRC specialist."`.

**Four steps** (numbered 01–04, from AGENTS.md "What's Included" workflow):

| Step | Title | One-line copy | Icon (inline SVG, Hex Blue) |
|------|-------|----------------|------------------------------|
| 01 | Book a consultation | 30-min free chat — we map your goals. | chat bubble |
| 02 | Join a cohort | Pick your track + schedule (US/UK friendly hours). | calendar |
| 03 | Train for 35 hours | Live sessions, mock interviews, case studies. | hex + clock |
| 04 | Get placed | Resume + LinkedIn polished. Interview ready. | rocket |

**Desktop layout — sticky-stack reveal (signature motion):**
- Each step is a full-width row inside a pinned section. ScrollTrigger pins for `+=1200px` total (`300px` per step).
- As you scroll, step cards stack into each other vertically — like a deck being dealt onto a table. Current step: `y: 80 → 0, opacity: 0 → 1`. Previous step: `scale: 1 → 0.95, opacity: 1 → 0.7, filter: brightness(1) → brightness(0.5)` — creates a "depth stack" where earlier steps recede.
- Vertical accent gradient line (4px) on the left of the stack grows as user scrolls — `scaleY` driven by ScrollTrigger scrub.

**Step card anatomy:**
- 60/40 split per row: left is the step number (`120px` weight 200 Chrome Lattice, gradient-tinted on current step), right is title (`28px` weight 600) + copy (`16px` Chrome Lattice) + small inline SVG icon (32px, Hex Blue).
- Icons draw in (`stroke-dashoffset → 0`) when their step becomes active.
- Each step has a progress node in the vertical accent line — a `16px` Hex Blue hexagon (clip-path) that fills with gradient when that step is reached.

**Mobile layout:**
- Pinning disabled. Vertical timeline with 4 steps stacked top-to-bottom. Each step's card reveals with `y: 40 → 0, opacity: 0 → 1`, stagger `0.15s`, on ScrollTrigger. Gradient progress line is full-height on the left, with 4 hex nodes — each fills in sequence when its step scrolls into view.

**Interactivity:**
- Current active step's number changes from Chrome Lattice to Hex Blue gradient (`background-clip: text`) and "pops" with `scale 1.08 → 1` — reinforces progression.
- Hovering a future step "previews" it: lifts slightly + accent line grows toward it.

### 5.8 Section 8 — Contact / Book a Consultation (final conversion)

**Layout:** Section head + contact form on left (55%), contact details on right (45%) on desktop; stacked form-first on mobile.

**Section head:** Eyebrow `"CONTACT"`, h2 `"Let's talk. Book your free consultation."`, subcopy "Reply within 24 hours. No spam. No obligation.".

**Left — Contact form** (`.contact-form`) **— mailto:/wa.me composer (no backend):**

> **Form behavior (confirmed decision D11):** The form is a **front-end composer only**. There is no POST, no `fetch`, no backend, no third-party form service. On submit, JS reads the field values and composes either a `mailto:` or `wa.me` URL that opens the visitor's own mail or WhatsApp client pre-filled with their details. See §10 for the future upgrade path.

**Fields:**
1. Name (text, required)
2. Email (email, required)
3. WhatsApp/Phone (tel, optional)
4. "Which describes you?" — segmented radio styled as pills: "New to GRC" / "Working professional" (drives destination channel on submit; required)
5. Message (textarea, optional, placeholder "I'd like to discuss GRC training...")

**Inputs** use the `.field` component (see §4.3): 14px Chrome Lattice label uppercase letter-spacing 1.5px, transparent inputs with 1px Steel bottom-border only. On focus: bottom-border becomes gradient (Hex Blue → Junction Blue) and grows from `scaleX 0` origin-left to 1 (`0.3s`, `power3.out`) — a "filling in" feel.

**Submit behavior:**
- The submit button (`.cta-primary`, full-width, magnetic) does NOT issue a network request. On click:
  1. Client-side validation runs (required fields present, email format valid, segmented radio selected).
  2. If invalid: visible Chrome Lattice error pill appears under the offending field(s). No submit.
  3. If valid: JS reads field values and URL-encodes them, then opens the appropriate URL based on segmented radio:
     - "New to GRC" → `mailto:omnyra.training@gmail.com?subject=GRC Training Inquiry&body=<composed message>`
     - "Working professional" → `https://wa.me/919063370816?text=<composed message>`
     - The composed message includes name, email/phone, persona, and the user's message.
  4. Mini success state: form card fades out, `.form-success` card fades in with a checkmark that draws in (`stroke-dashoffset`) + "Opening your email/WhatsApp…" + manual fallback link row.

**Fallback manual link row** (always visible below the submit button): "Or reach us directly: ✉ omnyra.training@gmail.com · ✆ +91 9063370816" with Hex Blue hover.

**Right — Direct contact details** (`.card`):
- Email: `omnyra.training@gmail.com` (animated mail icon, Hex Blue hover, opens mailto)
- WhatsApp: `+91 9063370816` (animated chat icon, opens wa.me)
- Location line: "Global · US & UK"
- Hours: "Mon–Sat, 9am–8pm IST"
- Each contact item reveals with `0.08s` stagger: icon draws in (`stroke-dashoffset → 0`), then label, then value.
- An inline-SVG "hex map" decoration at the bottom of the card (3×4 mini hex grid at 6% opacity) — final brand motif touch.

**Signature motion — "Final convergence":**
- ScrollTrigger pins the section for `+=400px`. As you scroll into it, the section's background darkens (dark theme) / whitens (light theme) toward `var(--carbon-foundation)` (or full white) — a "rest of the page fades away" effect. `backgroundColor` tween tied to scrub.
- The heading and form elements reveal with `0.1s` stagger — but the submit button holds back, scaling from `0.9 → 1` + glowing (`box-shadow: 0 0 0 0 rgba(0,168,232,0.4) → outward`) on a GSAP timeline only after everything else has landed (~`0.8s` in) — "we've been waiting for you" energy.
- Focus-driven glow: when any input is focused, the entire `.contact-form` glows faintly with a Hex Blue ring (`box-shadow: 0 0 80px rgba(0,168,232,0.08)`).

**Footer strip** (below the contact card, full-width):

- Top: 1px Steel divider.
- 3 columns:
  1. Logo (`Monochrome_white-transparent.png` on dark / `primary-logo-transparent.png` on light, 32px height) + tagline "Empowering Careers. Securing the Future."
  2. Quick nav (all 8 sections as small links).
  3. Contact reprise (email + WhatsApp icons with hover).
- Bottom row: "© 2026 OMNyra Group. All rights reserved." left + small "Back to top ↑" link right (smooth-scrolls to hero on click).
- Hex pattern bg at 4% behind the footer strip.

**Schema.org JSON-LD** (matches the existing root `index.html` Organization schema for consistency): the `Organization` JSON-LD block is included in `Website/index.html` and `Website/light.html` `<head>` for LLM/SEO consistency.

---

## 6. Motion & Performance Layer (cross-cutting)

The pieces below apply across all 8 sections. They are the reason "high-intensity motion" stays buttery instead of janky.

### 6.1 Three.js performance budget
- Lattice is hero-only (1 canvas instance, lifetime = mounted while hero in view).
- Object count: 80–120 hexagons, all `LineSegments` (cheap geometry).
- Renderer: `antialias: true`, `pixelRatio: Math.min(devicePixelRatio, 2)` capped (prevents retina-induced perf death).
- `setAnimationLoop` only runs while hero is on-screen (IntersectionObserver toggles it). Off-screen = paused, zero GPU cost.
- Unloads and disposes the renderer when user scrolls past hero + 200px; re-inits if they scroll back up — cached instance.
- EffectComposer with UnrealBloomPass only on dark theme; light theme uses cheaper `MeshBasicMaterial` emissive hack for glow.
- `prefers-reduced-motion: reduce` → static render only, no animation loop, no composer.

### 6.2 GSAP performance rules
- All scroll-triggered tweens use `will-change: transform, opacity` via CSS; cleared via `onComplete` to avoid paint hold.
- ScrollTrigger markers stay `false` in production.
- `ScrollTrigger.config({ ignoreMobileResize: true })` to avoid iOS resize-recompute bugs.
- Pinned sections cleaned up via `onLeaveBack` reset (no residual transforms when scrolling back up).
- Use `ScrollTrigger.batch` wherever possible to group multiple elements into one rAF tick.
- Lenis smooth-scroll NOT used by default (added weight). Native `scroll-behavior: smooth` + CSS is enough; revisit if user reports jank.

### 6.3 Parallax strategy (no library)
- All parallax implemented as ScrollTrigger scrub with `y` translate on `transform` only — no `top`/`margin` (avoids layout reflow).
- Mouse parallax on hero lattice uses `lerp` (not onScroll).
- Card tilts (`rotateX/Y`) use `transform: perspective()` — compositor-only, no reflow.

### 6.4 Custom cursor (desktop only)
- A single `16px` Hex Blue dot div with `id="cursor"` appended to body, `position: fixed, top: 0, left: 0`, `pointer-events: none`, `z-index: 9999`.
- Updated via `requestAnimationFrame` lerp toward `mouse.x/y` at `0.15`.
- Grows / changes blend mode when hovering interactive elements via a `data-cursor="hover"` attribute convention.
- Hidden by default on touch devices: `@media (pointer: coarse) { #cursor { display: none } }`.

### 6.5 prefers-reduced-motion
- `<html data-motion="full">` default. JS reads `window.matchMedia('(prefers-reduced-motion: reduce)')` and sets `data-motion="reduced"`.
- `[data-motion="reduced"]` → all GSAP tweens snap to end state, Three.js shows static frame, custom cursor disabled, scroll-pinned sections become normal flow.

### 6.6 Accessibility & keyboard
- All CTAs and form inputs keyboard reachable; focus-visible rings (2px Hex Blue).
- Mobile menu closes on `Escape`.
- Theme toggle navigates preserving `location.hash`.
- Form does not submit if segmented radio is unselected — visible Chrome Lattice error pill appears under it.

### 6.7 Asset weight budget
- Two HTML files `< 20KB` each (markup only).
- `styles.css` `< 30KB`.
- `lattice.js` + `interactions.js` combined `< 40KB` (no minifier; written lean).
- Three.js + GSAP loaded from CDN with `defer`. Total 3rd-party JS ~ `200KB` gzipped (acceptable for a marketing site).
- Existing logo PNGs already in `img/` — no new image assets needed. All visuals via SVG / WebGL / CSS.

---

## 7. SEO & Metadata

- Each HTML file has a complete `<head>`:
  - `<title>`: "OMNyra Group — GRC Training & Risk Advisory | Empowering Careers. Securing the Future."
  - `<meta name="description" content="Practitioner-led GRC training. 35 hours live training across GRC, TPRM, ISO 27001, Risk Management, Data Privacy, AI Cybersecurity. Mock interviews, resume guidance, career mentorship. US & UK.">`
  - Canonical: `<link rel="canonical" href="https://omnyragroup.online/">` on both files.
  - Light theme has `<link rel="alternate" hreflang="en" href="https://omnyragroup.online/light.html">`.
  - Dark theme has `<link rel="alternate" hreflang="en" href="https://omnyragroup.online/">`.
  - Open Graph + Twitter card meta tags with `icon-only-transparent.png` as the preview image.
- Schema.org Organization JSON-LD block included in both files (same as root `index.html` already does).
- `favicon.png` (copied from `icon-only-transparent.png`) referenced in both files.

**Note:** The live production site (`https://omnyragroup.online/`) currently points to the root `index.html` (the "Launching Soon" page). Deploy of these new `Website/index.html` / `Website/light.html` files is **out of scope** for this spec — the implementation plan will cover whether they replace the root page or live under `Website/`. That decision is deferred to the writing-plans phase.

---

## 8. Implementation Order (advisory, not binding)

The writing-plans skill will produce the actual task breakdown; this is the suggested order:

1. Scaffold `Website/assets/` and the two HTML file skeletons (head, nav, section stubs all 8).
2. Write `styles.css` with theme tokens + all base components (§4.3).
3. Build all 8 sections' static HTML markup first (no JS, no animation) — verify content + responsive layout.
4. Add `lattice.js` (Three.js hero canvas).
5. Add `interactions.js` GSAP reveals + nav + theme toggle + custom cursor.
6. Wire section-specific signature motions (section 3 hex scrub, section 4 pathways converge, section 5 hex assemble, section 6 price reveal, section 7 sticky-stack, section 8 CRT lock + form composer).
7. Audit `prefers-reduced-motion` paths.
8. Performance pass (asset budget, will-change cleanup, ScrollTrigger.refresh on resize).
9. SEO + meta + JSON-LD pass.
10. Cross-browser smoke test (Chrome, Firefox, Safari, iOS Safari, mobile Chrome).
11. Lighthouse pass targeting ≥ 90 on Performance, Accessibility, Best Practices, SEO on desktop.

---

## 9. Acceptance Criteria

The implementation is complete when:

1. Both `Website/index.html` (dark) and `Website/light.html` (light) render all 8 sections with the correct content per §5.
2. The theme toggle in the nav navigates between the two files preserving `location.hash`.
3. The Three.js hex lattice renders in the hero only, respects `prefers-reduced-motion`, and pauses when scrolled off-screen.
4. All signature section motions per §5.1–§5.8 are present and working on desktop Chrome at ≥ 60fps.
5. The custom cursor is visible on desktop pointing devices and hidden on touch.
6. The mobile hamburger menu opens the full-screen overlay, closes on link tap or `Escape`.
7. The contact form (§5.8) validates required fields, composes and opens a `mailto:` or `wa.me` URL based on the segmented radio, and shows the success state. No backend, no network request.
8. All focusable elements have a visible focus ring (2px Hex Blue).
9. `prefers-reduced-motion: reduce` → all animations snap to final states, no motion-induced layout shifts.
10. SEO + JSON-LD meta is present and valid in both HTML files.
11. Asset weight budget per §6.7 is met.
12. Lighthouse ≥ 90 on all four categories on desktop for `Website/index.html`.

---

## 10. Future Upgrade Path (out of scope for this implementation)

**Form upgrade:** If lead drop-off is observed because visitors don't have a mail client configured, swap the `form-submit` composer in `interactions.js` for a `fetch(FORMSPREE_ENDPOINT, { method: 'POST', body: formData })` call. The form's HTML markup stays the same; only the submit handler changes. Formspree endpoint ID would be added as a config constant at the top of `interactions.js`.

**Deploy / root index.html:** The existing root `index.html` (the "Launching Soon" page) is separate from these new `Website/index.html` and `Website/light.html` files. Whether the new files eventually replace the root page, or whether `Website/index.html` becomes the canonical `omnyragroup.online` page, is a deploy decision outside this spec.

**Light section conditional assets:** If asset weight becomes a concern, the Three.js EffectComposer could be conditionally loaded only when `data-theme="dark"` — the light theme uses the cheaper emissive-hack path.

---

*© 2026 OMNyra Group. All rights reserved.*
