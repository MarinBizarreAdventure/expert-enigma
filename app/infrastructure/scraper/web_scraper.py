from typing import List

from app.domain.entities.place import Place
from app.domain.entities.weather import Weather
from app.domain.services.place_service import PlaceService


class WebScraperPlaceService(PlaceService):
    async def find_places(self, city: str, query: str, weather: Weather) -> List[Place]:
        raise NotImplementedError
