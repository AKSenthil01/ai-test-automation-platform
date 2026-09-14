class GenerationParser:

    @staticmethod
    def parse(response):

        if not response:
            return ""

        response = response.replace("\r", "")

        if "```python" in response:
            response = response.split("```python", 1)[1]

        if "```" in response:
            response = response.split("```", 1)[0]

        lines = response.split("\n")

        start = None

        for i, line in enumerate(lines):

            s = line.strip()

            if (
                    s.startswith("import ")
                    or s.startswith("from ")
            ):
                start = i
                break

        if start is None:
            return response.strip()

        code = "\n".join(lines[start:]).strip()

        return code