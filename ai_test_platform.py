import streamlit as st
import pandas as pd
import os
from simulators.system_simulator import generate_logs_fast
from rag_engine.failure_analyzer import analyze_failure
from test_generation.generate_tests_from_docs import (
    create_traceability,
    automation_candidates, generate_excel
)

if "pytest_code" not in st.session_state:
    st.session_state["pytest_code"] = ""

st.title("AI Test Automation Platform")

excel_file = "ai_generated_test_suite.xlsx"

# ---------------------------------------------
# LOAD EXISTING DATA
# ---------------------------------------------
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file, sheet_name="Test Cases")
    st.session_state["test_cases"] = df
    st.success("Loaded existing test cases")

# ---------------------------------------------
# GENERATE TEST CASES
# ---------------------------------------------
if st.button("Generate Test Cases", key="generate_tests_btn"):
    with st.spinner("Generating AI Test Cases..."):

        df = generate_excel()

        st.session_state["test_cases"] = df

        rtm = create_traceability(df)
        auto = automation_candidates(df)

        with pd.ExcelWriter(excel_file) as writer:
            df.to_excel(writer, sheet_name="Test Cases", index=False)
            rtm.to_excel(writer, sheet_name="Traceability", index=False)
            auto.to_excel(writer, sheet_name="Automation", index=False)

        st.success(f"Generated {len(df)} test cases")


# ---------------------------------------------
# DISPLAY TEST CASES
# ---------------------------------------------
if "test_cases" in st.session_state:

    st.subheader("Generated Test Cases")
    st.dataframe(st.session_state["test_cases"])

# ---------------------------------------------
# GENERATE PYTEST
# ---------------------------------------------
if "test_cases" in st.session_state:

    if st.button("Generate Pytest Scripts", key="pytest_btn"):
        with st.spinner("Generating AI Pytest scripts..."):

            from core.fast_pytest_generator import generate_pytest_fast

            input_file = "ai_generated_test_suite.xlsx"

            if not os.path.exists(input_file):
                st.error("❌ Test case Excel not found. Generate test cases first.")
            else:
                # Step 2: Generate pytest code
                code = generate_pytest_fast(input_file)

                # Step 3: Store in session
                st.session_state["pytest_code"] = code

                st.success("✅ Pytest scripts generated successfully!")

if "pytest_code" in st.session_state:

    st.subheader("🧪 Generated Pytest Script")

    st.code(st.session_state["pytest_code"], language="python")

# ---------------------------------------------
# Download Pytest Scripts
# ---------------------------------------------
st.download_button(
    label="⬇️ Download Pytest Script",
    data=st.session_state["pytest_code"],
    file_name="test_ai_fast.py",
    mime="text/plain"
)

# ---------------------------------------------
# AI Log Analyzer
# ---------------------------------------------

st.subheader("AI Log Analyzer")

# ✅ Init STATE
if "logs" not in st.session_state:
    st.session_state["logs"] = ""

# ---------------------------------------------
# BUTTON: Generate Logs
# ---------------------------------------------
if st.button("Generate Simulated Logs", key="generate_logs_btn"):

    with st.spinner("Generating logs..."):

        logs = generate_logs_fast()   # ✅ FAST VERSION

        st.session_state["logs"] = logs

    st.success(f"Logs generated! Length: {len(logs)}")

# ---------------------------------------------
# DISPLAY LOGS
# ---------------------------------------------
if st.session_state["logs"]:

    st.text_area(
        "System Logs",
        st.session_state["logs"],   # ✅ DIRECT binding
        height=300,
        key="logs_display"
    )

else:
    st.info("No logs yet. Click 'Generate Simulated Logs'")

# ---------------------------------------------
# # Analyze logs
# ---------------------------------------------
if st.button("Analyze Failure", key="analyze_failure_btn"):

    if "test_cases" not in st.session_state:
        st.warning("Generate test cases first")

    elif st.session_state["logs"] == "":
        st.warning("Generate logs first")

    else:
        with st.spinner("Analyzing logs..."):

            result = analyze_failure(
                st.session_state["logs"],          # ✅ log_text
                st.session_state["test_cases"]     # ✅ test_cases_df
            )

        st.subheader("Analysis Result")
        st.json(result)

st.download_button(
    "⬇️ Download Logs",
    data=st.session_state["logs"],
    file_name="system_logs.txt"
)