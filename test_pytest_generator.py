from ai_engine.pytest_generator import PytestGenerator

generator = PytestGenerator()

path, code = generator.generate(

    "Verify A2L leak alarm during compressor startup"

)

print()

print("=" * 80)
print("Generated File")
print("=" * 80)

print(path)

print()

print("=" * 80)
print("Generated Code")
print("=" * 80)

print(code)