import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from anthropic import AsyncAnthropic

from app.domain.entities.user_profile import UserProfile
from app.domain.exceptions import AgentError
from app.domain.services.agent_service import AgentService
from app.infrastructure.scraper.web_scraper import WebScraper
from app.infrastructure.weather.open_meteo import OpenMeteoWeatherService

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 10

TOOLS = [
    {
        "name": "get_weather",
        "description": "Get weather forecast for a city on a specific date. Always call before suggesting outfits.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "date": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["city", "date"],
        },
    },
    {
        "name": "search_places",
        "description": "Search the web for real venues (restaurants, bars, pool halls, clubs) in a city. Use specific queries.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "query": {"type": "string", "description": "e.g. 'best pool hall Chisinau', 'fine dining restaurant center'"},
            },
            "required": ["city", "query"],
        },
    },
    {
        "name": "get_place_details",
        "description": "Scrape detailed info about a specific place. Use for 1-2 top picks only.",
        "input_schema": {
            "type": "object",
            "properties": {
                "place_name": {"type": "string"},
                "city": {"type": "string"},
                "url": {"type": "string", "description": "URL from search_places results"},
            },
            "required": ["place_name", "city"],
        },
    },
    {
        "name": "present_recommendation",
        "description": (
            "Call this as your FINAL step when you have place recommendations ready. "
            "This renders structured cards in the UI. Always call this when presenting places."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reply": {
                    "type": "string",
                    "description": "Your conversational message to the user",
                },
                "places": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string", "description": "e.g. pool hall, restaurant, bar"},
                            "address": {"type": "string"},
                            "why": {"type": "string", "description": "Why this fits the user's request"},
                            "price_range": {"type": "string", "description": "e.g. $, $$, $$$"},
                            "url": {"type": "string"},
                        },
                        "required": ["name", "type", "address", "why"],
                    },
                },
                "outfit": {
                    "type": "object",
                    "properties": {
                        "items": {"type": "array", "items": {"type": "string"}},
                        "reasoning": {"type": "string"},
                    },
                    "required": ["items", "reasoning"],
                },
            },
            "required": ["reply"],
        },
    },
]

SYSTEM_PROMPT_TEMPLATE = """You are an expert going-out assistant for {name}.

User profile:
- Default city: {default_city}
- Style: {style}
- Budget: {budget}
- Dietary restrictions: {dietary}
- Favorite cuisines: {cuisines}
- Avoid: {avoid}

Today: {today}

Workflow:
1. Check weather (get_weather)
2. Search for venues per activity (search_places)
3. Get details on 1-2 top picks (get_place_details)
4. Call present_recommendation with all results — ALWAYS use this when showing places

Rules:
- Never invent place names — only use results from search_places
- Outfit items must be specific: "dark slim jeans + white button-up + clean white sneakers"
- 3-5 place options per activity
- If user dislikes something, search for alternatives and call present_recommendation again
- For pure conversational replies (no places), just respond without calling present_recommendation
"""


