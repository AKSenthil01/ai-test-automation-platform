import pandas as pd
import os


def generate_pytest_fast(input_file):

    df = pd.read_excel(input_file, sheet_name="Test Cases")

    code = """import pytest
from pymodbus.client import ModbusTcpClient
from core.ai_assertion_engine import AIAssertionEngine

client = ModbusTcpClient("localhost", port=5020)
client.connect()

ai_validator = AIAssertionEngine()
"""

    for _, row in df.iterrows():

        test_id = row["Test Case ID"].replace(" ", "_")
        expected = row["Expected Results"]

        code += f'''

def test_{test_id.lower()}():

    # Requirement: {row["Requirement"]}

    # 🔹 Simulated system output (replace with real logic)
    
    #result = client.read_holding_registers(address=0, count=1)
    
     # 🔹 Simulated Modbus response (CI-safe)
    def simulate_modbus():
    return {"register": 0, "value": "OK"}

result = simulate_modbus()
   


    actual_output = str(result)

    # 🔥 AI validation
    assert ai_validator.validate(
        expected="""{expected}""",
        actual=actual_output
    ), "AI validation failed"
'''

    os.makedirs("tests", exist_ok=True)

    #with open("tests/test_ai_fast.py", "w") as f:
    #    f.write(code)
    file_path = "tests/test_ai_fast.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("✅ AI-enabled PyTest generated instantly!")
    return code