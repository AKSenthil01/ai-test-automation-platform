import ast

from ai_engine.api_catalog import APICatalog


class HallucinationDetector:
    """
    Detects hallucinated APIs, imports, wrapper classes,
    placeholder functions and forbidden patterns.
    """

    FORBIDDEN_IMPORTS = {
        "compressor",
        "controller",
        "hvac",
        "fake_module",
        "your_module",
    }

    FORBIDDEN_FUNCTIONS = {
        "wait_for_alarm",
        "poll_alarm",
        "sleep_until_alarm",
        "controller_connect",
        "controller_start",
        "controller_stop",
    }

    @staticmethod
    def detect(code):

        issues = []

        allowed = set(APICatalog.load())

        try:
            tree = ast.parse(code)

        except SyntaxError as e:
            return [f"Syntax Error : {e}"]

        for node in ast.walk(tree):

            # ----------------------------------------
            # Imports
            # ----------------------------------------

            if isinstance(node, ast.Import):

                for name in node.names:

                    module = name.name.split(".")[0]

                    if module in HallucinationDetector.FORBIDDEN_IMPORTS:

                        issues.append(
                            f"Forbidden import : {module}"
                        )

            if isinstance(node, ast.ImportFrom):

                module = (node.module or "").split(".")[0]

                if module in HallucinationDetector.FORBIDDEN_IMPORTS:

                    issues.append(
                        f"Forbidden import : {module}"
                    )

            # ----------------------------------------
            # Wrapper classes
            # ----------------------------------------

            if isinstance(node, ast.ClassDef):

                issues.append(
                    f"Wrapper class detected : {node.name}"
                )

            # ----------------------------------------
            # Placeholder functions
            # ----------------------------------------

            if isinstance(node, ast.FunctionDef):

                if len(node.body) == 1:

                    stmt = node.body[0]

                    if isinstance(stmt, ast.Pass):

                        issues.append(
                            f"Placeholder function : {node.name}"
                        )

            # ----------------------------------------
            # Function calls
            # ----------------------------------------

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    fn = node.func.id

                    if fn in HallucinationDetector.FORBIDDEN_FUNCTIONS:

                        issues.append(
                            f"Forbidden API : {fn}"
                        )

                    if (
                        fn not in allowed
                        and fn.startswith("verify_")
                    ):

                        issues.append(
                            f"Unknown verification API : {fn}"
                        )

        return sorted(set(issues))