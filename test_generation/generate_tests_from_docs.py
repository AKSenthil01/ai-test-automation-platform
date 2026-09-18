import json
import os
import re
from pathlib import Path
from typing import Any

import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from ai_engine.embeddings import EmbeddingManager


# ============================================================
# PATHS / CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vector_store" / "faiss_index"
OUTPUT_FILE = BASE_DIR / "generated_tests.xlsx"


MODEL_NAME = "llama3:8b"

TEMPERATURE = 0.1

TOP_K_RAG = 5


# ============================================================
# SOURCE DOCUMENTS
# ============================================================

SOURCE_FILES = [
    DATA_DIR / "a2l_leak_detection_spec.txt",
    DATA_DIR / "controller_manual.txt",
    DATA_DIR / "modbus_register_map.txt",
]


def load_source_text():
    """
    Load all source documentation.

    Missing files are reported explicitly rather than silently
    replaced with invented content.
    """

    documents = []

    for source_file in SOURCE_FILES:

        if not source_file.exists():
            print(
                f"WARNING: Source file not found: "
                f"{source_file}"
            )
            continue

        text = source_file.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            print(
                f"WARNING: Source file is empty: "
                f"{source_file}"
            )
            continue

        documents.append(
            f"\n===== {source_file.name} =====\n"
            f"{text}"
        )

    if not documents:
        raise RuntimeError(
            "No source documentation could be loaded."
        )

    return "\n".join(documents)


SOURCE_TEXT = load_source_text()


# ============================================================
# DOCUMENT NUMBER VALIDATION
# ============================================================

def extract_numbers(text):
    """
    Extract numeric tokens from text.

    This is intentionally conservative. It catches values such
    as 20, 30, 10.5, etc. while allowing documented values.
    """

    return re.findall(
        r"(?<![A-Za-z])\d+(?:\.\d+)?",
        str(text),
    )


def source_numbers():
    return set(
        extract_numbers(SOURCE_TEXT)
    )


# Structural numbering and documented source values.

ALLOWED_NUMBERS = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "25",
    "30001",
    "30002",
    "30003",
    "30004",
    "30005",
    "30006",
    "30007",
    "30008",
}


def contains_unsupported_number(text):
    numbers = extract_numbers(text)

    for number in numbers:

        if number not in ALLOWED_NUMBERS:
            return True

    return False


# ============================================================
# DOMAIN PLAN
# ============================================================

