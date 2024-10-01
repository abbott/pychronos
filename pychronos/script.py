# Python dependencies
import shutil
from datetime import timedelta, datetime
from subprocess import Popen, PIPE

# Third-party dependencies
from loguru import logger
import maya

# First-party dependencies
from pychronos.metadata import Session, Log
from pychronos.metadata import Script as ScriptModel
from pychronos.config import *
from pychronos.venv import *
from pychronos.event import event
from pychronos.task import dispatch_task


class Script:
    """Script class used to interact with scripts."""

    def __init__(self, uid):
        """Initialise script class given UID."""

        session = Session()

        # UID
        self.uid = uid

        # Get database entry
        self.db = session.query(ScriptModel).get(uid)

        # Store dictionary version of model
        self.dict = {
            "name": self.db.name,
            "triggers": self.db.triggers,
            "logs": self.logs(),
            "created": str(self.db.created),
        }

        self.enabled = self.db.enabled

        # Get script folder
        self.folder = PYCHRONOS + os.path.sep + "scripts" + os.path.sep + self.uid

        # Get path of script
        self.path = self.folder + os.path.sep + self.uid + ".py"

        # Get path of requirements file
        self.requirements = self.folder + os.path.sep + "requirements.txt"

        # Get path of execute.sh script
        self.execute_path = self.folder + os.path.sep + "execute.sh"

        # Get path of install.sh script
        self.install_requirements_path = self.folder + os.path.sep + "install.sh"

        session.close()

    def __dict__(self):
        return self.to_dict()

    def delete(self):
        """Delete script."""
        dispatch_task("delete_script", {"uid": self.uid}, task_priority="NOW")

    def action(self, action):
        if action == "delete":
            self.delete()

        if action == "execute":
            self.execute()

        if action == "install_requirements":
            self.install_requirements()

        if action == "disable":
            self.disable()

        if action == "enable":
            self.enable()

        return "OK"

    def get_contents(self):
        """Read contents of script"""
        return open(self.path, "r").read()

    def get_requirements(self):
        """Read contents of requirements.txt"""
        return open(self.requirements, "r").read()

    def write_contents(self, script):
        """Write new contents to script"""
        return open(self.path, "w").write(script)

    def write_requirements(self, requirements):
        """Write new contents to requirements.txt"""
        return open(self.requirements, "w").write(requirements)

    def logs(self, limit=10):
        """Find all log entries for script"""
        logs = []

        session = Session()

        for log in (
            session.query(Log)
            .filter(Log.script == self.uid)
            .order_by(Log.date.desc())
            .limit(limit)
            .all()
        ):
            try:
                stdout = log.text.decode("utf-8")
            except AttributeError:
                stdout = log.text

            try:
                stderr = log.error.decode("utf-8")
            except AttributeError:
                stderr = log.error

            logs.append(
                {
                    "stdout": stdout,
                    "stderr": stderr,
                    "date": maya.parse(log.date).rfc2822(),
                    "exitcode": log.exitcode,
                }
            )

        session.close()

        return logs

    def prune_logs(self):
        session = Session()

        if session.query(Log).count() > 10:
            logger.debug("Pruning logs for {}".format(self.uid))
            too_old = datetime.now() - timedelta(days=3)

            # logger.debug(too_old)

            logger.debug(
                "Found {} logs to be pruned".format(
                    session.query(Log).filter(Log.date < too_old).count()
                )
            )
            session.query(Log).filter(Log.date < too_old).delete()

        session.commit()
        session.close()

    def to_dict(self):
        """Return dictionary with script metadata"""
        return {
            **{
                "uid": self.uid,
                "contents": self.get_contents(),
                "requirements": self.get_requirements(),
                "logs": self.logs(),
                "enabled": self.enabled,
            },
            **self.dict,
        }

    def install_requirements(self):
        """Install requirements.txt"""
        dispatch_task(
            "install_pip_requirements", {"script_uid": self.uid}, task_priority="NOW"
        )

    def execute(self):
        dispatch_task("execute_script", {"script_uid": self.uid}, task_priority="NOW")

    def disable(self):
        session = Session()
        script_from_database = session.query(ScriptModel).get(self.uid)
        script_from_database.enabled = False
        session.commit()
        session.close()

        self.enabled = False

        event.trigger("script_updated", self.__dict__())
        event.trigger("action_complete", {"action": "disable", "uid": self.uid})

    def enable(self):
        session = Session()
        script_from_database = session.query(ScriptModel).get(self.uid)
        script_from_database.enabled = True
        session.commit()
        session.close()

        self.enabled = True

        event.trigger("script_updated", self.__dict__())
        event.trigger("action_complete", {"action": "enable", "uid": self.uid})



def get_all_scripts():
    scripts = []

    session = Session()

    for s in session.query(ScriptModel).all():
        scripts.append(Script(s.uid).to_dict())

    session.close()

    return scripts