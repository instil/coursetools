import configparser
from pathlib import Path
from shutil import copytree, ignore_patterns

training_repo = "/Users/ryan/Projects/training-repo"


def main():
    """
    Version 1 of my makerepo command
    Copies the React TypeScript files from the training repo into the current directory.
    """
    print("making a course react typescript repository")
    config = configparser.ConfigParser()
    template_file = (
        Path(__file__).absolute().parent / ".." / "templates/typescript-react.ini"
    )
    print(template_file)

    config.read(template_file)
    exclusion = list(config["excludes"])

    for key in config["paths"]:
        copytree(
            f"{training_repo}{key}",
            config["paths"][key],
            ignore=ignore_patterns(*exclusion),
            dirs_exist_ok=True,
        )

    return
