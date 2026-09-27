import re


class QueryPlanner:

    MODULE_KEYWORDS = {

        "BACnet": [
            "bacnet",
            "network",
            "communication",
            "timeout"
        ],

        "Controller": [
            "controller",
            "restart",
            "reboot",
            "startup"
        ],

        "Sensor": [
            "sensor",
            "temperature",
            "thermistor",
            "pressure"
        ],

        "Compressor": [
            "compressor",
            "cooling"
        ],

        "Defrost": [
            "defrost"
        ],

        "A2L Leak": [
            "a2l",
            "leak",
            "refrigerant"
        ],

        "Heat Furnace": [
            "heater",
            "heat",
            "furnace"
        ],

        "Alarm": [
            "alarm",
            "fault",
            "warning"
        ]

    }

    @classmethod
    def extract_modules(cls, text):

        modules = []

        lower = text.lower()

        for module, keywords in cls.MODULE_KEYWORDS.items():

            if any(keyword in lower for keyword in keywords):

                modules.append(module)

        return modules

    @classmethod
    def build_queries(cls, text):

        modules = cls.extract_modules(text)

        return text + " " + " ".join(modules)

    @classmethod
    def build_search_query(cls, text):
        """
        Backward compatibility wrapper.
        Older code calls build_search_query().
        """
        return cls.build_queries(text)