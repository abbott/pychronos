from pychronos.script import get_all_scripts
from pychronos.task import dispatch_task


def run(arguments, event):
    for script in get_all_scripts():
        for trigger in script["triggers"]:
            if trigger["type"] == "on_startup":
                dispatch_task(
                    "execute_script",
                    {"script_uid": script["uid"]},
                    task_priority="NOW",
                )

    return