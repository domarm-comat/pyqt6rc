import logging


def set_logger(disabled: bool = False) -> None:
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger("main")
    logger.info("sadads")
    logger.disabled = disabled
