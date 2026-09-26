class RootCauseClassifier:

    RULES = {

        "AssertionError": "Business Logic",

        "TimeoutError": "Synchronization",

        "NoSuchElementException": "Locator",

        "ConnectionRefusedError": "Communication",

        "SyntaxError": "AI Code Generation",

        "ImportError": "Dependency",

        "AttributeError": "Programming",

        "TypeError": "Programming",

        "KeyError": "Programming",

        "ValueError": "Programming"
    }

    def classify(self, failures):

        for failure in failures:

            error = failure.get("error", "")

            failure["root_cause"] = self.RULES.get(
                error,
                "Unknown"
            )

        return failures