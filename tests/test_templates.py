"""Unit tests for coursetools.templates module."""
import os
from pathlib import Path
import pytest
from coursetools.templates import load_templates, get_templates, load_template


class TestLoadTemplates:
    """Tests for load_templates function."""
    
    def test_load_templates_returns_list(self, mock_template_dir):
        """Test that load_templates returns a list of template names."""
        templates = load_templates(mock_template_dir)
        assert isinstance(templates, list)
    
    def test_load_templates_finds_ini_files(self, mock_template_dir):
        """Test that load_templates finds .ini files in directory."""
        templates = load_templates(mock_template_dir)
        assert len(templates) == 2
        assert "test-template" in templates
        assert "another-template" in templates
    
    def test_load_templates_strips_extension(self, mock_template_dir):
        """Test that load_templates removes .ini extension from names."""
        templates = load_templates(mock_template_dir)
        for template in templates:
            assert not template.endswith(".ini")
    
    def test_load_templates_empty_directory(self, temp_dir):
        """Test load_templates with empty directory."""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        templates = load_templates(empty_dir)
        assert templates == []


class TestGetTemplates:
    """Tests for get_templates function."""
    
    def test_get_templates_returns_list(self):
        """Test that get_templates returns a list."""
        templates = get_templates()
        assert isinstance(templates, list)
    
    def test_get_templates_contains_expected_templates(self):
        """Test that get_templates returns known templates."""
        templates = get_templates()
        # These templates exist in the actual src/templates directory
        assert "python" in templates
        assert "typescript" in templates
        assert "docker" in templates
    
    def test_get_templates_not_empty(self):
        """Test that get_templates returns non-empty list."""
        templates = get_templates()
        assert len(templates) > 0


class TestLoadTemplate:
    """Tests for load_template function."""
    
    def test_load_template_returns_config(self, mock_template_dir, monkeypatch):
        """Test that load_template returns a ConfigParser object."""
        # Temporarily override template_dir
        import coursetools.templates as templates_module
        original_dir = templates_module.template_dir
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        
        config = load_template("test-template")
        assert config is not None
        assert "paths" in config
        assert "excludes" in config
        
        # Restore original
        monkeypatch.setattr(templates_module, "template_dir", original_dir)
    
    def test_load_template_has_correct_sections(self, mock_template_dir, monkeypatch):
        """Test that loaded template has expected sections."""
        import coursetools.templates as templates_module
        original_dir = templates_module.template_dir
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        
        config = load_template("test-template")
        assert "/test/path1" in config["paths"]
        assert "/test/path2" in config["paths"]
        assert "node_modules" in config["excludes"]
        
        monkeypatch.setattr(templates_module, "template_dir", original_dir)
    
    def test_load_template_reads_paths_correctly(self, mock_template_dir, monkeypatch):
        """Test that template paths are read correctly."""
        import coursetools.templates as templates_module
        original_dir = templates_module.template_dir
        monkeypatch.setattr(templates_module, "template_dir", mock_template_dir)
        
        config = load_template("test-template")
        assert config["paths"]["/test/path1"] == "dest1"
        assert config["paths"]["/test/path2"] == "dest2"
        
        monkeypatch.setattr(templates_module, "template_dir", original_dir)


class TestRealTemplates:
    """Tests for real templates in the repository."""
    
    def test_python_template_exists(self):
        """Test that python.ini template exists and is valid."""
        templates = get_templates()
        assert "python" in templates
        
        config = load_template("python")
        assert "paths" in config
        assert "excludes" in config
    
    def test_typescript_template_exists(self):
        """Test that typescript.ini template exists and is valid."""
        templates = get_templates()
        assert "typescript" in templates
        
        config = load_template("typescript")
        assert "paths" in config
        assert "excludes" in config
    
    def test_docker_template_exists(self):
        """Test that docker.ini template exists and is valid."""
        templates = get_templates()
        assert "docker" in templates
        
        config = load_template("docker")
        assert "paths" in config
        assert "excludes" in config
    
    def test_all_templates_have_required_sections(self):
        """Test that all templates have paths and excludes sections."""
        templates = get_templates()
        for template_name in templates:
            config = load_template(template_name)
            assert "paths" in config, f"Template {template_name} missing paths section"
            assert "excludes" in config, f"Template {template_name} missing excludes section"
