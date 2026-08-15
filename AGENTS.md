# Project Context — OMNyra Group

## Overview
OMNyra Group is a premium **GRC (Governance, Risk & Compliance)** training and risk advisory firm.
The repository hosts the public-facing "Launching Soon" landing page plus the full brand identity
system (logo, stationery, social, certificates) and tooling to render/export those assets.

- **Tagline:** "Structure in Motion"
- **Mission:** Transform trainees into highly sought-after GRC specialists through practitioner-led training.
- **Focus areas:** GRC, ISO 27001 readiness, Third-Party Risk Management (TPRM), Regulatory Compliance.
- **Contact:** omnyra.training@gmail.com · +91 9063370816 (WhatsApp)
- **Founded:** 2026 · **Area served:** Global

## Tech Stack
- **Site:** Single static `index.html` (no build step) — vanilla HTML/CSS/SVG + a small inline JS script that draws the animated hexagonal lattice background.
- **Fonts:** Inter (Google Fonts).
- **Dev dependencies:** `shadcn` (^4.18.0) — design-system reference only, not wired into a build.
- **Runtime dependencies:** `docx` (^9.7.1) for editable Office documents, `playwright` (^1.62.1) for rendering SVG assets to PNG/JPEG.
- **No framework / bundler.** Everything is committed source.

## Repository Layout
- `index.html` — the live landing page (launching-soon hero, logo, contact, Schema.org Organization JSON-LD).
- `favicon.svg` — production favicon (blue hexagon mark on glow).
- `llms.txt` — LLM-facing site summary (services, facts, tagline).
- `robots.txt` / `sitemap.xml` — SEO; sitemap points to `https://omnyragroup.online/`.
- `CNAME` — `www.omnyragroup.online` (GitHub Pages custom domain). Canonical URL is `https://omnyragroup.online/`.
- `brand identity/` — brand system, organized by concept:
  - `Concept-A/`, `Concept-B/`, `Concept-C/` — three brand directions, each with:
    - `logos/` (primary, stacked, icon-only, monochrome dark/white)
    - `print/` (business card front/back)
    - `letterhead/`, `cert/` (certificate + seal), `social/` (cover, LinkedIn, post template, profile photo)
    - `digital/` (email signature, favicon)
    - `website-mockup/` (light + dark HTML mockups)
    - `brand-guidelines.md`, `design-philosophy.md`
  - Note: there is a duplicated nested `brand identity/brand identity/...` tree (same contents) — likely an accidental copy. Verify before relying on either path.

## Brand / Design System
CSS custom properties used on the landing page (the canonical palette):
- `--carbon-foundation: #0D1117` (near-black, primary text/ink)
- `--deep-carbon: #161B22`
- `--hex-blue: #00A8E8` (primary accent)
- `--junction-blue: #0077B6`
- `--chrome-lattice: #8B949E` (muted grey)
- `--steel: #C9D1D9`
- `--white: #FFFFFF`
- `--signal-red: #F85149`

Visual motif: hexagonal lattice / network made of hexagon cells with ascending paths and junction nodes —
"structure in motion." Logo mark = stylized hexagon with an upward-angled arrow path.

## Deployment
- Hosted on **GitHub Pages** via the `akashnikhra/OmnyraGroup` repo (`origin` remote, `main` branch).
- Custom domain: `www.omnyragroup.online` (`CNAME`). Root domain `omnyragroup.online` is canonical.

## Conventions / Notes
- Commits follow Conventional-style prefixes (`feat:`, `chore:`, `docs:`).
- Previously the brand assets lived under `brand-materials/` with generator scripts in `scripts/`
  (`render-assets.mjs`, `generate-letterhead.mjs`) and planning docs under `docs/superpowers/`.
  These are currently **deleted from the working tree** (visible in git history) — the assets now
  live under `brand identity/`. Confirm the intended canonical location before further work.
- SEO/LLM files (`llms.txt`, `robots.txt`, `sitemap.xml`) are kept current with the live single page.