DOMAIN_PLANS = [
    {
        "domain": "A2L Refrigerant Leak Detection",
        "count": 20,
        "scenario_types": [
            "Normal operation with refrigerant concentration below the configured safety threshold",
            "Leak alarm when refrigerant concentration exceeds 25% of LFL",
            "Immediate compressor shutdown after leak detection",
            "Fan activation for ventilation after leak detection",
            "Alarm status activation after leak detection",
            "Leak event logging in controller memory",
            "Recovery when gas concentration drops below the safe limit",
            "Manual technician reset after leak condition clears",
            "Sensor drift causing false leak detection",
            "Electrical noise causing false leak detection",
            "Sensor calibration error causing false leak detection",
            "Regular sensor calibration as a preventive control",
            "A2L refrigerant safety monitoring",
            "Continuous gas sensor monitoring",
            "Safety response sequence after detected leak",
            "Return to normal operation after leak recovery conditions",
            "Leak detection status representation",
            "Controller response to an active refrigerant leak",
            "False detection fault handling",
            "Documented leak detection safety behavior",
        ],
    },

    {
        "domain": "Controller Operating Modes and Safety Protections",
        "count": 20,
        "scenario_types": [
    "Cooling mode with compressor operation to maintain target temperature",
    "Cooling mode compressor operation",
    "Alarm mode activation when an abnormal condition occurs",
    "High discharge temperature protection causing compressor shutdown",
    "Low suction pressure protection preventing compressor damage from refrigerant loss",
    "Sensor failure protection when sensor input is invalid",
    "Controller entering safe mode after invalid sensor input",
    "Evaporator fan maintaining airflow across the evaporator coil",
    "Condenser fan dissipating heat from the condenser",
    "Evaporator temperature sensor monitoring",
    "Ambient temperature sensor monitoring",
    "Controller management of compressor operation",
    "Controller management of evaporator fan control",
    "Controller management of condenser fan control",
    "Controller safety protection behavior",
    "Controller handling of abnormal operating conditions",
    "Controller logging major events",
    "Controller logging faults for diagnostics",
    "BACnet MS/TP communication interface for building automation integration",
    "Modbus RTU communication interface for monitoring and configuration",
],
    },

    {
        "domain": "Modbus RTU Monitoring and Controller Registers",
        "count": 20,
        "scenario_types": [
            "Reading evaporator temperature from register 30001",
            "Reading suction pressure from register 30002",
            "Reading discharge temperature from register 30003",
            "Reading compressor status from register 30004",
            "Compressor status value 0",
            "Compressor status value 1",
            "Reading alarm status from register 30006",
            "Alarm status value 0",
            "Alarm status value 1",
            "Reading A2L leak status from register 30007",
            "A2L leak status value 0",
            "A2L leak status value 1",
            "Reading fan status from register 30008",
            "Fan status value 0",
            "Fan status value 1",
            "Monitoring controller operating state through registers",
            "Monitoring safety-related controller status through registers",
        ],
    },

    {
        "domain": "Compressor, Sensors, Fans and Alarm Handling",
        "count": 20,
        "scenario_types": [
            "Compressor operation during cooling mode",
            "Compressor shutdown from high discharge temperature protection",
            "Low suction pressure protection",
            "Evaporator fan operation",
            "Fan activation during A2L leak ventilation",
            "Condenser fan heat dissipation",
            "Evaporator temperature monitoring",
            "Ambient temperature monitoring",
            "Invalid sensor input handling",
            "Sensor failure protection",
            "Safe mode after sensor failure",
            "Alarm mode during abnormal conditions",
            "Leak alarm activation",
            "Controller event logging",
            "Compressor safety response",
            "Sensor-related abnormal condition handling",
        ],
    },

    {
        "domain": "BACnet MS/TP and Controller Communication",
        "count": 20,
        "scenario_types": [
            "BACnet MS/TP building automation integration",
            "Controller monitoring through BACnet MS/TP",
            "Controller integration with building automation systems",
            "Monitoring compressor operation through controller communication",
            "Monitoring fan control through controller communication",
            "Monitoring alarm conditions through controller communication",
            "Monitoring temperature information through controller communication",
            "Monitoring evaporator temperature",
            "Monitoring ambient temperature",
            "Monitoring safety protection state",
            "Monitoring controller faults",
            "Controller configuration through documented communication interfaces",
            "BACnet MS/TP as a communication interface",
            "Communication use for building automation integration",
            "Controller event and fault diagnostics",
            "Communication-based monitoring of controller state",
            "Monitoring refrigeration operating mode",
            "Monitoring abnormal controller conditions",
            "Controller communication and diagnostics",
        ],
    },
]


# ============================================================
# VECTOR STORE
# ============================================================

