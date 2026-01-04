"""Route handlers for the web interface."""

from fastapi import APIRouter, Request, HTTPException
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


@router.get("/project/{project_name}", response_class=HTMLResponse)
async def project_sessions(request: Request, project_name: str):
    """List all sessions in a project."""
    projects_dir = request.app.state.projects_dir
    templates = request.app.state.templates

    projects = find_all_sessions(projects_dir)

    # Find the requested project
    project = next((p for p in projects if p["name"] == project_name), None)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")

    return templates.TemplateResponse(
        request,
        "sessions.html",
        {
            "project": project,
        },
    )
