def simple_analyze(log_text):

    result = {
        "root_cause": "Unknown",
        "module": "Unknown",
        "severity": "Low"
    }

    log_text = log_text.lower()

    if "modbus timeout" in log_text:
        result["root_cause"] = "Modbus communication timeout"
        result["module"] = "Modbus"
        result["severity"] = "High"

    elif "bacnet communication lost" in log_text:
        result["root_cause"] = "BACnet network failure"
        result["module"] = "BACnet"
        result["severity"] = "High"

    elif "sensor failure" in log_text:
        result["root_cause"] = "Sensor malfunction"
        result["module"] = "Controller"
        result["severity"] = "Medium"

    elif "alarm" in log_text:
        result["root_cause"] = "System alarm triggered"
        result["module"] = "Controller"
        result["severity"] = "Medium"

    return result