class ClaudeAgentService(AgentService):
    def __init__(self, api_key: str, weather_service: OpenMeteoWeatherService, web_scraper: WebScraper):
        self._client = AsyncAnthropic(api_key=api_key)
        self._weather_service = weather_service
        self._web_scraper = web_scraper

    def _build_system_prompt(self, profile: UserProfile) -> str:
        return SYSTEM_PROMPT_TEMPLATE.format(
            name=profile.name,
            default_city=profile.default_city,
            style=", ".join(profile.style_preferences) or "not specified",
            budget=profile.budget_default,
            dietary=", ".join(profile.dietary_restrictions) or "none",
            cuisines=", ".join(profile.favorite_cuisines) or "any",
            avoid=", ".join(profile.avoid) or "nothing specific",
            today=datetime.now().strftime("%Y-%m-%d"),
        )

    async def _execute_tool(self, name: str, tool_input: dict) -> str:
        if name == "get_weather":
            city, date = tool_input["city"], tool_input["date"]
            logger.info("  [tool] get_weather  city=%s  date=%s", city, date)
            weather = await self._weather_service.get_weather(city, date)
            result = weather.model_dump()
            logger.info("  [tool] weather: %s°C, %s", result["temperature_c"], result["condition"])
            return json.dumps(result)

        if name == "search_places":
            city, query = tool_input["city"], tool_input["query"]
            logger.info("  [tool] search_places  query='%s'  city=%s", query, city)
            results = await self._web_scraper.search_places(city, query)
            logger.info("  [tool] search_places → %d results", len(results))
            return json.dumps(results)

        if name == "get_place_details":
            place, city = tool_input["place_name"], tool_input["city"]
            url = tool_input.get("url", "")
            logger.info("  [tool] get_place_details  place='%s'", place)
            details = await self._web_scraper.get_place_details(place, city, url or None)
            logger.info("  [tool] got details for '%s'", place)
            return json.dumps(details)

        raise AgentError(f"Unknown tool: {name}")

    async def _enrich_places_with_images(self, places: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        async def fetch(place: Dict[str, Any]) -> Dict[str, Any]:
            if place.get("url"):
                place["image_url"] = await self._web_scraper.get_og_image(place["url"])
            return place

        return list(await asyncio.gather(*[fetch(p) for p in places]))

    async def chat(
        self,
        profile: UserProfile,
        messages: List[dict],
    ) -> Tuple[str, List[dict], Optional[Dict[str, Any]]]:
        current_messages = list(messages)
        tool_rounds = 0

        logger.info("[agent] starting  user=%s  history=%d msgs", profile.user_id, len(messages))

        while True:
            logger.info("[agent] calling Claude  round=%d", tool_rounds)
            response = await self._client.messages.create(
                model="claude-opus-4-6",
                max_tokens=4096,
                system=self._build_system_prompt(profile),
                messages=current_messages,
                tools=TOOLS,
            )
            logger.info("[agent] Claude → stop_reason=%s", response.stop_reason)

            if response.stop_reason == "end_turn":
                reply = next((b.text for b in response.content if hasattr(b, "text")), "")
                current_messages.append({"role": "assistant", "content": [b.model_dump() for b in response.content]})
                logger.info("[agent] done (end_turn)  reply=%d chars", len(reply))
                return reply, current_messages, None

            if response.stop_reason == "tool_use":
                tool_rounds += 1
                if tool_rounds > MAX_TOOL_ROUNDS:
                    raise AgentError("Agent exceeded maximum tool call rounds")

                tool_names = [b.name for b in response.content if b.type == "tool_use"]
                logger.info("[agent] tools requested: %s", tool_names)

                current_messages.append({"role": "assistant", "content": [b.model_dump() for b in response.content]})

                structured_data: Optional[Dict[str, Any]] = None
                tool_results = []

                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    if block.name == "present_recommendation":
                        data = dict(block.input)
                        logger.info("[agent] present_recommendation  places=%d", len(data.get("places", [])))
                        if data.get("places"):
                            data["places"] = await self._enrich_places_with_images(data["places"])
                        structured_data = data
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps({"status": "presented"}),
                        })
                    else:
                        try:
                            result = await self._execute_tool(block.name, block.input)
                        except Exception as exc:
                            logger.warning("[agent] tool '%s' failed: %s", block.name, exc)
                            result = json.dumps({"error": str(exc)})
                        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

                current_messages.append({"role": "user", "content": tool_results})

                if structured_data is not None:
                    reply = structured_data.get("reply", "")
                    current_messages.append({"role": "assistant", "content": [{"type": "text", "text": reply}]})
                    logger.info("[agent] done (present_recommendation)  reply=%d chars", len(reply))
                    return reply, current_messages, structured_data

                continue

            raise AgentError(f"Unexpected stop reason: {response.stop_reason}")
