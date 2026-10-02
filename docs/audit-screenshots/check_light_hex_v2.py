from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(2000)

    # Switch to light theme
    page.evaluate('document.documentElement.setAttribute("data-theme", "light")')
    page.wait_for_timeout(1500)

    # Screenshot 1: Hero
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-v2-hero.png")

    # Screenshot 2: About
    page.evaluate('window.scrollTo(0, 900)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-v2-about.png")

    # Screenshot 3: Programs
    page.evaluate('window.scrollTo(0, 2000)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-v2-programs.png")

    # Screenshot 4: Plans
    page.evaluate('window.scrollTo(0, 3800)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-v2-plans.png")

    browser.close()
