import re


class CodeCleaner:

    @staticmethod
    def clean(response):

        response = re.sub(r"```python", "", response)
        response = re.sub(r"```", "", response)

        return response.strip()