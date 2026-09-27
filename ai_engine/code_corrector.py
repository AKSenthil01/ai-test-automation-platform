from ai_engine.base_llm import BaseLLM
from ai_engine.api_selector import APISelector
from ai_engine.correction_parser import CorrectionParser


class CodeCorrector:
    """
    Uses reviewer feedback to improve generated pytest code.
    """

    def __init__(self):

        self.llm = BaseLLM.get_llm()

        self.selector = APISelector()

    def correct(

            self,

            requirement: str,

            code: str,

            review_comments: list,

            debug: bool = False

    ) -> str:

        selected = self.selector.select(requirement)

        api_list = "\n".join(

            f"- {api}()"

            for api in selected

        )

        if review_comments:

            comments = "\n".join(

                f"- {comment}"

                for comment in review_comments

            )

        else:

            comments = "No reviewer comments."

        prompt = f"""
You are a Principal QA Automation Architect.

Your task is to CORRECT an existing pytest automation script.

Preserve all correct code.

Modify ONLY the issues identified by the reviewer.

==================================================

Requirement

{requirement}

==================================================

Allowed Controller APIs

{api_list}

==================================================

Current Script

{code}

==================================================

Reviewer Comments

{comments}

==================================================

Rules

1. ONLY use the listed APIs.

2. NEVER invent APIs.

3. NEVER invent modules.

4. NEVER write:

from your_module import ...

5. NEVER create wrapper classes.

6. NEVER create helper APIs.

7. NEVER create placeholder functions.

8. NEVER create fake fixtures.

9. Missing functionality becomes TODO comments.

10. Remove invalid APIs.

11. Preserve all correct logic.

12. Use pytest.

13. Use meaningful assertions.

14. Add cleanup.

15. Return ONLY executable Python.

16. Output MUST start with:

import

or

from

17. Never explain.

18. Never use Markdown.

19. Never use triple backticks.

20. Never say:

Here is the corrected script.

21. If an API does not exist:

# TODO: API not available in Controller_API.md
"""

        if debug:

            print("=" * 80)
            print("Sending correction prompt...")
            print("=" * 80)

        response = self.llm.invoke(prompt)

        corrected = CorrectionParser.parse(response)

        if not corrected.strip():

            if debug:

                print("Correction parser returned empty code.")

            return code

        if debug:

            print("=" * 80)
            print("Corrected Code")
            print("=" * 80)
            print(corrected)

        return corrected