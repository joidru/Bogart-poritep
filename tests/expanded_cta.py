from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:4173"
PAGES = ["delivery.html", "objects.html", "about.html"]


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for width, height, label in [(1440, 1000, "desktop"), (390, 844, "mobile")]:
        page = browser.new_page(viewport={"width": width, "height": height})
        for path in PAGES:
            page.goto(f"{BASE}/{path}", wait_until="networkidle")
            banner = page.locator(".calc-banner-detailed")
            assert banner.count() == 1, (label, path)
            assert banner.locator(".calc-copy").is_visible()
            assert banner.locator(".calc-ticket").is_visible()
            assert banner.locator(".calc-ticket li").count() == 3
            assert banner.locator(".calc-ticket-btn").is_visible()
            assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), (label, path)
        page.close()
    browser.close()
    print("PASS: expanded CTA blocks on delivery, objects and about")
