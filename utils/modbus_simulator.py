import time
import random
from utils.logger import get_logger

logger = get_logger("MODBUS")


def run_modbus():

    print("🚀 Modbus Simulator Running...")

    for _ in range(20):

        register = random.randint(0, 10)

        if random.random() < 0.8:
            logger.info(f"Read register {register} SUCCESS")
        else:
            logger.error(f"CRC error at register {register}")

        if random.random() < 0.1:
            logger.error("Modbus timeout")

        time.sleep(1)