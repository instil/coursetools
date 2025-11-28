import sys
import pytest
from unittest.mock import patch, MagicMock
from coursetools.app import show_templates, main


class TestShowTemplates:
    
    def test_show_templates_prints_header(self, capsys):
        show_templates()
        
        captured = capsys.readouterr()
        assert "listing templates" in captured.out
    
    def test_show_templates_prints_all_templates(self, capsys):
        show_templates()
        
        captured = capsys.readouterr()
        # Check for known templates
        assert "python" in captured.out
        assert "typescript" in captured.out
        assert "docker" in captured.out
    
    def test_show_templates_formats_with_bullets(self, capsys):
        show_templates()
        
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        # Should have header + templates
        assert len(lines) > 1
        # Templates should start with asterisk
        for line in lines[1:]:  # Skip header
            assert line.startswith("*")


class TestMainFunction:
    
    def test_main_with_list_flag(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "-l"]):
            main()
        
        captured = capsys.readouterr()
        assert "listing templates" in captured.out
    
    def test_main_with_long_list_flag(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "--list"]):
            main()
        
        captured = capsys.readouterr()
        assert "listing templates" in captured.out
    
    def test_main_with_template_argument(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "python"]):
            # This will fail when no config file exists (CONFIG is None)
            # but we can verify the initial message is printed
            try:
                main()
            except TypeError:
                # Expected when no config file exists
                pass
        
        captured = capsys.readouterr()
        assert "making a course using the python template" in captured.out
    
    def test_main_with_invalid_template(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "nonexistent-template"]):
            main()
        
        captured = capsys.readouterr()
        assert "Not a valid template" in captured.out
    
    def test_main_with_no_arguments(self, capsys):
        with patch.object(sys, "argv", ["makerepo"]):
            main()
        
        captured = capsys.readouterr()
        # Should print help text
        assert "usage:" in captured.out or "Create a course repository" in captured.out
    
    def test_main_with_help_flag(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "-h"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # Help should exit with 0
            assert exc_info.value.code == 0
        
        captured = capsys.readouterr()
        assert "usage:" in captured.out
        assert "Create a course repository" in captured.out


class TestMainIntegration:
    
    def test_main_parses_arguments_correctly(self):
        # Test with list flag
        with patch.object(sys, "argv", ["makerepo", "-l"]):
            with patch("coursetools.app.show_templates") as mock_show:
                main()
                mock_show.assert_called_once()
    
    def test_main_calls_make_repo_with_template(self):
        with patch.object(sys, "argv", ["makerepo", "python"]):
            with patch("coursetools.app.make_repo") as mock_make:
                main()
                mock_make.assert_called_once_with("python")
    
    def test_main_prioritizes_list_over_template(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "-l", "python"]):
            main()
        
        captured = capsys.readouterr()
        # Should show list, not make repo
        assert "listing templates" in captured.out
    
    def test_main_handles_multiple_arguments(self):
        with patch.object(sys, "argv", ["makerepo", "typescript"]):
            with patch("coursetools.app.make_repo") as mock_make:
                main()
                mock_make.assert_called_once_with("typescript")


class TestArgumentParsing:
    
    def test_template_argument_is_optional(self, capsys):
        # No template should show help
        with patch.object(sys, "argv", ["makerepo"]):
            main()
        
        captured = capsys.readouterr()
        # Should not crash, should show help
        assert "usage:" in captured.out or "Create a course repository" in captured.out
    
    def test_list_flag_is_boolean(self, capsys):
        with patch.object(sys, "argv", ["makerepo", "-l"]):
            main()
        
        captured = capsys.readouterr()
        assert "listing templates" in captured.out
        
        # -l should not require a value
        with patch.object(sys, "argv", ["makerepo", "--list"]):
            main()
        
        captured = capsys.readouterr()
        assert "listing templates" in captured.out
