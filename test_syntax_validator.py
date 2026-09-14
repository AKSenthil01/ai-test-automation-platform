from ai_engine.syntax_validator import SyntaxValidator

good_code = """
import pytest

def test_demo():
    assert True
"""

bad_code = """
import pytest

def test_demo(
    assert True
"""

print("GOOD CODE")
print(SyntaxValidator.validate(good_code))

print()

print("BAD CODE")
print(SyntaxValidator.validate(bad_code))
