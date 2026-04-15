import random
import time
from datetime import datetime


# ---------------------------------------------
# Helper: Timestamp
# ---------------------------------------------
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------
# Defrost Logic Simulation
# ---------------------------------------------
def simulate_defrost():
    logs = []

    temp = random.randint(-12, -5)

    logs.append(f"{get_timestamp()} | CONTROLLER | INFO | Defrost triggered at temp={temp}")

    if random.random() < 0.3:
        logs.append(f"{get_timestamp()} | CONTROLLER | ERROR | Defrost heater failure")
    else:
        logs.append(f"{get_timestamp()} | CONTROLLER | INFO | Defrost completed successfully")

    return logs


# ---------------------------------------------
# A2L Leak Detection Simulation
# ---------------------------------------------
def simulate_a2l():
    logs = []

    gas_level = random.randint(0, 100)

    logs.append(f"{get_timestamp()} | SENSOR | INFO | Gas level={gas_level} ppm")

    if gas_level > 60:
        logs.append(f"{get_timestamp()} | CONTROLLER | ALARM | A2L Leak Detected")
    else:
        logs.append(f"{get_timestamp()} | CONTROLLER | INFO | Gas levels normal")

    return logs


# ---------------------------------------------
# Controller Operation Simulation
# ---------------------------------------------
def simulate_controller():
    logs = []

    temp = random.randint(-10, 10)

    logs.append(f"{get_timestamp()} | CONTROLLER | INFO | Temperature reading={temp}")

    if temp > 5:
        logs.append(f"{get_timestamp()} | CONTROLLER | INFO | Compressor ON")
    elif temp < -8:
        logs.append(f"{get_timestamp()} | CONTROLLER | INFO | Defrost cycle initiated")
    else:
        logs.append(f"{get_timestamp()} | CONTROLLER | INFO | System stable")

    return logs


# ---------------------------------------------
# Modbus Simulation
# ---------------------------------------------
def simulate_modbus():
    logs = []

    register = random.randint(1, 20)

    if random.random() < 0.2:
        logs.append(f"{get_timestamp()} | MODBUS | ERROR | CRC error on register {register}")
    else:
        logs.append(f"{get_timestamp()} | MODBUS | INFO | Read register {register} SUCCESS")

    return logs


# ---------------------------------------------
# BACnet Simulation
# ---------------------------------------------
def simulate_bacnet():
    logs = []

    if random.random() < 0.2:
        logs.append(f"{get_timestamp()} | BACNET | ERROR | Timeout on ReadProperty")
    else:
        logs.append(f"{get_timestamp()} | BACNET | INFO | ReadProperty SUCCESS")

    return logs


# ---------------------------------------------
# MAIN SYSTEM SIMULATOR
# ---------------------------------------------
# def generate_logs():
#
#     logs = []
#
#     # Run multiple cycles (like real system)
#     for _ in range(5):
#
#         logs.extend(simulate_controller())
#         logs.extend(simulate_defrost())
#         logs.extend(simulate_a2l())
#         logs.extend(simulate_modbus())
#         logs.extend(simulate_bacnet())
#
#         time.sleep(0.1)  # simulate time gap
#
#     return "\n".join(logs)

# def generate_logs():
#
#     logs = []
#
#     for _ in range(2):   # 🔥 reduced cycles
#
#         logs.extend(simulate_controller())
#         logs.extend(simulate_defrost())
#         logs.extend(simulate_a2l())
#         logs.extend(simulate_modbus())
#         logs.extend(simulate_bacnet())
#
#     return "\n".join(logs)
def generate_logs_fast():
    logs = []

    for i in range(50):   # 🔥 reduce size (was 500+ maybe)

        logs.append(f"{i} | CONTROLLER | INFO | Defrost active at temp=-10")
        logs.append(f"{i} | MODBUS | INFO | Read register {i} SUCCESS")
        logs.append(f"{i} | BACNET | INFO | AV ReadProperty SUCCESS")

        # Inject one failure
        if i == 25:
            logs.append(f"{i} | MODBUS | ERROR | CRC error at register {i}")

    return "\n".join(logs)