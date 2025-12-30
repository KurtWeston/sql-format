"""Core SQL formatting logic."""
import sqlparse
from sqlparse.sql import Token, TokenList
from sqlparse.tokens import Keyword, DML, DDL
from typing import List
from .config import Config

class SQLFormatter:
    """Formats SQL queries with consistent style."""

    def __init__(self, config: Config):
        self.config = config

    def format(self, sql: str) -> str:
        """Format SQL query with configured style."""
        if not sql.strip():
            return sql

        formatted = sqlparse.format(
            sql,
            reindent=True,
            indent_width=self.config.indent_width,
            keyword_case=self.config.keyword_case,
            strip_comments=self.config.strip_comments,
            use_space_around_operators=True,
            wrap_after=self.config.line_length
        )

        if self.config.align_columns:
            formatted = self._align_select_columns(formatted)

        return formatted.strip() + '\n'

    def _align_select_columns(self, sql: str) -> str:
        """Align columns in SELECT statements."""
        parsed = sqlparse.parse(sql)
        if not parsed:
            return sql

        result = []
        for statement in parsed:
            result.append(self._process_statement(statement))

        return '\n\n'.join(result)

    def _process_statement(self, statement: TokenList) -> str:
        """Process a single SQL statement."""
        tokens = []
        in_select = False
        select_items: List[str] = []

        for token in statement.tokens:
            if token.ttype is DML and token.value.upper() == 'SELECT':
                in_select = True
                tokens.append(str(token))
            elif in_select and self._is_keyword_or_end(token):
                if select_items:
                    tokens.append(self._format_select_items(select_items))
                    select_items = []
                in_select = False
                tokens.append(str(token))
            elif in_select:
                item = str(token).strip()
                if item and item != ',':
                    select_items.append(item)
            else:
                tokens.append(str(token))

        if select_items:
            tokens.append(self._format_select_items(select_items))

        return ''.join(tokens)

    def _is_keyword_or_end(self, token: Token) -> bool:
        """Check if token is a keyword that ends SELECT clause."""
        if token.ttype in (Keyword, DML, DDL):
            return True
        if isinstance(token, TokenList):
            first = token.token_first(skip_ws=True, skip_cm=True)
            if first and first.ttype in (Keyword, DML, DDL):
                return True
        return False

    def _format_select_items(self, items: List[str]) -> str:
        """Format SELECT column list with alignment."""
        if not items:
            return ''
        
        cleaned = [item.rstrip(',') for item in items if item.strip()]
        if not cleaned:
            return ''

        indent = ' ' * self.config.indent_width
        formatted_items = [f'\n{indent}{item}' for item in cleaned]
        return ','.join(formatted_items)

    def format_query(self, sql: str) -> str:
        """Alias for format method."""
        return self.format(sql)