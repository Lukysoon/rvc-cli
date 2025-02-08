
import logging
import os 

def get_logger(path_to_log_file):

    # Create a namespaced logger for the current module
    logger = logging.getLogger(__name__) # Logger named `utils.module_a`
    logger.setLevel(logging.INFO)
    # File handler
    file_handler = logging.FileHandler(path_to_log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s"))
    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    # Add handlers to the logger
    logger.addHandler(file_handler)
    # Ensure logs are propagated to the root logger
    logger.propagate = False
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.info("TRAINING LOG")

    return logger