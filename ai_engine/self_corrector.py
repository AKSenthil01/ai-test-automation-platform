from ai_engine.api_validator import APIValidator
from ai_engine.code_reviewer import CodeReviewer
from ai_engine.code_corrector import CodeCorrector
from ai_engine.hallucination_detector import HallucinationDetector
from ai_engine.review_parser import ReviewParser
from ai_engine.syntax_validator import SyntaxValidator


class SelfCorrector:
    """
    Performs iterative review and correction until the generated
    pytest script reaches acceptable quality.
    """

    def __init__(self):

        self.reviewer = CodeReviewer()

        self.corrector = CodeCorrector()

    def improve(
            self,
            requirement: str,
            code: str,
            max_iterations: int = 3,
            debug: bool = True
    ) -> str:

        current_code = code

        for iteration in range(1, max_iterations + 1):

            if debug:
                print("\n" + "=" * 80)
                print(f"SELF-CORRECTION ITERATION {iteration}")
                print("=" * 80)

            comments = []

            # ---------------------------------------------------
            # Syntax Validation
            # ---------------------------------------------------

            syntax_ok, syntax_error = SyntaxValidator.validate(current_code)

            if not syntax_ok:
                comments.append(f"Syntax Error: {syntax_error}")

            # ---------------------------------------------------
            # API Validation
            # ---------------------------------------------------

            invalid_apis = APIValidator.validate(current_code)

            comments.extend(
                [
                    f"Invalid Controller API: {api}"
                    for api in invalid_apis
                ]
            )

            # ---------------------------------------------------
            # Hallucination Detection
            # ---------------------------------------------------

            hallucinations = HallucinationDetector.detect(current_code)

            comments.extend(hallucinations)

            # ---------------------------------------------------
            # LLM Review
            # ---------------------------------------------------

            review = self.reviewer.review(
                requirement,
                current_code
            )

            if isinstance(review, str):
                review = ReviewParser.parse(review)

            comments.extend(review.get("comments", []))

            # ---------------------------------------------------
            # Debug
            # ---------------------------------------------------

            if debug:

                print(f"Syntax OK       : {syntax_ok}")
                print(f"Invalid APIs    : {len(invalid_apis)}")
                print(f"Hallucinations  : {len(hallucinations)}")
                print(f"Review Status   : {review.get('status')}")

                if comments:
                    print("\nIssues Found:")
                    for c in comments:
                        print(" -", c)

            # ---------------------------------------------------
            # PASS
            # ---------------------------------------------------

            if (
                    syntax_ok
                    and review.get("status") == "PASS"
                    and not invalid_apis
                    and not hallucinations
            ):

                if debug:
                    print("\nScript passed all validation checks.")

                return current_code

            # ---------------------------------------------------
            # Correct
            # ---------------------------------------------------

            current_code = self.corrector.correct(
                requirement=requirement,
                code=current_code,
                review_comments=comments,
                debug=debug
            )

        if debug:
            print("\nMaximum correction iterations reached.")

        return current_code