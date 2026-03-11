import httpx

from app.domain.entities.weather import Weather
from app.domain.exceptions import WeatherUnavailable
from app.domain.services.weather_service import WeatherService

WMO_CODES: dict[int, str] = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "icy fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "heavy drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "light snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light rain showers",
    81: "moderate rain showers",
    82: "heavy rain showers",
    85: "light snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
    99: "thunderstorm with heavy hail",
}


class OpenMeteoWeatherService(WeatherService):
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def get_weather(self, city: str, date: str) -> Weather:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                geo_resp = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city, "count": 1, "language": "en", "format": "json"},
                )
                geo_resp.raise_for_status()
                geo_data = geo_resp.json()

                if not geo_data.get("results"):
                    raise WeatherUnavailable(city)

                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                weather_resp = await client.get(
                    f"{self._base_url}/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,apparent_temperature",
                        "forecast_days": 7,
                        "timezone": "auto",
                    },
                )
                weather_resp.raise_for_status()
                data = weather_resp.json()

                times = data["hourly"]["time"]
                target = f"{date}T12:00"
                if target not in times:
                    target = next((t for t in times if t.startswith(date)), None)
                    if target is None:
                        raise WeatherUnavailable(city)

                idx = times.index(target)
                hourly = data["hourly"]
                code = int(hourly["weather_code"][idx])

                return Weather(
                    temperature_c=round(hourly["temperature_2m"][idx], 1),
                    condition=WMO_CODES.get(code, f"weather code {code}"),
                    humidity=int(hourly["relative_humidity_2m"][idx]),
                    wind_kmh=round(hourly["wind_speed_10m"][idx], 1),
                    feels_like_c=round(hourly["apparent_temperature"][idx], 1),
                )
        except WeatherUnavailable:
            raise
        except Exception as exc:
            raise WeatherUnavailable(city) from exc
