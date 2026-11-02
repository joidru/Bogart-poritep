from pathlib import Path
from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:4173"
SCREENSHOT = Path("/tmp/poritep-studio-home.png")


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})

    page.goto(f"{BASE}/index.html", wait_until="networkidle")
    page.evaluate("localStorage.clear()")
    page.reload(wait_until="networkidle")
    page.locator(".hero-content h1").wait_for(state="visible")
    assert page.locator(".search button svg").is_visible()
    page.locator("#searchInput").fill("D400")
    page.locator("#searchResults.open").wait_for(state="visible")
    assert page.locator("#searchResults .search-result").count() >= 2
    assert "D400" in page.locator("#searchResults .search-result").first.inner_text()
    page.locator("#searchInput").fill("")
    page.locator("#searchResults").wait_for(state="hidden")
    page.screenshot(path=str(SCREENSHOT), full_page=True)

    page.goto(f"{BASE}/catalog.html", wait_until="networkidle")
    assert page.locator("#catalogProducts .product-card").count() >= 8
    page.locator("#catalogProducts .product-card .product-image").first.click()
    page.wait_for_load_state("networkidle")
    assert "product.html?id=" in page.url
    page.locator("#detailAdd").click()
    assert page.locator(".cart-count").inner_text() == "1"

    page.goto(f"{BASE}/cart.html", wait_until="networkidle")
    assert page.locator(".cart-item").count() == 1
    assert page.locator(".cart-summary").is_visible()

    print(f"PASS: search, catalog, product and cart; screenshot={SCREENSHOT}")
    browser.close()
