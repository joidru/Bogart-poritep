from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:4173"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in [(1440, 1000), (1024, 900), (390, 844)]:
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"{BASE}/index.html", wait_until="networkidle")
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        if width > 1000:
            container_x = page.locator(".hero-inner").bounding_box()["x"]
            content_x = page.locator(".hero-content").bounding_box()["x"]
            assert abs(container_x - content_x) < 1, (width, container_x, content_x)
            for line in page.locator(".hero-title-line").all():
                metrics = line.evaluate("el => ({height:el.getBoundingClientRect().height,line:parseFloat(getComputedStyle(el).lineHeight)})")
                assert metrics["height"] <= metrics["line"] * 1.15, (width, metrics)
        if width == 1440:
            page.screenshot(path="/tmp/poritep-hero-fixed.png", full_page=False)
        page.close()

    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(f"{BASE}/calculator.html", wait_until="networkidle")
    initial = page.locator("#resultVolume").inner_text()
    page.locator('[name="length"]').fill("12")
    page.locator('[name="length"]').press("Tab")
    changed = page.locator("#resultVolume").inner_text()
    assert not errors, errors
    assert initial != "—" and changed != initial, (initial, changed)
    assert page.locator("#resultPrice").inner_text().endswith("₽")
    page.screenshot(path="/tmp/poritep-calculator.png", full_page=True)

    page.goto(f"{BASE}/contacts.html", wait_until="networkidle")
    body = page.locator("body").inner_text()
    for value in ["+7 (831) 262-12-80", "89200200370@bogart.su", "Почаинская, 35", "Пн–Пт, 9:00–18:00"]:
        assert value in body, value
    browser.close()
    print("PASS: hero grid, calculator and contact details")
