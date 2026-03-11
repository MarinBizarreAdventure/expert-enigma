from abc import ABC, abstractmethod

from app.domain.entities.user_profile import UserProfile


class UserRepository(ABC):
    @abstractmethod
    async def get_profile(self, user_id: str) -> UserProfile:
        ...

    @abstractmethod
    async def save_profile(self, profile: UserProfile) -> UserProfile:
        ...

    @abstractmethod
    async def update_profile(self, user_id: str, updates: dict) -> UserProfile:
        ...
