import os
from pathlib import Path
import configparser
import pytest
from coursetools.config import load_config, get_config, CONFIG


class TestLoadConfig:
    
    def test_load_config_sets_global_config(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        # Mock Path.home() to return our test directory
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        
        # Reset CONFIG
        config_module.CONFIG = None
        
        load_config()
        assert config_module.CONFIG is not None
        assert isinstance(config_module.CONFIG, configparser.ConfigParser)
    
    def test_load_config_reads_from_home_directory(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        load_config()
        assert config_module.CONFIG is not None
        assert "config" in config_module.CONFIG
    
    def test_load_config_with_missing_file(self, temp_dir, monkeypatch):
        import coursetools.config as config_module
        
        # Point to directory without config
        monkeypatch.setattr(Path, "home", lambda: temp_dir)
        config_module.CONFIG = None
        
        load_config()
        # Should not raise error, CONFIG should remain None or empty
        assert config_module.CONFIG is None or len(config_module.CONFIG.sections()) == 0


class TestGetConfig:
    
    def test_get_config_returns_value(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        value = get_config("repo_root")
        assert value is not None
        assert "training-repo" in value
    
    def test_get_config_loads_config_if_not_loaded(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        value = get_config("repo_root")
        # Should have loaded config
        assert config_module.CONFIG is not None
    
    def test_get_config_returns_none_for_missing_key(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        value = get_config("nonexistent_key")
        assert value is None
    
    def test_get_config_with_no_config_file(self, temp_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: temp_dir)
        config_module.CONFIG = None
        
        # When config file doesn't exist, CONFIG remains None
        # This causes a TypeError when trying to access CONFIG["config"]
        with pytest.raises(TypeError):
            get_config("repo_root")
    
    def test_get_config_multiple_calls(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        value1 = get_config("repo_root")
        value2 = get_config("repo_root")
        
        assert value1 == value2
        assert value1 is not None


class TestConfigIntegration:
    
    def test_config_file_format(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        load_config()
        
        assert "config" in config_module.CONFIG.sections()
        assert "repo_root" in config_module.CONFIG["config"]
    
    def test_config_values_are_strings(self, mock_config_dir, monkeypatch):
        import coursetools.config as config_module
        
        monkeypatch.setattr(Path, "home", lambda: mock_config_dir.parent)
        config_module.CONFIG = None
        
        value = get_config("repo_root")
        assert isinstance(value, str)
