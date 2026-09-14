from ai_engine.auto_healer import AutoHealer

code = """
import pytest

from your_module import *

wait_for_alarm()

fake_api()

verify_alarm()
"""

healer = AutoHealer()

fixed, changes = healer.heal(code)

print(fixed)

print()

print(changes)