from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    AgentError,
    ProfileAlreadyExists,
    ProfileNotFound,
    ScrapingFailed,
    WeatherUnavailable,
)
from app.api.routes import health, profile, recommend

app = FastAPI(title="Expert Enigma", version="0.1.0")

app.include_router(health.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(recommend.router, prefix="/api/v1")


@app.exception_handler(ProfileNotFound)
async def profile_not_found_handler(request: Request, exc: ProfileNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "hint": "Create a profile first: POST /api/v1/profile",
        },
    )


@app.exception_handler(ProfileAlreadyExists)
async def profile_already_exists_handler(request: Request, exc: ProfileAlreadyExists) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(WeatherUnavailable)
async def weather_unavailable_handler(request: Request, exc: WeatherUnavailable) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


@app.exception_handler(ScrapingFailed)
async def scraping_failed_handler(request: Request, exc: ScrapingFailed) -> JSONResponse:
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )


@app.exception_handler(AgentError)
async def agent_error_handler(request: Request, exc: AgentError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
