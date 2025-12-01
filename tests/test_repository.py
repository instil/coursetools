import os
from pathlib import Path
import configparser
import pytest
from unittest.mock import patch, MagicMock
from coursetools.repository import make_repo
from tests import run_in_temporary_directory, create_directory_structure, create_mock_template


class TestMakeRepo:
    
    def test_make_repo_with_invalid_template(self, capsys):
        make_repo("nonexistent-template")
        
        captured = capsys.readouterr()
        assert "Not a valid template" in captured.out
    
    def test_make_repo_with_valid_template_name(self, mock_config_dir, mock_template_dir, monkeypatch, capsys):
        import coursetools.config as config_module
        import coursetools.templates as templates_module
        
        # Setup mocks
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        monkeypatch.setattr(templates_module, "templates", ["test-template", "another-template"])
        config_module.CONFIG = None
        
        # This will fail because the paths don't exist, but we can check the message
        make_repo("test-template")
        
        captured = capsys.readouterr()
        assert "making a course using the test-template template" in captured.out
    
    def test_make_repo_checks_template_existence(self, capsys):
        result = make_repo("definitely-not-a-real-template")
        
        captured = capsys.readouterr()
        assert "Not a valid template" in captured.out
        assert result is None
    
    def test_make_repo_with_real_template(self, capsys):
        # This will fail due to missing config, but tests template validation
        make_repo("python")
        
        captured = capsys.readouterr()
        assert "making a course using the python template" in captured.out


class TestMakeRepoFileOperations:
    
    def test_make_repo_copies_directory(self, temp_dir, mock_config_dir, monkeypatch, capsys):
        import coursetools.config as config_module
        
        # Setup config
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        # Create source directory
        create_directory_structure(temp_dir, {
            "training-repo": {
                "test-source": {
                    "file1.txt": "Content 1",
                    "file2.txt": "Content 2"
                }
            }
        })
        
        # Create template
        create_mock_template(
            temp_dir, monkeypatch, "test-copy",
            paths={"/test-source": "dest"},
            excludes={"*.old": ""}
        )
        
        def act_and_assert():
            make_repo("test-copy")
            
            # Check destination exists
            dest_dir = temp_dir / "dest"
            assert dest_dir.exists()
            assert (dest_dir / "file1.txt").exists()
            assert (dest_dir / "file2.txt").exists()
        
        run_in_temporary_directory(act_and_assert, temp_dir)
    
    def test_make_repo_copies_single_file(self, temp_dir, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        # Setup config
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        # Create source file
        create_directory_structure(temp_dir, {
            "training-repo": {
                "test-file.txt": "Test content"
            }
        })
        
        # Create template
        create_mock_template(
            temp_dir, monkeypatch, "test-file-copy",
            paths={"/test-file.txt": "output-file.txt"},
            excludes={}
        )
        
        def act_and_assert():
            make_repo("test-file-copy")
            
            # Check file was copied
            dest_file = temp_dir / "output-file.txt"
            assert dest_file.exists()
            assert dest_file.read_text() == "Test content"
        
        run_in_temporary_directory(act_and_assert, temp_dir)
    
    def test_make_repo_respects_exclusions(self, temp_dir, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        # Setup config
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        # Create source directory with files to exclude
        create_directory_structure(temp_dir, {
            "training-repo": {
                "test-exclusion": {
                    "keep.txt": "Keep this",
                    "exclude.old": "Exclude this",
                    "node_modules": {
                        "package.json": "{}"
                    }
                }
            }
        })
        
        # Create template with exclusions
        create_mock_template(
            temp_dir, monkeypatch, "test-exclusion",
            paths={"/test-exclusion": "output"},
            excludes={"*.old": "", "node_modules": ""}
        )
        
        def act_and_assert():
            make_repo("test-exclusion")
            
            # Check correct files exist
            dest_dir = temp_dir / "output"
            assert dest_dir.exists()
            assert (dest_dir / "keep.txt").exists()
            assert not (dest_dir / "exclude.old").exists()
            assert not (dest_dir / "node_modules").exists()
        
        run_in_temporary_directory(act_and_assert, temp_dir)
    
    def test_make_repo_handles_nonexistent_source(self, temp_dir, mock_config_dir, monkeypatch, capsys):
        import coursetools.config as config_module
        
        # Setup config
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        # Create template pointing to nonexistent source
        create_mock_template(
            temp_dir, monkeypatch, "test-missing",
            paths={"/nonexistent-path": "output"},
            excludes={}
        )
        
        def act_and_assert():
            make_repo("test-missing")
            
            captured = capsys.readouterr()
            assert "neither file or directory" in captured.out
        
        run_in_temporary_directory(act_and_assert, temp_dir)
