import os
import tempfile
from pathlib import Path
import pytest
import configparser


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
