class ScenarioPlanner:

    DEFAULT_SCENARIOS = [

        "Positive",
        "Negative",
        "Boundary",
        "Recovery",
        "Communication Failure",
        "Performance",
        "Stress",
        "Safety",
        "Configuration",
        "Protocol Failure"

    ]

    @classmethod
    def get_scenarios(cls, count):

        return cls.DEFAULT_SCENARIOS[:count]