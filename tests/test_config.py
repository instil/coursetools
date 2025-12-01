import os
from pathlib import Path
import configparser
import pytest
from coursetools.config import load_config, get_config, CONFIG


class TestLoadConfig:
    
    def initialise_config(self, home_dir, monkeypatch):
        import coursetools.config as config_module
        monkeypatch.setattr(Path, "home", lambda: home_dir)
        config_module.CONFIG = None
        return config_module
    
    def test_load_config_sets_global_config(self, mock_config_dir, monkeypatch):
        config_module = self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        load_config()
        assert config_module.CONFIG is not None
        assert isinstance(config_module.CONFIG, configparser.ConfigParser)
    
    def test_load_config_reads_from_home_directory(self, mock_config_dir, monkeypatch):
        config_module = self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        load_config()
        assert config_module.CONFIG is not None
        assert "config" in config_module.CONFIG
    
    def test_load_config_with_missing_file(self, temp_dir, monkeypatch):
        config_module = self.initialise_config(temp_dir, monkeypatch)
        
        load_config()
        # Should not raise error, CONFIG should remain None or empty
        assert config_module.CONFIG is None or len(config_module.CONFIG.sections()) == 0


class TestGetConfig:
    
    def initialise_config(self, home_dir, monkeypatch):
        import coursetools.config as config_module
        monkeypatch.setattr(Path, "home", lambda: home_dir)
        config_module.CONFIG = None
        return config_module
    
    def test_get_config_returns_value(self, mock_config_dir, monkeypatch):
        self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        value = get_config("repo_root")
        assert value is not None
        assert "training-repo" in value
    
    def test_get_config_loads_config_if_not_loaded(self, mock_config_dir, monkeypatch):
        config_module = self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        value = get_config("repo_root")
        # Should have loaded config
        assert config_module.CONFIG is not None
    
    def test_get_config_returns_none_for_missing_key(self, mock_config_dir, monkeypatch):
        self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        value = get_config("nonexistent_key")
        assert value is None
    
    def test_get_config_with_no_config_file(self, temp_dir, monkeypatch):
        self.initialise_config(temp_dir, monkeypatch)
        
        # When config file doesn't exist, CONFIG remains None
        # This causes a TypeError when trying to access CONFIG["config"]
        with pytest.raises(TypeError):
            get_config("repo_root")
    
    def test_get_config_multiple_calls(self, mock_config_dir, monkeypatch):
        self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        value1 = get_config("repo_root")
        value2 = get_config("repo_root")
        
        assert value1 == value2
        assert value1 is not None


class TestConfigIntegration:
    
    def initialise_config(self, home_dir, monkeypatch):
        import coursetools.config as config_module
        monkeypatch.setattr(Path, "home", lambda: home_dir)
        config_module.CONFIG = None
        return config_module
    
    def test_config_file_format(self, mock_config_dir, monkeypatch):
        config_module = self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        load_config()
        
        assert "config" in config_module.CONFIG.sections()
        assert "repo_root" in config_module.CONFIG["config"]
    
    def test_config_values_are_strings(self, mock_config_dir, monkeypatch):
        self.initialise_config(mock_config_dir.parent, monkeypatch)
        
        value = get_config("repo_root")
        assert isinstance(value, str)
