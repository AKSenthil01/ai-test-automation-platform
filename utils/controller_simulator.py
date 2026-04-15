import time
import random
from utils.logger import get_logger

logger = get_logger("CONTROLLER")


def run_controller():

    print("🚀 Controller Simulator Running...")

    for _ in range(20):

        temp = random.randint(-10, 10)

        # Defrost logic
        if temp < -5:
            logger.info(f"Defrost activated at temp={temp}")

        # Compressor logic
        if temp < 5:
            logger.info(f"Compressor ON at temp={temp}")
        else:
            logger.info(f"Compressor OFF at temp={temp}")

        # Sensor failure
        if random.random() < 0.2:
            logger.error("Temperature sensor failure detected")

        time.sleep(1)