"""Tests for CLI interface."""
import pytest
from click.testing import CliRunner
from pathlib import Path
from sql_format.cli import main, process_stdin, process_file, process_directory
from sql_format.formatter import SQLFormatter
from sql_format.config import Config


class TestCLI:
    """Test CLI commands."""

    def test_main_with_stdin(self):
        runner = CliRunner()
        result = runner.invoke(main, input="SELECT * FROM users")
        assert result.exit_code == 0
        assert "SELECT" in result.output

    def test_main_with_file(self, tmp_path):
        sql_file = tmp_path / "test.sql"
        sql_file.write_text("select * from users")
        runner = CliRunner()
        result = runner.invoke(main, [str(sql_file)])
        assert result.exit_code == 0
        assert "SELECT" in result.output

    def test_main_with_output_file(self, tmp_path):
        sql_file = tmp_path / "test.sql"
        output_file = tmp_path / "output.sql"
        sql_file.write_text("select * from users")
        runner = CliRunner()
        result = runner.invoke(main, [str(sql_file), '-o', str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "SELECT" in content

    def test_main_in_place(self, tmp_path):
        sql_file = tmp_path / "test.sql"
        sql_file.write_text("select * from users")
        runner = CliRunner()
        result = runner.invoke(main, [str(sql_file), '-i'])
        assert result.exit_code == 0
        content = sql_file.read_text()
        assert "SELECT" in content

    def test_main_in_place_with_backup(self, tmp_path):
        sql_file = tmp_path / "test.sql"
        original = "select * from users"
        sql_file.write_text(original)
        runner = CliRunner()
        result = runner.invoke(main, [str(sql_file), '-i', '--backup'])
        assert result.exit_code == 0
        backup_file = tmp_path / "test.sql.bak"
        assert backup_file.exists()
        assert backup_file.read_text() == original

    def test_main_dry_run(self, tmp_path):
        sql_file = tmp_path / "test.sql"
        original = "select * from users"
        sql_file.write_text(original)
        runner = CliRunner()
        result = runner.invoke(main, [str(sql_file), '--dry-run'])
        assert result.exit_code == 0
        assert sql_file.read_text() == original
        assert "SELECT" in result.output

    def test_main_with_directory(self, tmp_path):
        (tmp_path / "test1.sql").write_text("select * from users")
        (tmp_path / "test2.sql").write_text("select * from orders")
        runner = CliRunner()
        result = runner.invoke(main, ['-d', str(tmp_path)])
        assert result.exit_code == 0

    def test_main_keyword_case_lower(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--keyword-case', 'lower'], input="SELECT * FROM users")
        assert result.exit_code == 0
        assert "select" in result.output

    def test_main_indent_2_spaces(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--indent', '2'], input="SELECT * FROM users WHERE id = 1")
        assert result.exit_code == 0

    def test_main_strip_comments(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--strip-comments'], input="SELECT * FROM users -- comment")
        assert result.exit_code == 0
        assert "comment" not in result.output
