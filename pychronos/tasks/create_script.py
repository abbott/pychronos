import json
import os

from pychronos.script import Script
from pychronos.config import PYCHRONOS
from pychronos.util import generate_uid, for_uid
from pychronos.venv import *
from pychronos.metadata import Session
from pychronos.metadata import Script as ScriptModel


def run(arguments, event):
    arguments = json.loads(arguments)
    name = arguments["name"]

    session = Session()

    """Create a new script by creating a virtualenv, creating .sh scripts and registering metadata."""
    if name is "":
        # Generate random UID if no name is given
        uid = generate_uid()
    else:
        # Convert name to UID by "sluggifying" it (e.g. "Simon's script" -> "simons-script")
        uid = for_uid(name)

    # Check that the scripts folder exists (important for first-time users)
    if not os.path.isdir(PYCHRONOS + os.path.sep + "scripts"):
        os.mkdir(PYCHRONOS + os.path.sep + "scripts")

    # Find script path given UID
    path = PYCHRONOS + os.path.sep + "scripts" + os.path.sep + uid

    # Create folder, if it doesn't already exist
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        os.rmdir(path)
        os.mkdir(path)

    # Create virtual environment
    create_env(uid)

    # Create database entry
    script = ScriptModel(name=name, uid=uid, enabled=True, triggers=[])
    session.add(script)
    session.commit()

    # Create script and requirements.txt file
    script_path = path + os.path.sep + uid + ".py"
    requirements_path = path + os.path.sep + "requirements.txt"
    open(script_path, "a").close()
    open(requirements_path, "a").close()

    # Create execute script
    # TODO: Move this script to a folder so it can be copied instead
    with open(path + os.path.sep + "execute.sh", "w") as file:
        file.write(
            '''#!/bin/bash
cd "{}"
source "{}"
python -u "{}"'''.format(
                path, get_activate(uid), script_path
            )
        )

    # Create pip install
    # TODO: Move this script to a folder so it can be copied instead
    with open(path + os.path.sep + "install.sh", "w") as file:
        file.write(
            '''#!/bin/bash
source "{}"
pip install -r "{}"'''.format(
                get_activate(uid), requirements_path
            )
        )

    event.trigger("script_created", Script(uid).to_dict())

    return uid
