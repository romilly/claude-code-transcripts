"""FastAPI application for browsing Claude Code transcripts."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import router


def create_app(projects_dir: Path | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        projects_dir: Path to Claude projects directory.
                     Defaults to ~/.claude/projects
    """
    if projects_dir is None:
        projects_dir = Path.home() / ".claude" / "projects"

    app = FastAPI(
        title="Claude Code Transcripts",
        description="Browse and search Claude Code conversation transcripts",
    )

    # Store projects_dir in app state for routes to access
    app.state.projects_dir = projects_dir

    # Set up Jinja2 templates
    templates_dir = Path(__file__).parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    app.state.templates = templates

    # Include routes
    app.include_router(router)

    return app
