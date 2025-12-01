import os
from pathlib import Path
import pytest
from coursetools.templates import load_templates, get_templates, load_template


class TestLoadTemplates:
    
    def test_load_templates_returns_list(self, mock_template_dir):
        templates = load_templates(mock_template_dir)
        assert isinstance(templates, list)
    
    def test_load_templates_finds_ini_files(self, mock_template_dir):
        templates = load_templates(mock_template_dir)
        assert len(templates) == 2
        assert "test-template" in templates
        assert "another-template" in templates
    
    def test_load_templates_strips_extension(self, mock_template_dir):
        templates = load_templates(mock_template_dir)
        for template in templates:
            assert not template.endswith(".ini")
    
    def test_load_templates_empty_directory(self, temp_dir):
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        templates = load_templates(empty_dir)
        assert templates == []


class TestGetTemplates:
    
    def test_get_templates_returns_list(self):
        templates = get_templates()
        assert isinstance(templates, list)
    
    def test_get_templates_contains_expected_templates(self):
        templates = get_templates()
        # These templates exist in the actual src/templates directory
        assert "python" in templates
        assert "typescript" in templates
        assert "docker" in templates
    
    def test_get_templates_not_empty(self):
        templates = get_templates()
        assert len(templates) > 0


class TestLoadTemplate:
    
    def test_load_template_returns_config(self, mock_template_dir, monkeypatch):
        # Temporarily override template_dir
        import coursetools.templates as templates_module
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        
        config = load_template("test-template")
        assert config is not None
        assert "paths" in config
        assert "excludes" in config
    
    def test_load_template_has_correct_sections(self, mock_template_dir, monkeypatch):
        import coursetools.templates as templates_module
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        
        config = load_template("test-template")
        assert "/test/path1" in config["paths"]
        assert "/test/path2" in config["paths"]
        assert "node_modules" in config["excludes"]
    
    def test_load_template_reads_paths_correctly(self, mock_template_dir, monkeypatch):
        import coursetools.templates as templates_module
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        
        config = load_template("test-template")
        assert config["paths"]["/test/path1"] == "dest1"
        assert config["paths"]["/test/path2"] == "dest2"
