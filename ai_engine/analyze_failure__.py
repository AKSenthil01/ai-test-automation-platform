import json

from ai_engine.rag_retriever import RAGRetriever
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.llm_client import LLMClient


class FailureAnalyzer:

    def __init__(self):

        self.retriever = RAGRetriever()

        self.llm = LLMClient()

    def analyze(self, log_text):

        docs = self.retriever.retrieve(
            log_text,
            top_k=5
        )

        prompt = PromptBuilder.build_failure_prompt(
            log_text,
            docs
        )

        response = self.llm.ask(prompt)

        response = response.strip()

        start = response.find("{")
        end = response.rfind("}") + 1

        return json.loads(response[start:end])