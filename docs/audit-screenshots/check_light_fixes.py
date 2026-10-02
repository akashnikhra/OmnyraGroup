from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(2000)

    # Switch to light theme
    page.evaluate('document.documentElement.setAttribute("data-theme", "light")')
    page.wait_for_timeout(1500)

    # Plans section (for team banner + framework pills)
    page.evaluate('window.scrollTo(0, 3800)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-fix-plans.png")

    # Contact section (for general queries + pills)
    page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight - 900)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-fix-contact.png")

    # Corporate section (for "Or WhatsApp Us")
    page.evaluate('window.scrollTo(0, 4500)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-fix-corp.png")

    # Hero (for Explore pill)
    page.evaluate('window.scrollTo(0, 0)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-fix-hero.png")

    browser.close()
