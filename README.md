# sql-format

A CLI tool that formats SQL queries with consistent style and indentation for improved readability

## Features

- Format SQL queries with consistent keyword capitalization (uppercase/lowercase configurable)
- Apply consistent indentation (2 or 4 spaces, configurable)
- Support multiple SQL dialects (PostgreSQL, MySQL, SQLite, MSSQL)
- Process single queries from stdin or command arguments
- Batch process multiple .sql files in a directory
- Preserve or strip SQL comments based on configuration
- Align columns in SELECT statements for readability
- Format JOIN clauses with proper indentation
- Handle subqueries with nested indentation
- Dry-run mode to preview changes without modifying files
- In-place file modification with backup option
- Configurable line length for wrapping long queries
- Output formatted SQL to stdout or overwrite source file

## How to Use

Use this project when you need to:

- Quickly solve problems related to sql-format
- Integrate python functionality into your workflow
- Learn how python handles common patterns with click

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/sql-format.git
cd sql-format

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python using click

## Dependencies

- `click`
- `sqlparse`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
