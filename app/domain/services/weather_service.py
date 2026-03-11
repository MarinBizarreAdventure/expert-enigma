from abc import ABC, abstractmethod

from app.domain.entities.weather import Weather


class WeatherService(ABC):
    @abstractmethod
    async def get_weather(self, city: str, date: str) -> Weather:
        ...
