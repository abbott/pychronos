# TODO: Find another place for this line
import os

from loguru import logger


PYCHRONOS = os.getenv("PYCHRONOS_PATH")

if PYCHRONOS is None:
    logger.critical("Enviroment variable PYCHRONOS_PATH not set, aborting program")
    logger.info("The PYCHRONOS_PATH variable must contain the PyChronos metadata folder.")
    exit()
