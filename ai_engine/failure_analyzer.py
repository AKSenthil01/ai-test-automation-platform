from ai_engine.logger import PipelineLogger
from ai_engine.query_planner import QueryPlanner
from ai_engine.smart_retriever import SmartRetriever
from ai_engine.llm_client import LLMClient
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.json_parser import JSONParser

import inspect
from ai_engine.smart_retriever import SmartRetriever

print("Loaded SmartRetriever from:")
print(inspect.getfile(SmartRetriever))

logger = PipelineLogger


class FailureAnalyzer:

    def __init__(self):
        self.retriever = SmartRetriever()
        self.llm = LLMClient()

    def analyze(self, log_text):

        logger.info("Searching Vector Database...")
        modules = QueryPlanner.extract_modules(log_text)

        query = QueryPlanner.build_search_query(log_text)

        docs = self.retriever.retrieve(
            query=query,
            modules=modules,
            top_k=5
        )

        logger.info(f"{len(docs)} similar test cases retrieved.")

        prompt = PromptBuilder.build_failure_prompt(
            log_text,
            docs
        )

        logger.info("Sending prompt to Llama3...")

        response = self.llm.ask(prompt)

        logger.info("Response received.")

        return JSONParser.parse(response)

