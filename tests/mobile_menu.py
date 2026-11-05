from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://127.0.0.1:4173/index.html", wait_until="networkidle")

    menu_button = page.locator(".menu-button")
    menu_icon = page.locator(".menu-button i")
    mobile_nav = page.locator("#mobileNav")
    content = page.locator(".hero-shop")

    assert menu_button.is_visible()
    assert menu_icon.is_visible()
    icon_box = menu_icon.bounding_box()
    assert icon_box and icon_box["width"] >= 20 and icon_box["height"] >= 12
    assert page.evaluate("getComputedStyle(document.querySelector('.menu-button')).color") == "rgb(255, 255, 255)"

    content_y_before = content.bounding_box()["y"]
    menu_button.click()
    assert mobile_nav.is_visible()
    assert menu_button.get_attribute("aria-expanded") == "true"
    assert page.evaluate("getComputedStyle(document.querySelector('#mobileNav')).position") == "absolute"
    content_y_after = content.bounding_box()["y"]
    assert content_y_after == content_y_before

    page.screenshot(path="/tmp/poritep-mobile-menu.png")
    print(f"PASS: mobile icon visible; content shift={content_y_after - content_y_before}px")
    browser.close()
