# Brand Materials: Editable Formats & Image Exports

**Date:** 2026-08-14
**Status:** Approved
**Project:** OMNyra Group Brand Identity (Concept B: Precision Weave)

## Goal

Make brand materials editable (not locked in SVG) and export platform-ready image formats. Sync everything to the Open Design project.

## Deliverables

### 1. Editable HTML — Business Cards
- `brand-materials/print/business-card-front.html`
- `brand-materials/print/business-card-back.html`
- Self-contained HTML/CSS, open in any browser
- Placeholder text marked with `[brackets]`: `[Full Name]`, `[Title]`, `[Phone]`, `[Email]`
- Exact visual fidelity to the SVG originals (same colors, layout, hexagonal motifs)
- Print-ready: 85mm × 55mm at 300dpi proportions

### 2. Word Document — Letterhead
- `brand-materials/letterhead/letterhead-a4.docx`
- Generated via npm `docx` library
- A4 page (210 × 297mm)
- Embedded OMNyra logo (top-left)
- Blue accent line (top)
- Footer with company info
- Hexagonal watermark at 3% opacity (centered)
- Placeholder body text areas
- Editable in Microsoft Word, Google Docs, LibreOffice

### 3. Cleaned HTML — Email Signature
- `brand-materials/digital/email-signature.html` (overwrite existing)
- Clearer `[placeholder]` markers
- Inline CSS only (email client compatible)
- Same visual design

### 4. Image Exports — Logos (PNG, 2x)
All 5 logo variants rendered to PNG at 2x resolution:
- `brand-materials/logos/primary-logo.png`
- `brand-materials/logos/stacked-logo.png`
- `brand-materials/logos/icon-only.png`
- `brand-materials/logos/monochrome-dark.png`
- `brand-materials/logos/monochrome-white.png`

Transparent background. Rendered via Playwright headless browser.

### 5. Image Exports — Social Media (JPEG, 2x)
All 4 social templates rendered to JPEG at 2x:
- `brand-materials/social/linkedin-cover.jpg` (1584 × 396 → 3168 × 792)
- `brand-materials/social/cover-banner.jpg` (same dimensions)
- `brand-materials/social/post-template-training.jpg` (1080 × 1080 → 2160 × 2160)
- `brand-materials/social/profile-photo.png` (PNG, transparent background)

White background for JPEGs. Rendered via Playwright.

### 6. Open Design Sync
All new files pushed to project `omnyragroup-brand-identity-b41b` via `write_file`.

## Tools
- **Image rendering:** Playwright (already installed via designlang)
- **DOCX generation:** npm `docx` library (install locally)
- **HTML:** Hand-written, matching existing SVG designs

## File Structure (final)
```
brand-materials/
├── logos/
│   ├── primary-logo.svg / .png
│   ├── stacked-logo.svg / .png
│   ├── icon-only.svg / .png
│   ├── monochrome-dark.svg / .png
│   └── monochrome-white.svg / .png
├── print/
│   ├── business-card-front.svg / .html
│   └── business-card-back.svg / .html
├── social/
│   ├── linkedin-cover.svg / .jpg
│   ├── cover-banner.svg / .jpg
│   ├── post-template-training.svg / .jpg
│   └── profile-photo.svg / .png
├── letterhead/
│   ├── letterhead-a4.svg
│   └── letterhead-a4.docx          ← NEW
├── digital/
│   ├── email-signature.html        ← EDITED
│   ├── favicon.svg
│   └── favicon.ico.html
└── cert/
    ├── training-certificate.svg
    └── certification-seal.svg
```
