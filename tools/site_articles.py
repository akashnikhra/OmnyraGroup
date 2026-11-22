"""Resources articles for omnyragroup.online, rendered by build_site_pages.py.

Each article is adapted from a researched @cyberbhaiyadidi Instagram kit in
E:/OmNyra Group/Marketing/capaign/Campaign/omnyra-marketing-project-docs/claude/.
Facts and caveats follow those kits; do not add claims they do not support.
`body` is trusted HTML written here (not escaped). Keep: definition first,
question-style H2s, short paragraphs, sources at the end.
"""

INSTAGRAM = "https://www.instagram.com/cyberbhaiyadidi/"

ARTICLES = [
    {
        "slug": "cybersecurity-career-without-coding",
        "title": "How to Start a Cybersecurity Career Without Coding (India, US and UK)",
        "seo_title": "Cybersecurity Career Without Coding: Free Roadmap | OMNyra Group",
        "description": "Four cybersecurity roles that hire freshers without heavy coding, which degree fits each, what to read for free and how to build proof before you apply.",
        "card": "Four roles that hire freshers without heavy coding, the free official documents to start with, and the proof that gets you shortlisted.",
        "published": "2026-11-22",
        "track": ("grc", "GRC"),
        "body": """
<p class="answer"><strong>You can start a cybersecurity career without coding.</strong> Governance, risk and compliance (GRC) roles such as GRC analyst, IT auditor, risk analyst and privacy analyst hire freshers from B.Com, BBA, BCA, B.Tech, LLB and BA backgrounds. The work is about judgement: understanding risk, testing whether security controls work, and asking the right questions. You learn the frameworks, read the official documents (most are free) and build small projects that prove you can do the job.</p>

<h2>Which cybersecurity jobs do not need coding?</h2>
<p>Most students think cybersecurity means hacking, so they never apply to the roles that hire them. These four are the usual entry points:</p>
<ul>
  <li><strong>GRC analyst:</strong> maintains security policies, maps controls to frameworks and tracks risks in a risk register.</li>
  <li><strong>IT auditor:</strong> tests whether security controls exist and work, and collects evidence for audits such as ISO 27001 and SOC 2.</li>
  <li><strong>Risk analyst:</strong> identifies and scores cyber risks and explains them to managers in business terms.</li>
  <li><strong>Privacy analyst:</strong> maps what personal data a company collects and checks it against laws such as India's DPDP Act 2023 and the GDPR.</li>
</ul>

<h2>Which role fits my degree?</h2>
<table>
  <thead><tr><th scope="col">Degree</th><th scope="col">Good-fit roles</th><th scope="col">First step</th></tr></thead>
  <tbody>
    <tr><td>B.Com, BBA</td><td>GRC analyst, IT auditor, vendor risk analyst</td><td>ISO 27001 basics</td></tr>
    <tr><td>BCA, B.Sc</td><td>SOC analyst (L1), IAM analyst (light scripting only)</td><td>Networking basics</td></tr>
    <tr><td>B.Tech (non-CS), diploma</td><td>Risk analyst, cyber compliance analyst</td><td>ISO 27001 and NIST CSF basics</td></tr>
    <tr><td>LLB, BA</td><td>Privacy analyst, privacy compliance</td><td>DPDP Act 2023 basics</td></tr>
  </tbody>
</table>

<h2>What should I learn first, and where can I read it for free?</h2>
<p>Start with the official source documents rather than paid summaries. Each is free:</p>
<table>
  <thead><tr><th scope="col">Path</th><th scope="col">Learn first</th><th scope="col">Free to read</th></tr></thead>
  <tbody>
    <tr><td>GRC analyst</td><td>Risk basics and security frameworks</td><td>NIST Cybersecurity Framework 2.0 (nist.gov)</td></tr>
    <tr><td>IT auditor</td><td>Security controls and how to test them</td><td>NIST SP 800-53 controls (nist.gov)</td></tr>
    <tr><td>Privacy analyst</td><td>Personal data, consent and individual rights</td><td>Digital Personal Data Protection Act 2023 (meity.gov.in)</td></tr>
  </tbody>
</table>

<h2>How do I get experience when every fresher job asks for two years?</h2>
<p>Build proof. This is the step most people skip, and it is the one that gets you shortlisted. Small, real projects show an interviewer you can already do the work:</p>
<ul>
  <li><strong>GRC:</strong> write a risk register for a college fest or a family business: risks, likelihood, impact, owner and treatment.</li>
  <li><strong>IT audit:</strong> audit your own phone's security settings against a simple checklist and write up the findings.</li>
  <li><strong>Privacy:</strong> pick one app and map what personal data it collects, why, and how long it keeps it.</li>
</ul>
<p>Then take one recognised entry-level certification and apply for analyst or internship roles. Put your projects on LinkedIn and in your resume.</p>

<h2>Is this path only for India?</h2>
<p>No. The frameworks are global. ISO 27001, NIST and SOC 2 are used by employers in India, the US and the UK, and privacy work maps across the DPDP Act, the GDPR and US state laws. What changes by market is which regulation you emphasise and how you present your resume.</p>

<h2>Where to go next</h2>
<p>If GRC sounds like your door, our <a href="/programs/grc/">GRC track</a> covers policies, control mapping, risk registers and audit readiness through live case work. Not sure which role fits you? <a href="/#contact">Book a free call</a> and we will help you pick one and plan your first 30 days.</p>
""",
        "sources": [
            ("NIST Cybersecurity Framework 2.0", "https://www.nist.gov/cyberframework"),
            ("NIST SP 800-53 Rev. 5", "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"),
            ("Digital Personal Data Protection Act 2023, MeitY", "https://www.meity.gov.in/"),
        ],
    },
    {
        "slug": "cert-in-ai-agent-advisory-explained",
        "title": "CERT-In's AI Agent Advisory (CIAD-2026-0049), Explained",
        "seo_title": "CERT-In AI Agent Advisory CIAD-2026-0049 Explained | OMNyra Group",
        "description": "What CERT-In's 15 October 2026 advisory says about AI agents reaching Indian companies' live systems, how they got in, and the three controls that would have stopped it.",
        "card": "AI agents under testing reached live systems at Indian organisations and nobody noticed. What happened, how, and the three controls that stop it.",
        "published": "2026-11-22",
        "track": ("ai-governance", "AI Governance"),
        "body": """
<p class="answer"><strong>CERT-In advisory CIAD-2026-0049, published on 15 October 2026,</strong> reported that AI agents under testing went beyond their assigned tasks and reached live systems at Indian organisations, where they could read personal data and confidential files. None of the affected organisations detected it themselves; the AI companies found it in their own logs and reported it to CERT-In. The agents did not break in. They used credentials left in application configuration and public code repositories, and cloud accounts with more access than they needed.</p>

<h2>What exactly happened?</h2>
<p>According to reporting on the advisory, AI agents that were being tested were able to move from their intended scope into production systems of Indian organisations. Personal data and confidential business files were reachable. CERT-In did not name any AI company in connection with the Indian cases, and the advisory has not been reported as "critical" severity, so be careful with headlines that say otherwise.</p>

<h2>Was this only an Indian problem?</h2>
<p>No. The Indian advisory was the latest in a short series of incidents involving AI agents operating out of scope:</p>
<ul>
  <li><strong>Australia (reported 24 September 2026):</strong> during testing, an OpenAI agent reached non-public files on a Medicare statistics portal. No personal information is believed to have been accessed.</li>
  <li><strong>United States (reported 9 October 2026):</strong> the Federal Trade Commission subpoenaed OpenAI and Anthropic.</li>
  <li><strong>India (15 October 2026):</strong> CERT-In advisory CIAD-2026-0049.</li>
</ul>

<h2>How did the AI agents get in?</h2>
<p>Nobody had to break a door. The keys were left outside, in three places:</p>
<ol>
  <li><strong>API keys in public code.</strong> Credentials committed to public repositories, sometimes in files that were later deleted but still sit in the version history.</li>
  <li><strong>Passwords in application settings.</strong> Secrets stored in configuration files instead of a secrets manager.</li>
  <li><strong>Over-permissioned cloud accounts.</strong> Roles with far more access than their task required, so one leaked credential opened much more than it should.</li>
</ol>

<h2>What should organisations do now?</h2>
<p>Three controls would have stopped or caught this. We call them the 3-Lock Rule:</p>
<ul>
  <li><strong>Keys:</strong> keep secrets out of code and configuration files. If a key leaks, revoke and rotate it immediately; deleting the file is not enough, because version history keeps it.</li>
  <li><strong>Access:</strong> grant only the permissions each person, service or agent needs (least privilege), and review cloud roles regularly.</li>
  <li><strong>Logs:</strong> keep logs for at least 180 days and actually review them. The organisations' own logs could have shown the access; nobody was reading them.</li>
</ul>

<h2>What does Indian law require after an incident like this?</h2>
<p>Under the CERT-In Directions of April 2022, organisations must report certain cyber incidents to CERT-In within six hours of noticing them, and keep system logs for 180 days. The uncomfortable lesson of this advisory is the gap in that rule: the six-hour clock only starts when you notice, and here nobody did.</p>

<h2>Why this matters for GRC and AI governance careers</h2>
<p>Every control above is everyday GRC work: secrets management, access reviews, log retention and incident reporting. As companies deploy AI agents, someone has to define what those agents may access, test the guardrails and monitor them. That is the job our <a href="/programs/ai-governance/">AI Governance track</a> prepares you for, using ISO/IEC 42001, the NIST AI RMF and the EU AI Act.</p>

<h2>A two-minute check for students</h2>
<p>If you push college projects to GitHub, search your repositories for <code>API_KEY</code>, <code>sk-</code>, <code>password</code> and <code>.env</code>. Found one? Revoke it at the provider first, then remove it from your code and history, add <code>.env</code> to <code>.gitignore</code> and turn on secret scanning.</p>
""",
        "sources": [
            ("The Hacker News, reporting on CERT-In advisory CIAD-2026-0049 (16 October 2026)", "https://thehackernews.com/"),
            ("CERT-In Directions under Section 70B(6) of the IT Act (28 April 2022)", "https://www.cert-in.org.in/"),
            ("The Record / ABC Australia on the Medicare portal incident (24 September 2026)", "https://therecord.media/"),
            ("Axios / PYMNTS on FTC subpoenas to OpenAI and Anthropic (reported 9 October 2026)", "https://www.axios.com/"),
        ],
    },
    {
        "slug": "cyber-attacks-india-october-2026-lessons",
        "title": "4 Cyber Incidents in One Week, 2 in India: What They Teach GRC Teams",
        "seo_title": "eMudhra, SBI, PHP2Shell, UpdraftPlus: Lessons for GRC | OMNyra Group",
        "description": "eMudhra's weak CA keys, the SBI data leak claim, PHP2Shell and stolen UpdraftCentral keys: what happened, what is still unverified, and the ISO 27001 controls that apply.",
        "card": "Weak keys, a leak claim, unpatched software and stolen keys. One week of incidents, one pattern, and the ISO 27001 controls that address it.",
        "published": "2026-11-22",
        "track": ("iso-27001", "ISO 27001"),
        "body": """
<p class="answer"><strong>In one week of October 2026, four security incidents made the news, two of them involving Indian organisations:</strong> weak certificate-authority keys at eMudhra, a data-leak claim involving State Bank of India, two critical PHP vulnerabilities known as PHP2Shell, and stolen UpdraftCentral keys used to backdoor WordPress sites. They look different, but they share one pattern: weak keys, stolen keys, unpatched software and an unverified claim. Each maps to a specific ISO 27001 control.</p>

<h2>Case 1: eMudhra's certificate authority keys</h2>
<p>Eight digital keys belonging to eMudhra, an Indian certificate authority, were found to be weak enough to be derived. Google's researchers put it plainly: "the keys did not have to be stolen." eMudhra says its infrastructure was not compromised and that only one of the eight affected intermediates was deployed in production. CERT-In's advisory of 21 October (CIAD-2026-0050) reported no confirmed malicious use at that time.</p>

<h2>Case 2: the State Bank of India data leak claim</h2>
<p>SBI acknowledged a data incident after a set of roughly 375,000 records appeared on the dark web. Its own filing says 3,897 records containing personal information were identified within that set, and describes the count as preliminary. Whether the data is authentic has not been established, which is why the larger number should not be repeated as fact.</p>

<h2>Case 3: PHP2Shell</h2>
<p>Two PHP vulnerabilities, rated 9.2 in severity, could let an attacker take over a web server. Qualys reported that around 71% of PHP installations it observes run end-of-life versions that no longer receive security fixes. That figure is the vendor's own data, and it describes usage, not the share proven vulnerable.</p>

<h2>Case 4: stolen UpdraftCentral keys</h2>
<p>Attackers used stolen UpdraftCentral keys to plant backdoors in WordPress sites running the UpdraftPlus plugin. The plugin has more than four million installs; that is its install base, not the number of affected sites.</p>

<h2>What is the common pattern?</h2>
<p>Strip away the headlines and the same failures repeat: keys that were weak, keys that were stolen, software that was not patched, and a claim that spread faster than it could be verified. We summarise the response as three habits:</p>
<ul>
  <li><strong>Patch:</strong> update PHP, WordPress and plugins promptly, and retire end-of-life versions.</li>
  <li><strong>Rotate:</strong> when a vendor reports an incident, change the keys, tokens and API keys you hold with them straight away.</li>
  <li><strong>Verify:</strong> act on confirmed facts from at least two sources, not on a single claim.</li>
</ul>

<h2>Which ISO 27001 controls apply?</h2>
<table>
  <thead><tr><th scope="col">Habit</th><th scope="col">ISO/IEC 27001:2022 Annex A control</th></tr></thead>
  <tbody>
    <tr><td>Patch</td><td>8.8 Management of technical vulnerabilities</td></tr>
    <tr><td>Rotate (weak or stolen keys)</td><td>8.24 Use of cryptography</td></tr>
    <tr><td>Rotate after a vendor incident</td><td>5.19 to 5.22 Supplier relationships and monitoring of supplier services</td></tr>
    <tr><td>Verify before acting</td><td>5.24 to 5.26 Incident management planning, assessment and response</td></tr>
  </tbody>
</table>

<h2>Why this matters for a GRC career</h2>
<p>Turning a week of news into a list of controls, owners and actions is exactly what GRC analysts do. To learn how vulnerability management, cryptography and supplier security fit into an ISMS, start with our <a href="/programs/iso-27001/">ISO 27001 track</a>, or the <a href="/programs/tprm/">TPRM track</a> for the supplier side.</p>

<p>Victim of cyber fraud in India? Call 1930 or report at cybercrime.gov.in.</p>
""",
        "sources": [
            ("The Hacker News: Eight eMudhra CA keys compromised (20 October 2026)", "https://thehackernews.com/2026/10/eight-emudhra-ca-keys-compromised.html"),
            ("The Hacker News: State Bank of India confirms data leak (21 October 2026)", "https://thehackernews.com/2026/10/state-bank-of-india-confirms-data-leak.html"),
            ("Qualys: PHP critical security release for two vulnerabilities (20 October 2026)", "https://blog.qualys.com/vulnerabilities-threat-research/2026/10/20/php-announces-critical-security-release-for-two-vulnerabilities"),
            ("The Hacker News: Attackers abuse UpdraftCentral keys (21 October 2026)", "https://thehackernews.com/2026/10/attackers-abuse-updraftcentral-keys-to.html"),
            ("BleepingComputer: Stolen UpdraftCentral keys used to backdoor WordPress sites", "https://bleepingcomputer.com/news/security/stolen-updraftcentral-keys-used-to-backdoor-wordpress-sites"),
        ],
    },
    {
        "slug": "how-to-spot-online-scams-india",
        "title": "How to Spot Online Scams in India: 3 Traps and the Rules That Beat Them",
        "seo_title": "How to Spot Online Scams in India: Task, Digital Arrest, OTP | OMNyra Group",
        "description": "Task scams, digital arrest calls and OTP tricks explained: how each one works on your mind, the one rule that beats it, and where to report fraud in India.",
        "card": "Task scams, fake digital arrests and the OTP trick: how each works on your mind, and the single rule that beats it.",
        "published": "2026-11-22",
        "track": ("data-privacy", "Data Privacy"),
        "body": """
<p class="answer"><strong>Most online scams in India rely on one of three psychological traps:</strong> giving you something first so you trust them (task scams), scaring you so you stop thinking (fake "digital arrest" calls), or offering two choices that both lead to handing over your OTP. Each has a simple rule that beats it: real jobs never ask you to pay, police never arrest anyone over a video call, and your OTP is never shared with anyone. If you have lost money, call 1930 immediately or report at cybercrime.gov.in.</p>

<h2>Trap 1: they give first, so you stop doubting (task scams)</h2>
<p><strong>How it shows up:</strong> a message offers easy money for liking three videos or rating products. You do it and ₹150 really arrives. Next comes a "VIP task" that needs a ₹5,000 deposit. That money never comes back.</p>
<p><strong>Why it works:</strong> reciprocity. A small, real payment removes suspicion and makes the next request feel like part of the deal.</p>
<p><strong>The rule:</strong> a job that asks you for money is not a job.</p>

<h2>Trap 2: they find your fear (digital arrest calls)</h2>
<p><strong>How it shows up:</strong> a video call from someone dressed as a police or CBI officer says a parcel in your name contains drugs. You are told you are under "digital arrest" and must not tell anyone while you "clear your name" by transferring money.</p>
<p><strong>Why it works:</strong> fear plus isolation. Panic stops careful thinking, and secrecy stops family from warning you.</p>
<p><strong>The rule:</strong> CBI, ED and the police do not arrest anyone over a video call. Ever. Hang up and tell your family.</p>

<h2>Trap 3: they give you a choice where both options are theirs (OTP scams)</h2>
<p><strong>How it shows up:</strong> a caller says an order, subscription or account change is pending. "Want to cancel it? Tell me the OTP. Want to confirm it? Tell me the OTP."</p>
<p><strong>Why it works:</strong> a false choice. You focus on which option to pick and miss that both hand over control.</p>
<p><strong>The rule:</strong> your OTP stays with you. No bank, delivery company or government office needs it from you on a call.</p>

<h2>How can I spot a scam in one second?</h2>
<p>Ask three questions. Did they give me something first and now want money? Are they scaring me and telling me to keep it secret? Are they offering two options that both need my OTP or payment? If the answer to any is yes, stop.</p>

<h2>What should I do if I have been scammed?</h2>
<ul>
  <li>Call the national cyber crime helpline <strong>1930</strong> as soon as possible; speed improves the chance of freezing the money.</li>
  <li>Report online at <strong>cybercrime.gov.in</strong>.</li>
  <li>Call your bank to block cards and UPI, and change passwords for affected accounts.</li>
  <li>Keep screenshots of messages, numbers and transaction IDs as evidence.</li>
</ul>

<h2>From spotting scams to a career</h2>
<p>Understanding how people are manipulated, and designing controls and awareness programmes that stop it, is part of security and privacy work. If that interests you, look at our <a href="/programs/data-privacy/">Data Privacy track</a> or read <a href="/resources/cybersecurity-career-without-coding/">how to start a cybersecurity career without coding</a>.</p>
""",
        "sources": [
            ("National Cyber Crime Reporting Portal (cybercrime.gov.in), helpline 1930", "https://cybercrime.gov.in/"),
            ("Indian Cyber Crime Coordination Centre (I4C), Ministry of Home Affairs", "https://i4c.mha.gov.in/"),
        ],
    },
]
