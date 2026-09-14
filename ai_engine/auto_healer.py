import re

from ai_engine.api_catalog import APICatalog


class AutoHealer:

    def __init__(self):

        self.valid_apis = APICatalog.load()

    def heal(self, code):

        healed = code

        changes = []

        healed, c = self.fix_fake_imports(healed)
        changes.extend(c)

        healed, c = self.fix_fake_modules(healed)
        changes.extend(c)

        healed, c = self.fix_invalid_apis(healed)
        changes.extend(c)

        healed, c = self.fix_placeholder_functions(healed)
        changes.extend(c)

        return healed, changes

    def fix_fake_imports(self, code):

        changes = []

        lines = []

        for line in code.splitlines():

            if "your_module" in line:

                changes.append(
                    "Removed imaginary import your_module"
                )

                continue

            if "compressor import" in line:

                changes.append(
                    "Removed imaginary compressor import"
                )

                continue

            lines.append(line)

        return "\n".join(lines), changes

    def fix_fake_modules(self, code):

        changes = []

        patterns = [

            r"from .* import Compressor",

            r"import Compressor",

            r"from your_module.*"

        ]

        healed = code

        for p in patterns:

            healed = re.sub(
                p,
                "",
                healed
            )

        return healed, changes

    def fix_invalid_apis(self, code):

        changes = []

        tokens = re.findall(

            r'([A-Za-z_][A-Za-z0-9_]*)\(',

            code

        )

        healed = code

        ignore = {

            "assert",

            "print",

            "len",

            "range"

        }

        for token in tokens:

            if token in ignore:

                continue

            if token.startswith("test_"):

                continue

            if token not in self.valid_apis:

                healed = healed.replace(

                    token + "(",

                    f"# TODO Invalid API {token}\n# {token}("

                )

                changes.append(

                    f"Disabled invalid API {token}"

                )

        return healed, changes

    def fix_placeholder_functions(self, code):

        changes = []

        placeholders = [

            "wait_for_alarm",

            "wait_until_alarm",

            "poll_alarm",

            "sleep_until_alarm",

            "wait_for_controller"

        ]

        healed = code

        for func in placeholders:

            if func in healed:

                healed = healed.replace(

                    func,

                    "verify_alarm"

                )

                changes.append(

                    f"Replaced {func}()"

                )

        return healed, changes