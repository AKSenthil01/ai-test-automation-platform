from ai_engine.api_selector import APISelector
from ai_engine.example_selector import ExampleSelector
from ai_engine.assertion_selector import AssertionSelector
from ai_engine.fixture_selector import FixtureSelector


class CodePromptBuilder:

    @staticmethod
    def build(requirement, docs):

        apis = APISelector().select(requirement)

        examples = ExampleSelector().select(requirement)

        assertions = AssertionSelector().select(requirement)

        fixtures = FixtureSelector().select(requirement)

        api_text = "\n".join(
            f"- {api}"
            for api in apis
        )

        example_text = "\n\n".join(
            examples
        )

        assertion_text = "\n\n".join(
            assertions
        )

        fixture_text = "\n\n".join(
            fixtures
        )

        retrieved = "\n\n".join(docs)

        prompt = f"""
You are a Principal QA Automation Architect.

Generate production-quality pytest automation code.

========================================================

Requirement

{requirement}

========================================================

Allowed Controller APIs

{api_text}

========================================================

Relevant Pytest Examples

{example_text}

========================================================

Relevant Assertions

{assertion_text}

========================================================

Relevant Fixtures

{fixture_text}

========================================================

Retrieved Knowledge

{retrieved}

========================================================

Rules

1. Use ONLY listed APIs.

2. Never invent APIs.

3. Never invent modules.

4. Never create wrapper classes.

5. Never write placeholder functions.

6. Use pytest fixtures.

7. Use meaningful assertions.

8. Add cleanup.

9. Add comments.

10. Return ONLY executable Python code.

11. Output starts with

import

or

from

Nothing else.
"""

        return prompt