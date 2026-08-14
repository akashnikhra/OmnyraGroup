# Brand Materials: Editable Formats & Image Exports — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create editable HTML business cards, a Word .docx letterhead, cleaned email signature, and high-res PNG/JPEG exports of logos and social covers. Sync all to Open Design.

**Architecture:** Self-contained HTML files for business cards (edit source directly). npm `docx` library for Word letterhead. Playwright headless browser for SVG→PNG/JPEG rendering. All assets synced to Open Design via `write_file`.

**Tech Stack:** Node.js, npm `docx`, Playwright (already installed)

---

## File Map

```
brand-materials/
├── print/
│   ├── business-card-front.html    ← CREATE
│   └── business-card-back.html     ← CREATE
├── letterhead/
│   └── letterhead-a4.docx          ← CREATE
├── digital/
│   └── email-signature.html        ← OVERWRITE (cleaner)
├── logos/
│   ├── primary-logo.png            ← CREATE
│   ├── stacked-logo.png            ← CREATE
│   ├── icon-only.png               ← CREATE
│   ├── monochrome-dark.png         ← CREATE
│   └── monochrome-white.png        ← CREATE
├── social/
│   ├── linkedin-cover.jpg          ← CREATE
│   ├── cover-banner.jpg            ← CREATE
│   ├── post-template-training.jpg  ← CREATE
│   └── profile-photo.png           ← CREATE
scripts/
└── render-assets.mjs               ← CREATE (Playwright renderer)
```

---

### Task 1: Install dependencies

- [ ] **Step 1: Install `docx` library**

Run: `npm install docx`
Expected: package added to package.json

- [ ] **Step 2: Verify Playwright is accessible**

Run: `node -e "const {chromium}=require('playwright');console.log('ok')}"`
Expected: prints "ok"

- [ ] **Step 3: Commit**

```bash
git add package.json package-lock.json
git commit -m "chore: add docx dependency for letterhead generation"
```

---

### Task 2: Create editable business card HTML — Front

**Files:**
- Create: `brand-materials/print/business-card-front.html`

- [ ] **Step 1: Write business-card-front.html**

