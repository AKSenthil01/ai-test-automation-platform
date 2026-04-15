import time
import random
from utils.logger import get_logger

logger = get_logger("BACNET")


def run_bacnet():

    print("🚀 BACnet Simulator Running...")

    objects = ["AI", "AO", "AV", "BI", "BO"]

    for _ in range(20):

        obj = random.choice(objects)

        if random.random() < 0.8:
            logger.info(f"{obj} ReadProperty SUCCESS")
        else:
            logger.error(f"{obj} ReadProperty FAILED")

        if random.random() < 0.2:
            logger.error("BACnet MSTP timeout")

        time.sleep(1)