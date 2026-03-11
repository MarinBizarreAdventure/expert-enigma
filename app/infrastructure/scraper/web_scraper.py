import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

import httpx
from bs4 import BeautifulSoup
from ddgs import DDGS

_executor = ThreadPoolExecutor(max_workers=4)


def _ddg_text(query: str, max_results: int) -> list[dict]:
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


class WebScraper:
    async def search_places(self, city: str, query: str) -> list[dict[str, Any]]:
        loop = asyncio.get_event_loop()
        try:
            raw = await loop.run_in_executor(_executor, _ddg_text, f"{query} {city}", 8)
        except Exception:
            return []
        return [{"title": r.get("title", ""), "description": r.get("body", ""), "url": r.get("href", "")} for r in raw]

    async def get_place_details(self, place_name: str, city: str, url: str | None = None) -> dict[str, Any]:
        if not url:
            loop = asyncio.get_event_loop()
            try:
                raw = await loop.run_in_executor(_executor, _ddg_text, f"{place_name} {city} review menu hours", 3)
            except Exception:
                raw = []
            if raw:
                url = raw[0].get("href", "")
                return {"name": place_name, "city": city, "description": raw[0].get("body", ""), "url": url}
            return {"name": place_name, "city": city, "description": "No details found"}
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
                resp = await client.get(url)
                resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = " ".join(soup.get_text(separator=" ").split())[:4000]
            return {"name": place_name, "city": city, "description": text, "url": url}
        except Exception:
            return {"name": place_name, "city": city, "description": "Could not fetch details", "url": url}

    async def get_og_image(self, url: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=5, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
                resp = await client.get(url)
                resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            tag = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
            if tag and tag.get("content"):
                return tag["content"]
        except Exception:
            pass
        return None
