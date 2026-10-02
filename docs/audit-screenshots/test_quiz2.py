from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # Test 9: No "Advocate" or "ISO 27001 Consultant"
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(1500)
    page.click('.quiz__step[data-step="1"] .quiz__opt:nth-child(4)')
    page.wait_for_timeout(400)
    page.click('.quiz__step[data-step="2"] .quiz__opt:nth-child(4)')
    page.wait_for_timeout(400)
    page.click('.quiz__step[data-step="3"] .quiz__opt:nth-child(3)')
    page.wait_for_timeout(400)
    page.click('.quiz__step[data-step="4"] .quiz__opt:nth-child(3)')
    page.wait_for_timeout(400)
    page.click('.quiz__step[data-step="5"] .quiz__opt:nth-child(2)')
    page.wait_for_timeout(600)
    body = page.inner_text('#resultWrap')
    no_adv = "advocate" not in body.lower()
    no_cons = "iso 27001 consultant" not in body.lower()
    print(f"[{'PASS' if no_adv and no_cons else 'FAIL'}] T9: No 'Advocate' or 'ISO 27001 Consultant'")

    # T10: Region wording for all 4 options
    for i, expected in enumerate(["the US market", "the UK market", "the Indian market", "remote & global roles"]):
        page.goto("file:///F:/OmnyraGroup/Website/index.html")
        page.wait_for_timeout(1500)
        page.click('.quiz__step[data-step="1"] .quiz__opt:nth-child(1)')
        page.wait_for_timeout(400)
        page.click('.quiz__step[data-step="2"] .quiz__opt:nth-child(3)')
        page.wait_for_timeout(400)
        page.click('.quiz__step[data-step="3"] .quiz__opt:nth-child(3)')
        page.wait_for_timeout(400)
        page.click('.quiz__step[data-step="4"] .quiz__opt:nth-child(3)')
        page.wait_for_timeout(400)
        page.click(f'.quiz__step[data-step="5"] .quiz__opt:nth-child({i+1})')
        page.wait_for_timeout(600)
        text = page.inner_text('#resultCareer')
        ok = expected.lower() in text.lower()
        print(f"[{'PASS' if ok else 'FAIL'}] T10: Region '{expected}' -> '{text}'")

    browser.close()
