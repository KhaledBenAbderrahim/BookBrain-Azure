import logging
import sys

def setup_logger(name, level=logging.INFO):
    """Setup a logger that logs to stdout only"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger
