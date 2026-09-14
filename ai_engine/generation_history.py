import json
import os
from datetime import datetime


class GenerationHistory:
    """
    Stores every AI generation as a separate run.

    Each generation contains:
        - Requirement
        - Prompt
        - Generated code
        - Corrected code
        - Review result
        - Quality report
        - Execution result
    """

    def __init__(self, root="history"):

        self.root = root

        os.makedirs(root, exist_ok=True)

    # ---------------------------------------------------------

    def create_run(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        folder = os.path.join(

            self.root,

            f"generation_{timestamp}"

        )

        os.makedirs(folder, exist_ok=True)

        return folder

    # ---------------------------------------------------------

    @staticmethod
    def save_text(folder, filename, text):

        path = os.path.join(folder, filename)

        with open(

                path,

                "w",

                encoding="utf8"

        ) as f:

            f.write(text)

    # ---------------------------------------------------------

    @staticmethod
    def save_json(folder, filename, obj):

        path = os.path.join(folder, filename)

        with open(

                path,

                "w",

                encoding="utf8"

        ) as f:

            json.dump(

                obj,

                f,

                indent=4,

                ensure_ascii=False

            )

    # ---------------------------------------------------------

    def save_generation(

            self,

            requirement,

            prompt,

            generated_code,

            corrected_code,

            review,

            quality,

            execution

    ):

        folder = self.create_run()

        self.save_text(

            folder,

            "requirement.txt",

            requirement

        )

        self.save_text(

            folder,

            "prompt.txt",

            prompt

        )

        self.save_text(

            folder,

            "generated.py",

            generated_code

        )

        self.save_text(

            folder,

            "corrected.py",

            corrected_code

        )

        self.save_json(

            folder,

            "review.json",

            review

        )

        self.save_json(

            folder,

            "quality.json",

            quality

        )

        self.save_json(

            folder,

            "execution.json",

            execution

        )

        return folder