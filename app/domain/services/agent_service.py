from abc import ABC, abstractmethod

from app.domain.entities.recommendation import Recommendation
from app.domain.entities.user_profile import UserProfile
from app.domain.entities.weather import Weather


class AgentService(ABC):
    @abstractmethod
    async def generate_recommendation(
        self,
        profile: UserProfile,
        weather: Weather,
        city: str,
        date: str,
        time_of_day: str,
        occasion: str,
        budget: str,
        preferences: str,
    ) -> Recommendation:
        ...
