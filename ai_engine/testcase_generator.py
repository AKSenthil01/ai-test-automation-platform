from langchain_ollama import OllamaLLM

from ai_engine.logger import get_logger
from ai_engine.rag_retriever import RAGRetriever
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.scenario_planner import ScenarioPlanner
from ai_engine.testcase_parser import TestCaseParser
from ai_engine.excel_writer import ExcelWriter

logger = get_logger(__name__)


class TestCaseGenerator:

    def __init__(self):

        self.retriever = RAGRetriever()

        self.llm = OllamaLLM(

            model="llama3:8b",

            temperature=0.4

        )

    def generate(self, requirement, count=10):
        logger.info("Planning scenarios...")

        scenarios = ScenarioPlanner.get_scenarios(count)

        logger.info(f"{len(scenarios)} scenarios selected.")

        logger.info("Searching similar HVAC test cases...")

        docs = self.retriever.retrieve(

            requirement,

            top_k=8

        )

        logger.info(f"{len(docs)} similar test cases found.")

        prompt = PromptBuilder.build_testcase_prompt(

            requirement,

            docs,

            scenarios

        )

        logger.info("Generating test cases...")

        response = self.llm.invoke(prompt)

        print("\n" + "=" * 80)
        print("RAW RESPONSE")
        print("=" * 80)
        print(response)
        print("=" * 80)

        test_cases = TestCaseParser.parse(response)

        ExcelWriter.write(test_cases)

        logger.info(f"{len(test_cases)} test cases generated.")

        return test_cases