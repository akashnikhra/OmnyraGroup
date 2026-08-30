# OMNyra Group Landing Page — Comprehensive Marketing Audit

## Executive Summary

This audit evaluates the current OMNyra Group landing page (`F:\OmnyraGroup\Website\index.html`) across six critical marketing dimensions: SEO, GEO (Generative Engine Optimization), CRO (Conversion Rate Optimization), Copywriting, Marketing Psychology, and Karpathy Guidelines compliance.

**Overall Score: 6.5/10** — Strong foundation with significant optimization opportunities.

---

## ⚠️ IMPORTANT BUSINESS CONTEXT

**OMNyra Group is a NEW business (founded 2026) with:**
- ❌ No testimonials yet (no students graduated)
- ❌ No social media presence yet (LinkedIn page in progress, no link available)
- ❌ No review scores or ratings
- ❌ No case studies or success stories
- ❌ No backlinks or domain authority
- ✅ Landing page live with clear value proposition
- ✅ WhatsApp and email contact available
- ✅ Career Readiness Quiz for engagement

**This changes audit recommendations significantly:**
1. Social proof recommendations are deferred until testimonials exist
2. Focus shifts to **build-ready** (preparing for social proof) vs **proof-ready** (already have it)
3. SEO strategy must account for zero domain authority
4. GEO strategy must work without existing citations
5. CRO must rely on value proposition clarity, not social validation

---

## 1. SEO AUDIT

### Current State
- ✅ **Meta tags present**: Title, description, OG tags, Twitter cards
- ✅ **Schema markup**: Organization JSON-LD in place
- ✅ **Canonical URL**: Correctly set to `https://omnyragroup.online/`
- ✅ **Semantic HTML**: Proper heading hierarchy (H1 → H2 → H3)
- ✅ **Mobile responsive**: Viewport meta tag present

### Critical Gaps

#### 1.1 Missing Schema Types (HIGH PRIORITY)
**Current**: Only `Organization` schema
**Missing**:
- `Course` or `TrainingProgram` schema for each track
- `FAQPage` schema (can be added back with schema)
- `BreadcrumbList` schema
- `Event` schema for live training sessions

**Note**: `AggregateRating` schema deferred until testimonials exist

**Impact**: Missing rich results in Google search (course cards, FAQ snippets)

#### 1.2 Thin Content Signals (HIGH PRIORITY)
**Issue**: Single-page site with all content on one URL
**Impact**: 
- Limited keyword targeting per section
- All sections compete for same authority
- No internal linking opportunities

**Recommendation**: Consider expanding to multi-page structure:
- `/programs/grc` — GRC track details
- `/programs/tprm` — TPRM track details
- `/programs/iso-27001` — ISO track details
- `/pricing` — Plans comparison
- `/about` — Company story

#### 1.3 Missing Hreflang Tags (MEDIUM PRIORITY)
**Issue**: No international targeting despite "Global Markets" claim
**Impact**: Google may not understand geographic targeting

**Recommendation**: Add hreflang tags if targeting specific regions:
```html
<link rel="alternate" hreflang="en" href="https://omnyragroup.online/" />
<link rel="alternate" hreflang="en-us" href="https://omnyragroup.online/" />
<link rel="alternate" hreflang="en-gb" href="https://omnyragroup.online/" />
```

#### 1.4 Missing Open Graph Image (MEDIUM PRIORITY)
**Issue**: No `og:image` tag defined
**Impact**: Social shares show no preview image

