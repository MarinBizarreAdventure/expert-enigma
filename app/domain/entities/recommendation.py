from typing import List

from pydantic import BaseModel

from app.domain.entities.outfit import OutfitSuggestion
from app.domain.entities.place import Place
from app.domain.entities.weather import Weather


class Recommendation(BaseModel):
    weather: Weather
    places: List[Place]
    outfit: OutfitSuggestion
    summary: str
