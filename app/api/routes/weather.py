from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from app.api.dependencies import get_weather_service
from app.api.schemas.responses import WeatherResponse
from app.domain.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/{city}", response_model=WeatherResponse)
async def get_weather(
    city: str,
    date: Optional[str] = None,
    weather_service: WeatherService = Depends(get_weather_service),
) -> WeatherResponse:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    weather = await weather_service.get_weather(city, date)
    return WeatherResponse(**weather.model_dump())
