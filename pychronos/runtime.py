# Python dependencies
import os
from datetime import datetime
import threading

# Third-party dependencies
import cronex
from loguru import logger

# First-party dependencies
from pychronos.util import *
from pychronos.venv import *
from pychronos.metadata import Session
from pychronos.metadata import Script as ScriptModel
from pychronos.script import Script
from pychronos.task import dispatch_task
from pychronos.bus import interval_trigger

session = Session()


def evalaute_script_interval_triggers(tick, interval):
    second = tick * interval / 1000

    for script in session.query(ScriptModel).all():
        s = Script(script.uid)

        if script.enabled:

            for trigger in script.triggers:

                if trigger["type"] == "interval":
                    if second % int(trigger["options"]["interval"]) == 0:
                        dispatch_task(
                            "execute_script",
                            {"script_uid": script.uid},
                            task_priority="NOW",
                        )

        # Check that the script is enabled to run and that the interval is above 0
        """if script.interval != 0 and script.enabled:
            # Check that the interval is a multiple of the current tick
            if second % script.interval == 0:
                # Execute script in seperate thread, such that the loop is not affected
                dispatch_task(
                    "execute_script", {"script_uid": script.uid}, task_priority="NOW"
                )"""


def evalaute_script_cron_triggers(tick, interval):
    second = tick * interval / 1000

    for script in session.query(ScriptModel).all():
        s = Script(script.uid)

        if script.enabled:

            for trigger in script.triggers:

                if trigger["type"] == "cron":
                    # Evaluate cron expression
                    try:
                        cron = cronex.CronExpression(trigger["options"]["expression"])

                        time = tuple(list(datetime.now().timetuple())[:5])

                        if cron.check_trigger(time):
                            # Execute script in seperate thread, such that the loop is not affected
                            dispatch_task(
                                "execute_script",
                                {"script_uid": script.uid},
                                task_priority="NOW",
                            )
                    except(ValueError):
                        logger.error("CRON expression yielded error: {}", trigger["options"]["expression"])

def prune_script_logs():
    dispatch_task("prune_logs", {})
