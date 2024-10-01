import shutil
import json
import os

from pychronos.script import Script
from pychronos.metadata import Session, Log


def run(arguments, event):
    arguments = json.loads(arguments)
    uid = arguments["uid"]

    script = Script(uid)

    session = Session()

    # Remove script folder
    shutil.rmtree(script.folder)

    # Remove all logs from script
    session.query(Log).filter(Log.script == script.uid).delete()

    # Delete metadata
    session.delete(script.db)
    session.commit()
    session.close()

    event.trigger("action_complete", {"action": "delete", "uid": script.uid})
    event.trigger("script_deleted", {"uid": script.uid})

    return uid
