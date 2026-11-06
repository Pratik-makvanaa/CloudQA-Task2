# AI-Powered Test Automation Agent

An AI-powered browser testing agent that converts plain-English test instructions into executable browser automation using Google Gemini and Playwright.

## Tech Stack
- Python
- Google Gemini API
- Playwright
- python-dotenv

## Features
- Converts natural-language instructions into JSON test plans.
- Automates browser actions using Playwright.
- Supports navigation, form filling, clicking and text verification.
- Uses label-based locators with fallback strategies.
- Generates PASS/FAIL test reports.

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

4. Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model_name
```

5. Run:

```bash
python main.py
```

## Tested Scenarios
- PHPTravels form automation and field verification.
- SauceDemo successful login.
- SauceDemo invalid login and error verification.

## Limitations
- Locator fallback depends on available labels and page structure.
- Complex custom dropdowns may require specialized handling.
- AI-generated test plans may need correction.
- CAPTCHA and protected authentication flows are not automated.