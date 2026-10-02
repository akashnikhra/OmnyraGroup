from playwright.sync_api import sync_playwright

def run_quiz(page, q1_idx, q2_idx, q3_idx, q4_idx, q5_idx):
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(1500)
    page.click(f'.quiz__step[data-step="1"] .quiz__opt:nth-child({q1_idx + 1})')
    page.wait_for_timeout(400)
    page.click(f'.quiz__step[data-step="2"] .quiz__opt:nth-child({q2_idx + 1})')
    page.wait_for_timeout(400)
    page.click(f'.quiz__step[data-step="3"] .quiz__opt:nth-child({q3_idx + 1})')
    page.wait_for_timeout(400)
    page.click(f'.quiz__step[data-step="4"] .quiz__opt:nth-child({q4_idx + 1})')
    page.wait_for_timeout(400)
    page.click(f'.quiz__step[data-step="5"] .quiz__opt:nth-child({q5_idx + 1})')
    page.wait_for_timeout(600)
    return page.inner_text('#resultCareer'), page.inner_text('#resultPlanName')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    tests = [
        ("T1: Non-tech+0-2yr", 0, 1, 0, 1, 3, "Junior GRC Analyst", "Lattice"),
        ("T2: Non-tech+5+yr", 0, 3, 0, 1, 3, "GRC Manager", "Lattice"),
        ("T3: Gen IT+2-5yr", 1, 2, 0, 2, 3, "ISO 27001 Lead Implementer", "Lattice"),
        ("T4: Cybersec+0-2yr", 2, 1, 0, 2, 3, "Cybersecurity Risk Analyst", "Lattice"),
        ("T5: GRC+Student", 3, 0, 0, 1, 3, "GRC Analyst", "Lattice"),
        ("T6: GRC+UK", 3, 2, 0, 2, 1, "Data Privacy Analyst", "Lattice"),
        ("T7: AI goal", 0, 2, 0, 3, 3, "AI Governance", "Nexus"),
        ("T8: Team", 0, 0, 0, 4, 3, "team upskilling", "Custom"),
    ]

    for name, q1, q2, q3, q4, q5, exp_career, exp_plan in tests:
        career, plan = run_quiz(page, q1, q2, q3, q4, q5)
        c_ok = exp_career.lower() in career.lower()
        p_ok = exp_plan.lower() in plan.lower()
        s = "PASS" if (c_ok and p_ok) else "FAIL"
        print(f"[{s}] {name} -> career='{career}' plan='{plan}'")

    browser.close()
    print("Done.")
