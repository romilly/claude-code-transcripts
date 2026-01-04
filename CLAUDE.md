# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_generate_html.py::TestClassName::test_method_name -v
```

## Development Practices

Practice TDD: write a failing test, watch it fail, then make it pass.

Commit early and often. Commits should bundle the test, implementation, and documentation changes together.

## Architecture

The package converts Claude Code session files (JSON/JSONL) to paginated HTML transcripts.

### Module Structure

- `__init__.py` - Package initialization, public API re-exports
- `html_generation.py` - Core HTML generation: `generate_html()`, `generate_batch_html()`, pagination
- `rendering.py` - Markdown rendering and content block formatting (tool results, code blocks, etc.)
- `parsing.py` - Session file parsing (JSON/JSONL), text extraction
- `discovery.py` - Finding sessions in `~/.claude/projects`
- `analysis.py` - Conversation statistics, commit detection, GitHub repo detection
- `gist.py` - GitHub Gist creation via `gh` CLI
- `models.py` - Data classes (`ConversationStats`)

### Templates

HTML generation uses Jinja2 templates in `templates/`:
- `index.html`, `page.html` - Main transcript templates
- `macros.html` - Reusable HTML components
- `styles.css`, `main.js` - Extracted CSS/JS assets
- `gist_preview.js` - Script injected for gisthost.github.io compatibility

### Key Data Flow

1. Session file → `parsing.parse_session_file()` → loglines dict
2. Loglines → `html_generation._generate_html_from_data()` → conversations grouped by user prompt
3. Conversations → `rendering.render_message()` → HTML fragments
4. HTML fragments → Jinja2 templates → paginated HTML files

### Testing

Tests use pytest with syrupy for snapshot testing. Test data lives in `tests/data/`, snapshots in `tests/__snapshots__/`.
