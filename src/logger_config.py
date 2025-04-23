# src/logger_config.py
"""
Format-Preserving Encryption (FPE) is a class of encryption algorithms where
the ciphertext has the same format as the plaintext.
"""
import logging

from colorlog import ColoredFormatter


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Return a colourised logging.Logger instance.
    :param name: Logger name, defaults to module’s __name__
    :return: Configured :class:logging.Logger
    """
    log_colours = {
        "INFO": "blue",
        "DEBUG": "green",
        "WARNING": "light_yellow",
        "ERROR": "bold red",
    }

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = ColoredFormatter(
            "%(log_color)s %(asctime)s - %(levelname)s]: %(message)s",
            log_colors=log_colours,
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
