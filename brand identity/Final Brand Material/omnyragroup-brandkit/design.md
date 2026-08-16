# OMNyra GROUP — Design System Reference

Technical reference for implementing OMNyra Group brand assets across digital products.

---

## CSS Custom Properties

```css
:root {
  /* Primary Colors */
  --carbon-foundation: #0D1117;
  --deep-carbon: #161B22;
  --hex-blue: #00A8E8;
  --junction-blue: #0077B6;

  /* Neutral Colors */
  --chrome-lattice: #8B949E;
  --steel: #C9D1D9;
  --white: #FFFFFF;

  /* Alert */
  --signal-red: #F85149;

  /* Gradients */
  --accent-gradient: linear-gradient(90deg, var(--hex-blue) 0%, var(--junction-blue) 100%);
  --dark-bg-gradient: linear-gradient(135deg, var(--carbon-foundation) 0%, var(--deep-carbon) 100%);
  --light-bg-gradient: linear-gradient(135deg, #f8f9fa 0%, #ffffff 50%, #f0f4f8 100%);

  /* Typography */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 40px;
  --space-3xl: 60px;

  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 50%;
}
```

---

## Color Token Mapping

| Token | Hex | RGB | HSL | Usage Context |
|-------|-----|-----|-----|---------------|
| `--carbon-foundation` | `#0D1117` | `13, 17, 23` | `216° 27% 7%` | Primary backgrounds, dark text on light |
| `--deep-carbon` | `#161B22` | `22, 27, 34` | `213° 21% 11%` | Secondary dark, card surfaces |
| `--hex-blue` | `#00A8E8` | `0, 168, 232` | `197° 100% 45%` | Primary accent, CTAs, links |
| `--junction-blue` | `#0077B6` | `0, 119, 182` | `200° 100% 36%` | Secondary accent, gradients |
| `--chrome-lattice` | `#8B949E` | `139, 148, 158` | `210° 9% 58%` | Muted text, labels |
| `--steel` | `#C9D1D9` | `201, 209, 217` | `210° 16% 82%` | Borders, dividers |
| `--white` | `#FFFFFF` | `255, 255, 255` | `0° 0% 100%` | Light backgrounds |
| `--signal-red` | `#F85149` | `248, 81, 73` | `2° 92% 63%` | Errors, warnings |

---

## Typography Scale

```css
/* Display / Hero */
.font-hero { font-size: 48px; font-weight: 700; line-height: 1.15; }

/* Headlines */
.font-headline { font-size: 44px; font-weight: 700; line-height: 1.15; }

/* Subheadlines */
.font-subheadline { font-size: 18px; font-weight: 400; line-height: 1.6; }

/* Body */
.font-body { font-size: 16px; font-weight: 400; line-height: 1.6; }

/* Small Body */
.font-small { font-size: 14px; font-weight: 400; line-height: 1.6; }

/* Caption / Label */
.font-caption { font-size: 12px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase; }

/* Micro */
.font-micro { font-size: 10px; font-weight: 400; letter-spacing: 1.5px; text-transform: uppercase; }
```

---

## Component Specifications

### Business Card

| Property | Value |
|----------|-------|
| Size | 3.5 × 2 inches (336 × 192 px at 96dpi) |
| Border radius | 8px |
| Front background | `linear-gradient(135deg, #0D1117 0%, #161B22 100%)` |
| Back background | `#FFFFFF` |
| Front logo | `Monochrome_white-transparent.png`, 140px width |
| Back logo | `primary-logo-transparent.png`, 160px width, centered |
| Watermark (front) | `icon-only-transparent.png`, 55px, 15% opacity, `#0077B6` tint |
| Watermark (back) | `icon-only-transparent.png`, 50px, 6% opacity |
| Accent bar | 3px height, gradient `#00A8E8` → `#0077B6` |
| Padding | 28px |
| Person name | 14px, weight 500, white (front) |
| Person title | 9px, weight 500, `#00A8E8`, uppercase, letter-spacing 1.5px |
| Contact text | 8.5px, color `#161B22` |
| Contact icons | 12×12px, fill `#00A8E8` |
| Tagline | 6.5px, `#8B949E`, uppercase, letter-spacing 1.5px, centered |

### Letterhead

| Property | Value |
|----------|-------|
| Size | 8.5 × 11 inches (816 × 1056 px at 96dpi) |
| Background | `#FFFFFF` |
| Padding | 60px |
| Side accent | 4px left edge, gradient `#00A8E8` → `#0077B6` (vertical) |
| Header border | 2px solid `#00A8E8` (bottom) |
| Logo | `primary-logo-transparent.png`, 50px height |
| Company name | 24px, weight 600, `#0D1117` |
| Company tagline | 9px, `#8B949E`, uppercase, letter-spacing 3px |
| Header contact | 9px, `#161B22`, right-aligned |
| Body text | 11px, `#161B22`, line-height 1.8 |
| Watermark | `icon-only-transparent.png`, 200px, 4% opacity |
| Footer border | 1px solid `#C9D1D9` |
| Footer text | 8px, `#8B949E` |
| Footer tagline | 7px, `#C9D1D9`, uppercase, letter-spacing 2px |

### LinkedIn Cover Banner

