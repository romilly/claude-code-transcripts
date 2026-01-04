"""Route handlers for the web interface."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..discovery import find_all_sessions

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """List all projects with their sessions."""
    projects_dir = request.app.state.projects_dir
    templates = request.app.state.templates

    projects = find_all_sessions(projects_dir)

    return templates.TemplateResponse(
        request,
        "projects.html",
        {
            "projects": projects,
            "projects_dir": projects_dir,
        },
    )
