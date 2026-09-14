class CodePrompt:

    @staticmethod
    def build(requirement, docs):

        context = ""

        for doc in docs:

            context += f"""

================================================

Source:
{doc.metadata.get("source", "")}

Module:
{doc.metadata.get("module", "")}

Test Case:
{doc.metadata.get("testcase", "")}

Knowledge:
{doc.page_content}

================================================
"""

        return f"""
You are a Senior Python SDET with expertise in HVAC Embedded Automation.

Generate executable pytest code.

Requirement
==========================

{requirement}

Retrieved Knowledge
==========================

{context}

Rules

1. Generate ONLY executable Python code.
2. Use pytest.
3. Use ONLY APIs present in the retrieved knowledge.
4. Do NOT invent controller APIs.
5. Use pytest fixtures when available.
6. Add meaningful assertions.
7. Add comments.
8. Follow Python best practices.
9. Do NOT explain the code.
10. Return ONLY Python code.
"""