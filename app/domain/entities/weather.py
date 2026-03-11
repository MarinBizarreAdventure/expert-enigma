from typing import Optional

from pydantic import BaseModel


class Weather(BaseModel):
    temperature_c: float
    condition: str
    humidity: int
    wind_kmh: float
    feels_like_c: Optional[float] = None
