import re


class APIExtractor:

    @staticmethod
    def extract():

        path = "knowledge/Controller_API.md"

        with open(path, encoding="utf8") as f:
            text = f.read()

        # Extract every API name after "Name:"
        matches = re.findall(
            r"Name:\s*\n([a-zA-Z_][a-zA-Z0-9_]*)",
            text
        )

        return sorted(set(matches))