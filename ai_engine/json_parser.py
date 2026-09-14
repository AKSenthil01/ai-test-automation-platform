import json
import re


class JSONParser:

    @staticmethod
    def parse(response):

        match = re.search(r"\{.*\}", response, re.DOTALL)

        if not match:
            raise ValueError("No JSON found")

        return json.loads(match.group())