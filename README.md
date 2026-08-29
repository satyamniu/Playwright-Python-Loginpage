# Playwright&Python-Loginpage

Playwright smoke tests for the authorized Teachable passwordless login page.

## Setup

Use Python 3.10 or newer, then create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
```

If `py` and `python` are unavailable, install Python from the official Python distribution and reopen the terminal.

## Run UI smoke tests

These tests load the public login page and do not request an OTP:

```powershell
python -m pytest -m "not otp"
```

The suite runs in the installed Google Chrome channel by default. It captures a screenshot for every test and retains traces when a test fails. Artifacts are written under `test-results`. The browser can be made visible with `--headed`, and the browser channel can be overridden with `--browser chromium`.

## Live OTP test

The live test is intentionally not runnable until an approved inbox adapter is implemented. Before enabling it:

- Use written authorization and a dedicated non-production test account.
- Configure `TEACHABLE_TEST_EMAIL` through the environment, never in source control.
- Set `TEACHABLE_OTP_ENABLED=true` only for a controlled run.
- Implement retrieval from an approved test inbox or provider sandbox.
- Do not bypass CAPTCHA, anti-bot controls, rate limits, or resend cooldowns.
- Never log OTP values or include them in screenshots/traces.

Run the opt-in test only after those prerequisites are complete:

```powershell
$env:TEACHABLE_OTP_ENABLED = "true"
$env:TEACHABLE_TEST_EMAIL = "your-dedicated-test-address"
python -m pytest -m otp --browser chromium
```

The current test fails with a configuration message when the feature is enabled without an inbox adapter. This prevents a false sense of end-to-end coverage.

## Artifacts and cleanup

Playwright screenshots, videos, and traces should be reviewed for secret leakage before sharing and kept outside version control. Use a fresh browser context per test and clean up the dedicated test account according to the account owner’s recovery policy.