def create_vector_store():

    print("\nLoading SentenceTransformer model...")

    embedding_manager = EmbeddingManager()

    embeddings = embedding_manager.embedding

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )

    documents = []

    for source_file in SOURCE_FILES:

        if not source_file.exists():
            continue

        text = source_file.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        chunks = splitter.split_text(text)

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source_file.name
                    },
                )
            )

    if not documents:
        raise RuntimeError(
            "No source documents available for vector store."
        )

    if VECTOR_DB_DIR.exists():

        try:

            print("Loading existing vector DB...")

            vector_db = FAISS.load_local(
                str(VECTOR_DB_DIR),
                embeddings,
                allow_dangerous_deserialization=True,
            )

            return vector_db

        except Exception as error:

            print(
                "Existing vector DB could not be loaded:"
                f" {error}"
            )

            print(
                "Rebuilding vector DB..."
            )

    vector_db = FAISS.from_documents(
        documents,
        embeddings,
    )

    VECTOR_DB_DIR.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    vector_db.save_local(
        str(VECTOR_DB_DIR)
    )

    print(
        "Vector DB created:"
        f" {VECTOR_DB_DIR}"
    )

    return vector_db


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_context(
    vector_db,
    query,
    k=TOP_K_RAG,
):

    documents = vector_db.similarity_search(
        query,
        k=k,
    )

    if not documents:
        return ""

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "unknown",
        )

        context_parts.append(
            f"[SOURCE: {source}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(
        context_parts
    )


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(
    domain_plan,
    context,
    count,
    existing_scenarios=None,
):

    domain = domain_plan["domain"]

    scenario_types = domain_plan[
        "scenario_types"
    ]

    scenario_text = "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(
            scenario_types,
            start=1,
        )
    )

    existing_text = ""

    if existing_scenarios:

        existing_text = """
ALREADY GENERATED SCENARIOS:

The following scenarios have already been
generated for this domain.

Do NOT repeat them.

Do NOT create wording-only variants.

Do NOT create a scenario that tests the same
behavior with superficial wording changes.

Previously generated scenarios:
""" + "\n".join(
            f"- {scenario}"
            for scenario in existing_scenarios
        )

    return f"""
You are a Principal QA Automation Architect
specializing in HVAC refrigeration controllers
and embedded systems.

Design exactly {count} DISTINCT AI-generated
test cases.

DOMAIN:
{domain}

SCENARIO AREAS TO COVER:

{scenario_text}

{existing_text}

SOURCE DOCUMENTATION:

{context}

============================================================
TEST DESIGN STRATEGY
============================================================

Use the scenario areas above as a deliberate
coverage plan.

Each generated test case must primarily cover
ONE specific scenario area or one clearly
documented behavioral aspect.

Across the requested test cases:

- Maximize coverage of different scenario areas.
- Do not repeatedly test the same behavior with
  different wording.
- Do not create artificial combinations just to
  increase the count.
- Do not create cosmetic variants.
- Each test must have a meaningful behavioral
  difference.
- Prefer different triggers, states, sequences,
  faults, recovery conditions, protection
  behaviors, registers, status values, or
  documented communication behaviors.
- If several scenario areas describe the same
  underlying behavior, treat them as one behavior.
- Do not duplicate another scenario using only
  different wording.
- Steps and expected results must correspond to
  the selected scenario.

============================================================
SOURCE GROUNDING RULES
============================================================

1. Use ONLY facts explicitly supported by the
   documentation.

2. Do NOT invent APIs, functions, protocols,
   register addresses, hardware behavior,
   limits, thresholds, timings, temperatures,
   pressures, voltages, or other numeric values.

3. The documentation explicitly defines 25% of LFL
   as the typical A2L leak threshold.
   This value may be used.

4. The Modbus documentation explicitly defines
   registers 30001 through 30008 and status
   values 0 and 1.
   These values may be used.

5. For configurable thresholds where no number is
   documented, use wording such as:

   "configured threshold"

   "below freezing"

   "configured safety limit"

6. Do NOT convert units.

7. Do NOT turn "below freezing" into a Celsius
   or Fahrenheit value.

8. Do NOT invent example values such as:

   10 minutes
   150°F
   10 bar
   20°C

   or any other undocumented values.

9. Test Data may be an empty string when the source
   provides no concrete input value.

10. Never invent data merely to populate Test Data.

11. Do NOT use "N/A".

12. Do NOT create artificial variants by adding
    phrases such as "with sensors", "with
    communication", or "with monitoring" to an
    otherwise identical scenario.

13. Every test must represent a genuinely different
    documented behavior.

14. Prefer source-specific scenarios over generic
    QA scenarios.

15. Expected results must be directly supported
    by the source.

16. Keep steps directly related to the selected
    scenario.

17. Tests must be suitable for later conversion
    into pytest.

============================================================
IMPORTANT NUMERIC RULE
============================================================

If the source does not define a numeric value,
DO NOT invent one.

============================================================
IMPORTANT FEATURE RULE
============================================================

The "feature" field MUST be exactly:

{domain}

Do not rename, shorten, split, or reinterpret
the feature.

============================================================
IMPORTANT SCENARIO RULE
============================================================

The "scenario" field must describe the specific
documented behavior being tested.

Do NOT use generic scenario names such as:

- system behavior
- normal test
- functional test
- controller test
- communication test

unless that wording genuinely represents the
documented behavior.

============================================================
OUTPUT REQUIREMENTS
============================================================

Return JSON ONLY.

Return exactly {count} test case objects.

Each object must contain:

[
  {{
    "test_case_id": "TEMP_ID",
    "requirement": "...",
    "feature": "{domain}",
    "scenario": "...",
    "steps": [
      "...",
      "...",
      "..."
    ],
    "expected_result": "...",
    "test_data": "...",
    "automation_candidate": "YES",
    "tool": "Pytest"
  }}
]

Do not include markdown fences.

Do not include explanations before or after
the JSON.
"""


