from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:4173"
GREEN = "rgb(104, 157, 32)"


def verify_quantity(page, selector, screenshot_path):
    quantity = page.locator(selector)
    quantity.scroll_into_view_if_needed()
    assert quantity.evaluate("el => getComputedStyle(el).overflow") == "hidden"
    assert quantity.evaluate("el => getComputedStyle(el).borderTopWidth") == "1px"
    assert quantity.evaluate("el => getComputedStyle(el).borderRightWidth") == "1px"
    assert quantity.evaluate("el => getComputedStyle(el).borderBottomWidth") == "1px"
    assert quantity.evaluate("el => getComputedStyle(el).borderLeftWidth") == "1px"

    field = quantity.locator("input")
    field.focus()
    page.wait_for_timeout(250)
    assert field.evaluate("el => getComputedStyle(el).outlineStyle") == "none"
    focus_color = quantity.evaluate("el => getComputedStyle(el).borderTopColor")
    assert focus_color == GREEN, focus_color
    page.screenshot(path=screenshot_path, full_page=True)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    for width, height, label in [(1440, 1000, "desktop"), (390, 844, "mobile")]:
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"{BASE}/product.html?id=d400-200", wait_until="networkidle")
        verify_quantity(page, ".qty-line .qty", f"/tmp/poritep-qty-product-{label}.png")

        page.evaluate("localStorage.setItem('poritep-cart', JSON.stringify({'d400-200': 2}))")
        page.goto(f"{BASE}/cart.html", wait_until="networkidle")
        verify_quantity(page, ".cart-item .qty", f"/tmp/poritep-qty-cart-{label}.png")
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        page.close()

    browser.close()
    print("PASS: quantity control border and focus on product and cart pages")
