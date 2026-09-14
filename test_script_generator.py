from ai_engine.script_generator import ScriptGenerator

generator = ScriptGenerator()

output = generator.generate(

    requirement="""
Verify A2L refrigerant leak alarm during compressor startup.
Controller shall stop compressor.
Alarm shall remain active until cleared.
""",

    filename="generated/test_a2l_alarm.py"

)

print(output)