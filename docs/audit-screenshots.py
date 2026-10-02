from playwright.sync_api import sync_playwright
import os

SCREENSHOT_DIR = "F:/OmnyraGroup/docs/audit-screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # Desktop screenshots
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///F:/OmnyraGroup/Website/index.html")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Full page screenshot
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-full.png", full_page=True)
    
    # Hero section
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-hero.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    
    # Scroll to programs section
    page.evaluate("document.getElementById('programs')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-programs.png")
    
    # Scroll to pricing section
    page.evaluate("document.getElementById('plans')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-pricing.png")
    
    # Scroll to contact section
    page.evaluate("document.getElementById('contact')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-contact.png")
    
    # Mobile screenshots
    mobile_page = browser.new_page(viewport={"width": 375, "height": 812})
    mobile_page.goto("file:///F:/OmnyraGroup/Website/index.html")
    mobile_page.wait_for_load_state("networkidle")
    mobile_page.wait_for_timeout(2000)
    
    mobile_page.screenshot(path=f"{SCREENSHOT_DIR}/mobile-full.png", full_page=True)
    mobile_page.screenshot(path=f"{SCREENSHOT_DIR}/mobile-hero.png", clip={"x": 0, "y": 0, "width": 375, "height": 812})
    
    # Scroll to programs on mobile
    mobile_page.evaluate("document.getElementById('programs')?.scrollIntoView({behavior:'instant'})")
    mobile_page.wait_for_timeout(500)
    mobile_page.screenshot(path=f"{SCREENSHOT_DIR}/mobile-programs.png")
    
    # Scroll to pricing on mobile
    mobile_page.evaluate("document.getElementById('plans')?.scrollIntoView({behavior:'instant'})")
    mobile_page.wait_for_timeout(500)
    mobile_page.screenshot(path=f"{SCREENSHOT_DIR}/mobile-pricing.png")
    
    # Test interactive elements
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    
    # Click dark/light theme toggle if exists
    try:
        toggle = page.locator('[data-theme-toggle], .theme-toggle, #themeToggle').first
        if toggle.is_visible():
            toggle.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-light-mode.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
            toggle.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    # Test quiz interaction
    page.evaluate("document.getElementById('matrixCard')?.scrollIntoView({behavior:'instant'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{SCREENSHOT_DIR}/desktop-quiz.png")
    
    browser.close()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")
