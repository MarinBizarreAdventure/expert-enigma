# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered going-out assistant. Given a user's city, preferences, and plans, it:
1. Fetches current/forecast weather for the user's city
2. Scrapes the internet to find going-out options (restaurants, bars, events, etc.) in that city
3. Recommends multiple place options based on preferences and weather
4. Suggests what to wear (wardrobe recommendations) based on weather, venue type, and user preferences
5. Helps with route planning between selected places

## Tech Stack

- **Language:** Python (use type hints everywhere, no comments in code)
- **Framework:** FastAPI
- **Validation:** Pydantic models for all DTOs, requests, responses
- **AI:** Claude API via Anthropic SDK - the agent's reasoning engine
- **Persistence:** JSON file-based repository (no database)
- **External services:** Open-Meteo weather API (free, no key), web scraping via httpx + BeautifulSoup

## Architecture (Clean Architecture + Dependency Injection)

```
expert-enigma/
├── app/
│   ├── main.py                      # FastAPI app entry, lifespan, exception handlers
│   ├── config.py                    # Pydantic BaseSettings, loads from .env
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── user_profile.py      # UserProfile (name, city, style preferences, allergies, budget)
│   │   │   ├── weather.py           # Weather (temp, condition, humidity, wind, forecast_hours)
│   │   │   ├── place.py             # Place (name, type, address, rating, price_range, dress_code)
│   │   │   ├── outfit.py            # OutfitSuggestion (items, reasoning, weather_fit)
│   │   │   └── recommendation.py    # Recommendation (places, outfits, route, summary)
│   │   ├── services/
│   │   │   ├── weather_service.py   # ABC: get_weather(city, date) -> Weather
│   │   │   ├── place_service.py     # ABC: find_places(city, preferences, weather) -> list[Place]
│   │   │   ├── agent_service.py     # ABC: generate_recommendation(profile, request) -> Recommendation
│   │   │   └── user_repository.py   # ABC: get_profile(user_id), save_profile(profile)
│   │   └── exceptions.py            # ProfileNotFound, WeatherUnavailable, ScrapingFailed, AgentError
│   ├── application/
│   │   └── use_cases/
│   │       ├── get_recommendation.py    # Main orchestrator: profile check -> weather -> places -> agent -> respond
│   │       ├── onboard_user.py          # Saves initial user profile to repository
│   │       ├── get_user_profile.py      # Retrieves existing profile
│   │       └── update_user_profile.py   # Updates profile preferences
│   ├── infrastructure/
│   │   ├── claude/
│   │   │   └── claude_agent.py      # Anthropic SDK client, implements AgentService
│   │   ├── weather/
│   │   │   └── open_meteo.py        # Open-Meteo HTTP client, implements WeatherService
│   │   ├── scraper/
│   │   │   └── web_scraper.py       # httpx + BeautifulSoup, implements PlaceService
│   │   └── persistence/
│   │       └── json_repository.py   # JSON file read/write, implements UserRepository
│   ├── api/
│   │   ├── routes/
│   │   │   ├── recommend.py         # Main agentic endpoint
│   │   │   ├── profile.py           # User profile CRUD
│   │   │   └── health.py            # Health check
│   │   ├── dependencies.py          # FastAPI Depends() wiring
│   │   └── schemas/
│   │       ├── requests.py          # RecommendationRequest, ProfileCreate, ProfileUpdate
│   │       └── responses.py         # RecommendationResponse, ProfileResponse, ErrorResponse
│   └── container.py                 # Builds and wires all dependencies
├── data/
│   └── users.json                   # JSON file storage (gitignored)
├── .env
├── .env.example
├── requirements.txt
└── tests/
    ├── test_recommendation.py
    ├── test_profile.py
    └── test_weather.py
```

### Layer Rules

