from typing import Optional, Tuple

from app.domain.services.agent_service import AgentService
from app.domain.services.conversation_repository import ConversationRepository
from app.domain.services.user_repository import UserRepository


class Chat:
    def __init__(
        self,
        user_repository: UserRepository,
        conversation_repository: ConversationRepository,
        agent_service: AgentService,
    ):
        self._user_repository = user_repository
        self._conversation_repository = conversation_repository
        self._agent_service = agent_service

    async def execute(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
    ) -> Tuple[str, str, Optional[dict]]:
        profile = await self._user_repository.get_profile(user_id)

        if conversation_id:
            conversation = await self._conversation_repository.get(conversation_id)
        else:
            conversation = await self._conversation_repository.create(user_id)

        messages = list(conversation.messages) + [{"role": "user", "content": message}]

        reply, updated_messages, structured_data = await self._agent_service.chat(profile, messages)

        conversation.messages = updated_messages
        await self._conversation_repository.save(conversation)

        return reply, conversation.id, structured_data
