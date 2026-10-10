import ast


class QualityReport:

    # ---------------------------------------------------------
    # Backward Compatible Score Method
    # ---------------------------------------------------------

    def score(self, code: str):

        score = 100
        issues = []

        if not code.strip():
            return {
                "score": 0,
                "issues": ["Generated code is empty."]
            }

        try:
            ast.parse(code)
        except Exception as e:
            score -= 40
            issues.append(f"Syntax Error: {e}")

        checks = {
            "import pytest": 10,
            "assert": 10,
            "def test_": 10,
            "configure_controller": 10,
            "reset_controller": 10,
        }

        for keyword, penalty in checks.items():

            if keyword not in code:

                score -= penalty

                issues.append(f"Missing '{keyword}'")

        score = max(score, 0)

        return {
            "score": score,
            "issues": issues
        }

    # ---------------------------------------------------------
    # Production Quality Report
    # ---------------------------------------------------------

    def generate(
            self,
            requirement,
            code,
            review_iterations=1,
            syntax_ok=True,
            api_ok=True
    ):

        result = self.score(code)

        score = result["score"]

        issues = list(result["issues"])

        if not syntax_ok:
            score -= 20
            issues.append("Syntax validation failed.")

        if not api_ok:
            score -= 20
            issues.append("API validation failed.")

        score -= max(review_iterations - 1, 0) * 5

        score = max(score, 0)

        grade = self._grade(score)

        return {

            "requirement": requirement,

            "score": score,

            "grade": grade,

            "review_iterations": review_iterations,

            "syntax_ok": syntax_ok,

            "api_ok": api_ok,

            "issues": issues

        }

    # ---------------------------------------------------------

    def _grade(self, score):

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"