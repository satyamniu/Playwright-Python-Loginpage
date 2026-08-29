import re

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect


def open_login_page(page: Page, otp_url: str):
    response = page.goto(otp_url, wait_until="domcontentloaded")
    verification = page.get_by_text("Performing security verification")
    try:
        verification.wait_for(state="visible", timeout=5_000)
        pytest.skip("The site is showing Cloudflare security verification.")
    except PlaywrightTimeoutError:
        pass
    return response


class TestOtpLoginPage:
    def test_login_page_loads(self, page: Page, otp_url: str) -> None:
        response = open_login_page(page, otp_url)

        assert response is not None
        assert response.ok
        expect(page).to_have_title(re.compile("log in|login", re.IGNORECASE))
        expect(page.get_by_role("heading", name=re.compile("log in", re.IGNORECASE))).to_be_visible()

    def test_email_login_controls_are_available(self, page: Page, otp_url: str) -> None:
        open_login_page(page, otp_url)

        email = page.get_by_label("Email")
        expect(email).to_be_visible()
        expect(email).to_have_attribute("type", "email")
        expect(page.get_by_role("button", name=re.compile("log in", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("password", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("sign up", re.IGNORECASE))).to_be_visible()

    def test_empty_email_is_rejected(self, page: Page, otp_url: str) -> None:
        open_login_page(page, otp_url)
        page.get_by_role("button", name=re.compile("log in", re.IGNORECASE)).click()

        email = page.get_by_label("Email")
        expect(email).to_have_attribute("required", "")
        expect(email).to_be_invalid()

    def test_malformed_email_is_rejected(self, page: Page, otp_url: str) -> None:
        open_login_page(page, otp_url)
        email = page.get_by_label("Email")
        email.fill("not-an-email")
        page.get_by_role("button", name=re.compile("log in", re.IGNORECASE)).click()

        expect(email).to_be_invalid()

    def test_navigation_links_are_present(self, page: Page, otp_url: str) -> None:
        open_login_page(page, otp_url)

        password_link = page.get_by_role("link", name=re.compile("password", re.IGNORECASE))
        signup_link = page.get_by_role("link", name=re.compile("sign up", re.IGNORECASE))
        expect(password_link).to_have_attribute("href", re.compile("/password"))
        expect(signup_link).to_have_attribute("href", re.compile("/sign_up/otp"))


@pytest.mark.otp
def test_authorized_otp_flow_requires_inbox_adapter(
    page: Page, otp_url: str, test_email: str, otp_enabled: bool
) -> None:
    if not otp_enabled:
        pytest.skip("Set TEACHABLE_OTP_ENABLED=true for an authorized live OTP test.")
    if not test_email:
        pytest.fail("TEACHABLE_TEST_EMAIL must be set for the live OTP test.")

    pytest.fail(
        "OTP inbox integration is not configured. Add an approved inbox adapter before enabling this test."
    )
