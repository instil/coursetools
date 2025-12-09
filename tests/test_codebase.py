import tempfile
from pathlib import Path

import pytest
import coursetools.codebase
from coursetools.codebase import parse_projects, fetch_projects, load_credentials


def create_credentials_file(home_dir, username="account/user", api_key="test-api-key"):
    codebase_dir = home_dir / ".codebase"
    codebase_dir.mkdir()
    cred_file = codebase_dir / "credentials.toml"
    cred_file.write_text(
        f"""username = "{username}"
api_key = "{api_key}"
"""
    )
    return cred_file


class TestLoadCredentials:

    def test_load_credentials_from_home_directory(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir)
            create_credentials_file(home_dir, "account/user", "home-api-key")
            monkeypatch.setenv("HOME", str(home_dir))

            creds = load_credentials()

            assert creds["username"] == "account/user"
            assert creds["api_key"] == "home-api-key"

    def test_load_credentials_returns_empty_dict_if_file_missing(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir)
            monkeypatch.setenv("HOME", str(home_dir))

            creds = load_credentials()

            assert creds == {}

@pytest.fixture
def projects_xml():
    fixture_path = Path(__file__).parent.parent / "fixturedata" / "projects.xml"
    with open(fixture_path) as f:
        return f.read()


class TestFetchProjects:

    def test_fetch_projects_with_no_credentials(self, monkeypatch):

        def mock_load_credentials():
            return {}

        monkeypatch.setattr(coursetools.codebase, "load_credentials", mock_load_credentials)

        projects = fetch_projects()

        assert projects == []

    def test_fetch_projects_returns_parsed_projects(self, projects_xml, monkeypatch):

        def mock_load_credentials():
            return {"username": "account/user", "api_key": "test-key"}

        def mock_fetch_xml(username, api_key):
            return projects_xml

        monkeypatch.setattr(coursetools.codebase, "load_credentials", mock_load_credentials)
        monkeypatch.setattr(coursetools.codebase, "fetch_xml", mock_fetch_xml)

        projects = fetch_projects(include_archived=False)

        assert len(projects) > 0
        for p in projects:
            assert p["status"] == "active"

    def test_parse_projects_from_fixture_data(self, projects_xml):
        projects = parse_projects(projects_xml)

        assert len(projects) > 0
        assert isinstance(projects[0], dict)

    def test_parse_projects_filters_active_by_default(self, projects_xml):
        projects = parse_projects(projects_xml, include_archived=False)

        for project in projects:
            assert project["status"] == "active"

    def test_parse_projects_includes_archived_when_requested(self, projects_xml):
        projects = parse_projects(projects_xml, include_archived=True)

        statuses = {p["status"] for p in projects}
        assert "active" in statuses
        assert "archived" in statuses
