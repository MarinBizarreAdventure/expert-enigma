import json
from datetime import datetime, timezone
from pathlib import Path

from app.domain.entities.conversation import Conversation
from app.domain.exceptions import ConversationNotFound
from app.domain.services.conversation_repository import ConversationRepository


class JsonConversationRepository(ConversationRepository):
    def __init__(self, data_dir: str):
        self._file_path = Path(data_dir) / "conversations.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._file_path.write_text("{}")

    def _read(self) -> dict:
        return json.loads(self._file_path.read_text())

    def _write(self, data: dict) -> None:
        self._file_path.write_text(json.dumps(data, indent=2))

    async def get(self, conversation_id: str) -> Conversation:
        data = self._read()
        if conversation_id not in data:
            raise ConversationNotFound(conversation_id)
        return Conversation(**data[conversation_id])

    async def save(self, conversation: Conversation) -> Conversation:
        data = self._read()
        conversation.updated_at = datetime.now(timezone.utc).isoformat()
        data[conversation.id] = conversation.model_dump()
        self._write(data)
        return conversation

    async def create(self, user_id: str) -> Conversation:
        conversation = Conversation(user_id=user_id)
        data = self._read()
        data[conversation.id] = conversation.model_dump()
        self._write(data)
        return conversation
