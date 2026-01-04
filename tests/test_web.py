"""Tests for the web interface."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from claude_code_transcripts.web import create_app


@pytest.fixture
def mock_projects_dir():
    """Create a mock ~/.claude/projects structure with test sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        projects_dir = Path(tmpdir)

        # Create project-a with 2 sessions
        project_a = projects_dir / "-home-user-projects-project-a"
        project_a.mkdir(parents=True)

        session_a1 = project_a / "abc123.jsonl"
        session_a1.write_text(
            '{"type": "user", "timestamp": "2025-01-01T10:00:00.000Z", "message": {"role": "user", "content": "Hello from project A"}}\n'
            '{"type": "assistant", "timestamp": "2025-01-01T10:00:05.000Z", "message": {"role": "assistant", "content": [{"type": "text", "text": "Hi there!"}]}}\n'
        )

        session_a2 = project_a / "def456.jsonl"
        session_a2.write_text(
            '{"type": "user", "timestamp": "2025-01-02T10:00:00.000Z", "message": {"role": "user", "content": "Second session"}}\n'
        )

        # Create project-b with 1 session
        project_b = projects_dir / "-home-user-projects-project-b"
        project_b.mkdir(parents=True)

        session_b1 = project_b / "ghi789.jsonl"
        session_b1.write_text(
            '{"type": "user", "timestamp": "2025-01-03T10:00:00.000Z", "message": {"role": "user", "content": "Hello from project B"}}\n'
        )

        yield projects_dir


@pytest.fixture
def client(mock_projects_dir):
    """Create a test client for the web app."""
    app = create_app(projects_dir=mock_projects_dir)
    return TestClient(app)


class TestProjectsPage:
    """Tests for the projects listing page."""

    def test_index_returns_html(self, client):
        """Test that index page returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_index_lists_projects(self, client):
        """Test that index page lists all projects."""
        response = client.get("/")
        assert "project-a" in response.text
        assert "project-b" in response.text

    def test_index_shows_session_counts(self, client):
        """Test that index page shows session counts."""
        response = client.get("/")
        # project-a has 2 sessions
        assert "2 sessions" in response.text
        # project-b has 1 session
        assert "1 session" in response.text

    def test_index_has_project_links(self, client):
        """Test that project names are clickable links."""
        response = client.get("/")
        assert 'href="/project/project-a"' in response.text
        assert 'href="/project/project-b"' in response.text


class TestEmptyProjectsDir:
    """Tests for when no projects exist."""

    def test_empty_projects_shows_message(self):
        """Test that empty projects directory shows helpful message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            app = create_app(projects_dir=Path(tmpdir))
            client = TestClient(app)

            response = client.get("/")
            assert response.status_code == 200
            assert "No projects found" in response.text
