from typing import List, Optional

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    user_id: str
    name: str
    default_city: str
    style_preferences: List[str] = []
    budget_default: str = "medium"
    dietary_restrictions: List[str] = []
    favorite_cuisines: List[str] = []
    avoid: List[str] = []


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    default_city: Optional[str] = None
    style_preferences: Optional[List[str]] = None
    budget_default: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None
    favorite_cuisines: Optional[List[str]] = None
    avoid: Optional[List[str]] = None


class RecommendationRequest(BaseModel):
    user_id: str
    city: str
    date: str
    time_of_day: str
    occasion: str
    budget: str = "medium"
    preferences: str = ""


class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None
