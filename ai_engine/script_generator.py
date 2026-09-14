from pathlib import Path

from ai_engine.api_selector import APISelector
from ai_engine.example_selector import ExampleSelector
from ai_engine.assertion_selector import AssertionSelector
from ai_engine.fixture_selector import FixtureSelector

from ai_engine.prompt_builder import PromptBuilder
from ai_engine.code_generator import CodeGenerator
from ai_engine.self_corrector import SelfCorrector


class ScriptGenerator:

    def __init__(self):

        self.api_selector = APISelector()
        self.example_selector = ExampleSelector()
        self.assertion_selector = AssertionSelector()
        self.fixture_selector = FixtureSelector()

        self.generator = CodeGenerator()
        self.corrector = SelfCorrector()

    def generate(self, requirement):

        print("=" * 80)
        print("Requirement")
        print("=" * 80)
        print(requirement)

        apis = self.api_selector.select(requirement)

        examples = self.example_selector.select(requirement)

        assertions = self.assertion_selector.select(requirement)

        fixtures = self.fixture_selector.select(requirement)

        prompt = PromptBuilder.build(
            requirement=requirement,
            apis=apis,
            examples=examples,
            assertions=assertions,
            fixtures=fixtures
        )

        print("=" * 80)
        print("Generating Script...")
        print("=" * 80)

        generated_code = self.generator.generate(prompt)

        print("=" * 80)
        print("Review + Self Correction")
        print("=" * 80)

        final_code = self.corrector.improve(
            requirement,
            generated_code
        )

        output_dir = Path("generated/scripts")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "generated_test.py"

        output_file.write_text(
            final_code,
            encoding="utf8"
        )

        print()
        print("Saved to:", output_file)

        return final_code