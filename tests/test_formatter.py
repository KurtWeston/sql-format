"""Tests for SQL formatter."""
import pytest
from sql_format.formatter import SQLFormatter
from sql_format.config import Config


class TestSQLFormatter:
    """Test SQLFormatter class."""

    def test_format_basic_select(self):
        config = Config(indent_width=4, keyword_case='upper')
        formatter = SQLFormatter(config)
        sql = "select id, name from users where active = true"
        result = formatter.format(sql)
        assert "SELECT" in result
        assert "FROM" in result
        assert "WHERE" in result

    def test_format_with_lowercase_keywords(self):
        config = Config(keyword_case='lower')
        formatter = SQLFormatter(config)
        sql = "SELECT * FROM users"
        result = formatter.format(sql)
        assert "select" in result
        assert "from" in result

    def test_format_empty_string(self):
        config = Config()
        formatter = SQLFormatter(config)
        result = formatter.format("")
        assert result == ""

    def test_format_whitespace_only(self):
        config = Config()
        formatter = SQLFormatter(config)
        result = formatter.format("   \n  \t  ")
        assert result.strip() == ""

    def test_strip_comments(self):
        config = Config(strip_comments=True)
        formatter = SQLFormatter(config)
        sql = "SELECT * FROM users -- this is a comment"
        result = formatter.format(sql)
        assert "comment" not in result

    def test_preserve_comments(self):
        config = Config(strip_comments=False)
        formatter = SQLFormatter(config)
        sql = "SELECT * FROM users -- keep this"
        result = formatter.format(sql)
        assert "keep this" in result

    def test_indent_width_2(self):
        config = Config(indent_width=2)
        formatter = SQLFormatter(config)
        sql = "SELECT id FROM users WHERE active = true"
        result = formatter.format(sql)
        assert result.count(' ') > 0

    def test_complex_query_with_joins(self):
        config = Config()
        formatter = SQLFormatter(config)
        sql = "select u.id, u.name, o.total from users u join orders o on u.id = o.user_id"
        result = formatter.format(sql)
        assert "SELECT" in result
        assert "JOIN" in result
        assert "ON" in result

    def test_subquery_formatting(self):
        config = Config()
        formatter = SQLFormatter(config)
        sql = "SELECT * FROM (SELECT id FROM users) AS subq"
        result = formatter.format(sql)
        assert "SELECT" in result
        assert result.count("SELECT") == 2

    def test_align_columns_enabled(self):
        config = Config(align_columns=True)
        formatter = SQLFormatter(config)
        sql = "SELECT id, name, email FROM users"
        result = formatter.format(sql)
        assert "id" in result
        assert "name" in result
        assert "email" in result
