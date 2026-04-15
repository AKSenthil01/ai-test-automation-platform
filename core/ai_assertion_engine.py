class AIAssertionEngine:

    def validate(self, expected, actual):

        expected = str(expected).lower()
        actual = str(actual).lower()

        keywords = expected.split()

        match_count = sum(1 for k in keywords if k in actual)

        return match_count >= max(1, len(keywords) // 3)