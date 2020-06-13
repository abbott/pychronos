# Python dependencies
import threading
import logging
import time
import sys
import os

# Third-party dependencies
from loguru import logger

# First-party dependencies
import chronos

# Print Chronos version
logger.info("Starting Chronos: {}", chronos.__version__)

from chronos.web import start_server
from chronos.config import CHRONOS
from chronos.task import dispatch_task
from chronos.bus import interval_trigger, on_startup_trigger
from chronos.event import event
from chronos.runtime import (
    evalaute_script_interval_triggers,
    evalaute_script_cron_triggers,
    prune_script_logs,
)
from chronos.metadata import migrate


# Configure logger
# logger.remove()
# logger.add(sys.stderr, level="INFO")
# logger.add(CHRONOS + "/logs/chronos.log", rotation="00:00", level="DEBUG")


migrate()

IS_RUNNING = True

# interval_trigger.listen(1000, execute_next_task)


def main():
    """Start main loop."""
    logger.info("Starting main loop")
    starttime = time.time()
    i = 1

    # on_startup_trigger.tick
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
