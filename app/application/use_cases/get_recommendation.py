from app.domain.entities.recommendation import Recommendation
from app.domain.services.agent_service import AgentService
from app.domain.services.user_repository import UserRepository
from app.domain.services.weather_service import WeatherService


class GetRecommendation:
    def __init__(
        self,
        user_repository: UserRepository,
        weather_service: WeatherService,
        agent_service: AgentService,
    ):
        self._user_repository = user_repository
        self._weather_service = weather_service
        self._agent_service = agent_service

    async def execute(
        self,
        user_id: str,
        city: str,
        date: str,
        time_of_day: str,
        occasion: str,
        budget: str,
        preferences: str,
    ) -> Recommendation:
        raise NotImplementedError("Use /api/v1/chat for recommendations")
