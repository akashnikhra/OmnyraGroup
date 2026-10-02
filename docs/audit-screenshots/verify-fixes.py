from playwright.sync_api import sync_playwright
import os

SCREENSHOT_DIR = "F:/OmnyraGroup/docs/audit-screenshots/fixes"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # Desktop screenshots
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Dark mode hero
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-hero-dark.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    
    # Toggle to light mode
    try:
        toggle = page.locator('.theme-toggle-btn').first
        if toggle.is_visible():
            toggle.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-hero-light.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
            toggle.click()
            page.wait_for_timeout(500)
    except Exception as e:
        print(f"Theme toggle error: {e}")
    
    # Programs section
    page.evaluate("document.getElementById('programs')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-programs.png")
    
    # Toggle to light mode for programs
    try:
        toggle = page.locator('.theme-toggle-btn').first
        if toggle.is_visible():
            toggle.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-programs-light.png")
            toggle.click()
            page.wait_for_timeout(500)
    except Exception as e:
        print(f"Theme toggle error: {e}")
    
    # Pricing section
    page.evaluate("document.getElementById('plans')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-pricing.png")
    
    # Mobile screenshots
    mobile_page = browser.new_page(viewport={"width": 375, "height": 812})
    mobile_page.goto("file:///F:/OmnyraGroup/Website/index.html")
    mobile_page.wait_for_load_state("networkidle")
    mobile_page.wait_for_timeout(2000)
    
    mobile_page.screenshot(path=f"{SCREENSHOT_DIR}/mobile-hero.png", clip={"x": 0, "y": 0, "width": 375, "height": 812})
    
    browser.close()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")
