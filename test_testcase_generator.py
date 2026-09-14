from ai_engine.testcase_generator import TestCaseGenerator

generator = TestCaseGenerator()

result = generator.generate(

    requirement="A2L leak detection during compressor startup",

    count=10

)

print(result)