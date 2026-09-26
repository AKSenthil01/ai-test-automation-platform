import json


class ReviewParser:

    @staticmethod
    def parse(response):

        try:

            start = response.index("{")

            end = response.rindex("}") + 1

            return json.loads(response[start:end])

        except Exception as e:

            return {
                "status": "FAIL",
                "comments": [
                    f"Unable to parse reviewer output: {e}"
                ]
            }