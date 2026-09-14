import os

from ai_engine.api_selector import APISelector
from ai_engine.assertion_selector import AssertionSelector
from ai_engine.code_generator import CodeGenerator
from ai_engine.example_selector import ExampleSelector
from ai_engine.execution_engine import ExecutionEngine
from ai_engine.fixture_selector import FixtureSelector
from ai_engine.generation_history import GenerationHistory
from ai_engine.html_report import HTMLReport
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.prompt_guard import PromptGuard
from ai_engine.quality_report import QualityReport
from ai_engine.rag_engine import RAGEngine
from ai_engine.self_corrector import SelfCorrector


class GenerationPipeline:

    def __init__(self):

        self.api_selector = APISelector()

        self.example_selector = ExampleSelector()

        self.assertion_selector = AssertionSelector()

        self.fixture_selector = FixtureSelector()

        self.rag = RAGEngine()

        self.generator = CodeGenerator()

        self.corrector = SelfCorrector()

        self.quality = QualityReport()

        self.executor = ExecutionEngine()

        self.history = GenerationHistory()

        self.html_report = HTMLReport()

    # ------------------------------------------------------------

    def generate(

            self,

            requirement,

            execute=True,

            save_test=True,

            test_file="generated_tests/test_generated.py"

    ):

        print("=" * 80)
        print("STEP 1 : Selecting APIs")
        print("=" * 80)

        apis = self.api_selector.select(requirement)

        print(apis)

        print("=" * 80)
        print("STEP 2 : Selecting Examples")
        print("=" * 80)

        examples = self.example_selector.select(requirement)

        print("=" * 80)
        print("STEP 3 : Selecting Assertions")
        print("=" * 80)

        assertions = self.assertion_selector.select(requirement)

        print("=" * 80)
        print("STEP 4 : Selecting Fixtures")
        print("=" * 80)

        fixtures = self.fixture_selector.select(requirement)

        print("=" * 80)
        print("STEP 5 : Retrieving Knowledge")
        print("=" * 80)

        knowledge = self.rag.retrieve(
            requirement,
            top_k=5
        )

        print("=" * 80)
        print("STEP 6 : Building Prompt")
        print("=" * 80)

        prompt = PromptBuilder.build(

            requirement=requirement,

            apis=apis,

            examples=examples,

            assertions=assertions,

            fixtures=fixtures,

            knowledge=knowledge

        )

        prompt = PromptGuard.clean(prompt)

        print("=" * 80)
        print("STEP 7 : Generating Code")
        print("=" * 80)

        generated_code = self.generator.generate(prompt)

        print("=" * 80)
        print("STEP 8 : Self Correction")
        print("=" * 80)

        corrected_code = self.corrector.improve(

            requirement=requirement,

            code=generated_code

        )

        print("=" * 80)
        print("STEP 9 : Quality Report")
        print("=" * 80)

        quality = self.quality.score(corrected_code)

        print(quality)

        # ---------------------------------------------------------
        # Save Generated Test
        # ---------------------------------------------------------

        if save_test:

            os.makedirs("generated_tests", exist_ok=True)

            with open(

                    test_file,

                    "w",

                    encoding="utf8"

            ) as f:

                f.write(corrected_code)

        # ---------------------------------------------------------
        # Execute Test
        # ---------------------------------------------------------

        if execute:

            print("=" * 80)
            print("STEP 10 : Executing Generated Test")
            print("=" * 80)

            execution = self.executor.run(test_file)

        else:

            execution = {

                "success": False,

                "message": "Execution skipped."

            }

        # ---------------------------------------------------------
        # Save Generation History
        # ---------------------------------------------------------

        history_folder = self.history.save_generation(

            requirement=requirement,

            prompt=prompt,

            generated_code=generated_code,

            corrected_code=corrected_code,

            review={
                "status": "Completed"
            },

            quality=quality,

            execution=execution

        )

        print(f"\nGeneration history saved to:\n{history_folder}")

        # ---------------------------------------------------------
        # HTML Report
        # ---------------------------------------------------------

        report_path = self.html_report.generate(

            requirement=requirement,

            apis=apis,

            generated_code=generated_code,

            corrected_code=corrected_code,

            quality=quality,

            execution=execution,

            review={
                "status": "Completed"
            }

        )

        print(f"\nHTML report generated:\n{report_path}")

        # ---------------------------------------------------------

        return {

            "generated_code": generated_code,

            "corrected_code": corrected_code,

            "quality": quality,

            "execution": execution,

            "history": history_folder,

            "report": report_path

        }