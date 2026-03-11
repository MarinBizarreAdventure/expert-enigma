from app.domain.entities.user_profile import UserProfile
from app.domain.services.user_repository import UserRepository


class UpdateUserProfile:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, user_id: str, updates: dict) -> UserProfile:
        return await self._user_repository.update_profile(user_id, updates)