# ============================================================
# JSON PARSING
# ============================================================

def parse_json_response(response):

    response = str(response).strip()

    response = re.sub(
        r"```(?:json)?",
        "",
        response,
        flags=re.IGNORECASE,
    ).strip()

    try:

        data = json.loads(response)

        if isinstance(
            data,
            (list, dict),
        ):
            return data

    except json.JSONDecodeError:
        pass

    array_match = re.search(
        r"\[[\s\S]*\]",
        response,
    )

    if array_match:

        try:

            data = json.loads(
                array_match.group()
            )

            if isinstance(
                data,
                list,
            ):
                return data

        except json.JSONDecodeError:
            pass

    decoder = json.JSONDecoder()

    objects = []

    position = 0

    while position < len(response):

        match = re.search(
            r"\{",
            response[position:],
        )

        if not match:
            break

        start = (
            position
            + match.start()
        )

        try:

            obj, end = decoder.raw_decode(
                response[start:]
            )

            if isinstance(
                obj,
                dict,
            ):
                objects.append(obj)

            position = (
                start
                + end
            )

        except json.JSONDecodeError:

            position = start + 1

    if objects:
        return objects

    raise ValueError(
        "Llama did not return valid JSON."
    )


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):

    return re.sub(
        r"\s+",
        " ",
        str(text).strip().lower(),
    )


def test_case_is_source_grounded(
    test_case,
):

    fields = [
        test_case.get(
            "requirement",
            "",
        ),

        test_case.get(
            "feature",
            "",
        ),

        test_case.get(
            "scenario",
            "",
        ),

        test_case.get(
            "steps",
            "",
        ),

        test_case.get(
            "expected_result",
            "",
        ),

        test_case.get(
            "expected_results",
            "",
        ),

        test_case.get(
            "test_data",
            "",
        ),
    ]

    combined = " ".join(
        str(value)
        for value in fields
        if value is not None
    )

    if contains_unsupported_number(
        combined
    ):
        return False

    return True


def normalize_test_case(
    test_case: Any,
    canonical_feature: str,
) -> dict[str, Any] | None:

    if not isinstance(
        test_case,
        dict,
    ):
        return None

    test_case_id = (
        test_case.get(
            "test_case_id"
        )
        or test_case.get(
            "id"
        )
        or ""
    )

    requirement = str(
        test_case.get(
            "requirement",
            "",
        )
    ).strip()

    feature = str(
        test_case.get(
            "feature",
            "",
        )
    ).strip()

    scenario = str(
        test_case.get(
            "scenario",
            "",
        )
    ).strip()

    expected_result = str(
        test_case.get(
            "expected_result",
            test_case.get(
                "expected_results",
                "",
            ),
        )
    ).strip()

    test_data = test_case.get(
        "test_data",
        "",
    )

    steps = test_case.get(
        "steps",
        [],
    )

    if not isinstance(
        steps,
        list,
    ):
        steps = [
            str(steps)
        ]

    cleaned_steps = []

    for step in steps:

        if isinstance(
            step,
            dict,
        ):

            description = (
                step.get(
                    "description"
                )
                or step.get(
                    "action"
                )
                or ""
            )

            if description:

                cleaned_steps.append(
                    str(
                        description
                    ).strip()
                )

        else:

            text = str(
                step
            ).strip()

            if text:

                cleaned_steps.append(
                    text
                )

    if (
        not test_case_id
        or not requirement
        or not feature
        or not scenario
        or not cleaned_steps
        or not expected_result
    ):
        return None

    normalized = {
        "test_case_id": str(
            test_case_id
        ).strip(),

        "requirement": requirement,

        "feature": feature,

        "scenario": scenario,

        "steps": cleaned_steps,

        "expected_result": expected_result,

        "test_data": test_data,

        "automation_candidate": str(
            test_case.get(
                "automation_candidate",
                "YES",
            )
        ),

        "tool": str(
            test_case.get(
                "tool",
                "Pytest",
            )
        ),
    }

    if not test_case_is_source_grounded(
        normalized
    ):
        return None

    return {
        "Test Case ID": normalized[
            "test_case_id"
        ],

        "Requirement": normalized[
            "requirement"
        ],

        "Feature": normalized[
            "feature"
        ],

        "Scenario": normalized[
            "scenario"
        ],

        "Steps": "\n".join(
            f"{index}. {step}"
            for index, step
            in enumerate(
                normalized[
                    "steps"
                ],
                start=1,
            )
        ),

        "Expected Results": normalized[
            "expected_result"
        ],

        "Test Data": (
            json.dumps(
                test_data,
                ensure_ascii=False,
            )
            if isinstance(
                test_data,
                (dict, list),
            )
            else str(
                test_data
            ).strip()
        ),

        "Automation Candidate": normalized[
            "automation_candidate"
        ],

        "Tool": normalized[
            "tool"
        ],
    }


