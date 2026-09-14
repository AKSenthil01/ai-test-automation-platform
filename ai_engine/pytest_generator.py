from langchain_ollama import OllamaLLM

from ai_engine.smart_retriever import SmartRetriever
from ai_engine.code_prompt import CodePrompt
from ai_engine.code_cleaner import CodeCleaner
from ai_engine.python_writer import PythonWriter


class PytestGenerator:

    def __init__(self):

        self.retriever = SmartRetriever()

        self.llm = OllamaLLM(
            model="llama3:8b",
            temperature=0
        )

    def generate(self, requirement):

        docs = self.retriever.retrieve(
            query=requirement,
            top_k=8
        )

        prompt = CodePrompt.build(
            requirement,
            docs
        )

        response = self.llm.invoke(prompt)

        code = CodeCleaner.clean(response)

        filename = (
            requirement.lower()
            .replace(" ", "_")
            .replace("/", "_")
            + ".py"
        )

        path = PythonWriter.write(
            code,
            filename
        )

        return path, code