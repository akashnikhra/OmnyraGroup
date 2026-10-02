from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(2000)

    # Switch to light theme
    page.evaluate('document.documentElement.setAttribute("data-theme", "light")')
    page.wait_for_timeout(1500)

    # Screenshot 1: Hero (top)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-hero.png")

    # Screenshot 2: Scroll to About
    page.evaluate('window.scrollTo(0, 800)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-about.png")

    # Screenshot 3: Scroll to Programs
    page.evaluate('window.scrollTo(0, 1800)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-programs.png")

    # Screenshot 4: Scroll to Plans
    page.evaluate('window.scrollTo(0, 3500)')
    page.wait_for_timeout(1000)
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-hex-plans.png")

    # Check canvas visibility
    canvas_opacity = page.evaluate('''() => {
        const canvas = document.querySelector("#canvas-container");
        return getComputedStyle(canvas).opacity;
    }''')
    print(f"Canvas opacity in light theme: {canvas_opacity}")

    browser.close()
