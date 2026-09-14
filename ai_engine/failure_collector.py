import re


class FailureCollector:

    def collect(self, stdout, stderr):

        text = stdout + "\n" + stderr

        failures = []

        current = {}

        for line in text.splitlines():

            line = line.strip()

            if line.startswith("FAILED"):

                current = {
                    "test": line,
                    "error": "",
                    "message": ""
                }

            elif "AssertionError" in line:

                current["error"] = "AssertionError"

                current["message"] = line

                failures.append(current)

            elif "TimeoutError" in line:

                current["error"] = "TimeoutError"

                current["message"] = line

                failures.append(current)

            elif "NoSuchElementException" in line:

                current["error"] = "NoSuchElementException"

                current["message"] = line

                failures.append(current)

            elif "ConnectionRefusedError" in line:

                current["error"] = "ConnectionRefusedError"

                current["message"] = line

                failures.append(current)

            elif "SyntaxError" in line:

                current["error"] = "SyntaxError"

                current["message"] = line

                failures.append(current)

        return failures