import re

from ai_engine.prompt_sections.requirement_section import RequirementSection
from ai_engine.prompt_sections.api_section import APISection
from ai_engine.prompt_sections.example_section import ExampleSection
from ai_engine.prompt_sections.assertion_section import AssertionSection
from ai_engine.prompt_sections.fixture_section import FixtureSection
from ai_engine.prompt_sections.knowledge_section import KnowledgeSection
from ai_engine.prompt_sections.rules_section import RulesSection


class PromptBuilder:
    """
    Builds the complete LLM prompt used for test generation.
    """

    SYSTEM_PROMPT = """
You are a Principal QA Automation Architect.

Generate production-quality pytest automation code.
"""

    def build(

            self,

            requirement,

            apis,

            examples,

            assertions,

            fixtures,

            knowledge,

            debug=False

    ):

        sections = [

            self.SYSTEM_PROMPT.strip(),

            RequirementSection.build(requirement),

            APISection.build(apis),

            ExampleSection.build(examples),

            AssertionSection.build(assertions),

            FixtureSection.build(fixtures),

            KnowledgeSection.build(knowledge),

            RulesSection.build()

        ]

        # Remove empty sections
        sections = [

            s.strip()

            for s in sections

            if s and s.strip()

        ]

        prompt = "\n\n".join(sections)

        # Normalize whitespace
        prompt = re.sub(

            r"\n{3,}",

            "\n\n",

            prompt

        )

        if debug:

            print("=" * 80)
            print("PROMPT STATISTICS")
            print("=" * 80)
            print(f"Characters : {len(prompt)}")
            print(f"Words      : {len(prompt.split())}")
            print(f"Est Tokens : {len(prompt)//4}")

        return prompt