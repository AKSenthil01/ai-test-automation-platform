from ai_engine.execution_engine import ExecutionEngine

engine = ExecutionEngine()

result = engine.execute(
    "generated_tests/test_generated.py"
)

print(result)