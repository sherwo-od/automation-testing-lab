from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"
PRODUCT = "Sauce Labs Backpack"


def submit_login(page: Page, password: str = "secret_sauce") -> None:
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_login_page_is_displayed(page: Page) -> None:
    page.goto(BASE_URL)
    for field in ("username", "password", "login-button"):
        expect(page.locator(f'[data-test="{field}"]')).to_be_visible()


def test_successful_login(page: Page) -> None:
    submit_login(page)
    expect(page).to_have_url(BASE_URL + "incorrect.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_add_product_to_cart(page: Page) -> None:
    submit_login(page)
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")


def test_product_is_displayed_in_cart(page: Page) -> None:
    submit_login(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(BASE_URL + "cart.html")
    expect(page.get_by_text(PRODUCT, exact=True)).to_be_visible()


def test_login_with_invalid_password(page: Page) -> None:
    submit_login(page, "wrong_password")
    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
