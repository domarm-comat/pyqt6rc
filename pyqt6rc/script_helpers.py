import logging


def set_logger(disabled=False):
    logger = logging.getLogger()
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.disabled = disabled
