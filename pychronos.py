# Python dependencies
import threading
import logging
import time
import sys
import os

# Third-party dependencies
from loguru import logger

# Configure logger
from pychronos.config import PYCHRONOS
logger.remove()
logger.add(PYCHRONOS + "/logs/pychronos.log", rotation="00:00", level="DEBUG")

if os.getenv("CHRONOS_DEBUG") == "true":
    logger.add(sys.stderr, level="DEBUG")
    logger.debug("PyChronos debug mode enabled")
else:
    logger.add(sys.stderr, level="INFO")

# First-party dependencies
import pychronos

# Print PyChronos version
logger.info("Starting PyChronos: {}", pychronos.__version__)

from pychronos.web import start_server
from pychronos.task import dispatch_task
from pychronos.bus import interval_trigger
from pychronos.event import event
from pychronos.runtime import (
    evalaute_script_interval_triggers,
    evalaute_script_cron_triggers,
    prune_script_logs,
)
from pychronos.metadata import migrate

migrate()

IS_RUNNING = True


def main():
    """Start main loop."""
    logger.info("Starting main loop")
    starttime = time.time()
    i = 1

    dispatch_task("trigger_on_startup")
    dispatch_task("create_default_settings")

    while IS_RUNNING:
        # execute_next_task()
        interval_trigger.tick()

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(1 - ((time.time() - starttime) % 1))
        i += 1

    logger.info("Exiting main loop")


main_thread = threading.Thread(target=main)
main_thread.start()


interval_trigger.listen(1000, event.garbage_collect)
interval_trigger.listen(1000, evalaute_script_interval_triggers, clock=True)
interval_trigger.listen(60000, evalaute_script_cron_triggers, clock=True)
interval_trigger.listen(60000, prune_script_logs)


logger.info("Starting API server")

# Start REST API
try:
    logger.info("API server started")
    start_server()
except (KeyboardInterrupt):
    IS_RUNNING = False
    reactor.callFromThread(reactor.stop)
