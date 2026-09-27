from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.e2e_runner import run_excel_to_pytest_pipeline
from core.failure_demo import create_simulated_failure, analyze_failure
from test_generation.generate_tests_from_docs import generate_excel


WORKBOOK = BASE_DIR / "generated_tests.xlsx"
INTERVIEW_WORKBOOK = BASE_DIR / "generated_tests_interview_ready_50.xlsx"
EXECUTION_LOG = BASE_DIR / "reports" / "excel_pytest_execution.log"
FAILURE_LOG = BASE_DIR / "reports" / "simulated_failure.log"


st.set_page_config(
    page_title="AI HVAC Test Automation Platform",
    page_icon="??",
    layout="wide",
)


st.title("AI HVAC Test Automation Platform")
st.caption(
    "AI-assisted HVAC test generation, pytest automation, "
    "deterministic simulation, and failure analysis"
)


# -------------------------------------------------------------------
# Test Case Generation
# -------------------------------------------------------------------

st.header("1. Generate Test Cases")

st.write(
    "Generate HVAC test cases from the project specifications "
    "using the existing RAG + LLM test-generation pipeline."
)

if st.button("Generate Test Cases", type="primary"):

    with st.spinner("Generating HVAC test cases..."):

        try:
            generate_excel()

            st.success("Test-case generation completed.")

            if WORKBOOK.exists():
                st.info(f"Generated workbook: {WORKBOOK.name}")

            if INTERVIEW_WORKBOOK.exists():
                st.info(
                    f"Validated interview-ready workbook: "
                    f"{INTERVIEW_WORKBOOK.name}"
                )

        except Exception as exc:
            st.error(f"Test-case generation failed: {exc}")


st.divider()


# -------------------------------------------------------------------
# Excel ? Pytest
# -------------------------------------------------------------------

st.header("2. Generate & Execute Pytest")

st.write(
    "Validate the Excel test cases, generate deterministic pytest "
    "automation for supported scenarios, and execute the generated tests "
    "against the refrigeration-controller simulator."
)

if st.button("Generate & Execute Tests", type="primary"):

    with st.spinner("Running Excel ? pytest pipeline..."):

        try:
            result = run_excel_to_pytest_pipeline()

            generation = result["generation"]
            execution = result["execution"]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Generation",
                    "PASSED" if generation["success"] else "FAILED",
                )

            with col2:
                st.metric(
                    "Execution",
                    (
                        "PASSED"
                        if execution and execution["success"]
                        else "FAILED"
                    ),
                )

            with col3:
                st.metric(
                    "Generated Test File",
                    "YES" if generation["generated_test"] else "NO",
                )

            st.subheader("Pipeline Output")

            st.code(
                generation["stdout"],
                language="text",
            )

            if execution:
                st.subheader("Pytest Results")

                st.code(
                    execution["output"],
                    language="text",
                )

            if result["success"]:
                st.success("Excel ? pytest pipeline completed successfully.")
            else:
                st.error(
                    f"Pipeline failed during: {result['stage']}"
                )

            if EXECUTION_LOG.exists():
                st.info(
                    f"Execution log: {EXECUTION_LOG.relative_to(BASE_DIR)}"
                )

        except Exception as exc:
            st.error(f"Pipeline execution failed: {exc}")


st.divider()


# -------------------------------------------------------------------
# Failure Analysis
# -------------------------------------------------------------------

st.header("3. Analyze Failure")

st.write(
    "Create a deterministic simulated HVAC failure and analyze it "
    "using the existing RAG + LLM failure-analysis pipeline."
)

if st.button("Generate & Analyze Failure", type="primary"):

    with st.spinner("Creating simulated failure..."):

        try:
            failure_log = create_simulated_failure()

            st.subheader("Simulated Failure Log")

            st.code(
                failure_log,
                language="text",
            )

            with st.spinner("Running failure analysis..."):

                result = analyze_failure(failure_log)

            st.subheader("Failure Analysis")

            if isinstance(result, dict):

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Root Cause**")
                    st.write(result.get("root_cause", ""))

                    st.write("**Component**")
                    st.write(result.get("component", ""))

                    st.write("**Category**")
                    st.write(result.get("category", ""))

                with col2:
                    st.write("**Failure Type**")
                    st.write(result.get("failure_type", ""))

                    st.write("**Recommendation**")
                    st.write(result.get("recommendation", ""))

                st.write("**Related Tests**")
                st.write(result.get("related_tests", []))

            else:
                st.json(result)

            if FAILURE_LOG.exists():
                st.info(
                    f"Failure log: {FAILURE_LOG.relative_to(BASE_DIR)}"
                )

        except Exception as exc:
            st.error(f"Failure analysis failed: {exc}")


st.divider()

st.caption(
    "Interview/demo architecture: RAG + LLM ? validated Excel ? "
    "pytest generation ? deterministic controller simulator ? "
    "failure analysis."
)
