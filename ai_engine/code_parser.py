import re


class CodeParser:

    @staticmethod
    def parse(text):

        match = re.search(
            r"```python(.*?)```",
            text,
            re.DOTALL
        )

        if match:
            return match.group(1).strip()

        return text.strip()