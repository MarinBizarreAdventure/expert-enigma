from typing import List

from pydantic import BaseModel


class UserProfile(BaseModel):
    user_id: str
    name: str
    default_city: str
    style_preferences: List[str] = []
    budget_default: str = "medium"
    dietary_restrictions: List[str] = []
    favorite_cuisines: List[str] = []
    avoid: List[str] = []
