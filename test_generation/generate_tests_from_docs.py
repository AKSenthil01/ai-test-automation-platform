import pd
import os
import pandas as pd
import json
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter


# ---------------------------------------------
# STEP 1: Load documents
# ---------------------------------------------
def load_documents():

    files = [
        "data/defrost_logic_spec.txt",
        "data/a2l_leak_detection_spec.txt",
        "data/controller_manual.txt",
        "data/modbus_register_map.txt"
    ]

    docs = []

    for f in files:
        if os.path.exists(f):
            with open(f, "r", encoding="utf-8") as file:
                docs.append(file.read())

    return docs


# ---------------------------------------------
# STEP 2: Create Vector DB (FAST)
# ---------------------------------------------
from langchain_community.vectorstores import FAISS
import os

VECTOR_PATH = "vector_store/faiss_index"


def create_vector_store():

    # ✅ If already exists → load
    if os.path.exists(VECTOR_PATH):
        print("⚡ Loading existing vector DB...")
        return FAISS.load_local(
            VECTOR_PATH,
            OllamaEmbeddings(model="llama3"),
            allow_dangerous_deserialization=True
        )

    # ❌ First time → create
    print("🚀 Creating vector DB (one-time)...")

    docs = load_documents()

    splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30
    )

    chunks = []
    for d in docs:
        chunks.extend(splitter.split_text(d))

    embeddings = OllamaEmbeddings(model="llama3")

    db = FAISS.from_texts(chunks, embeddings)

    # ✅ SAVE to disk
    db.save_local(VECTOR_PATH)

    print("✅ Vector DB saved at:", VECTOR_PATH)

    return db

# ---------------------------------------------
# STEP 3: FAST RAG (ONLY ONE AI CALL)
# ---------------------------------------------
def generate_base_ai_data(vector_db):

    llm = OllamaLLM(
        model="llama3:8b",
        temperature=0,
        timeout=20
    )

    print("🚀 Retrieving minimal context...")

    queries = [
        "defrost logic scenarios",
        "A2L leak detection scenarios",
        "controller operations and alarms",
        "Modbus register communication scenarios"
    ]

    docs = []

    for q in queries:
        docs.extend(vector_db.similarity_search(q, k=3))  # 3 per domain


    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    You are a senior HVAC + Embedded + Protocol test engineer.

    Based on the documentation below:

    {context}

    Generate test design covering ALL areas:

    1. Defrost logic
    2. A2L leak detection
    3. Controller operations (compressor, alarms, sensors)
    4. Modbus communication

    Generate:
    - 6 requirements
    - 5 features
    - 6 scenarios
    - 3 edge cases

    Return STRICT JSON ONLY:
    {{
        "requirements": [],
        "features": [],
        "scenarios": [],
        "edge_cases": []
    }}
    """

    try:
        response = llm.invoke(prompt)

        response = response.strip()
        start = response.find("{")
        end = response.rfind("}") + 1

        return json.loads(response[start:end])

    except Exception as e:
        print("❌ AI failed, using fallback:", e)

        return {
            "requirements": ["Compressor control"],
            "features": ["Cooling"],
            "scenarios": ["Normal"],
            "edge_cases": ["Boundary"]
        }


# ---------------------------------------------
# STEP 4: Python Scaling
# ---------------------------------------------
def expand_and_generate(ai_data):

    requirements = ai_data.get("requirements", [])
    features = ai_data.get("features", [])
    scenarios = ai_data.get("scenarios", [])
    edge_cases = ai_data.get("edge_cases", [])

    test_cases = []
    test_id = 1

    print("⚡ Generating test cases (Python scaling)...")

    for req in requirements:
        for feature in features:
            for scenario in scenarios:
                # ✅ CLEAN AI OUTPUT HERE
                requirement_text = req.get("description", str(req))
                feature_text = feature.get("name") or feature.get("description") or str(feature)
                scenario_text = scenario.get("description") or str(scenario)

                tc_id = f"TC_AI_{test_id:03d}"

                test_cases.append({
                    "Test Case ID": tc_id,
                    "Requirement": requirement_text,
                    "Steps": f"""
    1. Configure controller
    2. Trigger: {requirement_text}
    3. Validate: {feature_text}
    4. Apply: {scenario_text}
    """,
                    "Expected Results": f"{feature_text} works correctly under {scenario_text}"
                })

                test_id += 1
    return pd.DataFrame(test_cases)


# ---------------------------------------------
# STEP 5: Traceability
# ---------------------------------------------
def create_traceability(df):
    return df[["Test Case ID", "Requirement"]]


# ---------------------------------------------
# STEP 6: Automation
# ---------------------------------------------
def automation_candidates(df):

    df["Automation Candidate"] = "YES"
    df["Tool"] = "Pytest"

    return df[["Test Case ID", "Requirement", "Automation Candidate", "Tool"]]


# ---------------------------------------------
# STEP 7: Excel Output
# ---------------------------------------------
def generate_excel():

    print("🚀 FAST RAG Test Generation Started...")

    db = create_vector_store()

    ai_data = generate_base_ai_data(db)

    df_tests = expand_and_generate(ai_data)

    trace_df = create_traceability(df_tests)
    auto_df = automation_candidates(df_tests)

    output =  "ai_generated_test_suite.xlsx"

    with pd.ExcelWriter(output) as writer:
        df_tests.to_excel(writer, "Test Cases", index=False)
        trace_df.to_excel(writer, "Traceability", index=False)
        auto_df.to_excel(writer, "Automation", index=False)

    print("✅ File created:", os.path.abspath(output))
    print("📊 Total tests:", len(df_tests))
    return df_tests


# ---------------------------------------------
# MAIN
# ---------------------------------------------
if __name__ == "__main__":
    generate_excel()

