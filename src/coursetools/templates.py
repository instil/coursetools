import configparser
import glob
import os
from pathlib import Path

template_dir = (Path(__file__).absolute().parent / ".." / "templates").resolve()


def load_templates(template_directory):
    path = template_directory / "*.ini"
    return [os.path.splitext(Path(file).name)[0] for file in glob.glob(str(path))]


templates = load_templates(template_dir)


def get_templates():
    return templates


def load_template(template_file):
    config = configparser.ConfigParser()
    template_file = template_dir / f"{template_file}.ini"
    print(template_file)

    config.read(template_file)
    return config
