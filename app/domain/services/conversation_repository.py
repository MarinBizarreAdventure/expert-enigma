from abc import ABC, abstractmethod

from app.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    @abstractmethod
    async def get(self, conversation_id: str) -> Conversation:
        ...

    @abstractmethod
    async def save(self, conversation: Conversation) -> Conversation:
        ...

    @abstractmethod
    async def create(self, user_id: str) -> Conversation:
        ...
