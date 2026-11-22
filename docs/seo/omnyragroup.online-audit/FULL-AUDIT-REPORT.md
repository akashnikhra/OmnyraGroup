# SEO + GEO Audit: www.omnyragroup.online

Audit date: 22 November 2026. Method: live crawl of the deployed site (homepage, 6 program pages, hub, legal pages, Exam Portal), robots.txt, sitemap.xml, llms.txt, structured data, and a Bing index check (via DuckDuckGo). Google Search Console, CrUX field data and backlink tools were not available, so performance and backlink findings are lab or inferred, and are labelled as such.

## SEO Health Score: 50 / 100

| Category | Weight | Score | Main reason |
|---|---|---|---|
| Technical SEO | 22% | 55 | Canonical / redirect conflict on every page; private pages indexable |
| Content quality | 23% | 35 | 12 pages, no articles, no named experts, unverified claims |
| On-page SEO | 20% | 55 | Brand-first titles, slogan headings instead of search terms |
| Schema | 10% | 60 | Plenty of markup, but self-serving review stars and wrong host |
| Performance | 10% | 55 (lab estimate) | 220 KB HTML, 95 KB inline CSS/JS, Three.js on first load |
| AI search readiness | 10% | 40 | Crawlers allowed, but no citable content or off-site entity presence |
| Images | 5% | 70 | Alt text present; logos are 470 to 900 KB PNGs |

Business type: online education provider (GRC training), global with US/UK focus, no physical location. Local SEO does not apply.

## Why the site is not ranking (the short version)

1. **Google is told two different addresses for every page.** The site lives at `www.omnyragroup.online` (the bare domain 301-redirects there), but every canonical tag, `og:url`, hreflang tag, sitemap URL and schema URL points to `omnyragroup.online` without `www`. Canonicals that point at a redirect are a mixed signal; Google may pick either version or delay consolidating them.
2. **There is almost nothing to rank.** 12 indexable pages, no articles, guides or resources. The searches students actually make ("what is GRC", "how to become a GRC analyst", "TPRM interview questions", "ISO 27001 vs SOC 2") have no page on this site to match them.
3. **No authority.** A new domain on a `.online` TLD, with no evidence of backlinks, no named instructors, and brand mentions limited to its own LinkedIn page. The brand name is also easily confused with "Omnia Group" in search.
4. **Trust signals that could backfire.** A 4.9-star AggregateRating from 10 reviews marked up on your own Organization (Google does not show self-serving review stars and can treat them as spam if unverifiable), plus "96% placement success" and "Trained 250+ candidates" with no supporting evidence.

## Findings

### Critical

| # | Finding | Evidence | Fix |
|---|---|---|---|
| C1 | Canonical, sitemap, OG, hreflang and schema all use the bare domain, which redirects to `www` | `https://omnyragroup.online/` returns 301 to `https://www.omnyragroup.online/`; homepage canonical is `https://omnyragroup.online/` | Pick one host. Simplest: change the `CNAME` file to `omnyragroup.online` so the bare domain becomes primary and `www` redirects to it; every existing tag then becomes correct. Alternative: switch every URL to `www`. Then resubmit the sitemap in Search Console |
| C2 | The AIGP Mock Test answer key is publicly reachable and indexable | `/Exam%20Portal/AIGP%20Mock%20Test/...Answer%20Key.html` returns 200, no `noindex`, title "Bundled Page" | Remove it from the repo (or move it behind the portal login) |
| C3 | Exam Portal student and admin pages are in Bing's index | Bing `site:` search lists `/Exam%20Portal/student/index.html` and `/Exam%20Portal/admin/index.html`; no `noindex` on portal pages | Add `<meta name="robots" content="noindex, nofollow">` to every page under `Exam Portal/`; optionally `Disallow: /Exam%20Portal/` in robots.txt after the noindex has been crawled |

### High

| # | Finding | Fix |
|---|---|---|
| H1 | No content beyond the sales pages (`/blog/` is 404). Nothing targets informational searches, where most GRC career traffic is | Build a resources hub with 15 to 25 cornerstone guides mapped to the six tracks |
| H2 | Self-serving `AggregateRating` and 10 `Review` items on the Organization | Remove the review markup from schema. Keep testimonials on the page; collect reviews on Google Business Profile, Trustpilot or Course Report instead |
| H3 | Unsupported claims: "96% placement success", "Trained 250+ candidates", salary figures with no source | Back each with evidence (methodology page, named alumni with permission, salary source such as BLS or Glassdoor) or soften the wording |
| H4 | No named people. No instructor bios, credentials or LinkedIn profiles anywhere | Add an instructors/about page with real names, certifications (CISA, CRISC, ISO 27001 LA) and Person schema; link from every program page |
| H5 | Homepage title and H1 lead with the brand and slogans, not search terms. "OMNyra Group" has almost no search volume; H2s like "Career Architecture" and "Zero Guesswork" match no query | Title such as "GRC Training Online with Career Coaching | OMNyra Group"; rewrite H2s around real terms (GRC courses, TPRM training, ISO 27001 training) |
| H6 | `sameAs` lists Instagram and Twitter/X profiles that may not exist | Keep only profiles that exist; add YouTube once created |
| H7 | Leftover duplicate page still public: `/launching-soon-backup.html` (200) | Delete it |

### Medium

| # | Finding | Fix |
|---|---|---|
| M1 | Homepage weight: 220 KB HTML with 66 KB inline CSS and 29 KB inline JS, plus Three.js (about 600 KB) and GSAP loaded on every visit | Move CSS to a cached file, load Three.js after first interaction or desktop only, honour reduced motion |
| M2 | Course schema duplicated: six Course objects on the homepage and again on each program page | Keep Course schema on program pages only; homepage keeps Organization + ItemList |
| M3 | Logo PNGs are 470 to 900 KB | Export at display size as WebP or SVG |
| M4 | No custom 404 page | Add `404.html` linking to the programs hub and contact |
| M5 | No security headers (HSTS, CSP) | GitHub Pages cannot set them; revisit if you move to Cloudflare Pages or Netlify |
| M6 | No Google Business Profile, Bing Places or education directory listings | Create a GBP as an online service-area business; list on Course Report, Class Central, SwitchUp |

### Low

- `.online` TLD carries a mild trust penalty with some users; not a ranking blocker.
- `llms.txt` exists. Google ignores it; harmless for other AI tools.
- No About page with company story, founding date and team.

## AI search (GEO) readiness: 40 / 100

| Area | Status |
|---|---|
| AI crawler access | Good. GPTBot, OAI-SearchBot, ClaudeBot and PerplexityBot are allowed |
| Server-side rendering | Good. All copy is in the HTML |
| Citable passages | Weak. No "What is TPRM?"-style definitions or 130 to 170 word answer blocks; copy is persuasive, not explanatory |
| Authority / entity | Weak. Only LinkedIn. No YouTube, Reddit, Wikidata, podcast or press mentions |
| Freshness | Weak. No dated content |
| Platform view | Google AI Overviews: unlikely until pages rank top 10. ChatGPT / Perplexity: unlikely without Reddit, YouTube or third-party mentions |

## What already works

- HTTPS, clean URLs, GitHub Pages hosting, valid robots.txt and sitemap.
- Program pages with curriculum, FAQ and Course/FAQPage/Breadcrumb schema.
- All text is in the HTML, readable by search engines and AI crawlers.
- The brand query "OMNyra Group" returns the site first on Bing.

Limitations: Google indexation, rankings, Core Web Vitals field data and backlinks could not be measured without Search Console and a backlink tool. Generic-keyword rank checks were rate-limited.
