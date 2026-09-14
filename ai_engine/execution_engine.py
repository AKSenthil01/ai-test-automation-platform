import subprocess
import time


class ExecutionEngine:

    def execute(self, test_file):

        start = time.time()

        result = subprocess.run(
            [
                "pytest",
                test_file,
                "-q",
                "--tb=short"
            ],
            capture_output=True,
            text=True
        )

        execution_time = round(
            time.time() - start,
            2
        )

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "execution_time": execution_time
        }