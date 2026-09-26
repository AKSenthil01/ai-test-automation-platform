import json
import os
from datetime import datetime


class LearningDatabase:

    FILE = "generation_history/failure_learning.json"

    def __init__(self):

        os.makedirs(
            "generation_history",
            exist_ok=True
        )

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w") as f:

                json.dump([], f)

    def save(self, failure):

        with open(self.FILE) as f:

            data = json.load(f)

        failure["timestamp"] = datetime.now().isoformat()

        data.append(failure)

        with open(self.FILE, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def load(self):

        with open(self.FILE) as f:

            return json.load(f)