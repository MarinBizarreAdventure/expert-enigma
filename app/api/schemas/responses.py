from typing import List, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


class ErrorResponse(BaseModel):
    detail: str
    hint: Optional[str] = None


class WeatherResponse(BaseModel):
    temperature_c: float
    condition: str
    humidity: int
    wind_kmh: float
    feels_like_c: Optional[float] = None


class PlaceResponse(BaseModel):
    name: str
    type: str
    address: str
    why: str
    price_range: Optional[str] = None
    rating: Optional[float] = None
    dress_code: Optional[str] = None


class OutfitResponse(BaseModel):
    items: List[str]
    reasoning: str


class RecommendationResponse(BaseModel):
    weather: WeatherResponse
    places: List[PlaceResponse]
    outfit: OutfitResponse
    summary: str


class ProfileResponse(BaseModel):
    user_id: str
    name: str
    default_city: str
    style_preferences: List[str]
    budget_default: str
    dietary_restrictions: List[str]
    favorite_cuisines: List[str]
    avoid: List[str]
