import re

from ai_engine.api_catalog import APICatalog


class APIValidator:

    @staticmethod
    def extract_used_apis(code):

        return re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\(", code)

    @classmethod
    def validate(cls, code):

        allowed = APICatalog.load()

        used = cls.extract_used_apis(code)

        ignore = {
            "assert",
            "print",
            "len",
            "range",
            "int",
            "str",
            "float",
            "list",
            "dict",
            "set",
            "tuple"
        }

        invalid = []

        for api in used:

            if api in ignore:
                continue

            if api.startswith("test_"):
                continue

            if api not in allowed:
                invalid.append(api)

        return sorted(set(invalid))