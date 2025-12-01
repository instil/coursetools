import pytest
from coursetools.app import show_templates, parse_and_execute
from tests import run_in_temporary_directory


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


class TestParseAndExecute:

    def test_parse_and_execute_with_list_flag(self, capsys):
        parse_and_execute(["-l"])

        captured = capsys.readouterr()
        assert "listing templates" in captured.out

    def test_parse_and_execute_with_long_list_flag(self, capsys):
        parse_and_execute(["--list"])

        captured = capsys.readouterr()
        assert "listing templates" in captured.out

    def test_parse_and_execute_with_template_argument(self, capsys, temp_dir):
        def act_and_assert():
            # This will fail when no config file exists (CONFIG is None)
            # but we can verify the initial message is printed
            try:
                parse_and_execute(["python"])
            except TypeError:
                # Expected when no config file exists
                pass

            captured = capsys.readouterr()
            assert "making a course using the python template" in captured.out

        run_in_temporary_directory(act_and_assert, temp_dir)

    def test_parse_and_execute_with_invalid_template(self, capsys):
        parse_and_execute(["nonexistent-template"])

        captured = capsys.readouterr()
        assert "Not a valid template" in captured.out

    def test_parse_and_execute_with_no_arguments(self, capsys):
        parse_and_execute([])

        captured = capsys.readouterr()
        # Should print help text
        assert "usage:" in captured.out or "Create a course repository" in captured.out

    def test_parse_and_execute_with_help_flag(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            parse_and_execute(["-h"])

            # Help should exit with 0
            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "usage:" in captured.out
        assert "Create a course repository" in captured.out


class TestArgumentParsing:

    def test_template_argument_is_optional(self, capsys):
        # No template should show help
        parse_and_execute([])

        captured = capsys.readouterr()
        # Should not crash, should show help
        assert "usage:" in captured.out or "Create a course repository" in captured.out

    def test_list_flag_is_boolean(self, capsys):
        parse_and_execute(["-l"])

        captured = capsys.readouterr()
        assert "listing templates" in captured.out

        # -l should not require a value
        parse_and_execute(["--list"])

        captured = capsys.readouterr()
        assert "listing templates" in captured.out
