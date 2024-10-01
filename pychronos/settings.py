from loguru import logger

from pychronos.metadata import Setting, Session


def get_setting(key):
    """Get setting value from database. Return None or value."""
    session = Session()
    value = session.query(Setting).get(key)
    session.close()

    return value


def set_setting(key, value):
    """Update setting or create new."""
    session = Session()
    if get_setting(key) is None:
        session.add(Setting(key=key, value=value))
        logger.debug("Created new 'setting': {} with value: '{}'", key, value)
    else:
        session.query(Setting).get(key).value = value
        logger.debug("Updated 'setting': {} with value: '{}'", key, value)

    session.commit()
    session.close()


def get_all_settings():
    """Get all settings from database."""
    session = Session()

    all_settings = session.query(Setting).all()
    session.close()

    return session
