"""
Chat history management for AskMyDocs.
Stores conversation history in JSON files with timestamps.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ChatHistory:
    """Manages chat history storage and retrieval."""

    def __init__(self, history_dir: Path = None):
        """
        Initialize chat history manager.
        
        Args:
            history_dir: Directory to store chat history files
        """
        if history_dir is None:
            # Store in project root / chat_history
            project_root = Path(__file__).resolve().parent.parent
            history_dir = project_root / "chat_history"
        
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)
        logger.info(f"Chat history directory: {self.history_dir}")

    def save_conversation(
        self,
        session_id: str,
        messages: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Save a conversation to a JSON file.
        
        Args:
            session_id: Unique session identifier
            messages: List of message dicts with role, content, citations, etc.
            metadata: Optional metadata (user info, timestamps, etc.)
        
        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().isoformat()
        
        conversation = {
            "session_id": session_id,
            "timestamp": timestamp,
            "message_count": len(messages),
            "messages": messages,
            "metadata": metadata or {}
        }
        
        # Create filename with timestamp
        filename = f"{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.history_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved conversation: {filepath}")
        return filepath

    def load_conversation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load the most recent conversation for a session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            Conversation dict or None if not found
        """
        # Find all files for this session
        pattern = f"{session_id}_*.json"
        files = sorted(self.history_dir.glob(pattern), reverse=True)
        
        if not files:
            return None
        
        # Load the most recent one
        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List all chat sessions with metadata.
        
        Args:
            limit: Maximum number of sessions to return
        
        Returns:
            List of session summaries
        """
        sessions = {}
        
        for filepath in self.history_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                session_id = data.get("session_id")
                if session_id not in sessions:
                    sessions[session_id] = {
                        "session_id": session_id,
                        "first_message": data["timestamp"],
                        "last_message": data["timestamp"],
                        "message_count": data["message_count"],
                        "files": []
                    }
                
                sessions[session_id]["files"].append(str(filepath))
                sessions[session_id]["last_message"] = max(
                    sessions[session_id]["last_message"],
                    data["timestamp"]
                )
            except Exception as e:
                logger.error(f"Error loading {filepath}: {e}")
        
        # Sort by last message time
        sorted_sessions = sorted(
            sessions.values(),
            key=lambda x: x["last_message"],
            reverse=True
        )
        
        return sorted_sessions[:limit]

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all conversations for a session, sorted by time.
        
        Args:
            session_id: Session identifier
        
        Returns:
            List of conversation dicts
        """
        pattern = f"{session_id}_*.json"
        files = sorted(self.history_dir.glob(pattern))
        
        conversations = []
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    conversations.append(json.load(f))
            except Exception as e:
                logger.error(f"Error loading {filepath}: {e}")
        
        return conversations

    def delete_session(self, session_id: str) -> int:
        """
        Delete all conversations for a session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            Number of files deleted
        """
        pattern = f"{session_id}_*.json"
        files = list(self.history_dir.glob(pattern))
        
        count = 0
        for filepath in files:
            try:
                filepath.unlink()
                count += 1
            except Exception as e:
                logger.error(f"Error deleting {filepath}: {e}")
        
        logger.info(f"Deleted {count} files for session {session_id}")
        return count

    def export_session(self, session_id: str, output_path: Path) -> Path:
        """
        Export a session to a single JSON file.
        
        Args:
            session_id: Session identifier
            output_path: Path to save the export
        
        Returns:
            Path to the exported file
        """
        conversations = self.get_session_history(session_id)
        
        export_data = {
            "session_id": session_id,
            "export_timestamp": datetime.now().isoformat(),
            "conversation_count": len(conversations),
            "conversations": conversations
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported session to: {output_path}")
        return output_path


# ── Convenience functions ────────────────────────────────────────────────────

_history_instance: ChatHistory | None = None


def get_chat_history() -> ChatHistory:
    """Get or create a singleton chat history instance."""
    global _history_instance
    if _history_instance is None:
        _history_instance = ChatHistory()
    return _history_instance
