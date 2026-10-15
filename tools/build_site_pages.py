"""Generate OMNyra Group's static program, hub and legal pages.

Run from the repo root:  python tools/build_site_pages.py
Writes plain HTML (no build step at serve time); commit the output.
Program descriptions, frameworks, skills, jobs and deliverables are read from
the program tabs in index.html so the two never disagree. Curriculum modules,
levels and FAQ answers live in PROGRAMS below.
"""
import html
import json
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://omnyragroup.online"
EMAIL = "omnyra.training@gmail.com"
WA_NUMBER = "919063370816"
LINKEDIN = "https://www.linkedin.com/company/omnyratraining"
LEGAL_UPDATED = "15 October 2026"

e = html.escape


def wa_link(text):
    return "https://wa.me/%s?text=%s" % (WA_NUMBER, quote(text))


PLANS_NOTE = "10, 20 or 35 hours"

COMMON_FIT = [
    ("Students and fresh graduates", "Start a security career without years of technical experience."),
    ("Career switchers", "Move from IT, audit, legal, finance or operations into GRC."),
    ("Working professionals", "Formalise skills you already use and target senior roles."),
    ("International students", "Prepare for US, UK and remote roles with market-specific coaching."),
]

PROGRAMS = [
    {
        "key": "grc", "slug": "grc", "short": "GRC",
        "title": "Governance, Risk & Compliance (GRC)",
        "seo_title": "GRC Training Course | Governance, Risk & Compliance | OMNyra Group",
        "card": "Policies, control frameworks, risk registers and audit readiness: the core skill set every GRC analyst is hired for.",
        "level": "Beginner friendly",
        "prereq": "No. The GRC track starts from first principles and is designed for people coming from non-technical backgrounds as well as IT. Comfort with reading documents and working in spreadsheets is enough.",
        "cert": "CGRC, CISA or CRISC",
        "modules": [
            ("Foundations of governance, risk and compliance", ["How GRC teams are organised and who they work with", "The three lines model and where analysts sit", "What a typical GRC week looks like"]),
            ("Security frameworks and control mapping", ["NIST CSF functions and categories", "COBIT governance objectives", "Mapping one control to many frameworks"]),
            ("Policy writing and exception management", ["Policy, standard and procedure hierarchy", "Writing policy language people can follow", "Exception requests and compensating controls"]),
            ("Risk assessment and the risk register", ["Identifying, scoring and treating risk", "Register fields, owners and review cycles", "Reporting risk to leadership"]),
            ("Audit readiness and evidence", ["SOC 2 Type II trust services criteria", "Evidence requests and walkthroughs", "Testing control design and operating effectiveness"]),
            ("Regulatory mapping", ["SOX IT general controls", "HIPAA Security Rule and PCI DSS at analyst depth", "Turning requirements into testable controls"]),
            ("GRC tooling in practice", ["How ServiceNow GRC and RSAM model policies, risks and issues", "Workflows, attestations and dashboards"]),
            ("Capstone and interview preparation", ["Assemble your policy suite, control map and risk register", "Practise the questions GRC analyst interviews actually ask"]),
        ],
    },
    {
        "key": "tprm", "slug": "tprm", "short": "TPRM",
        "title": "Third-Party Risk Management (TPRM)",
        "seo_title": "Third-Party Risk Management (TPRM) Training | OMNyra Group",
        "card": "Vendor tiering, SIG questionnaires, SOC report reviews and continuous monitoring across the full vendor lifecycle.",
        "level": "Beginner to intermediate",
        "prereq": "No. A basic understanding of how businesses buy software and services helps, and the first module covers the vocabulary you need.",
        "cert": "CTPRP",
        "modules": [
            ("The third-party risk lifecycle", ["Planning, due diligence, contracting and onboarding", "Monitoring and offboarding", "Who owns each step"]),
            ("Vendor inventory and risk tiering", ["Inherent risk drivers: data, criticality, connectivity", "Building a tiering matrix", "Residual risk after controls"]),
            ("Due diligence questionnaires", ["SIG and SIG Lite structure", "CAIQ for cloud providers", "Reading answers critically and following up"]),
            ("Reading assurance reports", ["SOC 1 versus SOC 2, Type I versus Type II", "Exceptions, bridge letters and CUECs", "Checking certificate scope"]),
            ("Contracts and security clauses", ["Right to audit and breach notification terms", "Data protection and subprocessor clauses", "Security SLAs that can be enforced"]),
            ("Continuous monitoring and issues", ["Security ratings and re-assessment cadence", "Remediation tracking", "Supply chain views from NIST SP 800-161 and ISO 27036"]),
            ("TPRM platforms", ["How OneTrust TPRM and Prevalent run assessments at scale"]),
            ("Capstone and interview preparation", ["Tier a vendor portfolio and review a real SaaS vendor", "Write an assessment report for executive sign-off"]),
        ],
    },
    {
        "key": "iso", "slug": "iso-27001", "short": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Readiness",
        "seo_title": "ISO 27001:2022 Training | ISMS Implementation & Audit Readiness | OMNyra Group",
        "card": "ISMS scoping, the 93 Annex A controls, the Statement of Applicability and internal audit readiness.",
        "level": "Beginner to intermediate",
        "prereq": "No. We explain the standard clause by clause. People with some IT or compliance exposure move faster, but it is not required.",
        "cert": "ISO 27001 Lead Implementer or Lead Auditor",
        "modules": [
            ("How ISO 27001:2022 is structured", ["Clauses 4 to 10 and what each asks for", "Annex A themes: organisational, people, physical, technological", "What changed from the 2013 version"]),
            ("Context and scope", ["Interested parties and their requirements", "Writing a scope statement", "Boundaries and interfaces"]),
            ("Risk assessment and treatment", ["The ISO 27005 approach", "Treatment options and risk owners", "Building the risk treatment plan"]),
            ("Annex A controls and the Statement of Applicability", ["Selecting and justifying the 93 controls", "Using ISO 27002 implementation guidance", "Writing the SoA"]),
            ("Running the ISMS", ["Mandatory documented information", "Objectives, metrics and management review", "Collecting evidence with Vanta and Drata"]),
            ("Internal audit and certification", ["Planning an internal audit programme", "Stage 1 versus Stage 2 audits", "Nonconformities and corrective action"]),
            ("Capstone and interview preparation", ["Produce an SoA and risk treatment plan", "Run a simulated Stage 1 gap audit"]),
        ],
    },
    {
        "key": "risk", "slug": "risk-management", "short": "Risk Management",
        "title": "Enterprise & Cyber Risk Management",
        "seo_title": "Cyber Risk Management Training | FAIR, NIST RMF, COSO ERM | OMNyra Group",
        "card": "Quantify cyber risk in financial terms with FAIR, set risk appetite and brief executives on what to fund.",
        "level": "Intermediate",
        "prereq": "No formal prerequisite. You will use Excel for the quantitative modules, so being comfortable with formulas helps. We cover the statistics you need.",
        "cert": "CRISC",
        "modules": [
            ("Risk fundamentals", ["Enterprise, cyber and operational risk", "Risk appetite and tolerance", "Common vocabulary across frameworks"]),
            ("Risk frameworks", ["NIST RMF steps", "COSO ERM components", "Choosing a framework for an organisation"]),
            ("Threat scenarios and qualitative scoring", ["Writing scenarios executives understand", "Heat maps and their limits"]),
            ("Quantitative risk with FAIR", ["Loss event frequency and loss magnitude", "Working with ranges", "Building a Monte Carlo model in Excel"]),
            ("Business impact analysis", ["Critical processes and dependencies", "RTO and RPO", "Linking impact to risk ratings"]),
            ("Appetite, KRIs and reporting", ["Writing a risk appetite statement", "Key risk indicators", "How Archer and RiskLens support reporting"]),
            ("Capstone and interview preparation", ["Present a C-level risk briefing with cost-benefit analysis"]),
        ],
    },
    {
        "key": "privacy", "slug": "data-privacy", "short": "Data Privacy",
        "title": "Global Data Privacy & Protection",
        "seo_title": "Data Privacy Training | GDPR, CCPA/CPRA, DPIA | OMNyra Group",
        "card": "GDPR and CCPA/CPRA in practice: DPIAs, records of processing, data subject requests and cross-border transfers.",
        "level": "Beginner friendly",
        "prereq": "No. The track suits people from legal, compliance, HR and IT backgrounds alike. We start with privacy principles before moving into the operational work.",
        "cert": "CIPP/E, CIPP/US or CIPT",
        "modules": [
            ("Privacy principles and the regulatory map", ["GDPR, UK GDPR and CCPA/CPRA side by side", "Lawful bases for processing", "Controllers and processors"]),
            ("Data mapping and records of processing", ["Building a data inventory", "Article 30 RoPA fields", "Retention schedules"]),
            ("DPIAs and privacy by design", ["When a DPIA is required", "Running and documenting one", "Mitigations product teams can ship"]),
            ("Data subject rights", ["Access, deletion, correction and opt-out", "DSAR workflows and deadlines", "Automating the response"]),
            ("International data transfers", ["Standard Contractual Clauses", "Transfer impact assessments"]),
            ("Running a privacy programme", ["ISO 27701 privacy information management", "Breach notification", "How OneTrust and TrustArc support the programme"]),
            ("Capstone and interview preparation", ["Complete a DPIA, a DSAR playbook and a RoPA register"]),
        ],
    },
    {
        "key": "ai", "slug": "ai-governance", "short": "AI Governance",
        "title": "AI Governance & Risk Management",
        "seo_title": "AI Governance Training | ISO 42001, EU AI Act, NIST AI RMF | OMNyra Group",
        "card": "ISO/IEC 42001, the EU AI Act and NIST AI RMF, plus hands-on auditing of generative AI applications.",
        "level": "Intermediate",
        "prereq": "No coding is required. A basic understanding of GRC concepts helps, so some learners pair this track with the GRC track or take it after Lattice.",
        "cert": "AIGP",
        "modules": [
            ("The AI risk landscape", ["Types of AI systems and where risk appears", "Hallucination, IP, bias, data leakage and prompt injection"]),
            ("The EU AI Act", ["Prohibited, high-risk, limited and minimal risk tiers", "Obligations for providers and deployers", "General-purpose AI models"]),
            ("NIST AI RMF 1.0", ["Govern, Map, Measure, Manage", "Using the profiles in practice"]),
            ("ISO/IEC 42001 AI management systems", ["Structure of the standard", "AI policy and impact assessment", "Controls and evidence"]),
            ("Auditing LLM applications", ["OWASP Top 10 for LLM applications", "Guardrails, testing and monitoring"]),
            ("Bias, transparency and model governance", ["Model inventory and documentation", "Human oversight", "Tooling such as Credo AI"]),
            ("Capstone and interview preparation", ["Build an AI risk register and an algorithmic impact assessment", "Draft an ISO 42001-aligned AI acceptable use policy"]),
        ],
    },
]