# ============================================================
# DEDUPLICATION
# ============================================================

def deduplicate_test_cases(
    test_cases,
):

    unique = []

    seen = set()

    for test_case in test_cases:

        key = (
            normalize_text(
                test_case[
                    "Requirement"
                ]
            ),

            normalize_text(
                test_case[
                    "Feature"
                ]
            ),

            normalize_text(
                test_case[
                    "Scenario"
                ]
            ),
        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(
            test_case
        )

    return unique


# ============================================================
# ID ASSIGNMENT
# ============================================================

def assign_ids(
    test_cases,
):

    assigned = []

    for index, test_case in enumerate(
        test_cases,
        start=1,
    ):

        item = dict(
            test_case
        )

        item[
            "Test Case ID"
        ] = f"TC_AI_{index:03d}"

        assigned.append(
            item
        )

    return assigned


# ============================================================
# TRACEABILITY
# ============================================================

def create_traceability(
    df_tests,
):

    rows = []

    for _, row in df_tests.iterrows():

        rows.append(
            {
                "Test Case ID":
                    row["Test Case ID"],

                "Requirement":
                    row["Requirement"],

                "Feature":
                    row["Feature"],

                "Scenario":
                    row["Scenario"],

                "Source Grounded":
                    "YES",

                "Automation Candidate":
                    row[
                        "Automation Candidate"
                    ],

                "Tool":
                    row["Tool"],
            }
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# AUTOMATION CANDIDATES
# ============================================================

def automation_candidates(
    df_tests,
):

    rows = []

    for _, row in df_tests.iterrows():

        rows.append(
            {
                "Test Case ID":
                    row["Test Case ID"],

                "Feature":
                    row["Feature"],

                "Scenario":
                    row["Scenario"],

                "Automation Candidate":
                    row[
                        "Automation Candidate"
                    ],

                "Tool":
                    row["Tool"],
            }
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# AI GENERATION FOR ONE BATCH
# ============================================================

def generate_batch(
    llm,
    vector_db,
    domain_plan,
    existing_scenarios=None,
):

    domain = domain_plan[
        "domain"
    ]

    count = domain_plan[
        "count"
    ]

    existing_scenarios = (
        existing_scenarios
        or []
    )

    print(
        f"\nGenerating {count} AI test cases "
        f"for: {domain}"
    )

    context = retrieve_context(
        vector_db,
        domain,
        k=TOP_K_RAG,
    )

    prompt = build_prompt(
        domain_plan,
        context,
        count,
        existing_scenarios=existing_scenarios,
    )

    try:

        response = llm.invoke(
            prompt
        )

        data = parse_json_response(
            response
        )

        if isinstance(
            data,
            dict,
        ):

            data = data.get(
                "test_cases",
                [],
            )

        if not isinstance(
            data,
            list,
        ):

            raise ValueError(
                "Expected JSON array "
                "of test cases."
            )

        normalized = []

        rejected_grounding = 0

        for item in data:

            test_case = normalize_test_case(
    item,
    domain,
)

            if test_case:

                # Canonical feature rule.
                test_case[
                    "Feature"
                ] = domain

                normalized.append(
                    test_case
                )

            else:

                rejected_grounding += 1

        normalized = deduplicate_test_cases(
            normalized
        )

        print(
            "Valid unique source-grounded "
            f"cases returned: {len(normalized)}"
        )

        if rejected_grounding:

            print(
                "Rejected invalid/ungrounded "
                f"cases: {rejected_grounding}"
            )

        return normalized

    except Exception as error:

        print(
            f"AI batch failed for {domain}: "
            f"{error}"
        )

        return []


# ============================================================
# MAIN EXCEL GENERATION
# ============================================================

def generate_excel():

    print(
        "AI Test Generation Started..."
    )

    vector_db = create_vector_store()

    llm = OllamaLLM(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        timeout=60,
    )

    all_test_cases = []

    MAX_ATTEMPTS_PER_DOMAIN = 8

    for domain_plan in DOMAIN_PLANS:

        domain = domain_plan[
            "domain"
        ]

        target_count = domain_plan[
            "count"
        ]

        print(
            f"\n{'=' * 70}"
        )

        print(
            f"Generating domain: {domain}"
        )

        print(
            f"Target cases: {target_count}"
        )

        print(
            f"{'=' * 70}"
        )

        domain_cases = []

        attempt = 0

        while (
            len(domain_cases)
            < target_count
            and attempt
            < MAX_ATTEMPTS_PER_DOMAIN
        ):

            attempt += 1

            remaining = (
                target_count
                - len(domain_cases)
            )

            print(
                f"\nDomain attempt {attempt}: "
                f"{len(domain_cases)}/"
                f"{target_count} complete; "
                f"requesting {remaining} more."
            )

            existing_scenarios = [
                case[
                    "Scenario"
                ]
                for case in domain_cases
            ]

            request_plan = dict(
                domain_plan
            )

            request_plan[
                "count"
            ] = remaining

            batch = generate_batch(
                llm,
                vector_db,
                request_plan,
                existing_scenarios=existing_scenarios,
            )

            if not batch:

                print(
                    "No valid cases returned; "
                    "requesting replacements."
                )

                continue

            combined = (
                domain_cases
                + batch
            )

            domain_cases = (
                deduplicate_test_cases(
                    combined
                )
            )

            domain_cases = (
                domain_cases[
                    :target_count
                ]
            )

            print(
                f"Domain progress: "
                f"{len(domain_cases)}/"
                f"{target_count}"
            )

        if len(domain_cases) != target_count:

            raise RuntimeError(
                f"Unable to generate exactly "
                f"{target_count} unique, "
                f"source-grounded cases for "
                f"domain '{domain}'. "
                f"Generated "
                f"{len(domain_cases)} after "
                f"{attempt} attempts."
            )

        print(
            f"\nCompleted domain '{domain}': "
            f"{len(domain_cases)} cases"
        )

        all_test_cases.extend(
            domain_cases
        )

    print(
        "\nAI-generated cases before "
        "final deduplication:",
        len(all_test_cases),
    )

    all_test_cases = (
        deduplicate_test_cases(
            all_test_cases
        )
    )

    all_test_cases = assign_ids(
        all_test_cases
    )

    df_tests = pd.DataFrame(
        all_test_cases
    )

    if df_tests.empty:

        raise RuntimeError(
            "No valid AI test cases "
            "were generated."
        )

    # IMPORTANT:
    # Calculate this BEFORE using expected_total.
    #
    # This works for both:
    #   5 domains x 20 = 100
    #
    # and the smoke test:
    #   5 domains x 2 = 10

    expected_total = sum(
        plan["count"]
        for plan in DOMAIN_PLANS
    )

    if len(df_tests) != expected_total:

        raise RuntimeError(
            f"Expected exactly "
            f"{expected_total} test cases, "
            f"but generated "
            f"{len(df_tests)}."
        )

    trace_df = create_traceability(
        df_tests
    )

    auto_df = automation_candidates(
        df_tests
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with pd.ExcelWriter(
        OUTPUT_FILE
    ) as writer:

        df_tests.to_excel(
            writer,
            sheet_name="Test Cases",
            index=False,
        )

        trace_df.to_excel(
            writer,
            sheet_name="Traceability",
            index=False,
        )

        auto_df.to_excel(
            writer,
            sheet_name="Automation",
            index=False,
        )

    print(
        "\nFile created:",
        os.path.abspath(
            OUTPUT_FILE
        ),
    )

    print(
        "Total unique tests:",
        len(df_tests),
    )

    print(
        "\nTest distribution:"
    )

    print(
        df_tests[
            "Feature"
        ].value_counts()
    )

    return df_tests


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    generate_excel()
