from ai_engine.failure_analyzer import FailureAnalyzer
from ai_engine.logger import get_logger

logger = get_logger(__name__)


def main():

    log_text = """
BACnet communication timeout.

Controller restarted unexpectedly.

Temperature sensor returned invalid values.

Compressor stopped.

Alarm generated.
"""

    logger.info("Starting Failure Analysis...")

    analyzer = FailureAnalyzer()

    result = analyzer.analyze(log_text)

    logger.info("Failure Analysis Completed")

    print("\nRESULT\n")

    print(result)


if __name__ == "__main__":
    main()