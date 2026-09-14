from ai_engine.base_llm import BaseLLM
from ai_engine.prompt_guard import PromptGuard
from ai_engine.generation_parser import GenerationParser


class CodeGenerator:

    def __init__(self):
        self.llm = BaseLLM.get_llm()

    def generate(self, prompt):

        print("=" * 80)
        print("Sending Prompt to Llama3")
        print("=" * 80)
        print("=" * 80)
        print("PROMPT LENGTH")
        print("=" * 80)
        print(len(prompt))
        print(prompt[:1000])

        prompt = PromptGuard.protect(prompt)

        response = self.llm.invoke(prompt)

        print("=" * 80)
        print("RAW RESPONSE")
        print("=" * 80)
        print(repr(response))

        response = GenerationParser.parse(response)

        print("=" * 80)
        print("Generated Code")
        print("=" * 80)
        print(response)

        return response