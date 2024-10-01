from pychronos.metadata import Script as ScriptModel
from pychronos.metadata import Session
from pychronos.script import Script


def run(arguments, event):
    session = Session()

    for script in session.query(ScriptModel).all():
        script = Script(script.uid)
        script.prune_logs()

    return
