import argparse

from coursetools.repository import make_repo
from coursetools.templates import get_templates

description = """
Create a course repository by copying files from the training repo according to a template
"""


def show_templates():
    print("listing templates")
    for template in get_templates():
        print(f"* {template}")


def main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-l", "--list", action="store_const", const=True)
    parser.add_argument(
        "template", nargs="?", default=argparse.SUPPRESS, help="Use this template"
    )

    namespace = parser.parse_args()
    if "list" in namespace and namespace.list:
        show_templates()
    elif "template" in namespace:
        make_repo(namespace.template)
    else:
        parser.print_help()
