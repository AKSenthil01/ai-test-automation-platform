import os


class ScriptWriter:

    @staticmethod
    def write(code, filename):

        os.makedirs("generated_scripts", exist_ok=True)

        path = os.path.join(
            "generated_scripts",
            filename
        )

        with open(path, "w", encoding="utf8") as f:

            f.write(code)

        return path