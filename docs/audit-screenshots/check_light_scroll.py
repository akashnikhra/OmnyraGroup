from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_timeout(1000)
    # Switch to light theme
    page.evaluate('document.documentElement.setAttribute("data-theme", "light")')
    page.wait_for_timeout(500)
    # Check computed styles
    styles = page.evaluate("""() => {
        const el = document.querySelector(".scroll-indicator");
        const cs = getComputedStyle(el);
        return {
            color: cs.color,
            background: cs.background,
            border: cs.border,
            animation: cs.animation,
            animationName: cs.animationName,
            opacity: cs.opacity
        };
    }""")
    print("Light theme computed styles:", styles)
    # Take screenshot
    page.screenshot(path="F:/OmnyraGroup/docs/audit-screenshots/light-scroll-analysis.png")
    browser.close()