| Property | Value |
|----------|-------|
| Dimensions | 1584 × 396 px |
| Dark background | `linear-gradient(135deg, #0D1117 0%, #161B22 50%, #1a2332 100%)` |
| Light background | `linear-gradient(135deg, #f8f9fa 0%, #ffffff 50%, #f0f4f8 100%)` |
| Padding | `0 80px 0 60px` |
| Hex grid pattern | 60×52px hexagons, stroke 0.5px, 6% opacity (dark) / 4% opacity (light) |
| Logo (dark) | `Monochrome_white-transparent.png`, 50px height, 16px top margin |
| Logo (light) | `primary-logo-transparent.png`, 50px height, 16px top margin |
| Logo alignment | Left-aligned with headline, `align-items: flex-start` |
| Headline | 44px, weight 700, line-height 1.15, max-width 650px |
| Headline color (dark) | `#FFFFFF` |
| Headline color (light) | `#0D1117` |
| Accent word color | `#00A8E8` |
| Subheadline | 16px, max-width 520px, line-height 1.6 |
| Subheadline color (dark) | `#C9D1D9` |
| Subheadline color (light) | `#5a6577` |
| CTA button | `#00A8E8` bg, white text, 12px × 28px padding, 6px radius, 13px, weight 600, uppercase |
| CTA URL | 13px, `#8B949E` (dark) / `#6b7280` (light) |
| Watermark | `icon-only-transparent.png`, 320px, 8% opacity, right: 80px, vertically centered |
| Accent line | 4px bottom, gradient `#00A8E8` → `#0077B6` → `#00A8E8` |
| Content gap | 6px between elements |

### Social Post Template

| Property | Value |
|----------|-------|
| Dimensions | 1080 × 1080 px |
| Dark background | `linear-gradient(135deg, #0D1117 0%, #161B22 100%)` |
| Light background | `linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)` |
| Padding | 60px |
| Hex grid pattern | 40×35px hexagons, stroke 0.5px, 5% opacity (dark) / 4% opacity (light) |
| Logo (dark) | `Monochrome_white-transparent.png`, 50px height |
| Logo (light) | `primary-logo-transparent.png`, 50px height |
| Date badge | 11px, uppercase, weight 500, rounded 20px, 8px × 18px padding |
| Quote mark | 120px, 20% opacity, `#00A8E8` (dark) / `#0077B6` (light) |
| Quote text | 44px, weight 600, line-height 1.35, max-width 850px |
| Hashtags | 12px, weight 500, rounded 16px, 6px × 14px padding |
| CTA button | `#00A8E8` bg, white text, 14px × 32px padding, 8px radius |
| Watermark | `icon-only-transparent.png`, 280px, 6% opacity, right: 80px, vertically centered |
| Accent bar | 4px bottom, gradient `#00A8E8` → `#0077B6` |

### Email Signature

| Property | Value |
|----------|-------|
| Max width | 600px |
| Background | `#FFFFFF` |
| Padding | 30px |
| Border radius | 8px |
| Avatar/logo | `Stacked-logo-transparent.png`, 100×100px, no border, no circle |
| Person name | 18px, weight 600, `#0D1117` |
| Person title | 13px, weight 500, `#00A8E8` |
| Divider | 2px, gradient `#00A8E8` → `#0077B6` |
| Contact grid | 2 columns, 10px gap |
| Contact text | 12px, `#161B22` |
| Contact icons | 14×14px, fill `#00A8E8` |
| Social icons | 32×32px, 6px radius, `rgba(0, 168, 232, 0.1)` bg |
| Social SVG | 16×16px, fill `#00A8E8` |
| Tagline | 10px, `#8B949E`, uppercase, letter-spacing 1.5px |

---

## Icon System

All UI icons use inline SVG with the following default properties:

```css
.icon {
  width: 14px;
  height: 14px;
  fill: var(--hex-blue);
  flex-shrink: 0;
}
```

### Icon Sizes

| Context | Size |
|---------|------|
| Contact items (email sig) | 14×14px |
| Contact items (business card) | 12×12px |
| Footer contact (letterhead) | 10×10px |
| Social icons (email sig) | 16×16px (inside 32×32px container) |
| Application cards (brand guide) | 24×24px (inside 48×48px container) |

---

## Shadow System

```css
--shadow-sm: 0 2px 10px rgba(0, 0, 0, 0.1);       /* Cards, small elements */
--shadow-md: 0 10px 40px rgba(0, 0, 0, 0.1);       /* Email signature, medium */
--shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.15);      /* Business cards, letterhead */
--shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.2);       /* LinkedIn covers, social posts */
```

---

## Responsive Breakpoints

| Breakpoint | Width | Notes |
|------------|-------|-------|
| Desktop | ≥ 1200px | Full layout, max-width 1200px container |
| Tablet | 768px – 1199px | Adjusted padding, stacked grids |
| Mobile | < 768px | Single column, reduced font sizes |

---

## Implementation Notes

1. **Font Loading:** Load Inter from Google Fonts with `display=swap` for FOUT prevention
2. **Image Format:** All logos are transparent PNGs — use `object-fit: contain` for consistent sizing
3. **Hex Grid Pattern:** Use inline SVG `<pattern>` elements for scalable, resolution-independent backgrounds
4. **Gradient Consistency:** Always use the defined gradient variables — never approximate with flat colors
5. **Watermark Opacity:** Keep watermarks between 4-8% opacity for subtlety without invisibility
6. **Accent Bars:** Always use the blue gradient, never solid colors for decorative accents
7. **Print Assets:** Convert to CMYK before printing; these specs are for digital/screen use only

---

## Asset Directory

```
omnyragroup-brandkit/
├── primary-logo-transparent.png
├── Stacked-logo-transparent.png
├── icon-only-transparent.png
├── Monochrome_dark-transparent.png
├── Monochrome_white-transparent.png
├── business-card.html
├── letterhead.html
├── linkedin-cover.html
├── social-post-template.html
├── email-signature.html
├── brand-guidelines.html
├── brand-guidelines.md
└── design.md
```

---

*© 2026 OMNyra Group. All rights reserved.*
