from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from app.domain.entities.user_profile import UserProfile


class AgentService(ABC):
    @abstractmethod
    async def chat(
        self,
        profile: UserProfile,
        messages: List[dict],
    ) -> Tuple[str, List[dict], Optional[Dict[str, Any]]]:
        """
        Run the agent loop.
        Returns (reply_text, updated_messages, structured_data_or_None).
        structured_data contains: places, outfit (from present_recommendation tool).
        """
        ...
