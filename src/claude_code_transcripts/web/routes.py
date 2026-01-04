"""Route handlers for the web interface."""

import json

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from markupsafe import Markup

from ..discovery import find_all_sessions
from ..parsing import parse_session_file
from ..rendering import render_message

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


@router.get("/session/{project_name}/{session_id}", response_class=HTMLResponse)
async def view_session(request: Request, project_name: str, session_id: str):
    """View a single session's conversation."""
    projects_dir = request.app.state.projects_dir
    templates = request.app.state.templates

    projects = find_all_sessions(projects_dir)

    # Find the requested project
    project = next((p for p in projects if p["name"] == project_name), None)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")

    # Find the requested session
    session = next(
        (s for s in project["sessions"] if s["path"].stem == session_id),
        None
    )
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    # Parse the session file
    session_data = parse_session_file(session["path"])

    # Render messages
    rendered_messages = []
    for logline in session_data.get("loglines", []):
        msg_type = logline.get("type")
        if msg_type in ("user", "assistant"):
            message_json = json.dumps(logline.get("message", {}))
            timestamp = logline.get("timestamp", "")
            html = render_message(msg_type, message_json, timestamp)
            rendered_messages.append({
                "type": msg_type,
                "html": Markup(html),
            })

    return templates.TemplateResponse(
        request,
        "session.html",
        {
            "project": project,
            "session": session,
            "messages": rendered_messages,
        },
    )
