from app.domain.entities.user_profile import UserProfile
from app.domain.exceptions import ProfileAlreadyExists
from app.domain.services.user_repository import UserRepository


class OnboardUser:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, profile: UserProfile) -> UserProfile:
        try:
            await self._user_repository.get_profile(profile.user_id)
            raise ProfileAlreadyExists(profile.user_id)
        except Exception as e:
            from app.domain.exceptions import ProfileNotFound
            if not isinstance(e, ProfileNotFound):
                raise
        return await self._user_repository.save_profile(profile)
