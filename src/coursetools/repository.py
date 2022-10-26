from pathlib import Path
from shutil import copytree, ignore_patterns

from coursetools.config import get_config
from coursetools.templates import get_templates, load_template


def make_repo(course_template):
    """
    Copies the files defined in the template from the training repo into the current directory.

    course_template -- name of the template to run
    """
    print(f"making a course using the {course_template} template")
    if course_template not in get_templates():
        print("Not a valid template")
        return

    template = load_template(course_template)
    exclusion = list(template["excludes"])
    training_repo = get_config("repo_root")

    for key in template["paths"]:
        copytree(
            f"{training_repo}{key}",
            Path(template["paths"][key]).resolve(),
            ignore=ignore_patterns(*exclusion),
            dirs_exist_ok=True,
        )

    return
