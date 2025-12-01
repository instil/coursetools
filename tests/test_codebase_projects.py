import pytest
from pathlib import Path


def mock_get_projects_from_fixture(include_archived=False):
    fixture_path = Path(__file__).parent.parent / "fixturedata" / "projects.xml"
    with open(fixture_path) as f:
        from coursetools.codebase import parse_projects
        return parse_projects(f.read(), include_archived)


@pytest.fixture
def mock_codebase_projects(monkeypatch):
    import coursetools.app as app_module
    monkeypatch.setattr(app_module, "fetch_projects", mock_get_projects_from_fixture)


class TestListProjects:

    def test_list_projects_command_exists(self, capsys, mock_codebase_projects):
        from coursetools.app import parse_and_execute
        
        parse_and_execute(["-p"])
        
        captured = capsys.readouterr()
        assert "Visibility Check" in captured.out or "CME - Graduate Academy" in captured.out

    def test_list_projects_with_long_flag(self, capsys, mock_codebase_projects):
        from coursetools.app import parse_and_execute
        
        parse_and_execute(["--project"])
        
        captured = capsys.readouterr()
        assert "Visibility Check" in captured.out or "CME - Graduate Academy" in captured.out

    def test_list_projects_accepts_all_flag(self, capsys, mock_codebase_projects):
        from coursetools.app import parse_and_execute
        
        parse_and_execute(["-p", "--all"])
        
        captured = capsys.readouterr()
        assert len(captured.out.split("\n")) > 3

    def test_list_projects_shows_active_projects(self, capsys, mock_codebase_projects):
        from coursetools.app import parse_and_execute
        
        parse_and_execute(["-p"])
        
        captured = capsys.readouterr()
        assert "Visibility Check" in captured.out or "CME - Graduate Academy" in captured.out

    def test_list_projects_shows_all_with_flag(self, capsys, mock_codebase_projects):
        from coursetools.app import parse_and_execute
        
        parse_and_execute(["-p", "--all"])
        
        captured = capsys.readouterr()
        assert len(captured.out.split("\n")) > 3