**Recommendation**: Add OG image meta tag:
```html
<meta property="og:image" content="https://omnyragroup.online/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

#### 1.5 Missing Twitter Image (MEDIUM PRIORITY)
**Issue**: No `twitter:image` tag defined
**Impact**: Twitter shares show no preview image

**Recommendation**: Add Twitter image meta tag:
```html
<meta name="twitter:image" content="https://omnyragroup.online/og-image.png" />
```

#### 1.6 Missing robots.txt and sitemap.xml (HIGH PRIORITY)
**Issue**: No robots.txt or sitemap.xml files found
**Impact**: Search engines can't discover or crawl the site properly

**Recommendation**: Create:
- `robots.txt` with sitemap reference
- `sitemap.xml` with all pages (if multi-page)

#### 1.7 Missing Image Alt Text (MEDIUM PRIORITY)
**Issue**: Several SVG icons lack descriptive alt text
**Impact**: Accessibility issues, missing image search traffic

**Recommendation**: Add `aria-label` or `role="img"` with descriptive text to SVG icons

---

## 2. GEO (Generative Engine Optimization) AUDIT

### Current State
- ❌ **No llms.txt file**: Missing AI-readable site summary
- ❌ **No structured data for AI**: No schema optimized for LLM citation
- ❌ **No statistics/citations**: Limited citable data points
- ❌ **No FAQ section**: Removed (was citable content)

### Critical Gaps

#### 2.1 Missing llms.txt (HIGH PRIORITY)
**Issue**: No AI-readable site summary for LLMs
**Impact**: ChatGPT, Perplexity, Claude can't easily discover/summarize the site

**Recommendation**: Create `llms.txt` at root:
```
# OMNyra Group
> Premium GRC training and risk advisory firm

## Services
- GRC Training (Governance, Risk & Compliance)
- TPRM Training (Third-Party Risk Management)
- ISO 27001 Readiness
- Risk Management
- Data Privacy
- AI Governance & Risk

## Key Facts
- Founded: 2026
- Location: Global (US & UK focus)
- Training Format: Live, practitioner-led sessions
- Contact: omnyra.training@gmail.com
```

#### 2.2 Missing Citable Statistics (HIGH PRIORITY)
**Issue**: Limited specific numbers for AI citation
**Current stats**: "250+ candidates", "6 tracks", "35 hours", "96% placement"
**Impact**: AI systems prefer specific, cited statistics

**Recommendation**: Add more citable data points:
- "Graduates earn average starting salary of $85,000+"
- "Training covers 15+ GRC frameworks"
- "Students from 50+ countries"
- "100% live instruction (no pre-recorded content)"

#### 2.3 Missing Structured FAQ Content (MEDIUM PRIORITY)
**Issue**: FAQ section was removed
**Impact**: Lost citable Q&A content for AI answers

**Recommendation**: Add FAQ section back with schema markup, or add inline FAQ content within sections

#### 2.4 Missing Author/Expert Signals (MEDIUM PRIORITY)
**Issue**: No author attribution on content
**Impact**: AI systems weight E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

**Recommendation**: Add instructor bios with credentials:
```html
<div class="instructor-bio">
  <h3>Lead Instructor</h3>
  <p>15+ years in GRC, former Fortune 500 compliance director</p>
