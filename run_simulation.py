from utils.controller_simulator import run_controller
from utils.modbus_simulator import run_modbus
from utils.bacnet_simulator import run_bacnet
import threading


def start_simulation():

    t1 = threading.Thread(target=run_controller)
    t2 = threading.Thread(target=run_modbus)
    t3 = threading.Thread(target=run_bacnet)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("✅ Simulation Completed")


if __name__ == "__main__":
    start_simulation()