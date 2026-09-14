from ai_engine.code_generator import CodeGenerator

prompt = """
You are a Principal QA Automation Architect.

Generate executable pytest code.

Requirements:
- Return ONLY Python code.
- Do NOT explain anything.
- Do NOT use Markdown.
- Do NOT use triple backticks.
- Do NOT say "Here is the code".
- Output MUST start with:

import pytest

Requirement:
Verify compressor startup.

Allowed APIs:
configure_controller()
start_compressor()
get_compressor_status()
stop_compressor()
reset_controller()

Expected behavior:
1. Configure controller
2. Start compressor
3. Verify compressor status is RUNNING
4. Stop compressor
5. Reset controller

Generate a complete pytest file.
"""
generator = CodeGenerator()

code = generator.generate(prompt)

print("\nReturned Code\n")
print(code)