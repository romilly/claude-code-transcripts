"""Convert Claude Code session JSON to browsable HTML transcripts."""

from pathlib import Path

import click
from jinja2 import Environment, PackageLoader

from .models import ConversationStats
from .parsing import (
    extract_text_from_content,
    get_session_summary,
    parse_session_file,
)
from .discovery import (
    find_local_sessions,
    find_all_sessions,
    get_project_display_name,
)
from . import rendering
from .rendering import (
    format_json,
    render_markdown_text,
    is_json_like,
    render_todo_write,
    render_write_tool,
    render_edit_tool,
    render_bash_tool,
    render_content_block,
    render_user_message_content,
    render_assistant_message,
    make_msg_id,
    is_tool_result_message,
    render_message,
)
from .analysis import (
    COMMIT_PATTERN,
    GITHUB_REPO_PATTERN,
    LONG_TEXT_THRESHOLD,
    detect_github_repo,
    analyze_conversation,
    format_tool_stats,
)
from .gist import (
    GIST_PREVIEW_JS,
    inject_gist_preview_js,
    create_gist,
)
from .html_generation import (
    CSS,
    JS,
    PROMPTS_PER_PAGE,
    generate_pagination_html,
    generate_index_pagination_html,
    generate_html,
    generate_html_from_session_data,
    generate_batch_html,
    get_template,
)

# Set up Jinja2 environment
_jinja_env = Environment(
    loader=PackageLoader("claude_code_transcripts", "templates"),
    autoescape=True,
)


# Load macros template and expose macros
_macros_template = _jinja_env.get_template("macros.html")
_macros = _macros_template.module

# Initialize rendering module with dependencies
rendering.init(_macros, COMMIT_PATTERN)


@click.group()
@click.version_option(None, "-v", "--version", package_name="claude-code-transcripts")
def cli():
    """Browse and search Claude Code session transcripts."""
    pass


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
@click.option(
    "--projects-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Path to Claude projects directory (default: ~/.claude/projects)",
)
def serve(host: str, port: int, reload: bool, projects_dir: Path | None):
    """Start the web server to browse transcripts."""
    import uvicorn
    from .web import create_app

    if projects_dir is None:
        projects_dir = Path.home() / ".claude" / "projects"

    click.echo(f"Starting server at http://{host}:{port}")
    click.echo(f"Projects directory: {projects_dir}")

    # Create the app
    app = create_app(projects_dir=projects_dir)

    # Run with uvicorn
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
    )


def main():
    cli()
