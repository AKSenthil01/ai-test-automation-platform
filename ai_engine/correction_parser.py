import re


class CorrectionParser:

    @staticmethod
    def parse(response):

        if response is None:
            return ""

        response = response.strip()

        # -----------------------------
        # Markdown code block
        # -----------------------------
        match = re.search(
            r"```(?:python)?\s*(.*?)```",
            response,
            re.DOTALL
        )

        if match:
            return match.group(1).strip()

        # -----------------------------
        # Starts directly with Python
        # -----------------------------
        for keyword in (
            "import ",
            "from ",
            "def ",
            "@pytest",
            "class "
        ):

            idx = response.find(keyword)

            if idx != -1:
                return response[idx:].strip()

        # -----------------------------
        # "Here is the corrected script"
        # -----------------------------
        match = re.search(
            r"corrected script[:\s]*",
            response,
            re.IGNORECASE
        )

        if match:

            remaining = response[match.end():].strip()

            for keyword in (
                "import ",
                "from ",
                "def ",
                "@pytest",
                "class "
            ):

                idx = remaining.find(keyword)

                if idx != -1:
                    return remaining[idx:].strip()

        return response