Self-contained HTML/CSS file:
- 85mm × 55mm proportions (at 96dpi: 323px × 208px, scaled 2x for retina)
- Carbon (#0D1117) background
- Blue accent line at top (2px, gradient)
- OMNyra logo (inline SVG) top-left
- Placeholder `[Full Name]` in white, bold
- Placeholder `[Title] — GRC Advisory` in hex blue
- GRC badge
- Contact placeholders: `[Email]`, `[Phone]`, `[Address]`
- Hexagonal pattern watermark at 4% opacity
- All CSS inline for portability

- [ ] **Step 2: Verify renders correctly**

Open `brand-materials/print/business-card-front.html` in browser. Confirm:
- Dark background, blue accents visible
- All placeholders clearly marked with `[brackets]`
- Layout matches the SVG original

- [ ] **Step 3: Commit**

```bash
git add brand-materials/print/business-card-front.html
git commit -m "feat: add editable business card front HTML"
```

---

### Task 3: Create editable business card HTML — Back

**Files:**
- Create: `brand-materials/print/business-card-back.html`

- [ ] **Step 1: Write business-card-back.html**

Same structure as front:
- Carbon background
- Centered Sentinel Mark logo (larger, inline SVG)
- Hexagonal lattice pattern across full card
- Tagline: `STRUCTURE IN MOTION` centered below logo
- URL: `www.omnyragroup.online`
- Blue accent line at bottom

- [ ] **Step 2: Verify renders correctly**

Open in browser. Confirm layout matches SVG original.

- [ ] **Step 3: Commit**

```bash
git add brand-materials/print/business-card-back.html
git commit -m "feat: add editable business card back HTML"
```

---

### Task 4: Create Word letterhead (.docx)

**Files:**
- Create: `brand-materials/letterhead/letterhead-a4.docx`
- Create: `scripts/generate-letterhead.mjs`

- [ ] **Step 1: Write generate-letterhead.mjs**

Script using npm `docx` library:
- A4 page dimensions (210mm × 297mm)
- Header: OMNyra logo image (convert icon-only SVG to PNG first, or embed as base64)
- Header: blue accent line (top border)
- Footer: company name, tagline, contact info, URL
- Body: placeholder text areas for date, recipient, subject, body paragraphs
- Watermark: hexagonal shape at 3% opacity (using `docx`'s watermark or background shape)

Note: `docx` library may not support SVG images directly. Convert `icon-only.svg` to PNG first using Playwright, then embed in the .docx.

- [ ] **Step 2: Generate the letterhead**

Run: `node scripts/generate-letterhead.mjs`
Expected: creates `brand-materials/letterhead/letterhead-a4.docx`

- [ ] **Step 3: Verify the .docx**

Open `letterhead-a4.docx` in Word or Google Docs. Confirm:
- A4 page size
- Logo visible in header
- Blue accent line
- Footer with company info
- Editable placeholder text

- [ ] **Step 4: Commit**

```bash
git add brand-materials/letterhead/letterhead-a4.docx scripts/generate-letterhead.mjs
git commit -m "feat: add editable A4 letterhead (.docx)"
```

---

### Task 5: Clean up email signature HTML

**Files:**
- Modify: `brand-materials/digital/email-signature.html`

- [ ] **Step 1: Rewrite email-signature.html**

Cleaner version:
- All CSS inline (email client compatibility)
- Clear `[Full Name]`, `[Title]`, `[Email]`, `[Phone]` placeholders
- Same visual design: logo icon, blue divider, contact details, tagline badge
- Remove any non-essential markup

- [ ] **Step 2: Verify in browser**

Open in browser. Confirm clean layout, all placeholders visible.

- [ ] **Step 3: Commit**

```bash
git add brand-materials/digital/email-signature.html
git commit -m "feat: clean up email signature HTML with clear placeholders"
```

---

### Task 6: Create Playwright SVG renderer script

**Files:**
- Create: `scripts/render-assets.mjs`

- [ ] **Step 1: Write render-assets.mjs**

Node.js script using Playwright:
- Launches headless Chromium
- For each SVG file, opens it in a blank page, waits for render
- Exports to PNG (logos) or JPEG (social) at 2x device scale factor
- PNG: transparent background
- JPEG: white background, quality 95
- Reads from `brand-materials/` subdirectories
- Writes output to same directory with new extension

Input config:
```javascript
const tasks = [
  { src: 'logos/primary-logo.svg', out: 'logos/primary-logo.png', format: 'png' },
  { src: 'logos/stacked-logo.svg', out: 'logos/stacked-logo.png', format: 'png' },
  { src: 'logos/icon-only.svg', out: 'logos/icon-only.png', format: 'png' },
  { src: 'logos/monochrome-dark.svg', out: 'logos/monochrome-dark.png', format: 'png' },
  { src: 'logos/monochrome-white.svg', out: 'logos/monochrome-white.png', format: 'png' },
  { src: 'social/linkedin-cover.svg', out: 'social/linkedin-cover.jpg', format: 'jpeg' },
  { src: 'social/cover-banner.svg', out: 'social/cover-banner.jpg', format: 'jpeg' },
  { src: 'social/post-template-training.svg', out: 'social/post-template-training.jpg', format: 'jpeg' },
  { src: 'social/profile-photo.svg', out: 'social/profile-photo.png', format: 'png' },
];
```

- [ ] **Step 2: Test render one asset**

Run: `node scripts/render-assets.mjs` (with just one task)
Expected: creates the PNG/JPEG file

- [ ] **Step 3: Run full render**

Run: `node scripts/render-assets.mjs`
Expected: all 9 image files created

- [ ] **Step 4: Verify output**

Check each image file:
- PNGs have transparent background (where applicable)
- JPEGs have white background
- Resolution is 2x original SVG viewBox
- Colors match the SVG originals

- [ ] **Step 5: Commit**

```bash
git add scripts/render-assets.mjs brand-materials/logos/*.png brand-materials/social/*.jpg brand-materials/social/profile-photo.png
git commit -m "feat: add Playwright SVG renderer + high-res PNG/JPEG exports"
```

---

### Task 7: Sync all assets to Open Design

**Files:**
- All new/modified files in `brand-materials/`

- [ ] **Step 1: Upload editable HTML files to Open Design**

Use `write_file` for each:
- `print/business-card-front.html`
- `print/business-card-back.html`
- `digital/email-signature.html`

- [ ] **Step 2: Upload letterhead .docx to Open Design**

Use `write_file` for:
- `letterhead/letterhead-a4.docx` (base64 encoding)

- [ ] **Step 3: Upload image exports to Open Design**

Use `write_file` for each:
- `logos/primary-logo.png`
- `logos/stacked-logo.png`
- `logos/icon-only.png`
- `logos/monochrome-dark.png`
- `logos/monochrome-white.png`
- `social/linkedin-cover.jpg`
- `social/cover-banner.jpg`
- `social/post-template-training.jpg`
- `social/profile-photo.png`

- [ ] **Step 4: Final commit**

```bash
git add -A brand-materials/
git commit -m "feat: complete brand materials — editable formats + image exports"
```

- [ ] **Step 5: Push to GitHub**

Run: `git push origin main`
