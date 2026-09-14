from ai_engine.root_cause_classifier import RootCauseClassifier

classifier = RootCauseClassifier()

failures = [

    {
        "error": "TimeoutError"
    },

    {
        "error": "AssertionError"
    }

]

print(
    classifier.classify(failures)
)