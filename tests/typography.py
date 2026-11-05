from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:4173"
PAGES = [
    "index.html",
    "catalog.html",
    "product.html?id=d400-200",
    "cart.html",
    "delivery.html",
    "objects.html",
    "about.html",
    "contacts.html",
]


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for width, height, label in [(1440, 1000, "desktop"), (390, 844, "mobile")]:
        page = browser.new_page(viewport={"width": width, "height": height})
        for path in PAGES:
            page.goto(f"{BASE}/{path}", wait_until="networkidle")
            body_font = page.locator("body").evaluate("el => getComputedStyle(el).fontFamily")
            assert "Golos Text" in body_font and "Unbounded" not in body_font, f"{label} {path}: {body_font}"
            heading = page.locator("h1, h2, h3").first
            if heading.count():
                heading_font = heading.evaluate("el => getComputedStyle(el).fontFamily")
                assert "Golos Text" in heading_font and "Unbounded" not in heading_font, f"{label} {path}: {heading_font}"
            undersized = page.evaluate(
                """() => [...document.querySelectorAll('body *')]
                    .filter(el => {
                        const style = getComputedStyle(el);
                        return style.display !== 'none' && style.visibility !== 'hidden' &&
                            parseFloat(style.fontSize) < 12;
                    })
                    .map(el => ({tag: el.tagName, cls: el.className, size: getComputedStyle(el).fontSize}))"""
            )
            assert not undersized, f"{label} {path}: {undersized[:10]}"

        page.goto(f"{BASE}/catalog.html", wait_until="networkidle")
        if label == "desktop":
            assert page.locator(".filter-option").first.evaluate("el => getComputedStyle(el).fontSize") == "14px"
            assert page.locator("#sort").evaluate("el => getComputedStyle(el).fontSize") == "14px"
            page.screenshot(path="/tmp/poritep-golos-desktop.png", full_page=True)
        else:
            page.goto(f"{BASE}/product.html?id=d400-200", wait_until="networkidle")
            assert page.locator(".spec-mini").first.evaluate("el => getComputedStyle(el).fontSize") == "12px"
            assert page.locator(".product-note").evaluate("el => getComputedStyle(el).fontSize") == "12px"
            page.screenshot(path="/tmp/poritep-golos-mobile.png", full_page=True)
        page.close()

    print("PASS: Golos Text is the only site typeface; no visible text below 12px")
    browser.close()
