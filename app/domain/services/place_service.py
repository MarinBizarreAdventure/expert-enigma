from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.place import Place
from app.domain.entities.weather import Weather


class PlaceService(ABC):
    @abstractmethod
    async def find_places(self, city: str, query: str, weather: Weather) -> List[Place]:
        ...
