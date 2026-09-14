import os
import pandas as pd


class ExcelWriter:

    @staticmethod
    def write(test_cases, output_file="Generated_TestCases.xlsx"):

        rows = []

        for tc in test_cases:

            steps = tc.get("steps", [])

            # Convert list of steps to readable text
            if isinstance(steps, list):

                formatted = []

                for s in steps:

                    if isinstance(s, dict):

                        formatted.append(
                            f"{s['step']}. {s['description']}"
                        )

                    else:

                        formatted.append(str(s))

                step_text = "\n".join(formatted)

            else:

                step_text = str(steps)

            rows.append({

                "Test Case ID":
                    tc.get("test_case_id", ""),

                "Requirement":
                    tc.get("requirement", ""),

                "Steps":
                    steps,

                "Expected Results":
                    tc.get("expected_result", ""),

                "Automation Candidate":
                    tc.get("automation_candidate", "YES"),

                "Tool":
                    tc.get("tool", "Pytest")

            })

        df = pd.DataFrame(rows)

        os.makedirs("generated", exist_ok=True)

        output_path = os.path.join("generated", output_file)

        df.to_excel(
            output_path,
            index=False
        )

        return output_path