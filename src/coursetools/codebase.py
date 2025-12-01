from pathlib import Path
import xml.etree.ElementTree as ET
import urllib.request
import base64

base_url = "https://api3.codebasehq.com"


def fetch_projects(include_archived=False):
    creds = load_credentials()
    if not creds:
        print("credentials missing")
        return []

    xml_data = fetch_xml(creds["username"], creds["api_key"])
    return parse_projects(xml_data, include_archived)


def load_credentials(path=None):
    if path is None:
        home = Path.home()
        path = home / ".codebase" / "credentials.toml"
    else:
        path = Path(path)

    if not path.exists():
        print("credentials path does not exist")
        return {}

    import tomllib

    with open(path, "rb") as f:
        data = tomllib.load(f)

    return data


def fetch_xml(username, api_key):
    url = f"{base_url}/projects"
    auth = f"{username}:{api_key}"
    auth_header = base64.b64encode(auth.encode()).decode()

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {auth_header}")

    with urllib.request.urlopen(req) as response:
        return response.read().decode()


def parse_projects(xml_data, include_archived=False):
    root = ET.fromstring(xml_data)
    projects = []

    for project_elem in root.findall("project"):
        project = extract_project(project_elem)
        if include_archived or project["status"] == "active":
            projects.append(project)

    return projects


def extract_project(project_elem):
    return {
        "id": project_elem.findtext("project-id"),
        "name": project_elem.findtext("name"),
        "status": project_elem.findtext("status"),
        "permalink": project_elem.findtext("permalink"),
    }