def load_homepage_content():
    """Pull desc, frameworks, skills, jobs and deliverable from index.html."""
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

    def clean(x):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()

    for p in PROGRAMS:
        i = src.index('id="panel-%s"' % p["key"])
        j = src.find('class="program-panel"', i + 20)
        block = src[i:j if j > 0 else i + 12000]
        p["desc"] = clean(re.search(r'program-desc-text">(.*?)</p>', block, re.S).group(1))
        p["frameworks"] = [clean(x) for x in re.findall(r'framework-pill">(.*?)</span>', block, re.S)]
        p["skills"] = [clean(x) for x in re.findall(r'skills-check-item">.*?<span>(.*?)</span>', block, re.S)]
        p["jobs"] = [(clean(a), clean(b).replace("Median Salary:", "").strip())
                     for a, b in re.findall(r'job-title">(.*?)</div>\s*<div class="job-salary">(.*?)</div>', block, re.S)]
        p["deliverable"] = clean(re.search(r'deliverable-desc">(.*?)</p>', block, re.S).group(1))
        assert p["desc"] and p["frameworks"] and p["skills"] and p["jobs"], p["key"]


# ---------------------------------------------------------------- shared chrome

ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg>'
ICON_SUN = '<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
ICON_MOON = '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'
ICON_CHEV = '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_USERS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
ICON_VIDEO = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="6" width="14" height="12" rx="2"/><path d="M22 8l-6 4 6 4z"/></svg>'
ICON_LEVEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V14M10 20V9M16 20V4M22 20H2"/></svg>'

