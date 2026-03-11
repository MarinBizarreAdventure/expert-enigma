from app.domain.entities.weather import Weather
from app.domain.services.weather_service import WeatherService


class OpenMeteoWeatherService(WeatherService):
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def get_weather(self, city: str, date: str) -> Weather:
        raise NotImplementedError
