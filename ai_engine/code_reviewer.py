from langchain_ollama import OllamaLLM

from ai_engine.base_llm import BaseLLM

print("Loaded CodeReviewer from:", __file__)


class CodeReviewer:

    def __init__(self):

        self.llm = BaseLLM.get_llm()

    def review(self, requirement, code):

        prompt = f"""
You are a Senior QA Automation Architect reviewing AI-generated pytest code.

Requirement
-----------
{requirement}

Generated Code
--------------
{code}

Review the generated code carefully.

Check ALL of the following:

1. Correct pytest syntax.
2. Proper fixture usage.
3. Uses ONLY valid controller APIs from the knowledge base.
4. No fake APIs.
5. Assertions are meaningful.
6. No duplicate code.
7. Good readability.
8. Missing validation steps.
9. Missing cleanup.
10. Missing waits if required.

Return ONLY JSON.

Example PASS:

{{
    "status": "PASS",
    "comments": []
}}

Example FAIL:

{{
    "status": "FAIL",
    "comments": [
        "Missing assertion.",
        "Uses fake_function().",
        "verify_alarm() should be called."
    ]
}}
"""

        print("=" * 80)
        print("Sending review prompt to Llama3...")
        print("=" * 80)

        response = self.llm.invoke(prompt)

        print("=" * 80)
        print("Reviewer Response")
        print("=" * 80)
        print(response)

        return response