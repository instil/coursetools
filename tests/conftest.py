import os
import tempfile
from pathlib import Path
import pytest
import configparser


def run_in_temporary_directory(act_and_assert, temp_dir):
    """Execute a callable in a temporary directory and restore the original directory.
    
    Args:
        act_and_assert: A callable that performs actions and assertions
        temp_dir: The temporary directory path to change to
    """
    original_cwd = os.getcwd()
    try:
        os.chdir(temp_dir)
        act_and_assert()
    finally:
        os.chdir(original_cwd)


def create_directory_structure(base_path, structure):
    """Create a directory structure from a nested dictionary.
    
    Args:
        base_path: The base path where the structure should be created
        structure: A dictionary where:
            - If the value is a dict, the key is a directory name
            - If the value is a string, the key is a file name and value is content
    
    Example:
        structure = {
            "training-repo": {
                "test-source": {
                    "file1.txt": "Content 1",
                    "file2.txt": "Content 2"
                }
            }
        }
    """
    base = Path(base_path)
    
    for name, content in structure.items():
        path = base / name
        
        if isinstance(content, dict):
            # It's a directory
            path.mkdir(parents=True, exist_ok=True)
            # Recursively create subdirectories and files
            create_directory_structure(path, content)
        else:
            # It's a file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)


def create_mock_template(temp_dir, monkeypatch, template_name, paths, excludes):
    """Create a mock template configuration and patch the templates module.
    
    Args:
        temp_dir: The temporary directory path
        monkeypatch: The pytest monkeypatch fixture
        template_name: The name of the template (without .ini extension)
        paths: Dictionary of paths for the template config
        excludes: Dictionary of excludes for the template config
    
    Example:
        create_mock_template(
            temp_dir, monkeypatch, "test-copy",
            paths={"/test-source": "dest"},
            excludes={"*.old": ""}
        )
    """
    import coursetools.templates as templates_module
    
    # Create template directory
    template_dir = temp_dir / "templates"
    template_dir.mkdir(exist_ok=True)
    monkeypatch.setattr(templates_module, "template_dir", template_dir)
    
    # Create template file
    test_template = template_dir / f"{template_name}.ini"
    config = configparser.ConfigParser()
    config["paths"] = paths
    config["excludes"] = excludes
    
    with open(test_template, "w") as f:
        config.write(f)
    
    # Patch templates list
    monkeypatch.setattr(templates_module, "templates", [template_name])


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_template_dir(temp_dir):
    template_dir = temp_dir / "templates"
    template_dir.mkdir()
    
    # Create a test template
    test_template = template_dir / "test-template.ini"
    config = configparser.ConfigParser()
    config["paths"] = {
        "/test/path1": "dest1",
        "/test/path2": "dest2"
    }
    config["excludes"] = {
        "node_modules": "",
        "*.old": "",
        ".DS_Store": ""
    }
    
    with open(test_template, "w") as f:
        config.write(f)
    
    # Create another template
    another_template = template_dir / "another-template.ini"
    config2 = configparser.ConfigParser()
    config2["paths"] = {"/another/path": "output"}
    config2["excludes"] = {"archive": ""}
    
    with open(another_template, "w") as f:
        config2.write(f)
    
    return template_dir


@pytest.fixture
def mock_config_dir(temp_dir):
    config_dir = temp_dir / ".coursetools"
    config_dir.mkdir()
    
    config_file = config_dir / "config.ini"
    config = configparser.ConfigParser()
    config["config"] = {
        "repo_root": str(temp_dir / "training-repo")
    }
    
    with open(config_file, "w") as f:
        config.write(f)
    
    return config_dir


@pytest.fixture
def mock_repo_structure(temp_dir):
    repo_root = temp_dir / "training-repo"
    repo_root.mkdir()
    
    # Create some test directories and files
    test_dir = repo_root / "Python" / "Python3" / "examples"
    test_dir.mkdir(parents=True)
    
    (test_dir / "example1.py").write_text("# Example 1\nprint('Hello')")
    (test_dir / "example2.py").write_text("# Example 2\nprint('World')")
    
    # Create directory to exclude
    node_modules = test_dir / "node_modules"
    node_modules.mkdir()
    (node_modules / "package.json").write_text("{}")
    
    # Create another test directory
    exercises_dir = repo_root / "Python" / "Python3" / "exercises"
    exercises_dir.mkdir(parents=True)
    (exercises_dir / "exercise1.py").write_text("# Exercise 1")
    
    # Create a test file at root
    test_file = repo_root / "test_file.txt"
    test_file.write_text("Test content")
    
    return repo_root
