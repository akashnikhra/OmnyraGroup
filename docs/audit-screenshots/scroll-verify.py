from playwright.sync_api import sync_playwright
import os

SCREENSHOT_DIR = "F:/OmnyraGroup/docs/audit-screenshots/scroll-fix"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # Desktop - Dark mode
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{SCREENSHOT_DIR}/dark-hero.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    
    # Light mode
    toggle = page.locator('.theme-toggle-btn').first
    toggle.click()
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-hero.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    
    browser.close()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")
