import json
import re


class TestCaseParser:

    @staticmethod
    def parse(response):

        # Remove markdown fences if present
        response = response.replace("```json", "").replace("```", "")

        # Try JSON array first
        match = re.search(r"\[.*\]", response, re.DOTALL)

        if match:
            return json.loads(match.group())

        # Try single JSON object
        match = re.search(r"\{.*\}", response, re.DOTALL)

        if match:
            return [json.loads(match.group())]

        raise Exception("No valid JSON found.")