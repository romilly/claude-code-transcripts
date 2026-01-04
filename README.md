# claude-code-transcripts

[![PyPI](https://img.shields.io/pypi/v/claude-code-transcripts.svg)](https://pypi.org/project/claude-code-transcripts/)
[![Changelog](https://img.shields.io/github/v/release/simonw/claude-code-transcripts?include_prereleases&label=changelog)](https://github.com/simonw/claude-code-transcripts/releases)
[![Tests](https://github.com/simonw/claude-code-transcripts/workflows/Test/badge.svg)](https://github.com/simonw/claude-code-transcripts/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/claude-code-transcripts/blob/main/LICENSE)

Browse and search Claude Code session transcripts via a web interface.

[Example transcript](https://static.simonwillison.net/static/2025/claude-code-microjs/index.html) produced using this tool.

Read [A new way to extract detailed transcripts from Claude Code](https://simonwillison.net/2025/Dec/25/claude-code-transcripts/) for background on this project.

## Installation

Install this tool using `uv`:
```bash
uv tool install claude-code-transcripts
```

## Usage

Start the web server to browse your Claude Code transcripts:

```bash
claude-code-transcripts serve
```

This starts a local web server at http://127.0.0.1:8000 where you can:
- View all your Claude Code projects
- Browse sessions within each project
- Read full conversation transcripts

### Options

```bash
claude-code-transcripts serve --help

Options:
  --host TEXT               Host to bind to (default: 127.0.0.1)
  --port INTEGER            Port to bind to (default: 8000)
  --reload                  Enable auto-reload for development
  --projects-dir DIRECTORY  Path to Claude projects directory
                           (default: ~/.claude/projects)
```

## Library Usage

This package also provides functions for working with Claude Code session files programmatically:

```python
from claude_code_transcripts import (
    parse_session_file,
    generate_html,
    find_all_sessions,
    find_local_sessions,
)

# Parse a session file (JSON or JSONL)
session_data = parse_session_file("session.jsonl")

# Generate HTML output
generate_html("session.jsonl", output_dir="./output")

# Find all local sessions grouped by project
projects = find_all_sessions()  # Uses ~/.claude/projects by default

# Find recent local sessions
sessions = find_local_sessions(limit=10)
```

## Development

To contribute to this tool, first checkout the code. You can run the tests using `uv run`:
```bash
cd claude-code-transcripts
uv run pytest
```
