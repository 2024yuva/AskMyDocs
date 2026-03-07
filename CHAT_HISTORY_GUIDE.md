# 💬 Chat History Feature Guide

## Overview

AskMyDocs now includes persistent chat history! Your conversations are automatically saved and can be viewed, loaded, or deleted at any time.

## Features

### 1. Automatic Session Management
- Each browser session gets a unique ID
- Sessions are tracked automatically
- No login required

### 2. Save Conversations
Click **"💾 Save Conversation"** in the sidebar to save your current chat:
- Saves all messages (questions + answers)
- Includes citations and source documents
- Stores timestamp and metadata

### 3. View History
Click **"📜 View History"** to see your saved conversations:
- Shows last 10 sessions
- Displays date and message count
- Quick preview of each session

### 4. Load Previous Conversations
- Click **"Load"** on any saved session
- Restores all messages to the chat
- Continue where you left off

### 5. Delete Old Conversations
- Click **"Delete"** to remove a session
- Permanently deletes all files for that session
- Frees up storage space

### 6. Clear Current Chat
- Click **"🗑️ Clear Current Chat"**
- Starts fresh without deleting saved history
- Keeps your session ID

## Storage Location

Chat history is stored in:
```
AskMyDocs/
└── chat_history/
    ├── abc123_20250307_143022.json
    ├── abc123_20250307_150145.json
    └── def456_20250307_160330.json
```

Each file contains:
- Session ID
- Timestamp
- All messages with full context
- Citations and source documents
- Metadata

## File Format

```json
{
  "session_id": "abc123def456",
  "timestamp": "2025-03-07T14:30:22",
  "message_count": 5,
  "messages": [
    {
      "role": "user",
      "content": "What is RAG?"
    },
    {
      "role": "assistant",
      "content": "RAG stands for...",
      "citations": [...],
      "source_documents": [...]
    }
  ],
  "metadata": {
    "saved_at": "2025-03-07T14:35:00"
  }
}
```

## Use Cases

### 1. Research Sessions
Save your research conversations and come back later to review findings.

### 2. Team Collaboration
Export sessions to share with team members.

### 3. Audit Trail
Keep track of what questions were asked and what answers were provided.

### 4. Learning
Review previous conversations to understand topics better.

## Advanced Features

### Export Session (via Python)
```python
from app.chat_history import get_chat_history

history = get_chat_history()
history.export_session(
    session_id="abc123",
    output_path="my_research.json"
)
```

### List All Sessions (via Python)
```python
from app.chat_history import get_chat_history

history = get_chat_history()
sessions = history.list_sessions(limit=50)

for session in sessions:
    print(f"Session: {session['session_id']}")
    print(f"Messages: {session['message_count']}")
    print(f"Last active: {session['last_message']}")
```

### Load Specific Session (via Python)
```python
from app.chat_history import get_chat_history

history = get_chat_history()
conversation = history.load_conversation("abc123")

if conversation:
    for msg in conversation['messages']:
        print(f"{msg['role']}: {msg['content'][:100]}...")
```

## Privacy & Security

- **Local Storage**: All history is stored locally on your machine
- **No Cloud**: Nothing is sent to external servers
- **Full Control**: You can delete any conversation at any time
- **No Tracking**: Session IDs are random and not linked to personal info

## Tips

1. **Save Regularly**: Click save after important conversations
2. **Organize**: Use descriptive questions to make history searchable
3. **Clean Up**: Delete old sessions you don't need
4. **Backup**: Copy the `chat_history/` folder to backup your conversations

## Troubleshooting

### History not showing?
- Make sure you've saved at least one conversation
- Check that `chat_history/` folder exists
- Refresh the UI

### Can't load a session?
- The session file might be corrupted
- Try deleting and starting fresh
- Check file permissions

### Storage getting full?
- Delete old sessions you don't need
- Export important sessions and delete originals
- The JSON files are small (~1-5KB each)

## Future Enhancements

Planned features:
- 🔍 Search within history
- 📊 Analytics (most asked questions, etc.)
- 📤 Export to PDF/Markdown
- 🏷️ Tag conversations
- ⭐ Favorite important conversations

Enjoy your persistent chat history! 💬
