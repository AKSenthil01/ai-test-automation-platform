from langchain_ollama import OllamaLLM

from ai_engine.config import (
    LLM_MODEL,
    LLM_TEMPERATURE
)


class BaseLLM:
    """
    Singleton LLM instance.

    Loads Ollama only once.
    """

    _instance = None

    @classmethod
    def get_llm(cls):

        if cls._instance is None:

            print("\nLoading Ollama LLM...")

            cls._instance = OllamaLLM(
                model=LLM_MODEL,
                temperature=LLM_TEMPERATURE
            )

        return cls._instance