from playwright.sync_api import sync_playwright


ALLOWED_ACTIONS = {
    "navigate",
    "fill_by_label",
    "verify_value_by_label",
    "click_by_role",
    "verify_text"
}


def find_field(page, label):

    # Strategy 1: Accessible label
    try:
        locator = page.get_by_label(label, exact=True)

        if locator.count() == 1:
            return locator

    except Exception:
        pass

    # Strategy 2: Placeholder
    try:
        locator = page.get_by_placeholder(
            label,
            exact=True
        )

        if locator.count() == 1:
            return locator

    except Exception:
        pass

    # Strategy 3: Nearby form field
    try:
        locator = page.locator(
            "label"
        ).filter(has_text=label)

        if locator.count() == 1:
            field = locator.locator("input, textarea, select")

            if field.count() == 1:
                return field

    except Exception:
        pass

    raise Exception(
        f"Could not uniquely identify field: {label}"
    )


def execute_test(test_plan):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:

            for step in test_plan["steps"]:

                action = step.get("action")
                description = step.get("description", action)
                label = step.get("label", "")
                value = step.get("value", "")

                try:

                    if action not in ALLOWED_ACTIONS:
                        raise ValueError(
                            f"Unsupported action: {action}"
                        )

                    if action == "navigate":

                        if not value.startswith(
                            ("https://", "http://")
                        ):
                            raise ValueError("Invalid URL")

                        page.goto(
                            value,
                            wait_until="domcontentloaded",
                            timeout=30000
                        )

                    elif action == "fill_by_label":

                        field = find_field(page, label)

                        field.fill(
                            value,
                            timeout=10000
                        )
                    elif action == "click_by_role":
                        page.get_by_role(
                            "button",
                            name=label,
                            exact=True
                        ).click(timeout=10000)

                    elif action == "verify_text":
                        page.get_by_text(
                            value,
                            exact=True
                        ).wait_for(
                            state="visible",
                            timeout=10000
                        )

                    elif action == "verify_value_by_label":

                        field = find_field(page, label)

                        field.wait_for(
                            state="visible",
                            timeout=10000
                        )

                        actual_value = field.input_value()

                        if actual_value.strip() != value.strip():
                            raise AssertionError(
                                f"Expected '{value}', "
                                f"but found '{actual_value}'"
                            )

                    results.append({
                        "step": description,
                        "status": "PASS"
                    })

                    print(f"PASS: {description}")

                except Exception as error:

                    results.append({
                        "step": description,
                        "status": "FAIL",
                        "error": str(error)
                    })

                    print(f"FAIL: {description}")
                    print(f"Reason: {error}")

                    break

        finally:
            browser.close()

    return results
