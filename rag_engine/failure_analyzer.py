import json
from langchain_ollama import OllamaLLM


def analyze_failure(log_text, test_cases_df):

    llm = OllamaLLM(
        model="llama3:8b",
        temperature=0,
        timeout=20
    )

    # Convert test cases to string (LIMIT for speed)
    test_context = test_cases_df.head(20).to_string()

    prompt = f"""
    You are an expert HVAC + Embedded system failure analyst.

    Analyze the following system logs:

    {log_text}

    And correlate with these test cases:

    {test_context}

    Identify:
    1. Root cause of failure
    2. Affected module (Controller / BACnet / Modbus / Sensor)
    3. Related test case IDs
    4. Severity (Low / Medium / High)
    5. Suggested fix

    Return STRICT JSON:

    {{
        "root_cause": "",
        "module": "",
        "test_cases": [],
        "severity": "",
        "fix": ""
    }}
    """

    try:
        response = llm.invoke(prompt)

        response = response.strip()
        start = response.find("{")
        end = response.rfind("}") + 1

        return json.loads(response[start:end])

    except Exception as e:
        return {
            "root_cause": "AI failed",
            "module": "Unknown",
            "test_cases": [],
            "severity": "Unknown",
            "fix": str(e)
        }