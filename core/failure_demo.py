from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from simulators.controller_simulator import RefrigerationController
from ai_engine.failure_analyzer import FailureAnalyzer


REPORT_DIR = BASE_DIR / "reports"
FAILURE_LOG = REPORT_DIR / "simulated_failure.log"


def create_simulated_failure() -> str:
    """
    Create a deterministic HVAC failure scenario.
    """

    controller = RefrigerationController(
        compressor_on=True
    )

    controller.set_high_discharge_temperature()

    expected = "Compressor remains ON"
    actual = "Compressor is OFF"

    failure_log = f"""
SIMULATED HVAC TEST FAILURE
===========================

Test Case:
High discharge temperature protection

Condition:
Discharge temperature exceeds configured safety limit.

Expected:
{expected}

Actual:
{actual}

Controller State:
compressor_on={controller.compressor_on}
discharge_temperature={controller.discharge_temperature}

Event Log:
{controller.event_log}

Failure Type:
Application behavior mismatch
""".strip()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_LOG.write_text(
        failure_log,
        encoding="utf-8"
    )

    return failure_log


def analyze_failure(failure_log: str):
    """Run the failure log through the existing failure analyzer."""

    analyzer = FailureAnalyzer()
    return analyzer.analyze(failure_log)


def run_failure_demo():
    failure_log = create_simulated_failure()

    print("=" * 70)
    print("SIMULATED FAILURE → FAILURE ANALYSIS")
    print("=" * 70)

    print("\nFailure log:")
    print(failure_log)

    print("\nFailure analysis:")
    result = analyze_failure(failure_log)

    print(result)

    return result


if __name__ == "__main__":
    run_failure_demo()