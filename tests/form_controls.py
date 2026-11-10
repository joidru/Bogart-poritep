from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:4173"
RED = "rgb(201, 70, 77)"
GREEN = "rgb(104, 157, 32)"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    for width, height, label in [(1440, 1000, "desktop"), (390, 844, "mobile")]:
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"{BASE}/contacts.html", wait_until="networkidle")

        name = page.locator('.lead-form input[required]').first
        select = page.locator('.lead-form select').first
        textarea = page.locator('.lead-form textarea')

        assert name.evaluate("el => getComputedStyle(el).borderTopColor") == "rgb(207, 216, 201)"
        assert round(name.bounding_box()["height"]) == 50
        assert round(select.bounding_box()["height"]) == 50
        assert textarea.bounding_box()["height"] >= 140

        page.locator('.lead-form button[type="submit"]').click()
        page.wait_for_timeout(250)
        assert name.evaluate("el => getComputedStyle(el).borderTopColor") == RED
        assert page.locator('.lead-form').evaluate("form => form.classList.contains('was-validated')")

        name.fill("Александр")
        name.focus()
        page.wait_for_timeout(250)
        focus_color = name.evaluate("el => getComputedStyle(el).borderTopColor")
        assert focus_color == GREEN, focus_color

        if label == "desktop":
            page.screenshot(path="/tmp/poritep-controls-desktop.png", full_page=True)
        else:
            page.screenshot(path="/tmp/poritep-controls-mobile.png", full_page=True)

        page.evaluate("""() => {
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.id = 'test-radio';
            document.body.append(radio);
            const validationForm = document.createElement('form');
            validationForm.className = 'was-validated';
            const requiredArea = document.createElement('textarea');
            requiredArea.required = true;
            requiredArea.id = 'test-required-area';
            validationForm.append(requiredArea);
            document.body.append(validationForm);
        }""")
        radio = page.locator('#test-radio')
        assert round(radio.bounding_box()["width"]) == 20
        radio.check()
        page.wait_for_timeout(200)
        assert radio.evaluate("el => getComputedStyle(el).backgroundColor") == GREEN
        assert page.locator('#test-required-area').evaluate("el => getComputedStyle(el).borderTopColor") == RED

        page.close()

    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto(f"{BASE}/catalog.html", wait_until="networkidle")
    checkbox = page.locator('.filter-option input[type="checkbox"]').first
    assert round(checkbox.bounding_box()["width"]) == 20
    checkbox.check()
    page.wait_for_timeout(300)
    checkbox_color = checkbox.evaluate("el => getComputedStyle(el).backgroundColor")
    assert checkbox_color == GREEN, checkbox_color

    page.goto(f"{BASE}/calculator.html", wait_until="networkidle")
    assert round(page.locator('.calculator-fields input').first.bounding_box()["height"]) == 50
    assert round(page.locator('.calculator-fields select').first.bounding_box()["height"]) == 50

    browser.close()
    print("PASS: unified input, select, textarea, checkbox and radio states")
