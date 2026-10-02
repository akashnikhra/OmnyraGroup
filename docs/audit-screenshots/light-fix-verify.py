from playwright.sync_api import sync_playwright
import os

SCREENSHOT_DIR = "F:/OmnyraGroup/docs/audit-screenshots/light-fixes"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # Desktop - Light mode
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Toggle to light mode
    toggle = page.locator('.theme-toggle-btn').first
    toggle.click()
    page.wait_for_timeout(500)
    
    # Hero
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-hero.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    
    # Scroll through sections
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-about.png")
    
    page.evaluate("window.scrollTo(0, 1600)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-programs.png")
    
    page.evaluate("window.scrollTo(0, 3000)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-plans.png")
    
    page.evaluate("window.scrollTo(0, 4500)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-contact.png")
    
    # Full page
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-full.png", full_page=True)
    
    browser.close()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")
