from app.domain.entities.recommendation import Recommendation
from app.domain.entities.user_profile import UserProfile
from app.domain.entities.weather import Weather
from app.domain.services.agent_service import AgentService


class ClaudeAgentService(AgentService):
    def __init__(self, api_key: str):
        self._api_key = api_key

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
        raise NotImplementedError
