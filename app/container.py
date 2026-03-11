from functools import lru_cache

from app.config import Settings
from app.application.use_cases.chat import Chat
from app.application.use_cases.get_recommendation import GetRecommendation
from app.application.use_cases.get_user_profile import GetUserProfile
from app.application.use_cases.onboard_user import OnboardUser
from app.application.use_cases.update_user_profile import UpdateUserProfile
from app.infrastructure.claude.claude_agent import ClaudeAgentService
from app.infrastructure.persistence.json_conversation_repository import JsonConversationRepository
from app.infrastructure.persistence.json_repository import JsonUserRepository
from app.infrastructure.scraper.web_scraper import WebScraper
from app.infrastructure.weather.open_meteo import OpenMeteoWeatherService


class Container:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._user_repository = JsonUserRepository(settings.data_dir)
        self._conversation_repository = JsonConversationRepository(settings.data_dir)
        self._weather_service = OpenMeteoWeatherService(settings.open_meteo_base_url)
        self._web_scraper = WebScraper()
        self._agent_service = ClaudeAgentService(
            api_key=settings.claude_api_key,
            weather_service=self._weather_service,
            web_scraper=self._web_scraper,
        )

    def weather_service(self) -> OpenMeteoWeatherService:
        return self._weather_service

    def onboard_user(self) -> OnboardUser:
        return OnboardUser(self._user_repository)

    def get_user_profile(self) -> GetUserProfile:
        return GetUserProfile(self._user_repository)

    def update_user_profile(self) -> UpdateUserProfile:
        return UpdateUserProfile(self._user_repository)

    def chat(self) -> Chat:
        return Chat(
            user_repository=self._user_repository,
            conversation_repository=self._conversation_repository,
            agent_service=self._agent_service,
        )

    def get_recommendation(self) -> GetRecommendation:
        return GetRecommendation(
            user_repository=self._user_repository,
            weather_service=self._weather_service,
            agent_service=self._agent_service,
        )


@lru_cache
def get_container() -> Container:
    from app.config import settings
    return Container(settings)
