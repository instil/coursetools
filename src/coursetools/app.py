import argparse
import sys

from coursetools.repository import make_repo
from coursetools.templates import get_templates
from coursetools.codebase import fetch_projects


description = """
Create a course repository by copying files from the training repo according to a template
"""


def show_templates():
    print("listing templates")
    for template in get_templates():
        print(f"* {template}")


def show_projects(include_archived=False):
    projects = fetch_projects(include_archived)
    if not projects:
        print("No projects found")
        return

    print("\nActive Projects\n===================\n")
    for project in filter(lambda project: project['status'] == "active", projects):
        print(f"{project['name']} ({project['id']})")

    if include_archived:
        print("\nInactive Projects\n===================\n")
        for project in filter(lambda project: project["status"] == "archived", projects):
            print(f"{project['name']} ({project['id']})")


def parse_and_execute(argv):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-l", "--list", action="store_const", const=True)
    parser.add_argument("-p", "--project", action="store_const", const=True)
    parser.add_argument("--all", action="store_const", const=True)
    parser.add_argument(
        "template", nargs="?", default=argparse.SUPPRESS, help="Use this template"
    )

    namespace = parser.parse_args(argv)
    if "project" in namespace and namespace.project:
        include_archived = "all" in namespace and namespace.all
        show_projects(include_archived)
    elif "list" in namespace and namespace.list:
        show_templates()
    elif "template" in namespace:
        make_repo(namespace.template)
    else:
        parser.print_help()


def main():
    parse_and_execute(sys.argv[1:])
