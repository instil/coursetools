import configparser
from pathlib import Path

CONFIG = None


def load_config():
    global CONFIG
    config = configparser.ConfigParser()
    template_file = Path.home() / ".coursetools" / "config.ini"

    if template_file.exists():
        config.read(template_file)
        CONFIG = config


def get_config(key):
    if not CONFIG:
        load_config()
    if key in CONFIG["config"]:
        return CONFIG["config"][key]

    return None
