
from __future__ import annotations
import sys


import argparse
import json
import re
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from openpyxl import Workbook, load_workbook


from ai_engine.llm_client import LLMClient
from validation.validator import validate_workbook


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"

OUTPUT_WORKBOOK = BASE_DIR / "generated_tests.xlsx"

INTERVIEW_WORKBOOK = (
    BASE_DIR / "generated_tests_interview_ready_50.xlsx"
)


# ============================================================
# SOURCE DOCUMENTS
# ============================================================

SOURCE_FILES = [
    DATA_DIR / "a2l_leak_detection_spec.txt",
    DATA_DIR / "controller_manual.txt",
    DATA_DIR / "modbus_register_map.txt",
]


# ============================================================
# GENERATION CONFIGURATION
# ============================================================

DEFAULT_COUNT = 40

MAX_COUNT_PER_REQUEST = 10

MODEL_NAME = "llama3"

# Domains intentionally supported by the current simulator
# and source documents.
DOMAINS = [
    "A2L Leak Detection",
    "Controller Safety Protections",
    "Modbus Register Monitoring",
    "Compressor, Sensors, Fans and Alarm Handling",
]


# ============================================================
# SOURCE LOADING
# ============================================================

def load_source_documents() -> list[dict[str, str]]:
    """
    Load the HVAC source documents used for
    source-grounded LLM test-case generation.
    """

    documents: list[dict[str, str]] = []

    for path in SOURCE_FILES:

        if not path.exists():
            raise FileNotFoundError(
                f"Required source document not found: {path}"
            )

        text = path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            raise ValueError(
                f"Source document is empty: {path}"
            )

        documents.append(
            {
                "source": path.name,
                "content": text,
            }
        )

    return documents


# ============================================================
# SOURCE CONTEXT
# ============================================================

def build_source_context(
    documents: list[dict[str, str]],
) -> str:
    """
    Build the source-grounded context supplied to the LLM.
    """

    sections: list[str] = []

    for document in documents:

        sections.extend(
            [
                "=" * 70,
                f"SOURCE: {document['source']}",
                "=" * 70,
                document["content"],
                "",
            ]
        )

    return "\n".join(sections)


# ============================================================
# PROMPT
# ============================================================

def build_generation_prompt(
    requirement: str,
    source_context: str,
    count: int,
    domain: str,
) -> str:
    """
    Build a source-grounded prompt for HVAC test-case generation.
    """

    return f"""
You are a Principal QA Automation Architect specializing in
HVAC embedded systems, refrigeration controls, A2L refrigerants,
compressors, sensors, fans, alarms, safety protections,
Modbus RTU and software test automation.

Generate exactly {count} distinct software test cases.

TARGET DOMAIN:
{domain}

REQUIREMENT:
{requirement}

============================================================
SOURCE DOCUMENTS
============================================================

Use ONLY the supplied source documents as the technical basis
for the generated scenarios.

Do not invent:
- APIs
- registers
- controller functions
- hardware interfaces
- protocol features
- thresholds
- alarms
- behaviors
- configuration options

If a behavior is not supported by the source documents,
do not generate a test case for it.

============================================================
PROJECT SCOPE
============================================================

The current simulator supports software-level testing of:

1. A2L leak detection
2. Compressor shutdown
3. Fan activation
4. Alarm activation
5. Event logging
6. Manual reset
7. High discharge temperature protection
8. Low suction pressure protection
9. Invalid sensor input / safe mode
10. Modbus status registers

Do NOT generate:
- Defrost test cases
- BACnet test cases
- Unsupported BACnet behavior
- Physical hardware tests
- Real refrigerant handling procedures

============================================================
SCENARIO REQUIREMENTS
============================================================

Every test case must represent a distinct scenario.

Vary:
- normal conditions
- abnormal conditions
- safety conditions
- fault conditions
- recovery conditions
- boundary conditions
- sensor states
- compressor states
- fan states
- alarm states
- Modbus register values

Do not create duplicates by merely changing the
test-case ID.

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Return a JSON array.

Each element MUST contain exactly:

{{
    "test_case_id": "TC_AI_001",
    "requirement": "...",
    "feature": "...",
    "scenario": "...",
    "steps": [
        "Step 1",
        "Step 2",
        "Step 3"
    ],
    "expected_result": "...",
    "test_data": "...",
    "automation_candidate": "YES",
    "tool": "Pytest"
}}

============================================================
FIELD RULES
============================================================

test_case_id:
- Unique within this generated batch.
- Use TC_AI_001, TC_AI_002, etc.

feature:
- Must describe the actual HVAC feature.

scenario:
- Must describe one concrete scenario.

steps:
- At least 3 concrete actions.
- Avoid vague instructions.

expected_result:
- Must describe observable behavior.

test_data:
- Include concrete values or states where supported.

automation_candidate:
- Use YES only for deterministic software scenarios.

tool:
- Use Pytest.

============================================================
QUALITY RULES
============================================================

1. Generate exactly {count} cases.
2. Every case must be different.
3. Stay grounded in the supplied source documents.
4. Do not invent unsupported behavior.
5. Do not use N/A.
6. Do not use placeholders.
7. Include positive and negative cases where supported.
8. Include safety and fault scenarios where supported.
9. Keep cases suitable for later pytest automation.
10. Return ONLY JSON.
""".strip()


