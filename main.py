
from ai_engine import generate_test_steps
from browser_engine import execute_test
import json


instruction = input("\nEnter your test case: ")

try:

    test_plan = generate_test_steps(instruction)

    print("\n========== AI GENERATED TEST PLAN ==========")
    print(json.dumps(test_plan, indent=4))

    print("\n========== BROWSER AUTOMATION ==========")

    results = execute_test(test_plan)

    print("\n========== FINAL TEST REPORT ==========")

    passed = 0
    failed = 0

    for result in results:

        print(f"{result['status']} - {result['step']}")

        if result["status"] == "PASS":
            passed += 1
        else:
            failed += 1

    print("\nTotal:", len(results))
    print("Passed:", passed)
    print("Failed:", failed)

except Exception as error:
    print("\nAUTOMATION ERROR:", error)
