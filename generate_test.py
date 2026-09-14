from ai_engine.script_generator import ScriptGenerator

generator = ScriptGenerator()

code = generator.generate(

    "Verify A2L leak alarm during compressor startup"

)

print()

print("=" * 80)
print("FINAL GENERATED SCRIPT")
print("=" * 80)

print(code)