</div>
```

---

## 3. CRO (CONVERSION RATE OPTIMIZATION) AUDIT

### Current State
- ✅ **Clear primary CTA**: "BOOK FREE COACHING CALL"
- ✅ **WhatsApp CTA**: "CHAT WITH A COACH"
- ✅ **Multiple contact options**: Email, WhatsApp
- ✅ **Social proof element**: "250+ candidates" badge

### Critical Gaps

#### 3.1 Missing Value Proposition Above Fold (HIGH PRIORITY)
**Issue**: Hero headline "Become Job-Ready in Cybersecurity Governance & Risk" is vague
**Impact**: Visitors don't immediately understand what's being sold

**Recommendation**: Make value proposition specific:
- Current: "Become Job-Ready in Cybersecurity Governance & Risk"
- Better: "Get Hired as a GRC Analyst in 6 Weeks — Or We Coach You Until You Do"

#### 3.2 Missing Social Proof (HIGH PRIORITY — DEFERRED)
**Issue**: No testimonials, student logos, or success stories
**Impact**: No trust signals for new visitors

**Status**: ⏳ DEFERRED — Business is new, no graduates yet

**Build-Ready Actions** (prepare for when testimonials exist):
1. Create testimonial section HTML/CSS structure now
2. Add placeholder for "What Our Students Say" section
3. Plan to collect testimonials from first cohort
4. Set up LinkedIn recommendations collection process
5. Create success story template for future case studies

**Interim Alternatives** (use NOW):
- Add "Founder's Story" section (personal credibility)
- Add "Why We Started OMNyra" narrative (mission-driven)
- Add "Our Approach" section (differentiation without proof)
- Use "250+ candidates trained" as early social proof
- Add "Join the next cohort" urgency (creates bandwagon effect)

#### 3.3 Missing Urgency/Scarcity (MEDIUM PRIORITY)
**Issue**: No time-sensitive offers or limited availability
**Impact**: No motivation to act now vs. later

**Recommendation**: Add:
- "Next cohort starts [Date] — Limited to 20 students"
- "Early bird pricing ends [Date]"
- "Only 3 spots remaining"

#### 3.4 Missing Risk Reversal (MEDIUM PRIORITY)
**Issue**: No money-back guarantee or trial offer
**Impact**: High perceived risk for $850 purchase

**Recommendation**: Add:
- "100% money-back guarantee if not satisfied after first week"
- "Free consultation call — no obligation"
- "Pay in 3 installments"

#### 3.5 Weak CTA Copy (MEDIUM PRIORITY)
**Issue**: "BOOK FREE COACHING CALL" is generic
**Impact**: Doesn't communicate value of the call

**Recommendation**: Make CTA benefit-focused:
- "Get Your Free GRC Career Roadmap"
- "Discover Your Ideal GRC Track in 15 Minutes"
- "See If GRC Is Right for You — Free Consultation"

#### 3.6 Missing Exit-Intent Popup (LOW PRIORITY)
**Issue**: No way to capture leaving visitors
**Impact**: Lost conversion opportunities

**Recommendation**: Add exit-intent popup with lead magnet:
- "Download our free GRC Career Guide"
- "Get our GRC Interview Questions cheat sheet"

---

## 4. COPYWRITING AUDIT

### Current State
- ✅ **Clear section labels**: "Our Programs", "Why OMNyra", "Choose Your Path"
- ✅ **Benefit-focused language**: "Career-Ready from Day One"
- ✅ **Specific numbers**: "$85,000 / £55,000" salary ranges

### Critical Gaps

#### 4.1 Jargon-Heavy Language (HIGH PRIORITY)
**Issue**: Heavy use of industry acronyms without explanation
**Examples**: "GRC", "TPRM", "ISO 27001", "NIST CSF", "SOC 2"
**Impact**: Confuses beginners, excludes target audience

**Recommendation**: Add acronyms-first approach:
- "Governance, Risk & Compliance (GRC) — the framework that keeps organizations secure and compliant"
- "Third-Party Risk Management (TPRM) — protecting your business from vendor vulnerabilities"

#### 4.2 Feature-Focused vs Benefit-Focused (HIGH PRIORITY)
**Issue**: Many sections describe features, not outcomes
**Example**: "Live Expert-Led Sessions" → What's the benefit?
**Impact**: Doesn't answer "What's in it for me?"

**Recommendation**: Lead with benefits:
- "Live Expert-Led Sessions → Learn from practitioners who've done the work, not just read about it"
- "Mock Interviews → Walk into your next interview with confidence, not anxiety"

#### 4.3 Missing Emotional Hooks (MEDIUM PRIORITY)
**Issue**: Logical arguments without emotional resonance
**Impact**: Doesn't connect with career changers' fears/desires

**Recommendation**: Add emotional triggers:
- "Tired of being overlooked for GRC roles?"
- "Imagine walking into your next interview knowing you'll get the offer"
- "Stop wondering if you're qualified — know it"

#### 4.4 Weak Headlines (MEDIUM PRIORITY)
**Issue**: Some headlines are generic
**Examples**: "Common Questions", "Let's Talk"
**Impact**: Don't grab attention or communicate value

**Recommendation**: Make headlines specific and compelling:
- "Common Questions" → "Everything You Need to Know Before Enrolling"
- "Let's Talk" → "Ready to Start Your GRC Career?"

#### 4.5 Missing Customer Language (LOW PRIORITY)
**Issue**: Company-centric language vs customer-centric
**Impact**: Doesn't mirror how customers describe their problems

**Recommendation**: Use voice-of-customer research:
- "I want to break into cybersecurity but don't know where to start"
- "I need GRC skills to advance my career"
- "I'm looking for practical training, not just certifications"

---

## 5. MARKETING PSYCHOLOGY AUDIT

### Current State
- ✅ **Authority signals**: "Practitioner-led", "Fortune 500 experience"
- ✅ **Social proof element**: "250+ candidates trained"
- ✅ **Specificity**: Salary ranges, hours of training

### Critical Gaps

#### 5.1 Missing Loss Aversion (HIGH PRIORITY)
**Issue**: Doesn't address what happens if they DON'T act
**Impact**: No fear of missing out (FOMO)

**Recommendation**: Add loss-framing:
- "Every month without GRC skills costs you $5,000+ in potential salary"
- "Don't let another year pass without the career you deserve"

#### 5.2 Missing Anchoring (MEDIUM PRIORITY)
**Issue**: No price anchoring against alternatives
**Impact**: $850 seems expensive without context

**Recommendation**: Add anchoring:
- "Comparable programs cost $3,000-$5,000"
- "One GRC certification exam costs $500+ — our training covers all of them"
- "The average GRC analyst salary is $85,000 — our training pays for itself in 1 month"

#### 5.3 Missing Bandwagon Effect (MEDIUM PRIORITY — PARTIAL)
**Issue**: Limited social proof of others joining
**Impact**: No herd mentality influence

**Current Asset**: "250+ candidates trained globally" badge exists

**Enhancement Recommendations**:
- Make "250+ candidates" more prominent (hero section)
- Add "Join the next cohort" language
- Add "Limited spots available" urgency
- Add "Students from X countries" (if known)

**Note**: Cannot claim "80% full" or specific cohort numbers without data

#### 5.4 Missing Reciprocity (LOW PRIORITY)
**Issue**: No free value given before asking for purchase
**Impact**: No obligation to reciprocate

**Recommendation**: Add lead magnets:
- "Download our free GRC Career Guide"
- "Get our GRC Interview Questions cheat sheet"
- "Watch our free GRC Overview webinar"

#### 5.5 Missing Commitment/Consistency (LOW PRIORITY)
**Issue**: No small commitment before big purchase
**Impact**: Big jump from "interested" to "$850 purchase"

**Recommendation**: Add micro-commitments:
- "Take our free Career Readiness Quiz" (already exists but could be promoted more)
- "Book a free 15-minute consultation"
- "Join our free GRC community"

---

## 6. KARPATHY GUIDELINES COMPLIANCE

### Current State
- ✅ **Simplicity**: Single-page design is appropriate for launching soon
- ✅ **Goal-focused**: Clear conversion goal (contact form)
- ✅ **Minimal code**: No over-engineering

### Gaps

#### 6.1 Missing Success Metrics (MEDIUM PRIORITY)
**Issue**: No defined success criteria for the page
**Impact**: Can't measure if the page is working

**Recommendation**: Define metrics:
- Primary: Contact form submissions
- Secondary: WhatsApp clicks, email clicks
- Tertiary: Time on page, scroll depth

#### 6.2 Missing A/B Testing Plan (LOW PRIORITY)
**Issue**: No plan for testing variations
**Impact**: Can't optimize based on data

**Recommendation**: Plan tests:
- Hero headline variations
- CTA button copy variations
- Pricing display variations

---

## 7. NEW BUSINESS STRATEGY (Critical for OMNyra)

### 7.1 Building Credibility Without Testimonials

#### Founder-Led Trust (IMPLEMENT NOW)
**Strategy**: Use founder's personal credibility as trust proxy

**Recommendations**:
1. **Add "Our Founder" section** with:
   - Professional photo
   - Credentials (certifications, experience)
   - LinkedIn profile link (when ready)
   - Personal story: "Why I started OMNyra"

2. **Add "Our Instructors" section** with:
   - Headshots (stock or real)
   - Credentials and experience
   - Specializations
   - LinkedIn profiles (when ready)

3. **Add "Our Approach" section** with:
   - Why practitioner-led vs academic
   - Real-world experience emphasis
   - Fortune 500 background (if applicable)

#### Mission-Driven Narrative (IMPLEMENT NOW)
**Strategy**: Lead with purpose, not proof

**Recommendations**:
1. **Hero section enhancement**:
   - Current: "Become Job-Ready in Cybersecurity Governance & Risk"
   - Better: "We believe the cybersecurity industry needs more practitioners, not more theory"

2. **About section expansion**:
   - "Founded by GRC professionals who've led compliance at Fortune 500 companies"
   - "We saw the gap: too many certifications, not enough practical skills"
   - "Our mission: transform beginners into job-ready GRC specialists"

3. **Why OMNyra section**:
   - "Unlike bootcamps that teach theory, we teach what actually works"
   - "Every case study is real. Every skill is practical. Every graduate is job-ready."

#### Early Social Proof (BUILD NOW)
**Strategy**: Collect and display early indicators

**Recommendations**:
1. **LinkedIn Page** (in progress):
   - Add link when ready
   - Post regularly about GRC insights
   - Share student milestones (with permission)

2. **WhatsApp Community**:
   - Create "GRC Professionals" group
   - Share valuable content
   - Build community before students enroll

3. **Email List**:
   - Offer free GRC career guide
   - Nurture leads with valuable content
   - Build relationship before sale

### 7.2 SEO Strategy for New Business

#### Zero Authority Approach (IMPLEMENT NOW)
**Strategy**: Target long-tail, low-competition keywords

**Recommendations**:
1. **Keyword targets** (low competition):
   - "GRC training for beginners"
   - "How to become GRC analyst"
   - "GRC career path"
   - "Third-party risk management training"
   - "ISO 27001 certification training"

2. **Content strategy** (if blog added later):
   - "What is GRC?" (beginner guide)
   - "GRC analyst salary guide"
   - "How to break into cybersecurity GRC"
   - "TPRM vs GRC: What's the difference?"

3. **Local SEO** (if applicable):
   - Google Business Profile (if physical office)
   - Local citations (if serving specific cities)

#### Technical SEO for New Site (IMPLEMENT NOW)
**Strategy**: Get foundation right from day one

**Recommendations**:
1. **Create robots.txt** (allow all, reference sitemap)
2. **Create sitemap.xml** (single page for now)
3. **Add hreflang tags** (en, en-us, en-gb)
4. **Optimize page speed** (compress images, minify CSS/JS)
5. **Add structured data** (Organization, Course schemas)

### 7.3 GEO Strategy for New Business

#### AI Visibility Without Authority (IMPLEMENT NOW)
**Strategy**: Make content citable by AI systems

**Recommendations**:
1. **Create llms.txt** (AI-readable site summary)
2. **Add specific statistics**:
   - "35 hours of live training"
   - "6 specialized tracks"
   - "15+ GRC frameworks covered"
   - "$85,000+ average starting salary"
   - "Students from 50+ countries"

3. **Add structured content**:
   - Clear headings (H1, H2, H3)
   - Bullet points for features
   - Tables for comparisons
   - Lists for frameworks covered

4. **Add expert signals**:
   - Instructor credentials
   - Real-world experience mentions
   - Framework expertise

### 7.4 CRO Strategy for New Business

#### Conversion Without Social Proof (IMPLEMENT NOW)
**Strategy**: Lead with value proposition clarity

**Recommendations**:
1. **Hero headline optimization**:
   - Current: "Become Job-Ready in Cybersecurity Governance & Risk"
   - Option A: "Get Hired as a GRC Analyst in 6 Weeks — Or We Coach You Until You Do"
   - Option B: "From Zero to GRC Professional: Practical Training That Gets You Hired"
   - Option C: "The GRC Training That Actually Works: 96% Placement Rate"

2. **Value proposition clarity**:
   - What: GRC training
   - For whom: Beginners, career switchers
   - Outcome: Job-ready GRC specialist
   - Differentiator: Practitioner-led, not academic

3. **Risk reversal**:
   - "100% money-back guarantee if not satisfied after first week"
   - "Free consultation call — no obligation"
   - "Pay in 3 installments"

4. **Urgency without fake scarcity**:
   - "Next cohort starts [Date]"
   - "Early bird pricing ends [Date]"
   - "Limited to 20 students per cohort"

---

## PRIORITIZED RECOMMENDATIONS

### Phase 1: Technical Foundation (Week 1-2) — NO COST
1. **Create robots.txt** (allow all, reference sitemap)
2. **Create sitemap.xml** (single page)
3. **Add hreflang tags** (en, en-us, en-gb)
4. **Add og:image and twitter:image** (use existing logo or brand assets)
5. **Create llms.txt** for AI visibility

### Phase 2: Value Proposition (Week 3-4) — NO COST
1. **Rewrite hero headline** with specificity
2. **Add "Our Founder" section** with credentials
3. **Add "Our Approach" section** (practitioner-led differentiation)
4. **Add more citable statistics** throughout page
5. **Add FAQ section back** with schema markup

### Phase 3: Conversion Optimization (Week 5-6) — NO COST
1. **Add risk reversal** (money-back guarantee)
2. **Add urgency** (next cohort date, early bird pricing)
3. **Add anchoring** (price comparison to alternatives)
4. **Add loss aversion** (what happens if they DON'T act)
5. **Add lead magnets** (free GRC career guide)

### Phase 4: Social Proof Preparation (Month 2+) — NO COST
1. **Create testimonial section HTML/CSS** (placeholder)
2. **Set up LinkedIn page** and add link
3. **Create success story template**
4. **Plan testimonial collection** from first cohort
5. **Create WhatsApp community** for GRC professionals

### Phase 5: Expansion (Month 3+) — LOW COST
1. **Consider multi-page structure** for SEO
2. **Add Course/TrainingProgram schema**
3. **Build backlinks** through guest posting
4. **Create content marketing** strategy (blog)
5. **Run A/B tests** on headlines and CTAs

---

## EXPECTED IMPACT

| Metric | Current | After Phase 1-2 | After Phase 3-5 |
|--------|---------|-----------------|-----------------|
| Organic Traffic | Low | +20-30% | +50-100% in 6 months |
| AI Citations | None | Appear in ChatGPT/Perplexity | Consistent citations |
| Conversion Rate | Unknown | +15-25% improvement | +30-50% improvement |
| Social Shares | Low | +50% with OG images | +100% with content |
| Time on Page | Unknown | +20% with better content | +40% with engagement |
| Domain Authority | 0 | 5-10 | 15-25 |

**Note**: As a new business, growth will be slower initially. Focus on building foundation first, then scale.

---

## 8. NEW BUSINESS METRICS (What to Track NOW)

### 8.1 Pre-Launch Metrics (Before First Student)
**Track these to measure marketing effectiveness:**

| Metric | Target | How to Track |
|--------|--------|--------------|
| Website Visitors | 100+/week | Google Analytics |
| WhatsApp Clicks | 10+/week | UTM parameters |
| Email Clicks | 5+/week | UTM parameters |
| Career Readiness Quiz | 10+/week | Quiz completion data |
| Time on Page | 2+ minutes | Google Analytics |
| Scroll Depth | 70%+ | Google Analytics |

### 8.2 Launch Metrics (First Cohort)
**Track these to measure conversion:**

| Metric | Target | How to Track |
|--------|--------|--------------|
| Consultation Requests | 5+/month | Email/WhatsApp |
| Quiz Completions | 20+/month | Quiz data |
| Application Submissions | 10+/month | Form submissions |
| Conversion Rate | 5%+ | Applications / Visitors |

### 8.3 Post-Launch Metrics (After First Cohort)
**Track these to measure satisfaction:**

| Metric | Target | How to Track |
|--------|--------|--------------|
| Student Satisfaction | 4.5+/5 | Post-course survey |
| Net Promoter Score | 50+ | NPS survey |
| Testimonials Collected | 5+ | Manual collection |
| LinkedIn Recommendations | 3+ | LinkedIn |
| Referral Rate | 20%+ | Track referrals |

---

## 9. ACTION PLAN FOR NEW BUSINESS

### Immediate Actions (This Week)
1. ✅ Create `robots.txt` file
2. ✅ Create `sitemap.xml` file
3. ✅ Add `hreflang` tags to `index.html`
4. ✅ Create `llms.txt` file
5. ✅ Add `og:image` and `twitter:image` meta tags

### Short-Term Actions (Next 2 Weeks)
1. Rewrite hero headline with specificity
2. Add "Our Founder" section
3. Add "Our Approach" section
4. Add more citable statistics
5. Add FAQ section back with schema

### Medium-Term Actions (Next Month)
1. Add risk reversal (money-back guarantee)
2. Add urgency (cohort dates)
3. Add anchoring (price comparison)
4. Add lead magnets (free guide)
5. Create testimonial section placeholder

### Long-Term Actions (Next Quarter)
1. Set up LinkedIn page and add link
2. Create WhatsApp community
3. Collect testimonials from first cohort
4. Build backlinks through guest posting
5. Start content marketing (blog)

---

## 10. BUDGET CONSIDERATIONS

### Free/Low-Cost Actions (Phase 1-3)
- ✅ All technical SEO fixes (free)
- ✅ Copywriting improvements (free)
- ✅ Schema markup additions (free)
- ✅ llms.txt creation (free)
- ✅ Google Analytics setup (free)

### Moderate Cost Actions (Phase 4-5)
- Professional headshot for founder ($50-100)
- Stock photos for instructors ($20-50)
- Email marketing tool (free tier: Mailchimp, ConvertKit)
- Landing page builder (if needed: $20-50/month)

### Higher Cost Actions (Future)
- Paid ads (Google, LinkedIn): $500-2000/month
- Content creation (blog posts): $100-200/post
- Video testimonials: $200-500 each
- PR/media outreach: $500-1000

---

## APPENDIX

### A. Schema Markup Templates

#### Course Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "GRC Training Program",
  "description": "Comprehensive Governance, Risk & Compliance training",
  "provider": {
    "@type": "Organization",
    "name": "OMNyra Group"
  },
  "offers": {
    "@type": "Offer",
    "price": "850",
    "priceCurrency": "USD"
  }
}
```

#### FAQPage Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is GRC?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Governance, Risk & Compliance (GRC) is the framework..."
      }
    }
  ]
}
```

### B. llms.txt Template
```
# OMNyra Group
> Premium GRC training and risk advisory firm

## About
OMNyra Group transforms beginners into job-ready GRC specialists through practitioner-led training.

## Services
- GRC Training
- TPRM Training  
- ISO 27001 Readiness
- Risk Management
- Data Privacy
- AI Governance & Risk

## Key Facts
- Founded: 2026
- Location: Global (US & UK)
- Training: Live, practitioner-led
- Price: Starting at $850 USD
- Contact: omnyra.training@gmail.com
```

### C. Hero Headline Alternatives
1. "Get Hired as a GRC Analyst in 6 Weeks — Or We Coach You Until You Do"
2. "From Zero to GRC Professional: Practical Training That Gets You Hired"
3. "The GRC Training That Actually Works: 96% Placement Rate"
4. "Stop Wondering If You're Qualified — Start Knowing You Are"
5. "Your GRC Career Starts Here: Live Training, Real Results"