# ============================================================
# JSON EXTRACTION
# ============================================================

def extract_json(text: str) -> list[dict[str, Any]]:
    """
    Extract a JSON array from the LLM response.

    Handles responses where the model accidentally wraps JSON
    in markdown code fences.
    """

    text = text.strip()

    # Remove markdown fences.
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Find the first JSON array.
    start = text.find("[")

    if start == -1:
        raise ValueError(
            "LLM response does not contain a JSON array."
        )

    end = text.rfind("]")

    if end == -1:
        raise ValueError(
            "LLM response contains an incomplete JSON array."
        )

    payload = text[start : end + 1]

    try:
        data = json.loads(payload)


    except json.JSONDecodeError as exc:

        start_context = max(0, exc.pos - 120)

        end_context = min(len(payload), exc.pos + 120)

        context = payload[

            start_context:end_context

        ]

        raise ValueError(

            "Invalid JSON returned by LLM.\n"

            f"Error: {exc}\n"

            f"JSON context around error:\n{context}"

        ) from exc

    if not isinstance(data, list):
        raise ValueError(
            "LLM response JSON must be an array."
        )

    return data


# ============================================================
# TEST CASE NORMALIZATION
# ============================================================

REQUIRED_FIELDS = [
    "test_case_id",
    "requirement",
    "feature",
    "scenario",
    "steps",
    "expected_result",
    "test_data",
    "automation_candidate",
    "tool",
]


