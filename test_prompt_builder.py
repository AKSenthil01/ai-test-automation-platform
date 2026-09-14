from ai_engine.code_prompt_builder import CodePromptBuilder

docs = [
    "HVAC controller knowledge",
    "Compressor documentation"
]

prompt = CodePromptBuilder.build(
    "Verify A2L leak alarm during compressor startup",
    docs
)

print(prompt)