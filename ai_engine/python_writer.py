import os


class PythonWriter:

    @staticmethod
    def write(code, filename):

        os.makedirs("generated/scripts", exist_ok=True)

        path = f"generated/scripts/{filename}"

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return path