NAV_ITEMS = [
    ("/programs/", "Programs"),
    ("/#plans", "Plans"),
    ("/#corporate", "For teams"),
    ("/#testimonials", "Reviews"),
    ("/#contact", "Contact"),
]

ORG = {"@type": "Organization", "name": "OMNyra Group", "url": SITE,
       "logo": SITE + "/Website/img/primary-logo-transparent.png"}


def head(title, description, canonical_path, schema_blocks):
    url = SITE + canonical_path
    schema = "\n  ".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False, separators=(",", ":"))
        for s in schema_blocks)
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/png" sizes="512x512" href="/favicon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/favicon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="OMNyra Group">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{site}/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{site}/og-image.png">
  <script>(function(){{var d=document.documentElement;d.classList.add('js');try{{if(localStorage.getItem('omnyra-theme')==='light')d.setAttribute('data-theme','light');}}catch(e){{}}}})();</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css">
  {schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="ambient" aria-hidden="true"></div>
""".format(title=e(title), desc=e(description), url=e(url), site=SITE, schema=schema)


def nav(current=None):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href == current else "", e(label))
        for href, label in NAV_ITEMS)
    return """<header class="site-nav">
  <div class="container">
    <a class="brand" href="/" aria-label="OMNyra Group home"><img data-logo src="/Website/img/Monochrome_white-transparent.png" alt="OMNyra Group" width="1792" height="705"></a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <div class="nav-actions">
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle light or dark theme">{sun}{moon}</button>
      <a class="btn btn-primary" href="/#contact">Book a free call</a>
      <button class="icon-btn menu-btn" type="button" data-menu-btn aria-controls="mobile-panel" aria-expanded="false" aria-label="Open menu">{menu}</button>
    </div>
  </div>
</header>
<nav class="mobile-panel" id="mobile-panel" data-open="false" aria-label="Mobile">{links}<a class="btn btn-primary" href="/#contact">Book a free call</a></nav>
""".format(links=links, sun=ICON_SUN, moon=ICON_MOON, menu=ICON_MENU)


def footer():
    progs = "".join('<li><a href="/programs/%s/">%s</a></li>' % (p["slug"], e(p["short"])) for p in PROGRAMS)
    wa = wa_link("Hi OMNyra, I'd like to know more about your GRC programs.")
    return """<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-brand">
        <img data-logo src="/Website/img/Monochrome_white-transparent.png" alt="OMNyra Group" width="1792" height="705" loading="lazy">
        <p>Practitioner-led GRC training with 1-on-1 career coaching for global roles. Empowering Careers. Securing the Future.</p>
      </div>
      <div><h2>Programs</h2><ul>{progs}<li><a href="/programs/">Compare all tracks</a></li></ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="/#about">About</a></li>
        <li><a href="/#plans">Plans</a></li>
        <li><a href="/#corporate">Corporate training</a></li>
        <li><a href="/#testimonials">Reviews</a></li>
        <li><a href="/Exam%20Portal/">Student exam portal</a></li>
      </ul></div>
      <div><h2>Legal</h2><ul>
        <li><a href="/privacy/">Privacy policy</a></li>
        <li><a href="/terms/">Terms of service</a></li>
        <li><a href="/cookies/">Cookie policy</a></li>
      </ul></div>
      <div><h2>Contact</h2><ul>
        <li><a href="mailto:{email}">{email}</a></li>
        <li><a href="{wa}" target="_blank" rel="noopener noreferrer">WhatsApp +91 90633 70816</a></li>
        <li><a href="{li}" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
      </ul></div>
    </div>
    <div class="foot-base"><span>&copy; 2026 OMNyra Group. All rights reserved.</span><span>Serving learners in the US, UK and worldwide.</span></div>
  </div>
</footer>
<a class="wa-float" href="{wa}" target="_blank" rel="noopener noreferrer" aria-label="Chat with OMNyra on WhatsApp">{icon}<span>Chat with us</span></a>
<script src="/assets/site.js" defer></script>
</body>
</html>
""".format(progs=progs, email=EMAIL, wa=e(wa), li=LINKEDIN, icon=ICON_WA)


def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = []
    for i, (name, url) in enumerate(items):
        if i == len(items) - 1:
            parts.append('<li><span aria-current="page">%s</span></li>' % e(name))
        else:
            parts.append('<li><a href="%s">%s</a></li>' % (url, e(name)))
    return '<nav class="crumbs container" aria-label="Breadcrumb"><ol>%s</ol></nav>' % "".join(parts)


# ---------------------------------------------------------------- program page

def faqs_for(p):
    return [
        ("Do I need a technical background for the %s track?" % p["short"], p["prereq"]),
        ("Is the training live or recorded?",
         "Live. Every session is taught online by a practitioner in real time, with time for questions and "
         "case work. There are no pre-recorded lectures."),
        ("How many hours of training do I get?",
         "That depends on the plan you choose: Node is 10 hours, Lattice is 20 hours and Nexus is 35 hours. "
         "Nexus also includes all six tracks."),
        ("What will I have built by the end?", p["deliverable"]),
        ("Do you help with finding a job?",
         "Yes. Lattice and Nexus include ATS-friendly resume rebuilding, LinkedIn profile updates, a mock "
         "interview and ongoing career mentorship. Nexus adds 1-on-1 executive coaching and priority "
         "placement support."),
        ("Is a certification exam included?",
         "You receive an OMNyra certificate of completion. External certification exams and their fees are "
         "not included. If you plan to sit %s, ask on your free call how this track maps to it." % p["cert"]),
        ("Is there a discount for groups?",
         "Yes. Friends or colleagues enrolling together as a group of 3 or more get group pricing, and "
         "organisations can book a dedicated cohort with custom scheduling."),
    ]


def program_page(p):
    path = "/programs/%s/" % p["slug"]
    faqs = faqs_for(p)
    crumbs = [("Home", "/"), ("Programs", "/programs/"), (p["short"], path)]
    wa = wa_link("Hi OMNyra, I'm interested in the %s program. Can we set up a free call?" % p["title"])

    course = {
        "@context": "https://schema.org", "@type": "Course", "name": p["title"],
        "description": p["desc"], "url": SITE + path, "provider": ORG,
        "educationalLevel": p["level"], "inLanguage": "en", "teaches": p["skills"],
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "instructor": ORG},
        "offers": {"@type": "Offer", "category": "Paid", "url": SITE + path},
    }
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

    skills = "".join('<div class="skill reveal"><strong>%s</strong></div>' % e(s) for s in p["skills"])
    modules = "".join(
        '<details class="reveal"%s><summary><span class="num">%d</span><span>%s</span>%s</summary>'
        '<div class="body"><ul>%s</ul></div></details>' % (
            " open" if i == 0 else "", i + 1, e(title), ICON_CHEV, "".join("<li>%s</li>" % e(b) for b in bullets))
        for i, (title, bullets) in enumerate(p["modules"]))
    pills = "".join('<span class="pill">%s</span>' % e(f) for f in p["frameworks"])
    careers = "".join(
        '<div class="career reveal"><div><h3>%s</h3><p class="tag">%s</p></div><p class="pay">%s</p></div>' % (
            e(t), "Most common first role from this track" if i == 0 else "Also within reach", e(s))
        for i, (t, s) in enumerate(p["jobs"]))
    fit = "".join('<div class="reveal"><strong>%s</strong><span>%s</span></div>' % (e(a), e(b)) for a, b in COMMON_FIT)
    faq_html = "".join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in faqs)
    idx = PROGRAMS.index(p)
    related = [PROGRAMS[(idx + k) % len(PROGRAMS)] for k in (1, 2, 3)]
    related_html = "".join(
        '<a class="card-link reveal" href="/programs/%s/"><h3>%s</h3><p>%s</p><span class="go">View track</span></a>' % (
            o["slug"], e(o["title"]), e(o["card"]))
        for o in related)

    body = """{nav}
<main id="main">
  {crumbs}
  <section class="p-hero">
    <div class="container p-hero-grid">
      <div>
        <h1 class="reveal">{title}</h1>
        <p class="lead reveal">{desc}</p>
        <div class="cta-row reveal">
          <a class="btn btn-primary" href="/#contact">Book a free call</a>
          <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener noreferrer">{icon_wa}Ask on WhatsApp</a>
        </div>
        <div class="fact-row reveal">
          <span>{i_video}Live online</span>
          <span>{i_clock}10 to 35 hours</span>
          <span>{i_level}{level}</span>
          <span>{i_users}Small cohorts</span>
        </div>
      </div>
      <aside class="enrol-card reveal" aria-labelledby="enrol-h">
        <h2 id="enrol-h">Enrol in {short}</h2>
        <p class="sub">Choose the plan that fits where you are.</p>
        <dl>
          <dt>Format</dt><dd>Live, instructor-led</dd>
          <dt>Training</dt><dd>{plans}</dd>
          <dt>Start dates</dt><dd>Rolling cohorts</dd>
          <dt>Level</dt><dd>{level}</dd>
          <dt>You receive</dt><dd>Certificate of completion</dd>
        </dl>
        <div class="stack">
          <a class="btn btn-primary btn-block" href="/#contact">Get pricing and dates</a>
          <a class="btn btn-ghost btn-block" href="/#plans">Compare plans</a>
        </div>
        <p class="note">Pricing and your start date are confirmed on a free, no-obligation call.</p>
        <p class="group">Joining with 2 or more friends or colleagues? Ask about group pricing.</p>
      </aside>
    </div>
  </section>

  <section class="band" aria-labelledby="learn-h">
    <div class="container">
      <h2 id="learn-h" class="reveal">What you will be able to do</h2>
      <p class="intro reveal">The skills employers screen for in {short} roles, practised through live case work rather than slides.</p>
      <div class="skills">{skills}</div>
    </div>
  </section>

  <section class="band" aria-labelledby="curr-h">
    <div class="container">
      <h2 id="curr-h" class="reveal">Curriculum</h2>
      <p class="intro reveal">Delivered across live sessions. The depth of each module scales with the plan you choose.</p>
      <div class="modules">{modules}</div>
    </div>
  </section>

  <section class="band" aria-labelledby="tools-h">
    <div class="container split">
      <div class="reveal">
        <h2 id="tools-h">Frameworks and tools you will use</h2>
        <p class="intro">The standards and platforms named in real job descriptions for this field.</p>
        <div class="pill-wrap">{pills}</div>
      </div>
      <div class="deliverable reveal">
        <h3>Your portfolio deliverable</h3>
        <p>{deliverable}</p>
      </div>
    </div>
  </section>

  <section class="band" aria-labelledby="careers-h">
    <div class="container">
      <h2 id="careers-h" class="reveal">Where this track leads</h2>
      <p class="intro reveal">Roles our {short} learners prepare for, with median salaries in the US and UK.</p>
      <div class="careers">{careers}</div>
      <p class="fineprint">Salary figures are indicative US and UK medians and vary by city, employer and experience.</p>
    </div>
  </section>

  <section class="band" aria-labelledby="fit-h">
    <div class="container">
      <h2 id="fit-h" class="reveal">Who this track is for</h2>
      <div class="fit">{fit}</div>
    </div>
  </section>

  <section class="band" aria-labelledby="faq-h">
    <div class="container">
      <h2 id="faq-h" class="reveal">Questions about the {short} track</h2>
      <div class="faq">{faq}</div>
    </div>
  </section>

  <section class="band" aria-labelledby="rel-h">
    <div class="container">
      <h2 id="rel-h" class="reveal">Pair it with another track</h2>
      <div class="related">{related}</div>
    </div>
  </section>

  <section class="cta-band">
    <div class="container">
      <div class="cta-panel reveal">
        <h2>Not sure {short} is the right fit?</h2>
        <p>Book a free 1-on-1 call. We will look at your background and target market, then recommend a track and plan.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="/#contact">Book a free call</a>
          <a class="btn btn-ghost" href="/programs/">Compare all tracks</a>
        </div>
      </div>
    </div>
  </section>
</main>
""".format(nav=nav("/programs/"), crumbs=crumbs_html(crumbs), title=e(p["title"]), desc=e(p["desc"]),
           wa=e(wa), icon_wa=ICON_WA, i_video=ICON_VIDEO, i_clock=ICON_CLOCK, i_level=ICON_LEVEL, i_users=ICON_USERS,
           level=e(p["level"]), short=e(p["short"]), plans=e(PLANS_NOTE), skills=skills, modules=modules,
           pills=pills, deliverable=e(p["deliverable"]), careers=careers, fit=fit, faq=faq_html,
           related=related_html)

    desc = "%s Live, practitioner-led training with 1-on-1 career coaching." % p["card"]
    return head(p["seo_title"], desc, path, [course, faq_schema, breadcrumb(crumbs)]) + body + footer()


# ---------------------------------------------------------------- hub page

def hub_page():
    path = "/programs/"
    crumbs = [("Home", "/"), ("Programs", path)]
    cards = "".join(
        '<a class="card-link reveal" href="/programs/%s/"><span class="meta">%s</span><h3>%s</h3><p>%s</p>'
        '<span class="go">View curriculum</span></a>' % (p["slug"], e(p["level"]), e(p["title"]), e(p["card"]))
        for p in PROGRAMS)
    rows = "".join(
        '<tr><td><a href="/programs/%s/">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            p["slug"], e(p["short"]), e(p["level"]), e(", ".join(p["frameworks"][:3])), e(p["jobs"][0][0]))
        for p in PROGRAMS)
    item_list = {"@context": "https://schema.org", "@type": "ItemList", "name": "OMNyra Group Programs",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/programs/%s/" % p["slug"],
                                      "name": p["title"]} for i, p in enumerate(PROGRAMS)]}
    body = """{nav}
<main id="main">
  {crumbs}
  <section class="hub-hero container">
    <h1 class="reveal">Six GRC tracks. Pick the one that fits your next role.</h1>
    <p class="reveal">Every track is live, practitioner-led and paired with career coaching. Not sure where to start? Book a free call and we will recommend one.</p>
  </section>
  <section class="container"><div class="hub-grid">{cards}</div></section>
  <section class="band" aria-labelledby="cmp-h">
    <div class="container">
      <h2 id="cmp-h" class="reveal">Compare the tracks</h2>
      <p class="intro reveal">Level, core frameworks and the first role each track targets, side by side.</p>
      <div class="compare-wrap reveal">
        <table class="compare">
          <thead><tr><th scope="col">Track</th><th scope="col">Level</th><th scope="col">Core frameworks</th><th scope="col">Typical first role</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
  </section>
  <section class="cta-band">
    <div class="container">
      <div class="cta-panel reveal">
        <h2>Want every track?</h2>
        <p>The Nexus plan includes all six tracks across 35 hours of live training, plus 1-on-1 executive coaching.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="/#contact">Book a free call</a>
          <a class="btn btn-ghost" href="/#plans">See plans</a>
        </div>
      </div>
    </div>
  </section>
</main>
""".format(nav=nav("/programs/"), crumbs=crumbs_html(crumbs), cards=cards, rows=rows)
    return head("GRC Training Programs | TPRM, ISO 27001, Privacy, AI Governance | OMNyra Group",
                "Compare OMNyra Group's six live GRC training tracks: GRC, TPRM, ISO 27001, risk management, "
                "data privacy and AI governance.", path, [item_list, breadcrumb(crumbs)]) + body + footer()


# ---------------------------------------------------------------- legal pages

LEGAL = {
    "privacy": ("Privacy policy", "How OMNyra Group collects, uses and protects personal information.", [
        ("Who we are", ["OMNyra Group (\"OMNyra\", \"we\", \"us\") provides governance, risk and compliance training. "
                        "This policy explains how we handle personal information when you visit omnyragroup.online, "
                        "contact us or enrol in a program. Questions can be sent to %s." % EMAIL]),
        ("Information we collect", [[
            "Contact details you give us, such as your name, email address and phone or WhatsApp number.",
            "Information you share about your background and goals when you ask about a program.",
            "Enrolment and payment records when you join a program.",
            "Student exam portal data if you use it: your email address, display name, exam attempts and scores."]]),
        ("How we use it", [[
            "To answer your enquiries and arrange counselling calls.",
            "To deliver training, career coaching and certificates.",
            "To run the student exam portal and show your progress.",
            "To send service messages about your enrolment."], "We do not sell your personal information."]),
        ("Legal bases", ["Where data protection law such as the UK GDPR or EU GDPR applies, we rely on taking steps "
                         "at your request before entering a contract, performing that contract, our legitimate "
                         "interest in running and improving our training, and your consent where we ask for it."]),
        ("Service providers", [[
            "Google (Gmail) for email, and WhatsApp when you choose to contact us there.",
            "GitHub Pages to host this website.",
            "Google Fonts and cdnjs (Cloudflare) to deliver fonts and scripts. These providers receive your IP address when a page loads.",
            "Supabase to run the student exam portal."]]),
        ("Retention", ["We keep enquiry records for up to 24 months and enrolment records for as long as needed "
                       "to provide the service and meet legal, tax and accounting obligations."]),
        ("Your rights", ["Depending on where you live, you can ask to access, correct, delete or export your "
                         "personal information, or object to or restrict how we use it. Email %s and we will "
                         "respond within one month. You can also complain to your local data protection authority, "
                         "such as the ICO in the UK." % EMAIL]),
        ("International transfers", ["Our service providers may process data outside your country. Where required, "
                                     "we rely on safeguards such as standard contractual clauses."]),
        ("Changes", ["We will post any updates to this policy on this page and change the date at the top."]),
    ]),
    "terms": ("Terms of service", "The terms that apply when you use this website or enrol in an OMNyra Group program.", [
        ("About these terms", ["These terms apply to your use of omnyragroup.online and to OMNyra Group training "
                               "programs. By enrolling you agree to them."]),
        ("Enrolment and fees", ["Program fees, the payment schedule and any refund or rescheduling terms are confirmed "
                                "to you in writing before you pay. If that written confirmation differs from these "
                                "terms, the written confirmation applies."]),
        ("Live sessions", ["Programs are delivered live online. If we need to move a session, we will give you as much "
                           "notice as we can and offer a replacement time."]),
        ("Your responsibilities", [[
            "Keep your login details for any student system private.",
            "Do not record, share or resell course materials without our written permission.",
            "Be respectful to instructors and other learners."]]),
        ("Intellectual property", ["Course materials, templates and the OMNyra name and logo belong to OMNyra Group. "
                                   "You may use the work you build during a program in your own portfolio."]),
        ("Career outcomes", ["We provide training and career coaching, but we cannot guarantee a job offer, salary or "
                             "certification exam result. Salary figures on this site are indicative only."]),
        ("Liability", ["To the extent the law allows, our total liability to you for any claim related to a program is "
                       "limited to the fees you paid for that program. Nothing in these terms limits liability that "
                       "cannot be limited by law."]),
        ("Governing law", ["These terms are governed by the laws of India. If you are a consumer, you also keep any "
                           "protections given to you by the law of the country you live in."]),
        ("Contact", ["Questions about these terms can be sent to %s." % EMAIL]),
    ]),
    "cookies": ("Cookie policy", "How omnyragroup.online uses cookies and browser storage.", [
        ("Summary", ["We do not use advertising or analytics cookies on omnyragroup.online. We use a small amount "
                     "of browser storage to remember your preferences."]),
        ("What we store", ["__TABLE__"]),
        ("Third-party content", ["Fonts are loaded from Google Fonts and scripts from cdnjs (Cloudflare). These "
                                 "providers receive your IP address and may set their own technical cookies. If you "
                                 "follow a WhatsApp, LinkedIn or email link, that service's own policy applies."]),
        ("Managing storage", ["You can clear site data at any time in your browser settings. The site still works "
                              "without it; your theme choice resets to dark."]),
        ("Contact", ["Questions can be sent to %s." % EMAIL]),
    ]),
}

COOKIE_TABLE = """<table>
<thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">Purpose</th><th scope="col">Duration</th></tr></thead>
<tbody>
<tr><td>omnyra-theme</td><td>Local storage</td><td>Remembers whether you chose the light or dark theme.</td><td>Until you clear it</td></tr>
<tr><td>omnyra.exam.* and sb-*</td><td>Local storage</td><td>Keeps you signed in to the student exam portal and saves exam progress. Only set if you use the portal.</td><td>Until you sign out or clear it</td></tr>
</tbody></table>"""


def legal_page(slug):
    title, desc, sections = LEGAL[slug]
    path = "/%s/" % slug
    crumbs = [("Home", "/"), (title, path)]
    out = []
    for heading, blocks in sections:
        out.append("<h2>%s</h2>" % e(heading))
        for b in blocks:
            if b == "__TABLE__":
                out.append(COOKIE_TABLE)
            elif isinstance(b, list):
                out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % e(x) for x in b))
            else:
                out.append("<p>%s</p>" % e(b))
    body = """{nav}
<main id="main">
  {crumbs}
  <article class="container prose">
    <h1>{title}</h1>
    <p class="updated">Last updated {updated}</p>
    {content}
  </article>
</main>
""".format(nav=nav(), crumbs=crumbs_html(crumbs), title=e(title), updated=LEGAL_UPDATED,
           content="\n    ".join(out))
    return head("%s | OMNyra Group" % title, desc, path, [breadcrumb(crumbs)]) + body + footer()


def write(rel, content):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", rel)


def main():
    load_homepage_content()
    for p in PROGRAMS:
        write("programs/%s/index.html" % p["slug"], program_page(p))
    write("programs/index.html", hub_page())
    for slug in LEGAL:
        write("%s/index.html" % slug, legal_page(slug))


if __name__ == "__main__":
    main()
