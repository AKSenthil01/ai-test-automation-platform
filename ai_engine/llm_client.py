from langchain_ollama import OllamaLLM


class LLMClient:

    def __init__(self):

        self.llm = OllamaLLM(
            model="llama3:8b",
            temperature=0,
            timeout=30
        )

    def ask(self, prompt):

        return self.llm.invoke(prompt)