def normalize_test_case(
    item: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    """
    Normalize one generated test case and enforce the expected
    structure before writing to Excel.
    """

    if not isinstance(item, dict):
        raise ValueError(
            f"Generated item {index} is not a JSON object."
        )

    for field in REQUIRED_FIELDS:
        if field not in item:
            raise ValueError(
                f"Generated item {index} is missing field: {field}"
            )

    test_case_id = str(
        item["test_case_id"]
    ).strip()

    requirement = str(
        item["requirement"]
    ).strip()

    feature = str(
        item["feature"]
    ).strip()

    scenario = str(
        item["scenario"]
    ).strip()

    expected_result = str(
        item["expected_result"]
    ).strip()

    test_data = str(
        item["test_data"]
    ).strip()

    automation_candidate = str(
        item["automation_candidate"]
    ).strip().upper()

    tool = str(
        item["tool"]
    ).strip()

    steps = item["steps"]

    if not isinstance(steps, list):
        raise ValueError(
            f"{test_case_id}: steps must be a JSON array."
        )

    steps = [
        str(step).strip()
        for step in steps
        if str(step).strip()
    ]

    if len(steps) < 3:
        raise ValueError(
            f"{test_case_id}: at least 3 steps are required."
        )

    values = {
        "test_case_id": test_case_id,
        "requirement": requirement,
        "feature": feature,
        "scenario": scenario,
        "steps": steps,
        "expected_result": expected_result,
        "test_data": test_data,
        "automation_candidate": automation_candidate,
        "tool": tool,
    }

    for field, value in values.items():

        if field == "steps":
            continue

        if not value:
            raise ValueError(
                f"{test_case_id}: {field} cannot be empty."
            )

        if str(value).strip().upper() == "N/A":
            raise ValueError(
                f"{test_case_id}: {field} cannot be N/A."
            )

    return values


# ============================================================
# CONTENT FILTERING
# ============================================================

FORBIDDEN_FEATURES = {
    "defrost",
    "bacnet",
}


def is_in_scope(
    test_case: dict[str, Any],
) -> bool:
    """
    Reject scenarios outside the current project scope.
    """

    text = " ".join(
        [
            test_case["feature"],
            test_case["scenario"],
            test_case["expected_result"],
            test_case["test_data"],
            " ".join(test_case["steps"]),
        ]
    ).lower()

    for forbidden in FORBIDDEN_FEATURES:
        if forbidden in text:
            return False

    return True


# ============================================================
# DUPLICATE DETECTION
# ============================================================

def normalized_scenario_key(
    test_case: dict[str, Any],
) -> str:
    """
    Create a simple normalized semantic key for duplicate
    detection.

    This is intentionally lightweight. The AI/RAG layer handles
    generation; this function prevents obvious duplicates from
    entering the workbook.
    """

    text = " ".join(
        [
            test_case["feature"],
            test_case["scenario"],
            test_case["expected_result"],
        ]
    ).lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


def remove_duplicate_cases(
    cases: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove exact/near-exact normalized duplicates.
    """

    unique: list[dict[str, Any]] = []

    seen: set[str] = set()

    for case in cases:

        key = normalized_scenario_key(
            case
        )

        if not key:
            continue

        if key in seen:
            continue

        seen.add(key)
        unique.append(case)

    return unique


# ============================================================
# TEST CASE ID NORMALIZATION
# ============================================================

def assign_test_case_ids(
    cases: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Reassign deterministic IDs after duplicate removal.

    IDs are identifiers only; automation matching does not depend
    on them.
    """

    normalized: list[dict[str, Any]] = []

    for index, case in enumerate(
        cases,
        start=1,
    ):

        updated = dict(case)

        updated["test_case_id"] = (
            f"TC_AI_{index:03d}"
        )

        normalized.append(
            updated
        )

    return normalized


# ============================================================
# DOMAIN GENERATION
# ============================================================

def generate_domain_cases(
    llm: LLMClient,
    requirement: str,
    source_context: str,
    domain: str,
    count: int,
) -> list[dict[str, Any]]:
    """
    Generate one batch for one HVAC domain.

    The LLM must return a valid JSON array. If the first response
    violates the JSON contract, retry once with an explicit
    structured-output correction prompt.
    """

    prompt = build_generation_prompt(
        requirement=requirement,
        source_context=source_context,
        count=count,
        domain=domain,
    )

    print(
        f"\nGenerating {count} cases for: {domain}"
    )

    response = llm.ask(
        prompt
    )

    try:
        cases = extract_json(
            response
        )

    except ValueError as first_error:

        print(
            "  Invalid JSON returned by LLM."
        )
        print(
            "  Retrying with strict JSON correction..."
        )

        retry_prompt = f"""
The previous response was not valid JSON.

Generate the requested HVAC test cases again.

STRICT OUTPUT REQUIREMENTS:

1. Return ONLY a valid JSON array.
2. Do NOT use markdown.
3. Do NOT use ```json fences.
4. Do NOT include explanatory text.
5. Use standard JSON syntax only.
6. Use decimal numbers instead of hexadecimal literals.
7. Do NOT use values such as 0x00, 0x01, or 0x02.
8. All strings must use double quotes.
9. Do not leave objects or arrays incomplete.
10. Ensure every comma, quote, brace, and bracket is valid.
11. The response must be parseable by Python json.loads().

The requested domain is:

{domain}

Requirement:

{requirement}

Source context:

{source_context}

Generate exactly {count} test case(s).
"""

        response = llm.ask(
            retry_prompt
        )

        try:
            cases = extract_json(
                response
            )

        except ValueError as retry_error:
            raise ValueError(
                "LLM failed to produce valid JSON after "
                "one retry.\n"
                f"Initial error: {first_error}\n"
                f"Retry error: {retry_error}"
            ) from retry_error

    normalized: list[dict[str, Any]] = []

    for index, item in enumerate(
        cases,
        start=1,
    ):
        try:
            case = normalize_test_case(
                item,
                index,
            )

        except ValueError as exc:
            print(
                f"  Rejected generated case: {exc}"
            )
            continue

        if not is_in_scope(case):
            print(
                f"  Rejected out-of-scope case: "
                f"{case['scenario']}"
            )
            continue

        normalized.append(
            case
        )

    return normalized
# ============================================================
# EXCEL WRITING
# ============================================================

HEADERS = [
    "Test Case ID",
    "Requirement",
    "Feature",
    "Scenario",
    "Steps",
    "Expected Result",
    "Test Data",
    "Automation Candidate",
    "Tool",
]


def write_workbook(
    cases: list[dict[str, Any]],
    output: Path,
) -> None:
    """
    Write generated test cases into the canonical Excel format.
    """

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Test Cases"

    worksheet.append(
        HEADERS
    )

    for case in cases:

        steps = "\n".join(
            f"{index}. {step}"
            for index, step in enumerate(
                case["steps"],
                start=1,
            )
        )

        worksheet.append(
            [
                case["test_case_id"],
                case["requirement"],
                case["feature"],
                case["scenario"],
                steps,
                case["expected_result"],
                case["test_data"],
                case["automation_candidate"],
                case["tool"],
            ]
        )

    # Basic readability.
    worksheet.freeze_panes = "A2"

    widths = {
        "A": 16,
        "B": 40,
        "C": 35,
        "D": 55,
        "E": 70,
        "F": 55,
        "G": 40,
        "H": 22,
        "I": 15,
    }

    for column, width in widths.items():
        worksheet.column_dimensions[
            column
        ].width = width

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    workbook.save(
        output
    )


# ============================================================
# CACHE HANDLING
# ============================================================

def use_cached_workbook(
    source: Path,
    destination: Path,
) -> None:
    """
    Copy an existing validated workbook into the canonical
    generated_tests.xlsx location.

    This is the default path when a previously validated
    interview-ready workbook exists.
    """

    if not source.exists():
        raise FileNotFoundError(
            f"Cached workbook not found: {source}"
        )

    destination.write_bytes(
        source.read_bytes()
    )


# ============================================================
# MAIN GENERATION PIPELINE
# ============================================================

def generate_excel(
    requirement: str = (
        "Generate deterministic software test cases "
        "for the HVAC refrigeration controller using "
        "the supplied A2L, controller safety, and Modbus "
        "source documents."
    ),
    count: int = DEFAULT_COUNT,
    force: bool = False,
    use_cache: bool = True,
) -> Path:
    """
    Main document-to-Excel generation pipeline.

    By default, an existing interview-ready workbook is reused.
    This prevents accidentally triggering expensive local LLM
    generation when a validated workbook already exists.
    """

    # --------------------------------------------------------
    # Cache first
    # --------------------------------------------------------

    if (
        use_cache
        and not force
        and INTERVIEW_WORKBOOK.exists()
    ):
        print(
            "Using cached validated interview-ready workbook:"
        )

        print(
            f"  {INTERVIEW_WORKBOOK}"
        )

        use_cached_workbook(
            INTERVIEW_WORKBOOK,
            OUTPUT_WORKBOOK,
        )

        validate_workbook(
            str(OUTPUT_WORKBOOK)
        )

        print(
            "Workbook validation passed."
        )

        return OUTPUT_WORKBOOK

    # --------------------------------------------------------
    # Validate count
    # --------------------------------------------------------

    if count <= 0:
        raise ValueError(
            "count must be greater than zero."
        )

    if count > DEFAULT_COUNT:
        print(
            "Warning: large generation counts may be slow "
            "with local Ollama inference."
        )

    # --------------------------------------------------------
    # Load source documents
    # --------------------------------------------------------

    print(
        "\nLoading HVAC source documents..."
    )

    documents = load_source_documents()

    source_context = build_source_context(
        documents
    )

    print(
        f"Loaded {len(documents)} source documents."
    )

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    print(
        f"Using LLM: {MODEL_NAME}"
    )

    # llm = LLMClient(
    #     model=MODEL_NAME
    # )
    llm = LLMClient()

    # --------------------------------------------------------
    # Domain distribution
    # --------------------------------------------------------

    domain_count = max(
        1,
        count // len(DOMAINS),
    )

    generated_cases: list[
        dict[str, Any]
    ] = []

    remaining = count

    for index, domain in enumerate(
        DOMAINS
    ):

        domains_left = (
            len(DOMAINS) - index
        )

        if domains_left == 1:
            target = remaining
        else:
            target = min(
                domain_count,
                remaining,
            )

        if target <= 0:
            break

        cases = generate_domain_cases(
            llm=llm,
            requirement=requirement,
            source_context=source_context,
            domain=domain,
            count=target,
        )

        generated_cases.extend(
            cases
        )

        remaining -= len(cases)

        print(
            f"  Accepted: {len(cases)}"
        )

        print(
            f"  Running total: "
            f"{len(generated_cases)}"
        )

    # --------------------------------------------------------
    # Duplicate removal
    # --------------------------------------------------------

    before = len(
        generated_cases
    )

    generated_cases = remove_duplicate_cases(
        generated_cases
    )

    duplicates_removed = (
        before
        - len(generated_cases)
    )

    if duplicates_removed:
        print(
            f"\nRemoved {duplicates_removed} duplicate cases."
        )

    # --------------------------------------------------------
    # Limit and IDs
    # --------------------------------------------------------

    generated_cases = generated_cases[
        :count
    ]

    generated_cases = assign_test_case_ids(
        generated_cases
    )

    # --------------------------------------------------------
    # Final check
    # --------------------------------------------------------

    if not generated_cases:
        raise RuntimeError(
            "No valid test cases were generated."
        )

    print(
        f"\nFinal generated cases: "
        f"{len(generated_cases)}"
    )

    if len(generated_cases) < count:
        print(
            f"Warning: requested {count}, "
            f"but only {len(generated_cases)} "
            "source-grounded cases were accepted."
        )

    # --------------------------------------------------------
    # Write workbook
    # --------------------------------------------------------

    write_workbook(
        generated_cases,
        OUTPUT_WORKBOOK,
    )

    # --------------------------------------------------------
    # Validate workbook
    # --------------------------------------------------------

    print(
        f"\nGenerated workbook: "
        f"{OUTPUT_WORKBOOK}"
    )

    validate_workbook(
        str(OUTPUT_WORKBOOK)
    )

    print(
        "Workbook validation passed."
    )

    return OUTPUT_WORKBOOK


# ============================================================
# CLI
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate HVAC software test cases from "
            "source documents and write them to Excel."
        )
    )

    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=(
            f"Number of test cases to generate. "
            f"Default: {DEFAULT_COUNT}"
        ),
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Force fresh LLM generation instead of using "
            "the cached interview-ready workbook."
        ),
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help=(
            "Disable cached workbook reuse."
        ),
    )

    parser.add_argument(
        "--requirement",
        default=(
            "Generate deterministic software test cases "
            "for the HVAC refrigeration controller."
        ),
        help="Requirement supplied to the LLM.",
    )

    args = parser.parse_args()

    output = generate_excel(
        requirement=args.requirement,
        count=args.count,
        force=args.force,
        use_cache=not args.no_cache,
    )

    print(
        f"\nDone: {output}"
    )


if __name__ == "__main__":
    main()

