"""Configuration management for SQL Format."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json

@dataclass
class Config:
    """Configuration for SQL formatting."""
    indent_width: int = 4
    keyword_case: str = 'upper'
    strip_comments: bool = False
    line_length: int = 80
    dialect: str = 'postgresql'
    align_columns: bool = True

    @classmethod
    def from_file(cls, path: Path) -> 'Config':
        """Load configuration from JSON file."""
        if not path.exists():
            return cls()

        try:
            data = json.loads(path.read_text())
            return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
        except (json.JSONDecodeError, TypeError):
            return cls()

    @classmethod
    def find_config(cls, start_path: Optional[Path] = None) -> 'Config':
        """Find and load .sqlformatrc from current or parent directories."""
        search_path = start_path or Path.cwd()
        
        for parent in [search_path] + list(search_path.parents):
            config_file = parent / '.sqlformatrc'
            if config_file.exists():
                return cls.from_file(config_file)
        
        return cls()

    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            'indent_width': self.indent_width,
            'keyword_case': self.keyword_case,
            'strip_comments': self.strip_comments,
            'line_length': self.line_length,
            'dialect': self.dialect,
            'align_columns': self.align_columns
        }