from pathlib import Path
from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:4173"
SCREENSHOT = Path("/tmp/poritep-studio-home.png")
DELIVERY_SCREENSHOT = Path("/tmp/poritep-delivery.png")
OBJECTS_SCREENSHOT = Path("/tmp/poritep-objects.png")


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
    assert page.locator(".objects-showcase img").count() == 3
    assert page.locator(".faq-list details").count() == 5
    second_faq = page.locator(".faq-list details").nth(1)
    second_faq.locator("summary").click()
    assert second_faq.get_attribute("open") is not None
    page.screenshot(path=str(SCREENSHOT), full_page=True)

    page.goto(f"{BASE}/delivery.html", wait_until="networkidle")
    assert page.locator(".delivery-steps article").count() == 4
    assert "Богородск" in page.locator(".route-origin").inner_text()
    assert page.locator('.nav-row a.active[href="delivery.html"]').is_visible()
    page.screenshot(path=str(DELIVERY_SCREENSHOT), full_page=True)

    page.goto(f"{BASE}/objects.html", wait_until="networkidle")
    assert page.locator(".object-project").count() == 4
    assert page.locator(".object-project img").count() == 4
    assert page.locator('.nav-row a.active[href="objects.html"]').is_visible()
    page.screenshot(path=str(OBJECTS_SCREENSHOT), full_page=True)

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

    print(f"PASS: home, FAQ, delivery, objects, search, catalog, product and cart; screenshot={SCREENSHOT}")
    browser.close()
