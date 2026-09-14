from datetime import datetime


class PipelineLogger:
    WIDTH = 80

    @staticmethod
    def line():
        print("=" * PipelineLogger.WIDTH)

    @staticmethod
    def section(title):
        print()
        PipelineLogger.line()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {title}")
        PipelineLogger.line()

    @staticmethod
    def info(message):
        print(f"[INFO] {message}")

    @staticmethod
    def success(message):
        print(f"[SUCCESS] {message}")

    @staticmethod
    def warning(message):
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")

    @staticmethod
    def blank():
        print()

    @staticmethod
    def data(title, value):
        print(f"{title}:")
        print(value)
        print()


def get_logger(name=None):
    """
    Backward compatibility wrapper.

    Existing code can continue using:
        logger = get_logger(__name__)

    Returns the PipelineLogger class.
    """
    return PipelineLogger