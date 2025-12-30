"""Tests for configuration management."""
import pytest
import json
from pathlib import Path
from sql_format.config import Config


class TestConfig:
    """Test Config class."""

    def test_default_config(self):
        config = Config()
        assert config.indent_width == 4
        assert config.keyword_case == 'upper'
        assert config.strip_comments is False
        assert config.line_length == 80
        assert config.dialect == 'postgresql'
        assert config.align_columns is True

    def test_custom_config(self):
        config = Config(
            indent_width=2,
            keyword_case='lower',
            strip_comments=True,
            line_length=100,
            dialect='mysql'
        )
        assert config.indent_width == 2
        assert config.keyword_case == 'lower'
        assert config.strip_comments is True
        assert config.line_length == 100
        assert config.dialect == 'mysql'

    def test_to_dict(self):
        config = Config(indent_width=2, keyword_case='lower')
        result = config.to_dict()
        assert result['indent_width'] == 2
        assert result['keyword_case'] == 'lower'
        assert 'strip_comments' in result
        assert 'line_length' in result

    def test_from_file_valid_json(self, tmp_path):
        config_file = tmp_path / ".sqlformatrc"
        config_data = {
            "indent_width": 2,
            "keyword_case": "lower",
            "strip_comments": True
        }
        config_file.write_text(json.dumps(config_data))
        config = Config.from_file(config_file)
        assert config.indent_width == 2
        assert config.keyword_case == "lower"
        assert config.strip_comments is True

    def test_from_file_nonexistent(self, tmp_path):
        config_file = tmp_path / "nonexistent.json"
        config = Config.from_file(config_file)
        assert config.indent_width == 4
        assert config.keyword_case == 'upper'

    def test_from_file_invalid_json(self, tmp_path):
        config_file = tmp_path / ".sqlformatrc"
        config_file.write_text("not valid json {{{")
        config = Config.from_file(config_file)
        assert config.indent_width == 4

    def test_find_config_in_current_dir(self, tmp_path):
        config_file = tmp_path / ".sqlformatrc"
        config_data = {"indent_width": 2}
        config_file.write_text(json.dumps(config_data))
        config = Config.find_config(tmp_path)
        assert config.indent_width == 2

    def test_find_config_in_parent_dir(self, tmp_path):
        config_file = tmp_path / ".sqlformatrc"
        config_data = {"indent_width": 2}
        config_file.write_text(json.dumps(config_data))
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        config = Config.find_config(subdir)
        assert config.indent_width == 2

    def test_find_config_not_found(self, tmp_path):
        config = Config.find_config(tmp_path)
        assert config.indent_width == 4
