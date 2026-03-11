from typing import List

from pydantic import BaseModel


class OutfitSuggestion(BaseModel):
    items: List[str]
    reasoning: str
