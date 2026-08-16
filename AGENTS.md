# Project Context — OMNyra Group

## Overview
OMNyra Group is a premium **GRC (Governance, Risk & Compliance)** training and risk advisory firm.
The repository hosts the public-facing "Launching Soon" landing page plus the full brand identity
system (logo, stationery, social, certificates) and tooling to render/export those assets.

- **Tagline:** "Empowering Careers. Securing the Future."
- **Mission:** Transform trainees into highly sought-after GRC specialists through practitioner-led training.
- **Core Values:** Practical · Relevant · Career-Focused · Global Opportunities
- **Focus areas:** GRC, ISO 27001 readiness, Third-Party Risk Management (TPRM), Regulatory Compliance, Data Privacy, AI Cybersecurity.
- **Target Audience:** Students, Fresh Graduates, Career Switchers, Working Professionals (Global · US & UK)
- **Contact:** omnyra.training@gmail.com · +91 9063370816 (WhatsApp)
- **Website:** [omnyragroup.online](https://omnyragroup.online)
- **Founded:** 2026 · **Area served:** Global — primary markets US & UK

## Tech Stack
- **Site:** Single static `index.html` (no build step) — vanilla HTML/CSS/SVG + a small inline JS script that draws the animated hexagonal lattice background.
- **Fonts:** Inter (Google Fonts) — weights 300, 400, 500, 600, 700, 800.
- **Dev dependencies:** `shadcn` (^4.18.0) — design-system reference only, not wired into a build.
- **Runtime dependencies:** `docx` (^9.7.1) for editable Office documents, `playwright` (^1.62.1) for rendering SVG assets to PNG/JPEG.
- **No framework / bundler.** Everything is committed source.

## Repository Layout
- `index.html` — the live landing page (launching-soon hero, logo, contact, Schema.org Organization JSON-LD).
- `favicon.png` — production favicon (PNG, hexagonal icon mark from brand kit).
- `llms.txt` — LLM-facing site summary (services, facts, tagline).
- `robots.txt` / `sitemap.xml` — SEO; sitemap points to `https://omnyragroup.online/`.
- `CNAME` — `www.omnyragroup.online` (GitHub Pages custom domain). Canonical URL is `https://omnyragroup.online/`.
- `brand identity/Final Brand Material/omnyragroup-brandkit/` — canonical brand kit location:
  - **Logo files (all transparent PNGs):**
    - `primary-logo-transparent.png` — Full logo with icon + wordmark (light backgrounds)
    - `Stacked-logo-transparent.png` — Stacked version (icon above wordmark)
    - `icon-only-transparent.png` — Icon only (circular blue design, watermarks, favicons)
    - `Monochrome_dark-transparent.png` — Dark monochrome (for light backgrounds)
    - `Monochrome_white-transparent.png` — White monochrome (for dark backgrounds)
  - **HTML templates:**
    - `business-card.html` — Business card front & back
    - `letterhead.html` — US Letter letterhead template
    - `linkedin-cover.html` — LinkedIn cover banners (dark + light)
    - `social-post-template.html` — Social media post templates (dark + light)
    - `email-signature.html` — Email signature (HTML + plain text)
    - `brand-guidelines.html` — Interactive brand guidelines page
  - **Documentation:**
    - `brand-guidelines.md` — Full brand guidelines document
    - `design.md` — Technical design system reference (CSS variables, component specs)

## Brand / Design System

### Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| **Carbon Foundation** | `#0D1117` | Primary background, dark themes, body text on light backgrounds |
| **Deep Carbon** | `#161B22` | Secondary dark background, card surfaces, gradients |
| **Hex Blue** | `#00A8E8` | Primary accent — CTAs, links, highlights, icons, active states |
| **Junction Blue** | `#0077B6` | Secondary accent — gradients, hover states, subtle highlights |
| **Chrome Lattice** | `#8B949E` | Muted text, labels, secondary info, watermarks |
| **Steel** | `#C9D1D9` | Borders, dividers, subtle backgrounds |
| **White** | `#FFFFFF` | Light backgrounds, card surfaces, inverted text |
| **Signal Red** | `#F85149` | Errors, warnings, critical alerts only |

CSS custom properties (canonical):
- `--carbon-foundation: #0D1117`
- `--deep-carbon: #161B22`
- `--hex-blue: #00A8E8`
- `--junction-blue: #0077B6`
- `--chrome-lattice: #8B949E`
- `--steel: #C9D1D9`
- `--white: #FFFFFF`
- `--signal-red: #F85149`

### Logo Usage Rules

| Application | Logo Used | Notes |
|-------------|-----------|-------|
| **Business Card Front** | `Monochrome_white-transparent.png` | On dark background (#0D1117), watermark in #0077B6 at 15% |
| **Business Card Back** | `primary-logo-transparent.png` | Centered on white |
| **Letterhead Header** | `primary-logo-transparent.png` | Top-left, 50px height |
| **LinkedIn Cover (Dark)** | `Monochrome_white-transparent.png` | Left-aligned, 50px height, 16px top margin |
| **LinkedIn Cover (Light)** | `primary-logo-transparent.png` | Left-aligned, 50px height, 16px top margin |
| **Social Post (Dark)** | `Monochrome_white-transparent.png` | Top-left, 50px height |
| **Social Post (Light)** | `primary-logo-transparent.png` | Top-left, 50px height |
| **Email Signature** | `Stacked-logo-transparent.png` | No circle/border, 100×100px |
| **Brand Guidelines Header** | `Monochrome_white-transparent.png` | Centered on dark header, 80px height |
| **Favicon** | `icon-only-transparent.png` | Copied to repo root as `favicon.png` |

Visual motif: hexagonal lattice / network made of hexagon cells with ascending paths and junction nodes —
"Empowering Careers. Securing the Future." Logo mark = stylized hexagon with an upward-angled arrow path.

### Gradients
- **Accent:** `linear-gradient(90deg, #00A8E8 0%, #0077B6 100%)` — accent bars, dividers
- **Dark BG:** `linear-gradient(135deg, #0D1117 0%, #161B22 100%)` — dark theme surfaces
- **Light BG:** `linear-gradient(135deg, #f8f9fa 0%, #ffffff 50%, #f0f4f8 100%)` — light theme surfaces

## Deployment
- Hosted on **GitHub Pages** via the `akashnikhra/OmnyraGroup` repo (`origin` remote, `main` branch).
- Custom domain: `www.omnyragroup.online` (`CNAME`). Root domain `omnyragroup.online` is canonical.

## Conventions / Notes
- Commits follow Conventional-style prefixes (`feat:`, `chore:`, `docs:`).
- SEO/LLM files (`llms.txt`, `robots.txt`, `sitemap.xml`) are kept current with the live single page.
- Brand assets canonical location: `brand identity/Final Brand Material/omnyragroup-brandkit/`.
