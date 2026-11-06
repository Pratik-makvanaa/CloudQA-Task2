
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=API_KEY)


def generate_test_steps(user_instruction):

    prompt = f"""
You are an expert web testing planner.

Convert the user's instruction into a JSON browser test plan.

Return valid JSON only. No markdown.

Allowed actions:
1. navigate
2. fill_by_label
3. verify_value_by_label
4. click_by_role
5. verify_text

Rules:
- For fill_by_label, use the exact visible form label.
- For verify_value_by_label, use the exact visible form label.
- Never invent CSS selectors, IDs, or HTML attributes.
- Do not submit forms unless explicitly requested.
- Do not solve CAPTCHAs or bypass security checks.
- Do not invent values not provided by the user.
- Include only actions needed by the instruction.

JSON format:
{{
  "test_name": "Test name",
  "steps": [
    {{
      "action": "navigate",
      "description": "Open website",
      "label": "",
      "value": "https://example.com"
    }},
    {{
      "action": "fill_by_label",
      "description": "Enter first name",
      "label": "First name",
      "value": "Pratik"
    }},
    {{
      "action": "verify_value_by_label",
      "description": "Verify first name",
      "label": "First name",
      "value": "Pratik"
    }},
    {{
    "action": "click_by_role",
    "description": "Click login button",
    "label": "Login",
    "value": ""
    }},
    {{
    "action": "verify_text",
    "description": "Verify products page",
    "label": "",
    "value": "Products"
    }}
    
  ]
}}

User instruction:
{user_instruction}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    result = response.text.strip()

    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0].strip()

    try:
        plan = json.loads(result)

        if not isinstance(plan.get("steps"), list):
            raise ValueError("Invalid test plan: steps must be a list")

        return plan

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"Invalid AI test plan: {error}\n{result}")
