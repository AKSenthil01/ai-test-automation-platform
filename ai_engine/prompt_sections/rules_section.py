class RulesSection:

    @staticmethod
    def build():

        return """
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

11. Output MUST start with

import

or

from

Nothing else.
"""