"""CLI interface for SQL Format."""
import sys
import click
from pathlib import Path
from typing import Optional
from .formatter import SQLFormatter
from .config import Config

@click.command()
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('-i', '--in-place', is_flag=True, help='Modify file in place')
@click.option('--backup', is_flag=True, help='Create backup before in-place edit')
@click.option('-d', '--directory', type=click.Path(exists=True), help='Process all .sql files in directory')
@click.option('--indent', type=click.Choice(['2', '4']), default='4', help='Indentation spaces')
@click.option('--keyword-case', type=click.Choice(['upper', 'lower']), default='upper', help='Keyword case')
@click.option('--strip-comments', is_flag=True, help='Remove SQL comments')
@click.option('--dry-run', is_flag=True, help='Preview changes without writing')
@click.option('--line-length', type=int, default=80, help='Maximum line length')
@click.option('--dialect', type=click.Choice(['postgresql', 'mysql', 'sqlite', 'mssql']), default='postgresql', help='SQL dialect')
def main(input_file: Optional[str], output: Optional[str], in_place: bool, backup: bool,
         directory: Optional[str], indent: str, keyword_case: str, strip_comments: bool,
         dry_run: bool, line_length: int, dialect: str) -> None:
    """Format SQL queries with consistent style and indentation."""
    config = Config(
        indent_width=int(indent),
        keyword_case=keyword_case,
        strip_comments=strip_comments,
        line_length=line_length,
        dialect=dialect
    )
    formatter = SQLFormatter(config)

    if directory:
        process_directory(Path(directory), formatter, in_place, backup, dry_run)
    elif input_file:
        process_file(Path(input_file), formatter, output, in_place, backup, dry_run)
    else:
        process_stdin(formatter)

def process_stdin(formatter: SQLFormatter) -> None:
    """Read SQL from stdin and write formatted output to stdout."""
    sql = sys.stdin.read()
    formatted = formatter.format(sql)
    click.echo(formatted)

def process_file(path: Path, formatter: SQLFormatter, output: Optional[str],
                 in_place: bool, backup: bool, dry_run: bool) -> None:
    """Process a single SQL file."""
    sql = path.read_text(encoding='utf-8')
    formatted = formatter.format(sql)

    if dry_run:
        click.echo(f"--- {path} ---")
        click.echo(formatted)
        return

    if in_place:
        if backup:
            backup_path = path.with_suffix(path.suffix + '.bak')
            backup_path.write_text(sql, encoding='utf-8')
        path.write_text(formatted, encoding='utf-8')
        click.echo(f"Formatted: {path}")
    elif output:
        Path(output).write_text(formatted, encoding='utf-8')
        click.echo(f"Written to: {output}")
    else:
        click.echo(formatted)

def process_directory(directory: Path, formatter: SQLFormatter,
                      in_place: bool, backup: bool, dry_run: bool) -> None:
    """Process all .sql files in a directory."""
    sql_files = list(directory.glob('**/*.sql'))
    if not sql_files:
        click.echo(f"No .sql files found in {directory}")
        return

    for sql_file in sql_files:
        process_file(sql_file, formatter, None, in_place, backup, dry_run)

if __name__ == '__main__':
    main()