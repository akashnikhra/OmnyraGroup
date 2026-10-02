from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(2000)

    # Scroll to program tabs
    page.evaluate('document.querySelector(".program-tabs-nav").scrollIntoView({block: "center"})')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/program-icons-dark.png")

    # Light theme
    page.evaluate('document.documentElement.setAttribute("data-theme", "light")')
    page.wait_for_timeout(500)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/program-icons-light.png")

    browser.close()
