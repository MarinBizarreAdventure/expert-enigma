from fastapi import Depends

from app.application.use_cases.chat import Chat
from app.application.use_cases.get_recommendation import GetRecommendation
from app.application.use_cases.get_user_profile import GetUserProfile
from app.application.use_cases.onboard_user import OnboardUser
from app.application.use_cases.update_user_profile import UpdateUserProfile
from app.container import Container, get_container
from app.domain.services.weather_service import WeatherService


def get_onboard_user(container: Container = Depends(get_container)) -> OnboardUser:
    return container.onboard_user()


def get_get_user_profile(container: Container = Depends(get_container)) -> GetUserProfile:
    return container.get_user_profile()


def get_update_user_profile(container: Container = Depends(get_container)) -> UpdateUserProfile:
    return container.update_user_profile()


def get_chat(container: Container = Depends(get_container)) -> Chat:
    return container.chat()


def get_weather_service(container: Container = Depends(get_container)) -> WeatherService:
    return container.weather_service()


def get_get_recommendation(container: Container = Depends(get_container)) -> GetRecommendation:
    return container.get_recommendation()
