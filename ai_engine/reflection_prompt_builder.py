class ReflectionPromptBuilder:

    @staticmethod
    def build(

            requirement,

            code,

            review

    ):

        comments = "\n".join(

            "- " + c

            for c in review["comments"]

        )

        return f"""
Requirement

{requirement}

Generated pytest

```python
{code}
    """