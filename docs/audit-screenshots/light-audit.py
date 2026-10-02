from playwright.sync_api import sync_playwright
import os

SCREENSHOT_DIR = "F:/OmnyraGroup/docs/audit-screenshots/light-issues"
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
    page.evaluate("window.scrollTo(0, 300)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-scroll-300.png")
    
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-scroll-800.png")
    
    page.evaluate("window.scrollTo(0, 1500)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-scroll-1500.png")
    
    page.evaluate("window.scrollTo(0, 2500)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-scroll-2500.png")
    
    # Programs section
    page.evaluate("document.getElementById('programs')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-programs.png")
    
    # Plans section
    page.evaluate("document.getElementById('plans')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-plans.png")
    
    # Contact section
    page.evaluate("document.getElementById('contact')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-contact.png")
    
    # Full page
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SCREENSHOT_DIR}/light-full.png", full_page=True)
    
    browser.close()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")
