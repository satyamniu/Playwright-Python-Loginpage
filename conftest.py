import os

import pytest
from playwright.sync_api import Page


@pytest.fixture
def otp_url() -> str:
    return os.getenv(
        "TEACHABLE_OTP_URL",
        "https://sso.teachable.com/secure/9521/identity/login/otp",
    )


@pytest.fixture
def test_email() -> str:
    return os.getenv("TEACHABLE_TEST_EMAIL", "")


@pytest.fixture
def otp_enabled() -> bool:
    return os.getenv("TEACHABLE_OTP_ENABLED", "false").lower() == "true"


@pytest.fixture(autouse=True)
def configure_page(page: Page) -> None:
    page.set_default_timeout(10_000)