- **domain/** has zero external dependencies. Pure Python only.
- **application/** depends on domain. Use cases accept interfaces via constructor injection.
- **infrastructure/** implements the interfaces from domain/services. This is where Claude API calls, weather API calls, and web scraping live.
- **api/** is the delivery mechanism. Thin handlers that call use cases. All DI wiring happens via FastAPI's `Depends()`.
- Every layer communicates through abstract base classes, never concrete implementations directly.

## API Endpoints

### Main Agentic Endpoint
```
POST /api/v1/recommend
```
The single endpoint that does everything. Takes the user's request, orchestrates weather lookup, place discovery, and Claude reasoning, returns a full recommendation.

**Request body:**
```json
{
  "user_id": "user-123",
  "city": "Berlin",
  "date": "2026-03-14",
  "time_of_day": "evening",
  "occasion": "casual dinner with friends",
  "budget": "medium",
  "preferences": "outdoor seating if weather is nice, no sushi"
}
```

**Response body:**
```json
{
  "weather": {
    "temperature_c": 12,
    "condition": "partly cloudy",
    "humidity": 65,
    "wind_kmh": 15
  },
  "places": [
    {
      "name": "Example Restaurant",
      "type": "restaurant",
      "address": "...",
      "why": "Outdoor terrace, fits your budget, great for groups",
      "price_range": "$$",
      "rating": 4.5
    }
  ],
  "outfit": {
    "items": ["light jacket", "jeans", "sneakers"],
    "reasoning": "12°C with light wind - layer up but no heavy coat needed. Casual venue so sneakers work."
  },
  "summary": "Agent's natural language summary tying it all together"
}
```

**Flow:**
1. Load user profile from JSON repository (if no profile exists, return 404 with message to onboard first)
2. Fetch weather from Open-Meteo for the given city and date
3. Claude agent receives: user profile + weather data + user's request
4. Agent uses tools to scrape/search for places matching the criteria
5. Agent reasons about outfit based on weather + venue type + user style preferences
6. Agent returns structured recommendation

### User Profile Endpoints
```
GET    /api/v1/profile/{user_id}       # Get user profile
POST   /api/v1/profile                 # Create profile (onboarding)
PATCH  /api/v1/profile/{user_id}       # Update profile preferences
```

**Profile create request:**
```json
{
  "user_id": "user-123",
  "name": "Marin",
  "default_city": "Berlin",
  "style_preferences": ["casual", "streetwear"],
  "budget_default": "medium",
  "dietary_restrictions": ["vegetarian"],
  "favorite_cuisines": ["italian", "japanese"],
  "avoid": ["loud clubs"]
}
```

The profile is stored in `data/users.json`. When the main `/recommend` endpoint is called and no profile exists for the user_id, it returns a `404` with a message directing them to create a profile first.

### Utility Endpoints
```
GET  /api/v1/weather/{city}            # Test weather fetching independently
GET  /api/v1/health                    # Health check
```

## AI Agent Design

### How It Works

The Claude agent is implemented using the Anthropic SDK with **tool use**. The agent receives a system prompt + user context and has access to tools it can call in a loop until it has enough information to produce a recommendation.

### Agent System Prompt

```
You are a going-out assistant. Your job is to help the user find the perfect place
to go out and suggest what to wear.

You have access to the user's profile (style preferences, budget, dietary restrictions)
and current weather data for their city. Use the available tools to search for places
and gather information.

When making recommendations:
- Suggest 3-5 places that match the occasion, budget, and weather
- For each place, explain WHY it's a good fit
- Suggest an outfit based on: weather conditions, venue dress code, user's style preferences
- Keep it practical and specific (not "wear something warm" but "light jacket + jeans + sneakers")
- If weather is bad, prefer indoor options. If weather is great, include outdoor options.
- Respect dietary restrictions and cuisine preferences from the user profile
- Consider the time of day and occasion type

Return your response as structured JSON matching the required schema.
```

### Agent Tools

The Claude agent gets these tools registered via the Anthropic SDK `tools` parameter:

1. **search_places** - Scrapes the web for venues/restaurants/bars in the given city matching criteria. The infrastructure layer performs the actual HTTP requests and HTML parsing, returns structured results to the agent.

2. **get_place_details** - Given a place name and city, scrapes for more details (reviews, dress code, price range, opening hours).

### Agent Loop

```
1. API receives request
2. Use case loads user profile + fetches weather
3. Use case calls AgentService.generate_recommendation()
4. Claude agent receives: system prompt + user profile + weather + user's request
5. Agent calls search_places tool → infrastructure scrapes → returns results
6. Agent optionally calls get_place_details for top picks
7. Agent reasons about outfit based on all gathered data
8. Agent returns final structured JSON
9. Use case validates response with Pydantic, returns to API layer
```

## Environment Variables

All secrets and config go in `.env`, with `.env.example` committed to the repo:
```
CLAUDE_API_KEY=
OPEN_METEO_BASE_URL=https://api.open-meteo.com
APP_HOST=0.0.0.0
APP_PORT=8000
DATA_DIR=./data
```

## Python Environment

Always use a project-level virtual environment, never the global Python.

```bash
# Create venv (first time)
python -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

All commands below assume the venv is activated.

## Commands

```bash
# Run the server
uvicorn app.main:app --reload

# Run tests
pytest

# Run a single test
pytest tests/test_file.py::test_name
```

## Error Handling

- All external service calls (Claude API, weather API, scraping) must be wrapped with proper error handling
- Use domain-specific exceptions that get mapped to HTTP responses in the API layer
- Never expose internal errors or stack traces to the client
- If user profile doesn't exist, return 404 with onboarding instructions
- If weather service is down, agent should still work but note weather is unavailable
- If scraping fails for a source, agent should try alternative search terms before giving up
