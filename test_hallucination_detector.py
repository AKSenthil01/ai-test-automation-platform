from ai_engine.hallucination_detector import HallucinationDetector

code = """
import pytest
from compressor import Compressor

class HVAC:

    pass

def wait():

    pass

def test_demo():

    wait_for_alarm()

    verify_fake_alarm()
"""

issues = HallucinationDetector.detect(code)

print()

for issue in issues:
    print(issue)