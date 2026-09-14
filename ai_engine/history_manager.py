import json
import os

from datetime import datetime


class HistoryManager:

    def __init__(self):

        os.makedirs("history", exist_ok=True)

    def save(
            self,
            requirement,
            prompt,
            generated_code,
            reviewer_result,
            quality_score,
            metrics
    ):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = os.path.join(
            "history",
            f"{timestamp}.json"
        )

        history = {

            "timestamp": timestamp,

            "requirement": requirement,

            "prompt": prompt,

            "generated_code": generated_code,

            "review": reviewer_result,

            "quality_score": quality_score,

            "metrics": metrics

        }

        with open(
                filename,
                "w",
                encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False
            )

        return filename