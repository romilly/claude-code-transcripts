"""Data models for Claude Code transcripts.

These dataclasses provide typed structures for session data,
making the code easier to understand and enabling IDE support.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConversationStats:
    """Statistics extracted from analyzing a conversation."""

    tool_counts: dict[str, int] = field(default_factory=dict)
    long_texts: list[str] = field(default_factory=list)
    commits: list[tuple[str, str, str]] = field(default_factory=list)
    """List of (commit_hash, commit_message, timestamp) tuples."""


@dataclass
class Conversation:
    """A conversation starting with a user prompt.

    Groups all messages that follow a user prompt until the next prompt.
    """

    user_text: str
    timestamp: str
    messages: list[tuple[str, str, str]] = field(default_factory=list)
    """List of (log_type, message_json, timestamp) tuples."""
    is_continuation: bool = False
    """True if this is a continuation of a previous session."""


@dataclass
class SessionInfo:
    """Metadata about a session file for discovery/listing."""

    path: str
    """Path to the session file."""
    summary: str
    """Human-readable summary of the session."""
    modified_time: Optional[float] = None
    """Modification time as Unix timestamp."""


@dataclass
class ProjectInfo:
    """Information about a project containing sessions."""

    name: str
    """Display name of the project."""
    folder_name: str
    """Encoded folder name from ~/.claude/projects."""
    sessions: list[SessionInfo] = field(default_factory=list)
